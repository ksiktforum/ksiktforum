# -*- coding: utf-8 -*-

from Products.ksiktforum import psis
## This script is used to delete a comment (psis.comment) from articles (and other 
## content-types that has comments).

user = context.portal_membership.getAuthenticatedMember()

request = context.REQUEST
response = request.RESPONSE

requiredRole = "Manager" # TODO: update the way we do the permission-checks, once Svein Arild is sure how to
                         #       set up the security-system and do the checks.                         
if not requiredRole in user.getRoles():
    return u"""Du har ikke rettigheter til å gjøre dette! Du har bare rollene %s, men du må ha rollen "%s".""" % (user.getRoles(),requiredRole)
else:  
    deleteCount = 0  
    deletecomments = request.get('deletecomment', [])    
    for tmserial in deletecomments:       
        try:
            comment = context.getOccurrence(tmserial)
            context.removeOccurrence(comment)
            deleteCount += 1 
        except KeyError:
            pass # This happens if the user deletes one or more comments, and then clicks the 
                 # "reload" button in his browser. (context.getOccurrence(tmserial) will throw a KeyError exception)
            
    if deleteCount > 0:
        plural = ""
        if deleteCount > 1:
            plural = "er"
        messages = [u"%d kommentar%s ble slettet." % (deleteCount,plural,)]        
    else:
        messages = [u"Du må markere en eller flere kommentarer for å slette dem.",]
options = {}
options['status'] = {}
options['status']['errors'] = []
options['status']['messages'] = messages 
return context.content_view(**options)

        