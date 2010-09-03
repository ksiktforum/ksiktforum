from Products.ksiktforum import psis

def sentencelister(sequence, separator=', ', lastseparator=' og '):
    """ Return a sequence [1,2,3] as '1, 2 and 3'.  """
    sequence = sequence[:]
    if len(sequence)>1:
        last = sequence[-1]
        text = separator.join(sequence[:-1])
        text += lastseparator + last
    elif len(sequence)==1:
        text = sequence[0]
    else:
        text = ''
    return text
    
def topiclink(topic, lower=False):
    """ Return a HTML link to a topic. """
    title = topic.title_or_id()
    if lower:
        title = title.lower()
    return '<a href="%s">%s</a>'%(topic.absolute_url(), title)


#xxx
meta_type =  context.meta_type
if not meta_type in ['Topic', 'WorkArea','DocumentBank']:
    context = context.searchpage


if meta_type in ['Frontpage']:
    return {}
    
#namebinding
topicmap = context.getTopicMap()
atbsi = topicmap.assertTopicBySubjectIdentifier


content = {}

isEditor = False
isContributor = False
member = context.portal_membership.getAuthenticatedMember()
persontopic = context.getAuthenticatedMemberTopic()

if not context.portal_membership.isAnonymousUser() and member:
    rolesInContext = member.getRolesInContext(context)    
    if u'Editor' in rolesInContext or u'Manager' in rolesInContext:
        isEditor = True
    else:
        isContributor = True


content['isEditor'] = isEditor
content['isContributor'] = isContributor
edit_link = None
#you can not edit an article using the wizard unless you are the creator
creator = context.Creator()
if isEditor:
    edit_link = context.absolute_url()+'/content_edit_form'
elif  member.id == creator:    
    edit_link = context.absolute_url()+'/veiviser'
    
content['edit_link'] = edit_link

content['contenttype'] = context.Type()
content['contenttype_lower'] = context.Type().lower()
content['title'] = context.title_or_id()
content['ingress'] = context.getOccurrenceValue(psis.ingress, ignore=True) or context.getOccurrenceValue(psis.question, ignore=True)
content['text'] = context.getOccurrenceValue(psis.text, ignore=True) or context.getOccurrenceValue(psis.answer, ignore=True)

authors = context.associatedTopicsQuery(psis.authored
                                      , psis.authorship
                                      , psis.author
                                      , psis.person)
                                      

content['authors'] = sentencelister([topiclink(author) for author in authors])


content['structureddata'] = context.structureddata()

#modified = context.created()
modified = context.modified()

content['modified'] = modified.strftime("%d.%m.%y %H:%M")

categories = list(context.associatedTopicsQuery(associationtype=psis.categorization, topictype=psis.subject))
#raise SyntaxError, categories
content['categories'] = categories

specializations = list(context.associatedTopicsQuery( roletype=psis.generalization 
                                                     , associationtype=psis.taxonomy
                                                     , otherroletype=psis.specialization   
                                                     , topictype = psis.subject 
                                                     ))
content['specializations'] = specializations


query = {'types':[psis.faq,], 'categories':context.tm_serial}
lazy = context.portal_catalog(**query)
result_length = len(lazy)
faqs = []
append = faqs.append
for brain in lazy[:5]:
    topic = brain.getObject()
    append({'title_or_id':topic.title_or_id()
        , 'absolute_url':topic.absolute_url()
        , 'question':topic.getOccurrenceValue(psis.question)
        })

content['faqs'] = {}
query['types'] = [atbsi(psis.faq).tm_serial]
if faqs:
    content['faqs'] = {'content':faqs
                      ,'more_url':context.portal_searchtool.constructsearchpageurl(**query)
                      ,'result_length':result_length
                      }

contactpersons = []
append = contactpersons.append
atq = context.associatedTopicsQuery( 
                                    associationtype=psis.responsibility
                                   , otherroletype=psis.contactperson   
                                   , topictype = psis.person 
                                   )                                  
      
