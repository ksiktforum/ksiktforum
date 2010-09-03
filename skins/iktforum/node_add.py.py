request = context.REQUEST
response = request.RESPONSE

serial = request.get('serial', 0)
level = request.get('level', 0)
title = request.get('title', u'No title set')
ingress = request.get('ingress', u'No title set')    
context.addAgendaObject(title, ingress, serial, level)   



status = u'#node_'+str(serial)+u'?status.messages:record:ustring:utf8:list=The node was successfully added'
response.redirect(context.absolute_url()+status)

    

