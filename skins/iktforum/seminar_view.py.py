# -*- coding: utf-8 -*-
import DateTime
from Products.ksiktforum import psis

content = {} # 

separator   = u"¤¨" # must be the same as used in addSeminarAttendee.py. We should probably put this in some common file...


## Check if the current user can subscribe to the seminar.
max_attendees = context.getOccurrenceValue(psis.max_attendees,ignore=True,default="0")
try:
    max_attendees = int(max_attendees)
except ValueError:
    max_attendees = 0 # zero means no limit to the number of participants

attendees = context.listOccurrences(type=psis.attendee)

registrationOptionsString = context.getOccurrenceValue(psis.registration_options,ignore=True,default="")

## The registration-options are encoded as a multiline-string on this format:
##
##What do you want to drink for dinner?
##+water
##+beer
##+milk
##
##What is your favorite colour?
##*red
##*blue
##
## Each question is followed by one or more options. The option-lines must start with one of a 
## few characters, each of which has a specific effect on how the options is presented to the user:
##   *: means that the options are mutually exclusive. The options are rendered as a radiobox-group.
##   +: means that the options are not mutally exclusive. The options are rendered with one checkbox for each choice.
registrationOptions = []
if registrationOptionsString:
    registrationOptionsString = registrationOptionsString.strip()
    currentOption = {'question':"Registrerings valg",
                     'answers': []}
    templist = [currentOption]
    for line in registrationOptionsString.split("\n"):
        line = line.strip()
        if(         len(line)>1
            and not line.startswith("#")
            and not line.startswith(";") ): #skip empty lines and comments
        
            answertype = line[0]
            if answertype in u"*+-&": # It is up to the pagetemplate to figure out what these characters mean, but it is 
                                      # it is something like this: "*"=radiobutton "+"=checkbox.
                currentOption['answers'].append({'type':answertype,'text':line[1:]})
            else:
                ## This is a new question
                currentOption = {'question':line, 'answers':[]}
                templist.append(currentOption)

    ## Remove empty options
    for option in templist:
        if option['question'] and option['answers']:
            registrationOptions.append(option)

content['registrationOptions'] = registrationOptions



context.getOccurrenceValue(psis.max_attendees,ignore=True,default="0")



## If the current user is a registered member of the portal, we can check if he is already 
## signed up to the conference.
memberTopic = context.getAuthenticatedMemberTopic()
membersEmail = ''
membersName  = ''
membersTitle = ''
membersWorkplace = ''
membersPhone = ''
memberIsAlreadySignedUp = False
lowercase_membersEmail = None
lowercase_membersName  = None
lowercase_membersTitle  = None
lowercase_membersWorkplace  = None
lowercase_membersPhone  = None
if memberTopic:
    ## yep, the user is a member on the portal.
    membersName  = memberTopic.title_or_id()
    membersEmail = memberTopic.getOccurrenceValue(psis.email,ignore=True,default="")
    membersPhone = memberTopic.getOccurrenceValue(psis.phone,ignore=True,default="")
    membersTitle = memberTopic.getOccurrenceValue(psis.work,ignore=True,default="")
    membersWorkplace = memberTopic.getOccurrenceValue(psis.workplace,ignore=True,default="")
    if membersEmail:
        lowercase_membersEmail = membersEmail.lower()  
    lowercase_membersName  = membersName.lower()
        
attendeelist = []
content['attendeelist'] = attendeelist
content['attendeelistColumns'] = ({'title':u'Navn'                 ,  'fieldname':'name'},
                                  {'title':u'Tittel'               ,  'fieldname':'title'},
                                  {'title':u'Arbeidssted'          ,  'fieldname':'workplace'},
                                  {'title':u'Telefon'              ,  'fieldname':'phone'},
                                  {'title':u'Epost'                ,  'fieldname':'email'},
                                  {'title':u'Påmeldingstidspunkt'  ,  'fieldname':'created'},
                                  {'title':u'Registreringsvalg'    ,  'fieldname':'registrationoptions'},
                                  ) # This is used by the pagetemplate that displays the attendeelist.