for topic in atq:
    append({ 'title_or_id':topic.title_or_id()
            ,'absolute_url':topic.absolute_url()
            ,'email':topic.getOccurrenceValue(psis.email)
            ,'phone':topic.getOccurrenceValue(psis.phone) or topic.getOccurrenceValue(psis.mobilephone)
            })
content['contactpersons'] = contactpersons

content['relevant'] = list(context.associatedTopicsQuery( roletype=psis.relevant 
                                                        , associationtype=psis.relevancy
                                                        , otherroletype=psis.relevant   
                                                        , topictype = psis.article
                                                        ))
                                                        
content['relevant'] = content['relevant'] + list(context.associatedTopicsQuery( roletype=psis.relevant 
                                                        , associationtype=psis.relevancy
                                                        , otherroletype=psis.relevant   
                                                        , topictype = psis.handbook
                                                        ))	 
content['relevant'] = content['relevant'] + list(context.associatedTopicsQuery( roletype=psis.relevant 
                                                        , associationtype=psis.relevancy
                                                        , otherroletype=psis.relevant   
                                                        , topictype = psis.section
                                                        ))	
                                                        
content['relevant'] = content['relevant'] + list(context.associatedTopicsQuery( roletype=psis.relevant 
                                                        , associationtype=psis.relevancy
                                                        , otherroletype=psis.relevant   
                                                        , topictype = psis.documentbank
                                                        ))	

            
content['relevant_faq'] = list(context.associatedTopicsQuery( roletype=psis.relevant
                                                        , associationtype=psis.relevancy
                                                        , otherroletype=psis.relevant   
                                                        , topictype = psis.faq
                                                        ))
        
types = context.getTypes()
sis = []
append = sis.append
#typenames = []
#typenameappend = typenames.append
for type in types:
#    typenameappend(type.title_or_id())
    subjectids = type.getSubjectIdentifiers()
    for id in subjectids:
        append(id)


query = {'types':sis
        ,'categories':[category.tm_serial for category in content['categories']]
        ,'sort_on':'Date'        
        ,'sort_order':'reverse'
        }    
lazy = context.portal_catalog(**query)#[:5]
length = len(lazy)
lazy = lazy[:5]
samecategorization = []
append = samecategorization.append
for brain in lazy:    
    title = brain.Title
    if len(title) > 50:
        title = title[:50]+u' ...'
    append({ 'title_or_id': title
            ,'absolute_url': brain.getURL()
            ,'type_and_date': brain.Type+', '+context.ZopeTime(brain.Date).strftime('%d.%m.%Y')     
            })

query['types'] = [atbsi(si).tm_serial for si in query['types']]
query['categories'] = [category.tm_serial for category in content['categories']]
if samecategorization:    
    content['samecategorization'] = {'content':samecategorization
                                    ,'more_url':context.portal_searchtool.constructsearchpageurl(**query)
                                    ,'result_length':length
                                    }
else:
    content['samecategorization'] = samecategorization
    

            
lazy = context.portal_catalog(categories='toplevel', types=psis.subject, sort_by='Title')
mainsubjects = []
append = mainsubjects.append
for brain in lazy:
    append({'title_or_id':brain.Title, 'absolute_url':brain.getURL()})   

leftcolumn_link_list = context.index_html.portal_lists.aquirelist(6147)
links = []
append = links.append
for link in leftcolumn_link_list:
    topic = link['topic']
    append({'title_or_id':topic.title_or_id()
          ,'absolute_url':topic.getOccurrenceValue(psis.link, ignore=True) or topic.absolute_url()    
          })
          
if isEditor:
    append({'title_or_id':u'[Rediger listen]'
          ,'absolute_url':leftcolumn_link_list.edit_url()    
          })         

content['leftcolumn_link_list'] = links

