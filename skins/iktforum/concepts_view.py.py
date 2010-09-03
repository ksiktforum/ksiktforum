# -*- coding: utf-8 -*-

from Products.ksiktforum import psis


concepts = []
content = {'concepts' : concepts,
           }

for brain in context.portal_catalog(portal_type='concept',sort_on='Title'
                                    ):
    concept = brain.getObject()
    concepts.append(
                    {'title' : concept.title_or_id(),
                     'ingress':concept.getOccurrenceValue(psis.ingress,ignore=True,default=""),
                     'url'    :concept.absolute_url(),
                     }
                    )
return content