# -*- coding: utf-8 -*-

from Products.ksiktforum import psis
from Products.stripogram import html2text, html2safehtml
import DateTime

errors = [] ## If any problems with the form is detected, the error-messages will be added to this list.
formErrorMsg = u"" ## This will be set to a user-readable error-message if the form contains an error.
name    = u""
email   = u""
heading = u""
comment = u""

## Check that the anti-spam honeypot information looks ok, and get the mappings between the obfuscated 
## fieldnames and the real fieldnames.
(honeypots,formErrorMsg) = context.checkHoneyPots( context,  ("name","email","heading","comment") )

if formErrorMsg:
    ## This looks like a spam-bot, so we can skip the rest of the checks.
    errors.append(formErrorMsg)
else:
    ## Get the values of the form fields that contain the actual user-entered data.
    name    = html2text(    context.REQUEST[honeypots['fieldname2hashedfieldname']["name"]])
    email   = html2text(    context.REQUEST[honeypots['fieldname2hashedfieldname']["email"]])
    heading = html2safehtml(context.REQUEST[honeypots['fieldname2hashedfieldname']['heading']])
    comment = html2safehtml(context.REQUEST[honeypots['fieldname2hashedfieldname']["comment"]])
    
    ## Check that all the required fields are present
    for visibleFieldName,maxsize,fieldvalue in ( ("Navn",          100,  name),
                                                 ("Epostadresse",  255,  email),
                                                 ("Overskrift",     50,  heading),
                                                 ("Kommentar",    1000,  comment) ):
        if fieldvalue.strip() == "":
            errors.append( u"""Du må skrive noe i "%s" boksen.""" % (visibleFieldName,))
            
        
        if len(fieldvalue) > maxsize:
            errors.append(u"""Teksten i "%s" boksen er for lang! Prøv å korte ned teksten litt.""" % (visibleFieldName,))



    ## Check if the email-address looks plausible. 
    if email and not context.portal_topicmanagement.validateMailURI(email):      
        errors.append(u"Du må skrive inn en gyldig Epostadresse.")
        
    
if not errors:
    ## The form fields look ok, so we can store the comment
        
    ## We must pack all the fieldnames into a single string. The easiest way is to use
    ## a separator-string with seldomly used characters and then hope that no user ever
    ## uses those exact characters.
    separator   = u"¤¨" # must be the same as used in comment.py.py. We should probably put this in some common file...
    value = separator.join( (name, email, heading, comment) )
    
    
    ## if we try to add a comment with a value of an already existing comment, no new
    ## comment will be created, and the context.createOccurrence() function will return
    ## the existing, matching comment-object. I haven't found another way to check for
    ## this problem that by manually checking the values of the existing comments.
    ## I tried to do a check using the "modified()"-function of the comment-object to 
    ## check if it was newly created, but that funcion is not available in this context (access denied).
    for existingcomment in context.listOccurrences(type=psis.comment):
        if existingcomment.getValue() == value:
            ## This means that an identical comment already existed, so we must notify the user about it.
            errors.append( u"Kunne ikke lagre kommentaren din, siden en identisk kommentar allerede eksisterer.")
            break
        
    if not errors:
        newcomment = context.createOccurrence(value,psis.comment)
        if not newcomment:
            errors.append( u"Kunne ikke lagre kommentaren din! Snodig! (context.createOccurrence(value,psis.comment) returnerte fint lite)")

    
if not errors:
    sucessurl = context.absolute_url()+'?status.messages:ustring:utf8:list:record=Kommentaren din ble lagt til.'
    context.REQUEST.RESPONSE.redirect(sucessurl)
    return context.content_view(commentWasAddedOk=True,
                                status={'messages':(u"Kommentaren din ble lagret, og vises nederst på listen over kommentarer.",),
                                        }, # This is used by content_view.pt to display the message
                                )
else:
    ## Note that we must include the current form-field values, so that the pagetemplate can fill them in again.
    currentvalues = {}
    if honeypots: ## honeypots may be None if the form-data has been tampered with (by a would-be spammer)
        for hashedfieldname,fieldname in honeypots['hashedfieldname2fieldname'].items():                
            currentvalues[fieldname] = context.REQUEST[hashedfieldname]
  
    
    return context.content_view(formErrorMsg=formErrorMsg,    # 
                           status={'errors':errors}, # This is used by content_view.pt to display the error(s)
                           **currentvalues # these values are used to fill in the form again.
                           )

