request = context.REQUEST
response = request.RESPONSE

serial = request.get('serial', 0)
context.moveAgendaObjectUp(serial)

response.redirect(context.absolute_url()+"#node_"+str(serial))

