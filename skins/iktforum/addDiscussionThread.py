# -*- coding: utf-8 -*-

from DateTime import DateTime
from Products.ksiktforum import psis

topicmap = context.getTopicMap()
atbsi = topicmap.assertTopicBySubjectIdentifier
gtbs = topicmap.getTopicBySubjectIdentifier 
workareatopic = context.workareatopic()
request = context.REQUEST
response = request.RESPONSE

errors = []
messages = []
status = {'errors': errors, 'messages':messages}

discussionform = context.REQUEST.get("createthread",{})
heading = discussionform.get("heading","")
maintext= discussionform.get("maintext","")
member   = context.getAuthenticatedMemberTopic()

if not member:
    errors.append(u'Du må være logget inn på portalen for å opprette en diskusjonstråd')

if not heading:
    errors.append(u'Du må skrive inn en overskrift for diskusjonstråden')

if not maintext:
    errors.append(u'Du må skrive inn teksten for diskusjonstråden')

#TODO: check if path exists. Maybe put in in calculatecreationpath
creationpath = getattr(context, 'innlegg', context.diskusjoner)

## we want to base the id partially on the user-specified heading, so we must first remove illegal characters.
safeheading = heading.lower()
safeheading = safeheading.replace(u'ø',u'o') # first replace norwegian characters
safeheading = safeheading.replace(u'æ',u'ae')
safeheading = safeheading.replace(u'å',u'aa')
ascii_alphanums = string.ascii_letters + string.digits
safeheading = "".join([x for x in safeheading if x in ascii_alphanums ]) # remove any remaing non-ascii letters

discussionthreadid = "%s_%s" % (safeheading, DateTime().strftime("%d%m%Y%H%M")) #DateTime().strftime("%d.%m.%Y_%H.%M.S."))

if hasattr(creationpath,discussionthreadid):
    errors.append(u'Du har allerede laget en diskusjonstråd med denne overskriften. Prøv å endre overskriften til noe annet.')

#xxx
types = context.getTypes()   
roletype = psis.workarea    
discussionthreadtype = atbsi(psis.discussionthread)  
viewtemplate = context.workarea_view
if discussionthreadtype in types:
    roletype = psis.discussionthread
    viewtemplate = context.discussion_view
    
currentvalues = {}
if errors:
    ## Send back the form-field values, so that the pagetemplate can redisplay any existing data
    currentvalues = { 'createthread' : {
                                        'heading' : heading,
                                        'maintext' : maintext
                    }}
    return viewtemplate(status=status, **currentvalues)
else:
    ## All is well, so create a new discussion-thread       
    
    
    
    #create the discussionthread topic
    creationpath.invokeFactory(type_name="discussionthread", id=discussionthreadid)
    newthread = creationpath[discussionthreadid]
    newthread.setTitleAndName(heading) 
    newthread.setOccurrence(maintext,psis.text)
    
    otherroletype = psis.discussionthread
    if discussionthreadtype in types:
        otherroletype = psis.discussion_contribution
    
    ## create "discussion" association between the discussionthread and the context
    context.makeBinaryAssociation(
                               newthread #othertopic
                             , psis.discussion #assoctype
                             , roletype # roletype: TODO: should we call this something else? maybe discussionSubject?
                             , otherroletype # otherroletype
                             )
    
    ## create "authorship" association between the discussionthread and the user.
    newthread.makeBinaryAssociation(
                               member #othertopic
                             , psis.authorship #assoctype
                             , psis.discussionthread #roletype
                             , psis.author # otherroletype
                             )
                             
    subscribe = request.get("subscribe", False)
    if subscribe:
        ## The users wishes to be warned by email every time an entry is added to the discussion.
        newthread.makeBinaryAssociation(
                               member #othertopic
                             , psis.subscription #assoctype
                             , psis.subscribed #roletype
                             , psis.discussion_subscriber # otherroletype
                             )
                             
    #only send out notifications to subscribers when discussions are added to the main thread
    if discussionthreadtype in types:
        subscribers = context.associatedTopicsQuery( associationtype = psis.subscription
                                                   , roletype   = psis.subscribed
                                                   , otherroletype = psis.discussion_subscriber
                                                   , topictype  = psis.person
                                                   )
        fromemail = u''
        subject = u'%(title)s har fått et nytt innlegg' % {'title':context.title_or_id()}
        message = u"""Skrevet av %(membername)s <%(memberurl)s>
        

%(heading)s
%(maintext)s

Hele diskusjonen finner du her <%(discussion_url)s#tm_%(tm_serial)s>
""" % {'title':context.title_or_id()
      ,'membername':member.title_or_id()
      ,'heading':heading
      ,'maintext':maintext
      ,'discussion_url':context.absolute_url()
      ,'memberurl':member.absolute_url()
      ,'tm_serial':newthread.tm_serial
      }
        for subscriber in subscribers:
            toemail = subscriber.getOccurrenceValue(psis.email)
            if toemail:
                context.portal_topicmanagement.sendUnicodeMail(subject
                                                             , u'\n\n'+message 
                                                             ,(toemail,)
                                                             , context.portal.email_from_address #sender
                                                       )
                
    else:
        #toplevel discussionthread started. Alert all members of the workarea        
        message = u"Diskusjonstråden '%s' <%s> har blitt startet i arbeidsrommet %s <%s> av %s <%s>" % (heading, newthread.absolute_url(), workareatopic.title_or_id(), workareatopic.absolute_url(), member.title_or_id(), member.absolute_url())
        context.workarea_alert_change(message)                      
        
    response.redirect(context.absolute_url()+'/'+viewtemplate.id+'?status.messages:ustring:utf8:list:record='+'Et ny diskusjonstråd har blitt opprettet, og vises nederst på listen over tråder.')


