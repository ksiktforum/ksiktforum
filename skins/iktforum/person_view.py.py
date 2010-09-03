from Products.ksiktforum import psis

request = context.REQUEST
response = request.RESPONSE

if request.REQUEST_METHOD.lower() == 'post': 
    pass
                
else:
    content = {}
    #method = getattr(context, 'content_view.py')
    #content = method()
    
    #artikler
    associatedArticles = context.associatedTopicsQuery(associationtype=psis.authorship,roletype=psis.author, sort="date",reverse=True )
    
    articles = []
    append = articles.append
    for article in associatedArticles:
        append({ 'title_or_id' : article.title_or_id()
               , 'absolute_url' : article.absolute_url()    
               , 'date' : context.ZopeTime(article.Date()).strftime("%d.%m.%Y")
               })
    if articles:
        content['articles'] = { 'heading' : 'Artikler skrevet av %s'%(context.title_or_id())
                              , 'articles' : articles
                              }
              
 
    subjects = []
    
    append = subjects.append
    atq = context.associatedTopicsQuery( roletype=psis.contactperson 
                                   , associationtype=psis.responsibility
                                   , otherroletype=psis.subject   
                                   , topictype = psis.subject 
                                   )
    for topic in atq:
        append({ 'title_or_id':topic.title_or_id()
                ,'absolute_url':topic.absolute_url()           
                })            
    
    content['contact_for'] = subjects
        
    
    return content

