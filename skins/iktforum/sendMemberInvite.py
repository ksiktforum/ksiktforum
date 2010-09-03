# -*- coding: utf-8 -*-

import DateTime
from Products.ksiktforum import psis

## TODO: this is a copy of a function in content_view.py.py. This must be put into some common
## module somewhere. Ask Svein Arild about the best way to do this. 
def sentencelister(sequence, separator=', ', lastseparator=' og '):
    """ Return a sequence [1,2,3] as '1, 2 and 3'.  """
    sequence = sequence[:]
    if len(sequence)>1:
        last = sequence[-1]
        text = separator.join(sequence[:-1])
        text += lastseparator + last
    elif len(sequence)==1:
        text = sequence[0]
    else:
        text = ''
    return text


"""
All members on the ksikt portal can invite other people to become members. They do this by filling
in a form on the portal where the specify the name and email of the person they want to invite.
They also specify a messages to the person they want to invite ("I want you to join this portal because...")
and a message to the portal's administrator ("I want to invite this person because...").

When the member has filled in the form and clicked the submit-button, the followings happens:
  First, a couple of error-checks are done:
    * Check if the specified email belongs to a person who is already a member.
    * Check if all the fields looks sane: If the email-address is valid, if the messages to the 
      portal's admin is long enough, etc.
  If any of the checks fail, an error-message is displayed to the user, and nothing else happens.      
 
  If the form passes all the checks, this happens:

   * A unique and random hex-string hash is generated. 
   * An email is sent to the invited person (using the specified email address.) The email contains
     a link that looks something like this: "ksikt.no:/acceptInvitation?hash=<the newly generated hash>"
   * A new line is added to a "lines"-property on the portal (called something like "pending_userinvites"). This property
     is a list of strings, where each string represent a pending invitation. Each string is a 
     concatenation of the following: The hash, the username of the invitor, the email-address of the invitee
     and the message to the administrator.



When the invitee clicks on the link in his email-message, the acceptInvitaiton.py script will use
the hash-value too look up the correct string in the portal's "pending_userinvites" property.
     
 If a mapping is found, an email will be sent to the administrator and a new member will be created
 on the portal. This involves creating a new "person"-topic for the new user, and a corresponding
 entry in the "acl_users" folder. The id of the new user will be generated based on the users
 email-name (The part in front of the "@"). If neccessary, the name will be made unique by adding
 a number to it ("knutj", "knutj2", "knutj3", etc).
     
     
     
TODO: 
  * how to get rid of stale invites? (Each invite has a timestamp).
  * how to handle duplicated invites? perhaps remove all pending invites with the same email-address when
    an invitee accepts the invitation?
  * Ask Arnar how the security-stuff should be set up: Which roles etc.
  
  
QUESTIONS/BUGS:
 * It doens't work to log in with the invited users: Ask Arnar about permissions and roles.
 * Something that is probably related to user-permissions: The search context.portal_catalog(portal_type='person')
   just returns an empty list when I try it as the generated user "knutj42", but returns the expected result when I try it
   as the user "knutj" (the user that Svein Arild created manually). Note: "knutj42" has had his role manually changed
   from "Member" to "Manager", since it didn't work to log in with that user when it was just a "Member".
"""

if context.portal_membership.isAnonymousUser():
    return

errors = [] ## If any problems is found with the form, appropriate error-messages will be added to this list

invitemember = context.REQUEST.get("invitemember",{}) # The form-fields are collected in a record called "invitemember"

fullname = invitemember.get('fullname', u"")
emailstring    = invitemember.get("emails",u"")
inviteemessage = invitemember.get("inviteemessage",u"")
adminmessage   = invitemember.get("adminmessage"  ,u"")
emails = []
fullnames = []


if emailstring:
    ## One or more emails where specified, so try to separate the emailstring into separate email addresses. 
    for separatorchar in ", :\t\n\r": # We want to accept just about all possible separator characters
        emailstring = emailstring.replace(separatorchar,";")
    for email in emailstring.split(";"):
        email = email.strip()
        if email: # ignore empty emails, since the user probably entered two separator-characters by mistake
            emails.append(email)

if fullname:
    ## One or more emails where specified, so try to separate the emailstring into separate email addresses. 
    for separatorchar in ",:\t\n\r": # We want to accept just about all possible separator characters
        fullname = fullname.replace(separatorchar,";")
    for fn in fullname.split(";"):
        fn = fn.strip()
        if fn: # ignore empty emails, since the user probably entered two separator-characters by mistake
            fullnames.append(fn)
    
