# -*- coding: utf-8 -*-

from Products.ksiktforum import psis
import DateTime
from Products.CMFCore.utils import getToolByInterfaceName
from Products.CMFDefault.utils import decode
from Products.CMFDefault.utils import Message as _

"""This script is called when a user has been invited to the KSIKT forum by an existing member.
The invitation email is sent by the sendMemberInvite.py script.



TODO: Ask Arnar about how to set the user-permissions on this script. It must be legal for anyone to run this
      script, since this is where new user-accounts will get created. 
      When I try to follow an invitation-link without already being logged into the portal, I get asked
      for a username and password. When I press the cancel-button, the script runs, but it seems that
      it is not allowed to access the portal's propertyvalue pending_member_invites: The symptom is
      the script always claims that the invitation has expired.

"""
separator = u"¤¨" # we just use a rarely-used character-sequence ("¤¨") and hope that it isn't used in the adminmessage.
errors = []   # Any error-messages will be appended here and passed on to content_view()
messages = [] # Any status-messages will be appended here and passed on to content_view()

returnURL = context.memberInviteError # the url to display. This will be set based on how the member-invite works out.
                 


## Check if the specified confirmHash is valid
confirmHash = context.REQUEST.get("confirm","")
matchingInvite = None
if confirmHash:
    requiredStartString = confirmHash + separator
    pendingInvites = list(context.portal.pending_member_invites)
    for pendingInvite in pendingInvites:
        if pendingInvite.startswith(requiredStartString):
            ## Ok, found a matching invite, so remove it and update the list.
            matchingInvite = pendingInvite
            pendingInvites.remove(pendingInvite)
            context.portal.manage_changeProperties({"pending_member_invites" : pendingInvites})
            break

if not matchingInvite:
    errors.append(u"Denne invitasjon ser ut til å ha gått ut på dato. Send en epost til personen som inviterte deg og be ham/henne om å invitere deg på nytt.")

