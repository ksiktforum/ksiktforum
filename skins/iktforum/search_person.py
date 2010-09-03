# -*- coding: utf-8 -*-

from Products.ksiktforum import psis

request = context.REQUEST
response = request.RESPONSE

searchableText = request.get('searchableText', '')
lazy = context.portal_catalog(types=psis.person, sort_on="Title", sort_order="reverse", SearchableText=searchableText)
persons = []
append = persons.append
workareamembers = list(context.associatedTopicsQuery(  associationtype = psis.workareamembership
                                           , roletype   = psis.workarea
                                           , otherroletype = psis.workareamanager
                                           , topictype  = psis.person
                                           ))
                                           
for brain in lazy:
    topic = brain.getObject()
    if topic not in workareamembers:        
        append({'title_or_id':brain.Title
               ,'tm_serial':brain.tm_serial    
               ,'absolute_url':brain.getURL()
        })
    

return context.workarea_view(persons=persons)
