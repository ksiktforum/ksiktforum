# -*- coding: utf-8 -*-

from DateTime import DateTime
from Products.ksiktforum import psis

errors = []
messages = []
status = {'errors': errors, 'messages':messages}

discussionform = context.REQUEST.get("createfollowup",{})
maintext= discussionform.get("maintext","")
member   = context.getAuthenticatedMemberTopic()


if not member:
    errors.append(u'Du må være logget inn på portalen for å opprette en diskusjonstråd')

if not maintext:
    errors.append(u'Du må skrive inn teksten for innlegget ditt')


currentvalues = {}
if errors:
    ## Send back the form-field values, so that the pagetemplate can redisplay any existing data
    currentvalues = { 'createfollowup' : {
                         'maintext' : maintext
                    }}
else:
    ## All is well, so create a new discussion-thread followup
    
    ## we create the id of the followup by adding a number to the id of the discussionthread.
    followups = context.associatedTopicsQuery(  associationtype = psis.discussionfollowup, sort='date' )
    followupCount = 0
    lastFollowupText = ""
    for followup in followups:
        followupCount += 1
        lastFollowupText = followup.getOccurrenceValue(psis.text,ignore=True,default="")
        
    if maintext == lastFollowupText:
        errors.append(u"Teksten du skrev er identisk til det siste innlegget (Trykket du reload i nettleseren din etter å ha opprettet et innlegg?)")
        
    if not errors:
        followupid = "%s_%d" % (context.id, followupCount+1)
    
        #create the followup topic
        creationpath = context # we store the followups as children of the discussionthread itself.
        creationpath.invokeFactory(type_name="discussionthreadfollowup", id=followupid)
        followup = creationpath[followupid]
        followup.setOccurrence(maintext,psis.text)
        followup.setTitleAndName("%s - svar %d" % (context.title_or_id(),followupCount+1))
        
        ## create "discussionfollowup" association between the discussionthread and the context
        context.makeBinaryAssociation(
                                   followup #othertopic
                                 , psis.discussionfollowup #assoctype
                                 , psis.discussionthread # roletype: 
                                 , psis.discussionthreadfollowup # otherroletype
                                 )
        
        ## create "authorship" association between the followup and the user.
        followup.makeBinaryAssociation(
                                   member #othertopic
                                 , psis.authorship #assoctype
                                 , psis.discussionthreadfollowup #roletype
                                 , psis.author # otherroletype
                                 )
        
       
        messages.append(u'Et nytt innlegg har blitt opprettet, og vises nederst på listen over innlegg.')
    
return context.discussionthread_view(status=status, **currentvalues) # TODO: How to call the default view-function here?