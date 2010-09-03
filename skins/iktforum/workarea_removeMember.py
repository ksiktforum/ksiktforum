# -*- coding: utf-8 -*-
from Products.ksiktforum import psis

request = context.REQUEST
response = request.RESPONSE

tm_serials = request.get('tm_serial', [])

workareatopic = context.workareatopic()
roletypetopic = psis.workarea

persontopic = context.getAuthenticatedMemberTopic()
sender_email = persontopic.getOccurrenceValue(psis.email)
sender_title = persontopic.title_or_id()

topicmap = context.getTopicMap()
gtbs = topicmap.getTopicBySerial
atbsi = topicmap.assertTopicBySubjectIdentifier

admin_email = context.portal.email_from_address

def sendNotice(to_email, sender_title, workroomname):
    subject = u'Du mistet tilgang til et arbeidsrom på KSIKT-Forum'
    body = u"""Automatisk beskjed fra KSIKT-Forum
    
%(sender_title)s <%(personurl)s> har tatt fra deg tilgangen til arbeidsrommet %(workareaname)s <%(workareaUrl)s>    
""" % {'sender_title':sender_title
         , 'workareaname':workroomname
         , 'personurl':persontopic.absolute_url()
         , 'workareaUrl':workareatopic.absolute_url()
         }
    context.portal_topicmanagement.sendUnicodeMail(subject, u'\n\n'+body, [to_email], admin_email)


subscribedTopic = atbsi(psis.subscribed)

for tm_serial in tm_serials:
    removedPersontopic = gtbs(tm_serial)    
    #remove person as subscriber to the workarea
    workareatopic.workarea_unsubscribe_to_change(removedPersontopic)
    
    #remove this association        
    roles= workareatopic.listRoles(type=roletypetopic)      
    
    to_email = removedPersontopic.getOccurrenceValue(psis.email)    
    for role in roles:
        assoc = role.getAssociation()                     
        otherrole = assoc.getOtherRole(role)
        if otherrole.getPlayer().tm_serial == tm_serial:                        
            context.removeAssociation(assoc)            

    #remove person as subscriber to discussions in this workroom
    for discussion in context.associatedTopicsQuery(associationtype=psis.discussion):
        subscribers = discussion.associatedTopicsQuery( associationtype = psis.subscription
                                           , roletype   = psis.subscribed
                                           , otherroletype = psis.discussion_subscriber
                                           , topictype  = psis.person
                                           )
        for subscriber in subscribers:
            if subscriber == removedPersontopic:
                #remove the subscription-association between the currently logged in user and the discussiontopic        
                roles= discussion.listRoles(type=subscribedTopic)   
                for role in roles:
                    assoc = role.getAssociation()                     
                    otherrole = assoc.getOtherRole(role)
                    if otherrole.getPlayer().tm_serial == removedPersontopic.tm_serial:                        
                        context.removeAssociation(assoc)
                        
    if to_email:
        sendNotice(to_email, removedPersontopic.title_or_id(), workareatopic.title_or_id())
        
        
workareatopic.updateWorkArea()
workareatopic.reindexObject()       
#need to reindex the file topics in order to update allowedRolesAndUsers
lazy = context.portal_catalog(path='/'.join(workareatopic.getPhysicalPath()), types=[psis.file])
for brain in lazy:
    topic = brain.getObject()
    topic.reindexObject()
response.redirect("%s/workarea_view?status.messages:ustring:utf8:list:record=De valgte medlemmene har ikke lenger tilgang til dette arbeidsrommet"%context.absolute_url())