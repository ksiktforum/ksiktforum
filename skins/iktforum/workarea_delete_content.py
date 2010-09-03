# -*- coding: utf-8 -*-

topicmap = context.getTopicMap()
contentlist = context.REQUEST.get('selectedContent',[])

count = 0
for tm_serial in contentlist:
    topic = topicmap.getTopicBySerial(tm_serial)
    if topic:
        container = topic.aq_parent
        container.manage_delObjects([topic.id,])   
        count += 1
    
if count > 0:
    return personTopic.workspace_view(status={'messages':[u'De valgte elementene er nå slettet']})
else:
    return personTopic.workspace_view(status={'errors':[u'Ingen elementer var valgt.']})

    
