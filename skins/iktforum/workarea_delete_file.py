# -*- coding: utf-8 -*-

request = context.REQUEST
response = request.RESPONSE

topicmap = context.getTopicMap()
gtbs = topicmap.getTopicBySerial

tm_serials = request.get('tm_serial', [])

workareatopic = context.workareatopic()

creationpath = workareatopic.filer

for tm_serial in tm_serials:
    topic = gtbs(tm_serial)
    resource = topic.resource_object()
    #topicmap.removeTopic(topic)
    workareatopic.filer.manage_delObjects([resource.id, topic.id])

status="/workarea_view?status.messages:ustring:utf8:list:record=De valgte filene ble slettet"
response.redirect(context.absolute_url()+status)
