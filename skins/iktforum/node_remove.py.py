request = context.REQUEST
response = request.RESPONSE

nodeToRemoveSerial = request.get('serial', None)
if nodeToRemoveSerial:
    context.removeAgendaObject(nodeToRemoveSerial)
    
    status = u'?status.messages:record:ustring:utf8:list=The node has successfully been removed'
    
    response.redirect(context.absolute_url()+status)
