filetypes = { 'application/pdf' : 'pdf'
             ,'application/vnd.ms-excel' : 'excel'
             ,'application/vnd.ms-word' : 'word'
             ,'application/msexcel' : 'excel'
             ,'application/msword' : 'word'
             ,'application/mspowerpoint' : 'powerpoint'
             ,'application/vnd.oasis.opendocument.text' : 'odt'
             ,'application/vnd.oasis.opendocument.spreadsheet' : 'ods'             
             ,'image/png' : 'bilde'
             ,'image/jpeg' : 'bilde'
             ,'image/gif' : 'bilde'
            }

fileicons = { 'excel':'xls'
             ,'pdf':'pdf'
             ,'powerpoint':'ppt'
             ,'word':'doc'
             ,'bilde':'gif'
             ,'odt':'odt'
             ,'ods':'ods'
             ,'fil':'txt'
            }

filenames = { 'excel':'Excel file'
             ,'pdf':'PDF file'
             ,'word':'Word file'
             ,'powerpoint':'Powerpoint file'
             ,'bilde':'Image file'
             ,'odt':'OpenDocument file'
             ,'ods':'OpenDocument spreadsheet'
             ,'fil':'File'
            }

request = context.REQUEST
response = request.RESPONSE

serial = request.get('serial', False)
agendaNode = context.getAgendaNode(serial)


if request.REQUEST_METHOD.lower() == 'post':    
    #file upload
    files = request.get('newfile', [])
    filetitles = request.get('filetitle', [])
    overwrite = request.get('overwrite', False)
    target = request.get('target', 'documentbank_view')
        
    if agendaNode:    
        kw = {'title':request.get('title',u'')
             ,'ingress':request.get('ingress',u'')
              }
        agendaNode.update(kw)
        
        #file upload
        errors = []
        messages = []
        status = {}
        status['messages'] = messages
        status['errors'] = errors

        if len(files) != len(filetitles):   
            raise AssertionError, "inconsistent number for files and filetitles"    
        index = 0        
        documentbank = context.documentbanktopic()
        file_serials = []        
        for title in filetitles:      
            if title:
                f = files[index]        
                try:
                    tm_serial = documentbank.uploadFile(f, title, overwrite)
                    if overwrite:
                        if tm_serial in agendaNode.files:
                            pass
                        else:
                            file_serials.append(tm_serial)
                    else:
                        file_serials.append(tm_serial)
                    messages.append(u'Upload of %s was successful'%unicode(f.filename,'utf-8'))
                except AssertionError, e:    
                    errors.append(e)                
            else:
                pass        
            index = index+1   

        if errors:    
            target = 'documentbank_view'
            return getattr(context, target)(status=status)
                
        added_existing_files = request.get('added_existing_files', [])
        
        file_serials = file_serials + added_existing_files + agendaNode.files        
        
        #marked for removal
        toBeRemoved = request.get('remove_connectedFile', [])
        
        for tm_serial in toBeRemoved:
            file_serials.remove(tm_serial)
        
        
        update = {}
        
        
        update['files'] = file_serials
        if update:
            agendaNode.update(update)
        
    #TODO: Add message
    target = 'documentbank_view'#request.get('target', 'documentbank_view')
    responsetext = "&status.messages:ustring:utf8:list:record=The upload was successful"
    response.redirect(u'%s?%s%s' % (context.absolute_url(), target, responsetext))
    
else:
    content = {}
    
    topicmap = context.getTopicMap()
    gtbs = topicmap.getTopicBySerial
    
    if agendaNode:    
        
        #get all files from the filearchive        
        uploadedFiles = []
        append = uploadedFiles.append
        
        #lazy = context.portal_catalog(portal_type='file', path='/'.join(context.filearchive.getPhysicalPath()))
        lazy = context.portal_catalog(portal_type='file', sort_on="Title")
        for brain in lazy:
            topic = brain.getObject()
            if topic:
                fileobject = topic.resource_object()
                content_type = fileobject and fileobject.content_type or ""
                
                
                filetype = filetypes.has_key(content_type) and filetypes[content_type] or "fil"
                        
                file_icon = fileicons[filetype]
                file_type = filenames[filetype]
                append({  'attachment' : topic
                        , 'title': topic.title_or_id()
                        , 'url' : topic.resource_url()
                        , 'iconclass' : file_icon
                        , 'type': file_type
                        , 'disabled': topic.tm_serial in agendaNode.files
                        })    
        content['uploadedFiles'] = uploadedFiles
        
        connectedFiles = []
        append = connectedFiles.append
        
        for serial in agendaNode.files:
            topic =gtbs(int(serial))
            
            #lazy removal
            if not topic:
                agendaNode.files.remove(serial)
                continue
            
            fileobject = topic.resource_object()
            content_type = fileobject and fileobject.content_type or ""
            
            
            filetype = filetypes.has_key(content_type) and filetypes[content_type] or "fil"
                    
            file_icon = fileicons[filetype]
            file_type = filenames[filetype]
            append({  'attachment' : topic
                    , 'title': topic.title_or_id()
                    , 'filetitle': fileobject.title_or_id()
                    , 'tm_serial': topic.tm_serial
                    , 'url' : topic.resource_url()
                    , 'iconclass' : file_icon
                    , 'type': file_type
                    })
        
        content['connectedFiles'] = connectedFiles
        
        
    return content
    
    
    
        
