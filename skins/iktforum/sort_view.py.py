from Products.ksiktforum import psis

content =  {}

#Articles in a handbook
articles = []
append = articles.append
art_topics = context.associatedTopicsQuery( roletype=psis.handbook 
                                   , associationtype=psis.has_chapter
                                   , otherroletype=psis.chapter   
                                   , topictype = psis.article 
                                   , sort='internalorder'
                                   )

for topic in art_topics:
   roles_topic= topic.listRoles(type=psis.chapter)
   for role_topic in roles_topic:
      assoc = role_topic.getAssociation()                     
      tm_otherrole = assoc.getOtherRole(role_topic)
      if tm_otherrole.getPlayer().tm_serial == context.tm_serial:
          roleserial = int(assoc.tm_serial)
          otherroleserial = int(tm_otherrole.tm_serial)
          append({ 'title_or_id':topic.title_or_id()
            ,'absolute_url':topic.absolute_url()
	    ,'tm_serial':topic.tm_serial
	    ,'role_serial':roleserial
	    ,'otherrole_serial':otherroleserial
            })

content['articles'] = articles
return content