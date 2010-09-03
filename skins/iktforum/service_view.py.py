from Products.ksiktforum import psis

topicmap = context.getTopicMap()
atbsi = topicmap.assertTopicBySubjectIdentifier

content = {}
request = context.REQUEST

tb = None
try:
    tb = request.tb
except:
    pass

akse1 = None
categorization = None
othercategorization = None
if tb:
    #Gets all tjenestebehandlinger from portal_catalog
    akse1 = context.portal_catalog(types=[psis.servicetreatement])
    categorization = psis.servicetreatementcategorization
    othercategorization = psis.servicecategorization 
else:
    #Gets all services from portal_catalog
    akse1 = context.portal_catalog(types=[psis.service])
    categorization = psis.servicecategorization  
    othercategorization = psis.servicetreatementcategorization       
   
if akse1:	 
    for serviceitem in akse1:
        topic = serviceitem.getObject()
        title = topic.title_or_id()
        content [title] = []
        topics = topic.associatedTopicsQuery(  associationtype = categorization
                                           , roletype   = psis.category
                                           , otherroletype = psis.categorized
                                           )
        
        for article in topics:
            akse2_topics = article.associatedTopicsQuery( associationtype= othercategorization
                                      , roletype= psis.categorized
                                      , otherroletype= psis.category 
                                      )
            for akse2_topic in akse2_topics:
                new_entry = {'title': akse2_topic.title_or_id(), 'url': article.absolute_url()}
                content[title].append(new_entry)
return content