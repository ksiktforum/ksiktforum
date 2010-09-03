# -*- coding: utf-8 -*-

from DateTime import DateTime
from Products.ksiktforum import psis

request = context.REQUEST
response = request.RESPONSE

#file upload
files = request.get('newfile', [])
filetitles = request.get('filetitle', [])
overwrite = request.get('overwrite', False)
target = request.get('target', 'workarea_view')

errors = []
messages = []
status = {}
status['messages'] = messages
status['errors'] = errors


if len(files) != len(filetitles):
    raise AssertionError, "inconsistent number for files and filetitles"
    
index = 0
        
workarea = context.workareatopic()
file_serials = []        
for title in filetitles:      
    if title:
        f = files[index]        
        try:
            workarea.uploadFile(f, title, overwrite)
            messages.append(u'Upload of %s was successful'%unicode(f.filename,'utf-8'))
        except AssertionError, e:    
            errors.append(e)                
    else:
        pass        
    index = index+1   

if errors:
    return getattr(context, target)(status=status)

#responsetext = u''
#for message in messages:
#    responsetext = responsetext + u'status.messages:ustring:utf8:list:record='+message+u'&'
#for error in errors:
#    responsetext = responsetext + u'status.errors:ustring:utf8:list:record='+error+u'&'
responsetext = "status.messages:ustring:utf8:list:record=The upload was successful"
response.redirect(u'%s/%s?%s' % (context.absolute_url(), target, responsetext)) 