for attendee in attendees:
    #context.removeOccurrence(attendee)
    #continue
    ## The entire comment (name, email, ) are stored as a single unicode value,
    ## delimited by a special character sequence.
    attendeestring = attendee.getValue()
    
    tokens = attendeestring.split(separator)
    while len(tokens) < 6: ## add backwards compatibility with old seminar data (before the registrationoptions where implemented)
        tokens.append("")
    (name, email, title, phone, workplace, registrationoptions) = tokens[:6]
    
    created = attendee.created().strftime("%d.%m.%y %H:%M")
    ## We return each attendee as a dictionary, so that the pagetemplage can easily pick out the
    ## various parts.
    attendeelist.append( {"name":name,
                          "email": email, 
                          "workplace": workplace, 
                          "phone": phone, 
                          "title": title, 
                         "created":created,
                         "tm_serial":attendee.tm_serial,
                         "registrationoptions": registrationoptions,
                         } )
    
    if(     (not memberIsAlreadySignedUp) 
        and lowercase_membersName 
        and lowercase_membersEmail
        and (email.lower() == lowercase_membersEmail) 
        and (name.lower() == lowercase_membersName)
        ):
        memberIsAlreadySignedUp = True

if max_attendees > 0: # a value of zero or less means that there is no limit to the number of participants
    vacantSpots = max(0,max_attendees - len(attendees)) # clamp to zero, just in case someone has modified the attendee-list or the max_attendees number manually.
else:
    vacantSpots = -1 # -1 means that there is no limit to the number of participants. The pagetemplate must check for this.
content['vacantSpots'] = vacantSpots    


## The membersEmail and membersName values are used to fill the registration-form with default values. 
content['membersName'] = membersName
content['membersTitle'] = membersTitle
content['membersWorkplace'] = membersWorkplace
content['membersPhone'] = membersPhone
content['membersEmail'] = membersEmail
content['memberIsAlreadySignedUp'] = memberIsAlreadySignedUp
content['seminarEmail'] = context.getOccurrenceValue(psis.email,ignore=True,default="")
errors = []
content['errors'] = errors

current_date = DateTime.DateTime()

startdateString = context.getOccurrenceValue(psis.startdate,ignore=True,default="")
try:
    start_date = DateTime.DateTime(startdateString)
except:
    start_date = current_date
    
registration_start_dateString = context.getOccurrenceValue(psis.registration_start_date,ignore=True,default="")
try:
    registration_start_date = DateTime.DateTime(registration_start_dateString)
except:
    ## No registration startdate was specified, so we default to the current date, or to the startdate, which ever is earliest.
    registration_start_date = min(start_date,current_date)

registration_end_dateString = context.getOccurrenceValue(psis.registration_end_date,ignore=True,default="")
try:
    registration_end_date = DateTime.DateTime(registration_end_dateString)
except:
    ## No registration enddate was specified, so we default to the startdate of the seminar.
    registration_end_date = start_date


registrationTimeHasStarted = current_date >= registration_start_date
registrationTimeHasEnded   = current_date >  registration_end_date
content['registrationTimeHasStarted'] = registrationTimeHasStarted
content['registrationTimeHasEnded']   = registrationTimeHasEnded
content['registration_start_date'] = registration_start_date
content['registration_end_date']   = registration_end_date
content['current_date'] = current_date
if (vacantSpots != 0) and registrationTimeHasStarted and (not registrationTimeHasEnded):
    canSignUp = True
    ## We can display the registration-form.
    ## Generate the anti-spam stuff. TODO; perhaps move this to the PageTemplate, where the names of the
    ## form-fields and the css-styles really belong?
    timestamp = DateTime.DateTime()
    ipaddress = context.REQUEST.getClientAddr()
    entryid   = context.tm_serial
    content['timestamp']  = timestamp
    content['ipaddress'] = ipaddress
    content['entryid']    = entryid
    content['honeypots'] = context.getHoneyPots(timestamp,ipaddress, entryid,
                                                  (('attendeename',   'textInput'),
                                                   ('attendeeemail',  'textInput'),
                                                   ('attendeephone',  'textInput'),
                                                   ('attendeetitle',  'textInput'),
                                                   ('attendeeworkplace',  'textInput'),
                                                   ),
                                                   ("dn",), ## an invisible css class
                                                  )
else:
    canSignUp = False
    
    
content['canSignUp'] = canSignUp



return content