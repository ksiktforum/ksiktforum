# -*- coding: utf-8 -*-

topicmap = context.getTopicMap()
contentlist = context.REQUEST.get('selectedDiscussionThreadFollowups',[])

user = context.portal_membership.getAuthenticatedMember()
requiredRole = "Manager" # TODO: update the way we do the permission-checks, once Svein Arild is sure how to
                         #       set up the security-system and do the checks.                         
if not requiredRole in user.getRoles():
    return u"""Du har ikke rettigheter til å gjøre dette! Du har bare rollene %s, men du må ha rollen "%s".""" % (user.getRoles(),requiredRole)


count = 0
for tm_serial in contentlist:
    try:
        topic = topicmap.getTopicBySerial(tm_serial)
    except:
        topic = None
    if topic:
        container = topic.aq_parent
        container.manage_delObjects([topic.id,])   
        count += 1
    
if count > 0:
    return context.discussion_view(status={'messages':[u'De valgte elementene er nå slettet']})
else:
    return context.discussion_view(status={'errors':[u'Ingen elementer var valgt.']})

    