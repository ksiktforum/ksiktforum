# -*- coding: utf-8 -*-

from Products.ksiktforum import psis



topicmap = context.getTopicMap()
atbsi = topicmap.assertTopicBySubjectIdentifier
#xxx
types = context.getTypes()   

roletype = psis.workarea    
discussionthreadtype = atbsi(psis.discussionthread)  
viewtemplate = context.workarea_view
if discussionthreadtype in types:
    roletype = psis.discussionthread
    viewtemplate = context.discussion_view


contentlist = context.REQUEST.get('selectedDiscussionThreads',[])

user = context.portal_membership.getAuthenticatedMember()
requiredRole = "Manager" # TODO: update the way we do the permission-checks, once Svein Arild is sure how to
                         #       set up the security-system and do the checks.                         
if not requiredRole in user.getRoles():
    return u"""Du har ikke rettigheter til å gjøre dette! Du har bare rollene %s, men du må ha rollen "%s".""" % (user.getRoles(),requiredRole)


count = 0
for tm_serial in contentlist:
    try:
        thread = topicmap.getTopicBySerial(tm_serial)
    except:
        thread = None
    if thread:
        count += 1
        
        #raise SyntaxError, list(thread.associatedTopicsQuery(associationtype=psis.discussion, sort='date', otherroletype=psis.discussion_contribution))
        ## delete all discussionthread followups
        for followup in thread.associatedTopicsQuery(associationtype=psis.discussion, sort='date', otherroletype=psis.discussion_contribution ):
            container = followup.aq_parent
            container.manage_delObjects([followup.id,])

        ## delete the discussion-thread itself.
        container = thread.aq_parent
        container.manage_delObjects([thread.id,])   
    
if count > 0:
    return viewtemplate(status={'messages':[u'De valgte elementene er nå slettet']})
else:
    return viewtemplate(status={'errors':[u'Ingen elementer var valgt.']})

    