# -*- coding: utf-8 -*-

## This script gets called when a user wants to sign up for a conference.


from Products.ksiktforum import psis
from Products.stripogram import html2text, html2safehtml
import DateTime



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


errors = [] ## If any problems with the form is detected, the error-messages will be added to this list.
messages = [] # Any status-messages will be added to this list.
name    = u""
email   = u""
phone   = u""
workplace   = u""
title   = u""

## Check that the anti-spam honeypot information looks ok, and get the mappings between the obfuscated 
## fieldnames and the real fieldnames.
(honeypots,formErrorMsg) = context.checkHoneyPots( context,  ("attendeename","attendeeemail","attendeeworkplace","attendeephone","attendeetitle",) )

if formErrorMsg:
    ## This looks like a spam-bot, so we can skip the rest of the checks.
    errors.append(formErrorMsg)
else:
    ## Get the values of the form fields that contain the actual user-entered data.
    name    = html2text(    context.REQUEST[honeypots['fieldname2hashedfieldname']["attendeename"]])
    email   = html2text(    context.REQUEST[honeypots['fieldname2hashedfieldname']["attendeeemail"]])
    phone   = html2text(    context.REQUEST[honeypots['fieldname2hashedfieldname']["attendeephone"]])
    workplace   = html2text(    context.REQUEST[honeypots['fieldname2hashedfieldname']["attendeeworkplace"]])
    title   = html2text(    context.REQUEST[honeypots['fieldname2hashedfieldname']["attendeetitle"]])
    
    ## Check that all the required fields are present
    for visibleFieldName,maxsize,fieldvalue in ( ("Navn",          100,  name),
                                                 ("Epostadresse",  255,  email),
                                                 ("Telefon",  100,  phone),
                                                 ("Tittel",  100,  title),
                                                 ("Arbeidssted",  100,  workplace),
                                                  ):
        if fieldvalue.strip() == "":
            errors.append( u"""Du må skrive noe i "%s" boksen.""" % (visibleFieldName,))
            
        
        if len(fieldvalue) > maxsize:
            errors.append(u"""Teksten i "%s" boksen er for lang! Prøv å korte ned teksten litt.""" % (visibleFieldName,))


    ## Check if the email-address looks plausible.
    if email and not context.portal_topicmanagement.validateMailURI(email):      
        errors.append(u"Du må skrive inn en gyldig Epostadresse.")
        


## Get the registration-options from the seminar topic. We need this to translate from
## the question and answer indexes in the form-data to the answer-texts. We want to store the
## answer-texts in the attendee-occurences, since that is more robust than to store the indexes
## (The person responsible for the seminar might insert a new answer to an exising question,
## and that would change the indexes for the answers). We still require the indexes of the questions
## to remain valid, though.
seminarinfo = getattr(context,"seminar_view.py")() # TODO: this seems a bit hackish. What is the best way of sharing code bethween the pythonscripts in this folder?
registrationOptionsFromSeminarTopic = seminarinfo['registrationOptions']


## Check if it is possible to register to the seminar at this time.
registration_start_date = seminarinfo['registration_start_date']
registration_end_date   = seminarinfo['registration_end_date']
current_date            = seminarinfo['current_date']
if current_date < registration_start_date:
    errors.append(u"Det er ikke mulig å melde seg på dette seminaret før %s." % (registration_start_date,))
    
if current_date > registration_end_date:
    errors.append( u"Det er ikke lenger mulig å melde seg på dette seminaret. Siste påmeldingstidspunkt var %s." % (registration_end_date,))




questionIndex = -1
registrationOptionsCurrentValues = [] # Used to fill in the form with the current values when we have to redisplay the form because of missing/wrong data 
useroptions = []
for option in registrationOptionsFromSeminarTopic:
    questionIndex += 1
    
    ## Get the form-values for this question from the http-request.
    userAnswerStrings = []
    userAnswers = context.REQUEST.get("registrationOption%d" % (questionIndex,),[])
    if userAnswers:
        answerIndex = -1
        for answer in option['answers']:
            answerIndex += 1
            if answerIndex in userAnswers:
                ## The user has selected this answer, so store the answer-text
                userAnswerStrings.append(u'"' + answer['text'] + '"')
                ## Also store the value that will be used if we have to redisplay the form.
                registrationOptionsCurrentValues.append("registrationOption_%d_%d" % (questionIndex,answerIndex))
                
    ## Pack the answers into a list on the form: "svar1, svar2 og svar3".
    ## Note that we must append to the useroptions list even if no answers
    ## where specified, since there might be more than one question, and the 
    ## order of the answers implicitly specify which question they belong to.
    useroptions.append("%s: %s" % (questionIndex+1, sentencelister(userAnswerStrings)))
        
