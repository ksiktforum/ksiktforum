## Script (Python) "structureddata.py"
##bind container=container
##bind context=context
##bind namespace=ns
##bind script=script
##bind subpath=traverse_subpath
##parameters=scope=None
##title=
##

#from Products.ksiktforum import psis

topicmap = context.getTopicMap()
atbsi = topicmap.assertTopicBySubjectIdentifier
structuredmarker = atbsi(u'http://psi.ksikt-forum.no/ontology/structuredmarker')#atbsi(psis.structuredmarker)

def mailto(data):
    return u'<a href="mailto:%s">%s</a>'%(data,data)

formatters = { 'mailto': mailto
             }

occs_to_process = []
fieldnames = {}

if hasattr(context,'getTypes'):
    for topictype in context.getTypes():
        occs = topictype.listAllOccurrences()
        occtypesserials = [occ.getType().tm_serial for occ in occs if occ.getType()]
        for supertype in topictype.getSuperTypes() :
            superoccs = supertype.listAllOccurrences()
            for superocc in superoccs:
                superocctype = superocc.getType()
                if superocctype and superocctype.tm_serial not in occs:
                    occs.append(superocc)
        for occurrence in occs:
            occtype = occurrence.getType()
            if occtype:
                marker = occtype.getOccurrence(structuredmarker, ignore=True)
                if marker:
                    markerdata = marker.getData()
                    if marker and bool(markerdata):
                        serial = occtype.tm_serial
                        occs_to_process.append(serial)
                        if not serial in fieldnames:
                            data = occurrence.getData().strip()
                            if markerdata in formatters:
                                data = formatters[markerdata](data)
                            fieldnames[occtype.tm_serial] = occtype.title_or_id().capitalize()#occtype.getName(psi.titletopic,scope=topictype)
    structured_data = []
    append = structured_data.append
    for occurrence in context.listAllOccurrences():
        occtype = occurrence.getType()
        if occtype and occtype.tm_serial in occs_to_process:
            append((occs_to_process.index(occtype.tm_serial), fieldnames[occtype.tm_serial], occurrence.getData()))
    structured_data.sort()
         
    templist = []
    
    for index, title,value in structured_data:
        if value:
            # XXX: hack
            
            if title.lower() == 'hjemmeside' or title.lower() == 'lenke':
                templist.append({'title': title , 'value':'<a href="%s">%s</a>' % (value, context.title_or_id())})
            elif title.lower() == 'epost':
                templist.append({'title':title, 'value':mailto(value)})
            else:
                templist.append({'title':title, 'value':value})
  
    return templist
return []
