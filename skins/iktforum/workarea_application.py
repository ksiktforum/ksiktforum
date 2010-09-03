# -*- coding: utf-8 -*-

from Products.ksiktforum import psis

request = context.REQUEST
response = request.RESPONSE

status = {}
messages = []
errors = []
status['messages'] = messages
status['errors'] = errors

persontopic = context.getAuthenticatedMemberTopic()
sender_email = persontopic.getOccurrenceValue(psis.email)
if not sender_email:
    errors.append(u'Du må ha fylt ut din epostadresse i din personlige profil før du kan søke om arbeidsrom')

workarea_title = request.get('workarea_title' , '')
if not workarea_title:
    errors.append(u'Tittel er et påkrevd felt når du skal søke om et arbeidsrom')
    
if errors:
    return context.workspace_view(status=status)
    
workarea_description = request.get('workarea_description', '')

#TODO: send application to webeditor
subject = u'Søknad om opprettelse av arbeidsrom på KSIKT-Forum'
body = u"""%(name)s <%(personurl)s> ønsker å få opprettet et arbeidsrom. Han/hun har oppgitt følgende informasjon:
    
Tittel:
%(title)s

Beskrivelse:
%(description)s

""" % {'name':persontopic.title_or_id()
     , 'personurl':persontopic.absolute_url()
     , 'title':workarea_title
     , 'description': workarea_description or u'Innsender gav ingen beskrivelse'
     }
     
admin_email = context.portal.email_from_address

context.portal_topicmanagement.sendUnicodeMail(subject, u"\n\n"+body, admin_email, sender_email)
#(self, subject, message, recipients, sender, REQUEST=None):

response.redirect(context.absolute_url()+'/workspace_view?status.messages:ustring:utf8:list:record=Søknad sendt til webredaktør. Du vil motta en epost når arbeidsrommet har blitt godkjent og opprettet')

    
