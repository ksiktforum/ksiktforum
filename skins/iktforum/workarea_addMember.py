# -*- coding: utf-8 -*-
from Products.ksiktforum import psis

request = context.REQUEST
response = request.RESPONSE

persontopic = context.getAuthenticatedMemberTopic()
sender_email = persontopic.getOccurrenceValue(psis.email)
sender_title = persontopic.title_or_id()

topicmap = context.getTopicMap()
gtbs = topicmap.getTopicBySerial

admin_email = context.portal.email_from_address

def sendNotice(to_email, sender_title, workroomname):
    subject = u'Du er gitt tilgang til et arbeidsrom på KSIKT-Forum'
    body = u"""Automatisk beskjed fra KSIKT-Forum
    
%(sender_title)s <%(personurl)s> har gitt deg tilgang til arbeidsrommet %(workareaname)s <%(workareaUrl)s>    

Du vil også finne igjen lenke til dette arbeidsrommet på din personlige arbeidsflate
""" % {'sender_title':sender_title
         , 'workareaname':workroomname
         , 'personurl':persontopic.absolute_url()
         , 'workareaUrl':workareatopic.absolute_url()
         }
    context.portal_topicmanagement.sendUnicodeMail(subject, u'\n\n'+body, [to_email], admin_email)    

workareatopic = context.workareatopic()

tm_serials = request.get('tm_serial', [])
for tm_serial in tm_serials:
    addedPersontopic = gtbs(tm_serial)
    to_email = addedPersontopic.getOccurrenceValue(psis.email)    
    workareatopic.makeBinaryAssociation(othertopic=addedPersontopic
                                 ,assoctype=psis.workareamembership
                                 ,roletype=psis.workarea
                                 ,otherroletype=psis.workareamanager
    )    
    if to_email:
        sendNotice(to_email, persontopic.title_or_id(), workareatopic.title_or_id())
    
    

workareatopic.updateWorkArea()
workareatopic.reindexObject()     
#need to reindex the file topics in order to update allowedRolesAndUsers
lazy = context.portal_catalog(path='/'.join(workareatopic.getPhysicalPath()), types=[psis.file])
for brain in lazy:
    topic = brain.getObject()
    topic.reindexObject()

message = u"%s <%s> har blitt lagt til som medlem i arbeidsrommet %s <%s> av %s <%s>" % (addedPersontopic.title_or_id(), addedPersontopic.absolute_url(), workareatopic.title_or_id(), workareatopic.absolute_url(), persontopic.title_or_id(), persontopic.absolute_url())
alert_on_member_add = bool(workareatopic.getOccurrenceValue(psis.alert_on_add_newmember)) 
if alert_on_member_add:
    context.workarea_alert_change(message)

response.redirect("%s/workarea_view?status.messages:ustring:utf8:list:record=De valgte personene har nå tilgang til dette arbeidsrommet"%context.absolute_url())

