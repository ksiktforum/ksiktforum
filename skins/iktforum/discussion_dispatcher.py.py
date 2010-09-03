request = context.REQUEST
response = request.RESPONSE

from Products.ksiktforum import psis

topicmap = context.getTopicMap()
atbsi = topicmap.assertTopicBySubjectIdentifier 
dctype = atbsi(psis.discussion_contribution)

topics = list(context.associatedTopicsQuery(  associationtype = psis.discussion
                                           , roletype   = psis.discussion_contribution
                                           , otherroletype = psis.discussionthread
                                           , topictype  = psis.discussionthread
                                        ))
if topics:
    topic = topics[0]
    response.redirect(topic.absolute_url()+'#tm_'+str(context.tm_serial))



return context.discussion_view()