leftcolumn_top_list = context.index_html.portal_lists.aquirelist(6153)
links = []
append = links.append

for link in leftcolumn_top_list:
    topic = link['topic']
    append({'title_or_id':topic.title_or_id()
          ,'absolute_url':topic.getOccurrenceValue(psis.link, ignore=True) or topic.absolute_url()    
          })
if isEditor:
    append({'title_or_id':u'[Rediger listen]'
          ,'absolute_url':leftcolumn_top_list.edit_url()    
          })
          
content['leftcolumn_top_list'] = links

header_link_list = context.index_html.portal_lists.aquirelist(6169)
links = []
append = links.append
for link in header_link_list:
    topic = link['topic']
    append({'title_or_id':topic.title_or_id()
          ,'absolute_url':topic.getOccurrenceValue(psis.link, ignore=True) or topic.absolute_url()    
          })
if isEditor:
    append({'title_or_id':u'[Rediger listen]'
          ,'absolute_url':header_link_list.edit_url()    
          })

loggedInInfo = {}
if isEditor or isContributor:
    loggedInInfo['title_or_id'] = persontopic.title_or_id()
    loggedInInfo['workspace_url'] = persontopic.absolute_url()+'/workspace_view'
    
content['loggedInInfo'] = loggedInInfo   

#Articles in a handbook
articles = []
append = articles.append
art_topics = context.associatedTopicsQuery( roletype=psis.handbook 
                                   , associationtype=psis.has_chapter
                                   , otherroletype=psis.chapter                                      
                                   , sort='internalorder'
                                   )

for topic in art_topics:
#   roles_topic= topic.listRoles(type=psis.article)
#   for role_topic in roles_topic:
#      assoc = role_topic.getAssociation()                     
#      tm_otherrole = assoc.getOtherRole(role_topic)
#      if tm_otherrole.getPlayer().tm_serial == context.tm_serial:
#          roleserial = int(assoc.tm_serial)
#          otherroleserial = int(tm_otherrole.tm_serial)

   append({ 'title_or_id':topic.title_or_id()
            ,'absolute_url':topic.absolute_url()
	    ,'tm_serial':topic.tm_serial
	    #,'role_serial':roleserial
	    #,'otherrole_serial':otherroleserial
            })

#Handbook associated with articles
handbooks = []
handbook_topics = context.associatedTopicsQuery( roletype=psis.chapter 
                                   , associationtype=psis.has_chapter
                                   , otherroletype=psis.handbook   
                                   , topictype = psis.handbook 
                                   )
#get articles in handbooks
for handbook in handbook_topics:
    handbooks.append({ 'title_or_id':handbook.title_or_id()
            ,'absolute_url':handbook.absolute_url()
            })
    art_topics = handbook.associatedTopicsQuery( roletype=psis.handbook 
                                   , associationtype=psis.has_chapter
                                   , otherroletype=psis.chapter                                      
                                   , sort='internalorder'
                                   )
    for topic in art_topics:
        append({ 'title_or_id':topic.title_or_id()
            ,'absolute_url':topic.absolute_url()
												,'tm_serial':topic.tm_serial
            })																																			
content['articles'] = articles
content['handbooks'] = handbooks

          
content['header_link_list'] = links
content['mainsubjects'] = mainsubjects 
content['categorysentence'] = sentencelister([topiclink(category, lower=True) for category in content['categories']])
content['categorysentence_nolinks'] = sentencelister([category.title_or_id().lower() for category in content['categories']])
content['attachments'] = context.attachments()
content['display'] = content['relevant_faq'] or content['categories'] or content['relevant'] or content['specializations'] or content['attachments'] or content['contactpersons']
content['image'] = context.imageData(psis.subjectimage) or context.imageData(psis.caseimage) or context.imageData(psis.portraitimage)
content['comments_allowed'] = context.getOccurrenceValue(type=psis.comments_allowed, ignore=True)
return content
