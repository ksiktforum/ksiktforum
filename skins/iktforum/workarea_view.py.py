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

filenames = { 'excel':'Excel-fil'
             ,'pdf':'PDF-fil'
             ,'word':'Word-fil'
             ,'powerpoint':'Powerpoint-fil'
             ,'bilde':'Bildefil'
             ,'odt':'OpenDocument-fil'
             ,'ods':'OpenDocument regneark-fil'
             ,'fil':'Fil'
            }


content = {}
threads = []
content['threads']=threads

topicmap = context.getTopicMap()
gtbs = topicmap.getTopicBySerial

for thread in context.associatedTopicsQuery(associationtype=psis.discussion
                                             , sort='date'
                                                     ):
    
    
    authors = thread.associatedTopicsQuery(  associationtype = psis.authorship
                                           , roletype   = psis.discussionthread
                                           , otherroletype = psis.author
                                           , topictype  = psis.person
                                           )
    authorinfo = {}
    for author in authors:
        authorinfo = { "name" : author.title_or_id(),
                     "email": author.getOccurrenceValue(psis.email,ignore=True,default=""),
                     "url"  : author.absolute_url(),
                     }
        break  # there should be only one author.


    followups = thread.associatedTopicsQuery(  associationtype = psis.discussion, sort='date')
    followupCount = -1
    lastFollowupTime = DateTime(0)
    lastFollowup = None
    for followup in followups:
        followupCount += 1
        created = followup.created()        
        if created > lastFollowupTime: 
            lastFollowup = followup 
            lastFollowupTime = created
            
    
    threadinfo = {"url":   thread.absolute_url(),
                  "tm_serial" : thread.tm_serial,
                  "heading": thread.title_or_id(),
                  "maintext":thread.getOccurrenceValue(psis.text,ignore=True,default=""),
                  "contenttype": thread.Type(),
                  "createdtime" : thread.modified(),
                  "author" : authorinfo,  
                  "followupcount" : followupCount}

    
    if lastFollowup:
        lastFollowupInfo = {}
        threadinfo['lastfollowup'] = lastFollowupInfo
        lastFollowupInfo['createdtime'] = DateTime(lastFollowup.modified())
        authors = followup.associatedTopicsQuery(  associationtype = psis.authorship
                                                   )
        for author in authors:
            lastFollowupInfo["author"] = { "name" : author.title_or_id(),
                                           "email": author.getOccurrenceValue(psis.email,ignore=True,default=""),
                                           "url"  : author.absolute_url(),
                                         }
            break  # there should be only one author.

        
    
    threads.append(threadinfo)

#TODO: get from object itself    
managers = context.associatedTopicsQuery(associationtype=psis.workareamembership
                                             , sort='title'
                                                     )
content['managers'] = list(managers)

latestchanges = []
append = latestchanges.append
lazy = context.portal_catalog(path='/'.join(context.getPhysicalPath()), types=[psis.file, psis.discussionthread], sort_on='created', sort_order='Reverse')
for brain in lazy[:3]:
    topic = brain.getObject()
    append({'absolute_url':topic.resource_url() or topic.absolute_url()
            #,'type_and_date': topic.Type()+', '+context.ZopeTime(topic.Date()).strftime('%d.%m.%Y %H:%M')            
            ,'type_and_date': topic.Type()+', '+context.ZopeTime(topic.created()).strftime('%d.%m.%Y %H:%M')            
            ,'title_or_id':topic.Title() or topic.resource_object().title_or_id()
            })
            
content['latestchanges'] = latestchanges

files = []
append = files.append
lazy = lazy = context.portal_catalog(path='/'.join(context.getPhysicalPath()), types=[psis.file], sort_on='created', sort_order='Reverse')

for brain in lazy:
    topic = brain.getObject()    
    fileobject = topic.resource_object()
    content_type = fileobject and fileobject.content_type or ""           
    filetype = filetypes.has_key(content_type) and filetypes[content_type] or "fil"                
    file_icon = fileicons[filetype]
    file_type = filenames[filetype]    
    
    if fileobject:
        append({'title_or_id':topic.title_or_id()
        ,'Creator':topic.Creator
        ,'iconclass':file_icon
        ,'modified': context.ZopeTime(topic.created()).strftime('%d.%m.%Y %H:%M')
        ,'tm_serial':topic.tm_serial
        ,'absolute_url':fileobject.absolute_url()
        
    })
    

content['files'] = files

person = context.getAuthenticatedMemberTopic()
email = person.getOccurrenceValue(psis.email)
statusText = u'Du må oppgi en epostadresse i din personlige profil før du kan benytte epostvarsling for diskusjoner'
canSubscribe = False 
if email:
    canSubscribe = True
    statusText = u'Varsle meg på epost ved nye diskusjonsinnlegg'
content['subscriber_status'] = {'statusText':statusText
                               ,'canSubscribe':canSubscribe
                                }
        
change_subscribers = context.associatedTopicsQuery(
                                             associationtype = psis.subscription
                                           , roletype  = psis.subscribed
                                           , otherroletype = psis.workarea_subscriber
                                           , topictype  = psis.person
                                           )
                                
subscriber = False
workarea_subscriber = {}  
statusText = u'Du må oppgi en epostadresse i din personlige profil før du kan benytte varsling for arbeidsrom'
buttonText = u'Aktiver endringsvarsel'
action = "workarea_subscribe_to_change" 
if person in change_subscribers:
    subscriber = True
    buttonText = u'Deaktiver endringsvarsel'
    action = "workarea_unsubscribe_to_change" 
workarea_subscriber['canSubscribe'] = canSubscribe
workarea_subscriber['statusText'] = statusText
workarea_subscriber['subscriber'] = subscriber
workarea_subscriber['buttonText'] = buttonText
workarea_subscriber['action'] = action

content['workarea_subscriber'] = workarea_subscriber
return content