answerstring = "; ".join(useroptions)
    
    
if not errors:
    ## The form fields look ok, so we can store the registration
    
    
    #return context.REQUEST
    ## Get the registration-options
    
        
    ## We must pack all the fieldnames into a single string. The easiest way is to use
    ## a separator-string with seldomly used characters and then hope that no user ever
    ## uses those exact characters.
    separator   = u"¤¨" # must be the same as used in seminar_view.py.py. We should probably put this in some common file...
    value = separator.join( (name, email, title, phone, workplace, answerstring ) )
    
    
    ## if we try to add an attendee-occurence with a value of an already existing attendee-occurence, no new
    ## occurence  will be created, and the context.createOccurrence() function will return
    ## the existing, matching attendee-object. I haven't found another way to check for
    ## this problem that by manually checking the values of the existing comments.
    ## I tried to do a check using the "modified()"-function of the attendee-object to 
    ## check if it was newly created, but that funcion is not available in this context (access denied).
    for existingattendee in context.listOccurrences(type=psis.attendee):
        existingname,existingemail = existingattendee.getValue().split(separator)[:2]
        if (existingemail == email) and (existingname == name):
            ## This means that an identical occurence already existed, so we must notify the user about it.
            errors.append( u"%s (%s)  er allerede påmeldt til dette seminaret." % (name,email))
            break
        
    if not errors:
        newcomment = context.createOccurrence(value,psis.attendee)
        if newcomment:
            messages.append(u"%s (%s) er nå meldt på til seminaret." % (name,email))                          
        else:
            errors.append( u"Kunne ikke lagre påmeldingen din! Snodig! (context.createOccurrence(value,psis.comment) returnerte fint lite)")


status = {}
if errors:
    status['errors'] = errors
if messages:
    status['messages'] = messages
    
if not errors:
    adminemail = context.portal.email_from_address
    title = context.title_or_id()
    startdate = context.getOccurrenceValue(psis.startdate)
    enddate = context.getOccurrenceValue(psis.enddate)
    location = context.getOccurrenceValue(psis.location)
    contactemail = context.getOccurrenceValue(psis.email) or adminemail  
    
    
    confirmationSubject = u"""Påmeldingsbekreftelse til %(title)s    
"""%{'title':title}

    valg = ""
    if answerstring:
      valg = "Valg:           %(options)s " % {'options':answerstring}
 

    confirmationBody = u"""Dette er en bekreftelse på at du er påmeldt %(title)s

Starttidspunkt: %(start)s
Sluttidspunkt:  %(end)s
Sted:           %(location)s
%(options)s
Skulle det være noe spørsmål så vennligst ta kontakt med %(email)s   

Informasjon om seminaret finner du på %(seminar_url)s

""" % {'title':title, 'start':startdate, 'end':enddate, 'location':location, 'email':contactemail, 'options':valg, 'seminar_url':context.absolute_url()}
    
    
    context.portal_topicmanagement.sendUnicodeMail(confirmationSubject
                                                 , '\n\n'+confirmationBody
                                                 , [email]
                                                 , adminemail
                                                 )
    
    adminSubject = u"Ny deltaker påmeldt %(title)s" % {'title':title}
     
    adminBody = u"""Navn:  %(name)s
Tittel: %(title)s
Arbeidssted: %(workplace)s
Telefon: %(phone)s
Epost: %(email)s
Valg:  %(options)s
""" % {'name':name, 'email':email, 'title':title, 'workplace':workplace, 'phone':phone, 'options':answerstring}

    context.portal_topicmanagement.sendUnicodeMail(adminSubject
                                                 , '\n\n'+adminBody
                                                 , [adminemail]
                                                 , adminemail
                                                 )
                                                 
    return context.seminar_view(status=status)
else:
    ## Note that we must include the current form-field values, so that the pagetemplate can fill them in again.
    currentvalues = {}
    if honeypots: ## honeypots may be None if the form-data has been tampered with (by a would-be spammer)
        for hashedfieldname,fieldname in honeypots['hashedfieldname2fieldname'].items():                
            currentvalues[fieldname] = context.REQUEST[hashedfieldname]
    
    for option in registrationOptionsCurrentValues:
        currentvalues[option] = True

  
    return context.seminar_view(status=status,
                                **currentvalues # these values are used to fill in the form again.
                                )
