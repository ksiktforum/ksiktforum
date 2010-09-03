# -*- coding: utf-8 -*-

from Products.ksiktforum import psis
## This script is used to remove attendees from (psis.attendee) from a seminar.

user = context.portal_membership.getAuthenticatedMember()

request = context.REQUEST
response = request.RESPONSE

requiredRole = "Manager" # TODO: update the way we do the permission-checks, once Svein Arild is sure how to
                         #       set up the security-system and do the checks.                         
if not requiredRole in user.getRoles():
    return u"""Du har ikke rettigheter til å gjøre dette! Du har bare rollene %s, men du må ha rollen "%s".""" % (user.getRoles(),requiredRole)
else:  
    deleteCount = 0  
    removeattendee = request.get('removeattendee', [])    
    for tmserial in removeattendee:       
        try:
            attendee = context.getOccurrence(tmserial)
            context.removeOccurrence(attendee)
            deleteCount += 1 
        except KeyError:
            pass # This happens if the user removes one or more attendees, and then clicks the 
                 # "reload" button in his browser. (context.getOccurrence(tmserial) will throw a KeyError exception)
            
    if deleteCount > 0:
        plural = ""
        if deleteCount > 1:
            plural = "e"
        messages = [u"%d deltaker%s ble fjernet." % (deleteCount,plural,)]        
    else:
        messages = [u"Du må markere en eller flere deltakere for å fjerne dem.",]
options = { 'status': {
               'errors'  : [],
               'messages': messages,
               }}
 
return context.seminar_view(**options)

        