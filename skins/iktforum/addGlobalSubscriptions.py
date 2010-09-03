from Products.ksiktforum import psis

request = context.REQUEST
response = request.RESPONSE


lazy = context.portal_catalog(portal_type=['workarea',])
for brain in lazy:
    workareatopic = brain.getObject()
    managers = workareatopic.managers()
    for persontopic in managers:
        workareatopic.makeBinaryAssociation(
                                       persontopic #othertopic
                                     , psis.subscription #assoctype
                                     , psis.subscribed #roletype
                                     , psis.workarea_subscriber # otherroletype
                                     )