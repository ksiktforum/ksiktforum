# -*- coding: utf-8 -*-

from DateTime import DateTime
from Products.ksiktforum import psis

content = {}
threads = []
content['threads']=threads
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


    followups = thread.associatedTopicsQuery(  associationtype = psis.discussionfollowup, sort='date' )
    followupCount = 0
    lastFollowupTime = DateTime(0)
    lastFollowup = None
    for followup in followups:
        followupCount += 1
        created = followup.created()
        if created > lastFollowupTime: 
            lastFollowup = followup           
            
    
    threadinfo = {"url":   thread.absolute_url(),
                  "tm_serial" : thread.tm_serial,
                  "heading": thread.title_or_id(),
                  "maintext":thread.getOccurrenceValue(psis.text,ignore=True,default=""),
                  "contenttype": thread.Type(),
                  "createdtime" : thread.created(),
                  "author" : authorinfo,  
                  "followupcount" : followupCount}

    
    if lastFollowup:
        lastFollowupInfo = {}
        threadinfo['lastfollowup'] = lastFollowupInfo
        lastFollowupInfo['createdtime'] = lastFollowup.created()
        authors = followup.associatedTopicsQuery(  associationtype = psis.authorship
                                                   )
        for author in authors:
            lastFollowupInfo["author"] = { "name" : author.title_or_id(),
                                           "email": author.getOccurrenceValue(psis.email,ignore=True,default=""),
                                           "url"  : author.absolute_url(),
                                         }
            break  # there should be only one author.

        
    
    threads.append(threadinfo)
    
return content