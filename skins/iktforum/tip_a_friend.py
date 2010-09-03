# -*- coding: utf-8 -*-
from Products.ksiktforum import psis

request = context.REQUEST
response = request.RESPONSE

errors = []
messages = []
status = {}
tip_from_email = request.get('tip_from_email', None)
tip_to_email = request.get('tip_to_email', None)

if not context.portal_topicmanagement.validateMailURI(tip_from_email):
    errors.append(u'Du må skrive inn en gyldig epostadresse i feltet for din epostadresse')
if not context.portal_topicmanagement.validateMailURI(tip_to_email):
    errors.append(u'Du må skrive inn en gyldig epostadresse i feltet for mottakers epostadresse')

if errors:
    status['errors'] = errors
    return context.content_view(status=status, tip_from_email=tip_from_email, tip_to_email=tip_to_email)

subject = u'Tips om innhold på KSIKT-Forum'    
title = context.title_or_id()
ingress = context.getOccurrenceValue(psis.ingress, default="", ignore=True)

typetext = context.Type().lower()

mailbody = u"""\n\n
Vi er blitt bedt om å tipse deg om %(type)s på ksikt-forum.no av %(tip_from_email)s.

%(ingress)s

Les mer her: <%(absolute_url)s>.
"""%{'tip_from_email':tip_from_email, 'ingress':ingress, 'absolute_url':context.absolute_url(), 'type':'innhold'}

#def sendUnicodeMail(self, subject, message, recipients, sender, REQUEST=None):
context.portal_topicmanagement.sendUnicodeMail(subject, mailbody, [tip_to_email] ,tip_from_email)

messages.append(u'Tipset har nå blitt sendt til '+tip_to_email)
status['messages'] = messages
return context.content_view(status=status)

