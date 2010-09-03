# -*- coding: utf-8 -*-

from DateTime import DateTime
from Products.ksiktforum import psis

request = context.REQUEST
response = request.RESPONSE

file = request.get('file', None)

overwrite = request.get('overwrite', False)

errors = []
messages = []
status = {}
status['messages'] = messages
status['errors'] = errors
membertopic = context.getAuthenticatedMemberTopic()
if not file:
    errors.append(u'Du har ikke valgt noen fil')
    return context.workarea_view(status=status)

topicmap = context.portal_topicmaps.getTopicMap()
atbsi = topicmap.assertTopicBySubjectIdentifier

filetopictype = atbsi(psis.file)

workareatopic = context.workareatopic()

creationpath = workareatopic.filer

filename = altTopicTitle = context.portal_topicmanagement.extractFilename(unicode(file.filename, 'utf8'))

origname = filename = context.portal_topicmanagement.normalizeid(filename)

counter = 1

idIsAvailable = creationpath.checkIdAvailable(filename)

if not idIsAvailable:
    if overwrite:
        topicid = filename+".topic"
        #delete topic and file        
        creationpath.manage_delObjects([filename, topicid])        
        idIsAvailable = True
    else:
        errors.append("En fil ved dette navnet eksisterer allerede. Ønsker du å overskrive denne filen må du markere for dette ved å krysse av for 'Overskriv hvis filen finnes fra før'")

if errors:
    return context.workarea_view(status=status)

checkIdAvailable = creationpath.checkIdAvailable
while not idIsAvailable:
    filename = origname[0:origname.rindex('.')]+'_'+str(counter)+'_'+origname[origname.rindex('.'):]
    counter += 1        
    idIsAvailable = checkIdAvailable(filename)    
    if counter >= 50:
            raise AssertionError, "You entered an endless loop during fileupload. This should not have happened. Please write down the steps you used to trigger this bug and report it to the ZTM developers."

  
title = request.get('title', '')
if not title:
    title = altTopicTitle

request.set('type_name', 'File')
creationpath.invokeFactory(type_name='File', id=filename)
newfile = getattr(creationpath, filename)
newfile.manage_upload(file)

#create file topic. set file as subjectlocatior
topicid = filename+".topic"
request.set('type_name', 'file')
creationpath.invokeFactory(type_name='file', id=topicid)
filetopic = getattr(creationpath, topicid)

filetopic.setTitleAndName(title)
filetopic.addSubjectLocator('x-zope-path:' + '/'.join(newfile.getPhysicalPath()))

filetopic.manage_permission("View",('Owner','Workarea manager'), acquire=0)
filetopic.manage_permission("Access contents information",('Owner','Workarea manager'), acquire=0)
filetopic.reindexObject()

message = u"Filen %s <%s> har blitt lastet opp i arbeidsrommet %s <%s> av %s <%s>" % (title, filetopic.absolute_url(), workareatopic.title_or_id(), workareatopic.absolute_url(), membertopic.title_or_id(), membertopic.absolute_url())
context.workarea_alert_change(message)

message = u"Opplastingen av filen %s var vellykket" % (filename,)
response.redirect('%s/workarea_view?status.messages:ustring:utf8:list:record=%s' % (context.absolute_url(), message))

