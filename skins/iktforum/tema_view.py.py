from Products.ksiktforum import psis

import DateTime

calendarMapping = {  '01':u'januar'
                    ,'02':u'februar'
                    ,'03':u'mars'
                    ,'04':u'april'
                    ,'05':u'mai'
                    ,'06':u'juni'
                    ,'07':u'juli'
                    ,'08':u'august'
                    ,'09':u'september'
                    ,'10':u'oktober'
                    ,'11':u'november'
                    ,'12':u'desember'                    
                    }

isEditor = False
isContributor = False
member = context.portal_membership.getAuthenticatedMember()
if member:
    rolesInContext = member.getRolesInContext(context)    
    if u'Editor' in rolesInContext or u'Manager' in rolesInContext:
        isEditor = True
    else:
        isContributor = True

content = {}

latest_categorized_content_dl = context.portal_lists.aquirelist(psis.latest_categorized_content)
latest_categorized_content = list(latest_categorized_content_dl)

result_length = len(latest_categorized_content)
latest_categorized_content = latest_categorized_content[:5]

latest_categorized = []
append = latest_categorized.append
for categorized_content in latest_categorized_content:
    topic = categorized_content['topic']        
    append({'absolute_url':topic.absolute_url()
            ,'imagedata': topic.imageData()
            ,'ingress':topic.getOccurrenceValue(psis.ingress, ignore=True)
            ,'type_and_date': topic.Type()+', '+context.ZopeTime(topic.Date()).strftime('%d.%m.%Y')            
            ,'title_or_id':topic.title_or_id()
    })
    
if isEditor:
    append({'title_or_id':u'[Rediger listen]'
          ,'absolute_url':latest_categorized_content_dl.edit_url()    
          ,'imagedata':None
          ,'ingress':''
          ,'type_and_date':''
          
          })


content['priority_content'] = latest_categorized[:3]
content['latest_content'] = {'content':latest_categorized[3:]
                             ,'more_url':context.portal_searchtool.constructsearchpageurl(**{'categories':[context.tm_serial,], 'sortindex':'date','sort_order':'reverse'})
                             ,'result_length':result_length
                            }

activities = []
append = activities.append
#topics = context.associatedTopicsQuery( roletype=psis.category 
#                                   , associationtype=psis.categorization
#                                   , otherroletype=psis.categorized 
#                                   , topictype = psis.activity)
last_midnight = DateTime.DateTime().earliestTime()
brains = context.portal_catalog( types=[psis.activity, psis.seminar]
                               , occurrence_startdate=(last_midnight, )
                               , occurrence_startdate_usage='range:min'  
                               , sort_on='occurrence_startdate'
                               , sort_order='Ascending'
                               , categories=[context.tm_serial,])
                               
topics = [brain.getObject() for brain in brains]

for topic in topics:
    startdate = context.ZopeTime(topic.getOccurrenceValue(psis.startdate))
    enddate = context.ZopeTime(topic.getOccurrenceValue(psis.enddate))   
    
    startday = startdate.strftime('%d')
    endday = enddate.strftime('%d')
    
    startmonth = startdate.strftime('%m')
    endmonth = startdate.strftime('%m')
    
    startyear = startdate.strftime('%Y')
    endyear = enddate.strftime('%Y')
    
    datestring = u''    
    
    if startyear == endyear:
        if startmonth == endmonth:
            if startday == endday:
                datestring = u'%s. %s %s'%(startday, calendarMapping[startmonth], startyear)
            else:
                datestring = u'%s. - %s. %s %s'%(startday, endday, calendarMapping[startmonth] , startyear)
        else:     
            datestring = u'%s. %s - %s. %s %s'%(startday, calendarMapping[startmonth], endday, calendarMapping[endmonth] , startyear)
    else:
        datestring = u'%s. %s %s - %s. %s %s'%(startday, calendarMapping[startmonth], startyear, endday, calendarMapping[endmonth] , endyear)        
    
    append({'title_or_id':topic.title_or_id()
           ,'absolute_url': topic.absolute_url()
           ,'location':topic.getOccurrenceValue(psis.location)
           ,'datestring': datestring    
    })
content['activities'] = activities

handbooks = []
append = handbooks.append
topics = context.associatedTopicsQuery( roletype=psis.category 
                                   , associationtype=psis.categorization
                                   , otherroletype=psis.categorized 
                                   , topictype = psis.handbook)
for topic in topics:
    append({ 'title_or_id':topic.title_or_id()
            ,'absolute_url':topic.absolute_url()
            })
content['handbooks'] = handbooks
content['display'] = content['handbooks'] or content['activities']
return content