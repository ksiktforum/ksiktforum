# -*- coding: utf-8 -*-

from Products.ksiktforum import psis

request = context.REQUEST
response = request.RESPONSE

persontopic = context.getAuthenticatedMemberTopic()

context.makeBinaryAssociation(
                               persontopic #othertopic
                             , psis.subscription #assoctype
                             , psis.subscribed #roletype
                             , psis.discussion_subscriber # otherroletype
                             )
response.redirect(context.absolute_url()+'/discussion_view'+'?status.messages:ustring:utf8:list:record='+'Epostvarsling for denne diskusjonen er nå slått på. Du vil bli tilsendt epost på epostadressen oppgitt i din profil når det legges inn nye innlegg.')


