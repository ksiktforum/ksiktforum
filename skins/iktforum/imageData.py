## Script (Python) "imageData.py"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters= imagetype=u'http://psi.ksikt-forum.no/ontology/caseimage', scope=None
##title=Get image and imagedata nicely packed in a dictionary
##
from Products.ksiktforum import psis
image = {}

scope=(context,)
try:
    imagetopic = context.portal_images.getDecoration(imagetype)
except AttributeError:
    imagetopic = None

if imagetopic:    
    address = imagetopic.resource_url()
    if address:
        occ = imagetopic.getOccurrenceValue(psis.dc_description, scope=scope, ignore=True, default='')
        original = list(imagetopic.associatedTopicsQuery(otherroletype=psis.original))
        photographer = ''
        if original:
          photographer = original[0].getOccurrenceValue(psis.photographer, ignore=True) or ''
        alttext = imagetopic.title_or_id()
        image =  { 'url': address
                 , 'text': occ
                 , 'alttext': alttext
                 , 'imagetopic' : imagetopic
                 , 'photographer' : photographer
                }
return image
