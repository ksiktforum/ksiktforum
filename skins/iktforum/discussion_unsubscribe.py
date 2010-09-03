# -*- coding: utf-8 -*-

from Products.ksiktforum import psis

request = context.REQUEST
response = request.RESPONSE

topicmap = context.getTopicMap()
atbsi = topicmap.assertTopicBySubjectIdentifier

persontopic = context.getAuthenticatedMemberTopic()

roletypetopic = atbsi(psis.subscribed) 

#remove the subscription-association between the currently logged in user and the current discussiontopic        
roles= context.listRoles(type=roletypetopic)   
for role in roles:
    assoc = role.getAssociation()                     
    otherrole = assoc.getOtherRole(role)
    if otherrole.getPlayer().tm_serial == persontopic.tm_serial:                        
        context.removeAssociation(assoc)
            

response.redirect(context.absolute_url()+'/discussion_view'+'?status.messages:ustring:utf8:list:record='+'Du vil ikke lenger bli varslet på epost når det kommer nye innlegg til denne diskusjonen.')


