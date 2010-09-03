##parameters=persontopic=None
# -*- coding: utf-8 -*-

from Products.ksiktforum import psis

workareatopic = context.workareatopic()
managers = workareatopic.managers()


request = context.REQUEST
response = request.RESPONSE

topicmap = context.getTopicMap()
atbsi = topicmap.assertTopicBySubjectIdentifier

if not persontopic:
    persontopic = context.getAuthenticatedMemberTopic()
if persontopic in managers:
        
    roletypetopic = atbsi(psis.subscribed) 
    
    #remove the subscription-association between the currently logged in user and the workarea        
    roles= workareatopic.listRoles(type=roletypetopic)   
    for role in roles:
        assoc = role.getAssociation()                     
        otherrole = assoc.getOtherRole(role)
        if otherrole.getPlayer().tm_serial == persontopic.tm_serial:                        
            context.removeAssociation(assoc)
                
    
    response.redirect(context.absolute_url()+'/workarea_view'+'?status.messages:ustring:utf8:list:record='+'Du vil ikke lenger bli varslet om endringer i dette arbeidsrommet.')

