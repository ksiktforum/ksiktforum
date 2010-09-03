# -*- coding: utf-8 -*-

from DateTime import DateTime
from Products.ksiktforum import psis

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
            
content = {}
threads = []
content['threads']=threads

topicmap = context.getTopicMap()
gtbs = topicmap.getTopicBySerial

latestchanges = []
append = latestchanges.append
lazy = context.portal_catalog(path='/'.join(context.getPhysicalPath()), types=[psis.file, psis.discussionthread], sort_on='modified', sort_order='Reverse')
for brain in lazy[:3]:
    topic = brain.getObject()
    if topic:
        append({'absolute_url':topic.resource_url() or topic.absolute_url()
                ,'type_and_date': topic.Type()+', '+context.ZopeTime(topic.Date()).strftime('%d.%m.%Y %H:%M')            
                ,'title_or_id':topic.Title() or topic.resource_object().title_or_id()
                })
            
content['latestchanges'] = latestchanges

files = []
append = files.append
lazy = context.portal_catalog(path='/'.join(context.getPhysicalPath()), types=[psis.file], sort_on='modified', sort_order='Reverse')

for brain in lazy:
    topic = brain.getObject()    
    fileobject = topic.resource_object()
    content_type = fileobject and fileobject.content_type or ""           
    filetype = filetypes.has_key(content_type) and filetypes[content_type] or "fil"                
    file_icon = fileicons[filetype]
    file_type = filenames[filetype]  
       
    is_open = False
    append({'title':topic.title_or_id()
    ,'filetitle':fileobject.title_or_id()
    ,'Creator':topic.Creator
    ,'iconclass':file_icon
    ,'modified': context.ZopeTime(topic.modified()).strftime('%d.%m.%Y %H:%M')
    ,'tm_serial':topic.tm_serial
    ,'url':fileobject.absolute_url()
    ,'is_open':is_open
        
    })
content['files'] = context.documentbanktopic().fileArchiveContents()

widgetMapping = {'edit':'node_edit'
                ,'add':'node_add'
}    

action = request.get('action','view')
action_serial = request.get('serial', 0)




def file_mapper(agendaNode):
    files = agendaNode.files
    
    connectedFiles = []
    append = connectedFiles.append
    for serial in files:        
        try:
            topic =gtbs(int(serial))
        except KeyError:        
            agendaNode.files.remove(serial)
            continue
        
        if topic:
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
    connectedFiles = [(x['title'].lower(),x) for x in connectedFiles]
    connectedFiles.sort()
    connectedFiles = [y for (x,y) in connectedFiles]

    return connectedFiles

isEditor = False
isContributor = False
member = context.portal_membership.getAuthenticatedMember()
if member:
    rolesInContext = member.getRolesInContext(context)    
    if u'Editor' in rolesInContext or u'Manager' in rolesInContext:
        isEditor = True
    else:
        isContributor = True
    
    
def agendaGenerator(serials, level=1, toplevel=True, toplevelIndex=1):
    level = level + 1    
    sublevel = 0
    agendaHTML = u'<ol>'    
    siblingNumber = 0
    numberOfSiblings = len(serials)    
    for serial in serials:    
        levelIndicator = " "
        if toplevel:
            pass
            #levelIndicator = str(siblingNumber+1)+" "
            #toplevelIndex = siblingNumber+1
        else:
            pass
            #levelIndicator = (str(toplevelIndex)+".")*(level-2)+str(siblingNumber+1)+" "
        
        agendaNode = context.getAgendaNode(serial)        
        if agendaNode:           
            agendaHTML = agendaHTML + u'<li id="node_'+str(serial)+'">'
            strLevel = str(level) 
            title = u'no title'
            serial = agendaNode.serial            
            
            widget = 'node'  
            
            up = bool(siblingNumber > 0)
            down = bool(siblingNumber == numberOfSiblings-1)            
            indent  = bool(siblingNumber > 0)
            outdent = bool(agendaNode.parent)
            
            
            
            title = u'<h'+strLevel+u'>'+levelIndicator+agendaNode.title+u'</h'+strLevel+'>'
            ingress = agendaNode.ingress
            
            options = {'widget': {            
                                     'title':title
                                    ,'ingress':ingress
                                    ,'serial':serial
                                    ,'connectedFiles': file_mapper(agendaNode)
                                    ,'debug': agendaNode      
                                    ,'up': up
                                    ,'down':down
                                    ,'indent':indent
                                    ,'outdent':outdent    
                                    ,'isEditor':isEditor
                                }            
                      }        
            
            
              
            if serial == action_serial:
                widget = widgetMapping.get(action, 'node')
                if action == 'edit':
                    title = agendaNode.title
                if action == 'add':                                        
                    agendaHTML = agendaHTML + getattr(context, 'node')(**options)                        
            
            options['widget']['title'] = title
            agendaHTML = agendaHTML + getattr(context, widget)(**options)            
            
            #agendaHTML = agendaHTML + '</div>'
            if agendaNode.children:
                agendaHTML = agendaHTML + agendaGenerator(agendaNode.children, level, toplevel=False, toplevelIndex=toplevelIndex)
            
            agendaHTML = agendaHTML + u'</li>'
            siblingNumber = siblingNumber + 1
    agendaHTML = agendaHTML + u'</ol>' 
    return agendaHTML

content['agendaHTML'] = agendaGenerator(context.getAgenda())
content['toplevel'] = context.getAgenda()

content['is_open'] = context.documentbanktopic().isOpen()


return content

