from Products.ksiktforum import psis

request = context.REQUEST
response = request.RESPONSE

context.enableRoleOrder()
order = context.internalroleorder
moveup = request.form.get('move_up',())
movedown = request.form.get('move_down',())
roles = request.form.get('assoclist',())
distance = request.form.get('move_length',  0)
distance = int(distance)
#print roles
#print distance
if roles and distance:
    roleserials = [int(role) for assoc, role in roles]
    if moveup:
       #print 'opp'
       context.reorderRoles(roleserials, -distance)									
    else:
       context.reorderRoles(roleserials, distance)				
       #print 'ned'

#return printed
response.redirect("%s/sort_view"%( context.absolute_url()))
