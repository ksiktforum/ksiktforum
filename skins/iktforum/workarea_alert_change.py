##parameters=message=u''
# -*- coding: utf-8 -*-
from Products.ksiktforum import psis

workarea = context.workareatopic()
admin_email = context.portal.email_from_address
if workarea:
    subject = u'Automatisk varsel om oppdatering i arbeidsrommet %s' % workarea.title_or_id()    
    subscribers = context.associatedTopicsQuery( associationtype = psis.subscription
                                                   , roletype   = psis.subscribed
                                                   , otherroletype = psis.workarea_subscriber
                                                   , topictype  = psis.person
                                                   )
    receivers = []
    
    for subscriber in subscribers:
        email = subscriber.getOccurrenceValue(psis.email)
        if email:
            receivers.append(email)
            
    if receivers:
        message = u'Automatisk beskjed fra KSIKT-Forum\n\n' + message +u'\n\nDu kan skru av endringsvarsel for individuelle arbeidsrom ved å trykke på knappen "Deaktiver endringsvarsel" som du finner i høyre kolonne i alle arbeidsrom'
        context.portal_topicmanagement.sendUnicodeMail(subject, u'\n\n'+message, receivers, admin_email)
            
            
    