if not errors:
    ## The invite is valid, so create a new user.
    
    ## Extract the information from the pending invite.
    storedConfirmHash = ''
    inviteTime = ''
    inviter_memberid = ''
    invitee_email = ''
    adminmessage = ''
    fullname = ''
    
    try:
        (storedConfirmHash,inviteTime,inviter_memberid,invitee_email,adminmessage,fullname) = matchingInvite.split(separator) 
    except ValueError:        
        (storedConfirmHash,inviteTime,inviter_memberid,invitee_email,adminmessage) = matchingInvite.split(separator) 
        fullname = invitee_email.split("@")[0]
   
    ## Check that the user isn't already a member on the portal
    brains = context.portal_catalog(portal_type='person')
    lowercase_invitee_email = invitee_email.lower()
    persontopics = [brain.getObject() for brain in brains]
    for persontopic in persontopics:
        existingmail = persontopic.getOccurrenceValue(psis.email,ignore=True,default=None)
        if existingmail and existingmail.lower() == lowercase_invitee_email:
            errors.append(u"""Det finnes allerede en konto med epost addressen "%s.""" % (invitee_email,))
            returnURL = persontopic.person_view # Display the existing user.
            break

    if not errors:
        ## Generate a unique username based on the email-nick. If the username already exists, add a number
        ## to it until it is unique.
        creationpath = context.personer#context.portal_topicmanagement.calculateContentCreationPath('person')
        emailnick = invitee_email.split("@")[0]
        username = usernameBase = context.portal_topicmanagement.normalizeid(fullname)
        username = username.replace('_','.')
        usernameCounter = 1
        while ( ## Note that we check both that no matching person-topic exist, and that no matching zope-user exists.
                ## There will usually be a one-to-one mapping of person-topics and zope-users, but some exceptions may exist.
                   hasattr(creationpath,username) 
                or context.acl_users.getUser(username)
                ):
            usernameCounter += 1
            username = usernameBase + str(usernameCounter) ## add a number to the username until it is unique.
            
        
       
        ##Create a person-topic for the new member
        
        creationpath.invokeFactory(type_name="person", id=username)
        newmember = creationpath[username]
        newmember.setOccurrence(invitee_email,psis.email)
        #context.portal_workflow.doActionFor(newmember, 'publish')
    
        ## Make a guess at the persons name, based on the email address. Often people
        ## have email-addresses that looks like this: "firstname.surname@somewhere.com" or  like this: "firstname_surname@somewhere.com"
        ## We split the email-nick up by "." and "_" characters and capitalize each part.
        personname = fullname or " ".join([namepart.capitalize() for namepart in emailnick.replace("_",".").split(".")])        
        newmember.setTitleAndName(personname) 
       
        ##Create a zope user for the new member.
        password = context.portal_topicmanagement.generatePassword() # Generate an initial password.
        context.acl_users.userFolderAddUser( name=username 
                                           , password=password
                                           , roles=('Member', 'Contributor') # TODO: Ask arnar how to do the permission-stuff.
                                           , domains=()
                                           )
        newmember.setOwner(username)
       
       
        ## Send an email to the user with his username and password
        subject = u'Velkommen til KS IKT-Forum [Automatisk generert epost]'
        
        message = u"""
Hei.

Du er nå registert som medlem på nettportalen for KS IKT-forum!

Ditt brukernavn: %s
Ditt passord   : %s

Du kan finne din bruker-profil ved å følge denne linken: 
  %s/view
""" % (username,password,newmember.absolute_url())
        context.portal_topicmanagement.sendUnicodeMail(subject, message, 
                                                       (invitee_email,), #recipients
                                                       context.portal.email_from_address #sender
                                                       )
                
        ## Send an email to the administrator
        inviterPerson = getattr(creationpath,inviter_memberid,None)
        if inviterPerson:
            inviterName = inviterPerson.title_or_id()
            inviterURL  = inviterPerson.absolute_url() + "/view"
        else:
            inviterName = inviter_memberid
            inviterURL  = """<Brukeren "%s" ble ikke funnet!>""" %( inviter_memberid,)
        
        context.portal_topicmanagement.sendUnicodeMail(u"Ny bruker opprettet: %s" % (username,) # subject
                                                       , u"""
                                                       
Kl %s ble det opprettet en ny bruker: %s (%s)

Brukeren ble invitert kl %s av brukeren %s (%s).

Invitasjonsgrunnen som ble oppgitt var: 
"%s"
""" % (DateTime.DateTime(),
       username,newmember.absolute_url()+"/view",
       inviteTime,inviterName,inviterURL,
       adminmessage)# message, 
                                                       ,(context.portal.email_from_address,)  #recipients
                                                       ,context.portal.email_from_address     #sender
                                                       )

        
        ## TODO: Find a more elegant way to automatically log in the user. This hack displays a form with hidden
        ## username and password fields, which requires the user to click a button to login and be redirekted
        ## to his workarea.
        
        return """
<html>
  <head>
    <title>Velkommen til KSIKT portalen.</title>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
  </head>
  <body>
    <form action="ksiktforum_login" method="post" name="KSIKTLoginForm">
      <h1>Velkommen som ny bruker til KSIKT portalen.</h1>
      Du vil nå bli overført til din brukerflate i løpet av noen sekunder. Hvis du ikke blir automatisk 
      videreført kan du trykke på "Gå til din arbeidsflate" knappen.
      <div>
        <input type="hidden" name="came_from" value="%s"/>
        <input id="__ac_name" type="hidden" name="__ac_name" value="%s" />
        <input id="password" type="hidden" name="__ac_password" value="%s"/>
        <input type="hidden" name="username" value="%s" />
        <input type="hidden" name="password" value="%s"/>
        <input type="hidden" name="__ac_persistent" value="1" checked="checked" id="cb_remember" />
        <input type="hidden" name="usersworkspaceurl" value="%s"/>
        <input type="submit" value="Gå til din arbeidsflate" name="log_in" />
      </div>      
      </form>
      
      <SCRIPT LANGUAGE="JavaScript">
        document.KSIKTLoginForm.submit();
      </SCRIPT>
   </body>
</html> 
""" % ( newmember.absolute_url().replace('http','https').replace('httpss', 'https')+"/workspace_view",username,password,username,password,newmember.absolute_url().replace('http','https')+"/workspace_view")

#        context.REQUEST.set('__ac_name', username)
#        context.REQUEST.set('__ac_password',  password)
#        
#
#        mtool = getToolByInterfaceName('Products.CMFCore.interfaces.IMembershipTool')
#        ptool = getToolByInterfaceName('Products.CMFCore.interfaces.IPropertiesTool')
#        stool = getToolByInterfaceName('Products.CMFCore.interfaces.ISkinsTool')
#        utool = getToolByInterfaceName('Products.CMFCore.interfaces.IURLTool')
#        portal_url = utool()
#        
#        
#        if stool.updateSkinCookie():
#            context.setupCurrentSkin()
#        
#        
#        options = {}
#        
#        isAnon = mtool.isAnonymousUser()
#        if isAnon:
#            context.REQUEST.RESPONSE.expireCookie('__ac', path='/')
#            options['is_anon'] = True
#            options['title'] = _(u'Login failure')
#            options['admin_email'] = ptool.getProperty('email_from_address')
#            return context.logged_in_template(**decode(options, script))
#        else:
#            mtool.createMemberArea()
#            member = mtool.getAuthenticatedMember()
#            now = context.ZopeTime()
#            last_login = member.getProperty('login_time', None)
#            member.setProperties(last_login_time=last_login, login_time=now)
#            member.setProperties(last_login_time='1999/01/01', login_time=now)
#            
#            context.REQUEST.RESPONSE.redirect( newmember.absolute_url() + "/workspace_view" )
#            return
            
        

 
status = {"errors":errors,
          "messages":messages,
         }
#return status
return returnURL(status=status)