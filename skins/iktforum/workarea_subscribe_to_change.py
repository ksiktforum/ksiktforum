##parameters=persontopic=None
# -*- coding: utf-8 -*-

from Products.ksiktforum import psis

request = context.REQUEST
response = request.RESPONSE

workareatopic = context.workareatopic()
managers = workareatopic.managers()

if not persontopic:
    persontopic = context.getAuthenticatedMemberTopic()
if persontopic in managers:
    context.makeBinaryAssociation(
                                   persontopic #othertopic
                                 , psis.subscription #assoctype
                                 , psis.subscribed #roletype
                                 , psis.workarea_subscriber # otherroletype
                                 )
    response.redirect(context.absolute_url()+'/workarea_view'+'?status.messages:ustring:utf8:list:record='+'Varsel når det skjer endringer i dette arbeidsrommet er nå slått på. Du vil bli tilsendt epost på epostadressen oppgitt i din profil når det legges inn nye innlegg.')