if emails:
    ## One or more email-addresses was specified, so we must check that they look valid
    for email in emails:
        if not context.portal_topicmanagement.validateMailURI(email):
            errors.append( u'"%s" er ikke en gyldig epost adresse.' % (email,))    
else:
    ## The user didn't specify any email-addresses
    errors.append( u"Du må oppgi email-addressen(e) til personen(e) du vil invitere.")
     
if not fullname:
    errors.append( u"Du må skrive inn det fulle navnet til personen en du ønsker å invitere")
    
if not adminmessage:
    errors.append( u"Du må skrive en beskjed til web-redaktøren, hvor du sier noen ord om hvorfor du vil invitere denne personen/disse personene.")
    
if len(fullnames) != len(emails):
    errors.append( u"Skal du invitere flere mennesker må du oppgi like mange epostadresser som navn på personer du inviterer")
    #errors.append(str(len(fullnames)))
    #errors.append(str(len(emails)))
    #errors.append(str(fullnames))
    


personFolder = context.personer#context.portal_topicmanagement.calculateContentCreationPath('person')


memberTopic = context.getAuthenticatedMemberTopic()
if not memberTopic:
    errors.append(u"Du må selv være bruker på KSIKT for å kunne invitere andre personer.")


## Check if any of the invitees are already members of the site
if emails:
    lowercaseemails = [x.lower() for x in emails]
    brains = context.portal_catalog(portal_type='person')
    persontopics = [brain.getObject() for brain in brains]
    for persontopic in persontopics:
        existingmail = persontopic.getOccurrenceValue(psis.email,ignore=True,default=None)
        if existingmail and existingmail.lower() in lowercaseemails:
            errors.append(u"""Det finnes allerede en konto med epost addressen "%s.""" % (existingmail,))

if not errors:
    ## The formdata is ok, so try to send emails and store information about the invite
    memberName      = memberTopic.title_or_id()
    memberEmail     = memberTopic.getOccurrenceValue(psis.email,ignore=True,default=context.portal.email_from_address)
       
        
    currentTime = str(DateTime.DateTime())
    counter = 0
    for email in emails:
        fullname = fullnames[counter]        
        
        counter = counter +1
            
        ## We store the information about the invite, so that when the invitee follows the link
        ## in his email, we can confirm that he has actually been invited.
        pending_member_invites_propertyname = 'pending_member_invites'
        if not context.portal.hasProperty(pending_member_invites_propertyname):
            context.portal.manage_addProperty(pending_member_invites_propertyname,'','lines')
        pendingInvites = list(context.portal.pending_member_invites)
    
        confirmHash = context.getMD5HexDigest(u'%s%sJust some secret value' % (currentTime,email))
    
        ## Add a line with the confirmation-hash, the time, the inviter, the email and the adminmessage to the list
        ## of pending invites, and update the property.
        pendingInvites.append(u"¤¨".join((confirmHash,currentTime,memberTopic.getId(),email,adminmessage,fullname) )) # note that we just use a rarely-used character-sequence ("¤¨") and hope that it isn't used in the adminmessage.
        context.portal.manage_changeProperties({pending_member_invites_propertyname : pendingInvites})
            
         
        subject = u'Invitasjon til KS IKT-Forum [Automatisk generert epost]'
        
        message = u"""
Hei.

%s ønsker deg velkommen som bruker av nettportalen for KS IKT-forum: 
"%s"

Følg denne lenken for å logge deg inn på KSIKT portalen:
  %s

""" % (memberName,  inviteemessage,
       "%s/acceptMemberInvite?confirm=%s" % (context.portal_url(),confirmHash) ,
       )

        # Send an email to the invitee(s)
        context.portal_topicmanagement.sendUnicodeMail(subject, message, 
                                                       (email,), #recipients
                                                       context.portal.email_from_address #sender
                                                       )
       
    
           
if not errors:
    ## All is well
    recipients = sentencelister(emails)
    return context.memberInviteForm( status={'messages':[u"En invitasjon har blitt sendt til %s." % (recipients,),],}
                           )
else:
    ## something went wrong (probably missing some of the form-fields)
    return context.memberInviteForm(invitemember={'emails': emailstring, 
                                         'inviteemessage': inviteemessage,
                                         'adminmessage'  : adminmessage,
                                         'fullname':fullname
                                         },
                            status={'errors':errors,}
                            )
    