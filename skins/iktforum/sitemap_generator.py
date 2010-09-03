## Script (Python) "site_map_generator"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##
from Products.ksiktforum import psis

topicmap = context.getTopicMap()

atbsi = topicmap.assertTopicBySubjectIdentifier

def cleanTitle(text):
    if len(text)>20 and not ' ' in text:
        text = text.replace('/', '/ ')
    return text

topics = []

mainsubjects = context.portal_catalog(categories='toplevel', types=psis.subject)

gtbs = topicmap.getTopicBySerial

for brain in mainsubjects:
    topic = brain.getObject()
    children = topic.associatedTopicsQuery( roletype=psis.generalization 
                                            , associationtype=psis.taxonomy
                                            , otherroletype=psis.specialization   
                                            , topictype = psis.subject 
                                          )
    children = [(subtopic.title_or_id(), subtopic) for subtopic in children]
    children.sort()
    subjects = [{ 'title': cleanTitle(title)
                , 'url': subtopic.absolute_url()
                } for title, subtopic in children]
    topics.append(( len(children)
                  , { 'title': topic.title_or_id()
                    , 'url': topic.absolute_url()
                    , 'subjects': subjects
                    }))

topics.sort()
topics.reverse()
topics = [item for length, item in topics]
#batches = []
#while topics:
#    batches.append(topics[:4])
#    topics = topics[4:]

return topics
