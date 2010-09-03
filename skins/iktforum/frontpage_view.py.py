import DateTime
from Products.ksiktforum import psis

content = {}

topicmap = context.getTopicMap()
atbsi = topicmap.assertTopicBySubjectIdentifier

isEditor = False
isContributor = False
member = context.portal_membership.getAuthenticatedMember()
if member:
    rolesInContext = member.getRolesInContext(context)    
    if u'Editor' in rolesInContext or u'Manager' in rolesInContext:
        isEditor = True
    else:
        isContributor = True

content['isEditor'] = isEditor
content['isContributor'] = isContributor

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


lazy = context.portal_catalog(categories='toplevel', types=psis.subject)
mainsubjects = []
append = mainsubjects.append
for brain in lazy:
    append({'title_or_id':brain.Title, 'absolute_url':brain.getURL()})
content['mainsubjects'] = mainsubjects                     


## First, get the full set of activities. This is required to get a correct value
## for the "result_length" variable. This is used in the "More activities"-link, to
## tell the user the total number of activities.
##lazy = context.portal_catalog(types=[psis.activity, psis.seminar])
##result_length = len(lazy)
## Then get a list of the activities and seminars that are starting today or later. This
## is the list that will be displayed to the user on the frontpage.
last_midnight = DateTime.DateTime().earliestTime() - 1
lazy = context.portal_catalog(types=[psis.activity, psis.seminar], 
                                      occurrence_startdate=(last_midnight, ),
                                      occurrence_startdate_usage='range:min',                                    
                                      sort_on='occurrence_startdate',
                                      sort_order='Ascending')



#context.portal_catalog(types=[psis.activity, psis.seminar], 
#                                      occurrence_enddate=(last_midnight, ),
#                                      occurrence_enddate_usage='range:min',                                    
#                                      sort_on='occurrence_enddate',
#                                      sort_order='Ascending')

total_upcoming = len(lazy) -3
if total_upcoming < 0:
    total_upcoming = 0

lazy = lazy[:3] # only display a few of the activities. The user can click on the "More activities" link to get the full list.
activities = []
append = activities.append
for brain in lazy:
    topic = brain.getObject()
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
           ,'arrangor':topic.getOccurrenceValue(psis.arrangor)											
           ,'datestring': datestring    
    })
#more_activities_url = context.portal_searchtool.constructsearchpageurl(**{'types':[atbsi(psis.activity).tm_serial, atbsi(psis.seminar).tm_serial], 'sort_on':'Date', 'sort_order':'reverse'})
more_activities_url = context.portal.absolute_url() + "/seksjoner/kalender"
content['activities'] = {'content': activities
                         ,'more_url':more_activities_url
                         ,'result_length':total_upcoming
                        }

campaigns = list(context.associatedTopicsQuery( roletype=psis.frontpage 
                                   , associationtype=psis.campaign
                                   , otherroletype=psis.article   
                                   , topictype = psis.article 
                                   ))

campaignMapping = {}
if campaigns:
    #we only consider one campaign
    campaign = campaigns[0]
    campaignimage = campaign.imageData(psis.campaignimage)
    campaignMapping['absolute_url'] = campaign.absolute_url()
    campaignMapping['imagedata'] = campaignimage 
    
content['campaign'] = campaignMapping    

latest_global_content_dl = context.portal_lists.aquirelist(psis.latest_global_content)
latest_global_content = list(latest_global_content_dl)
result_length = len(latest_global_content)

latest_content = []
append = latest_content.append
for global_content in latest_global_content:
    topic = global_content['topic']
    title = topic.title_or_id()
    if len(title) > 50:
        title = title[:50]+u' ...'
    append({'absolute_url':topic.absolute_url()
            ,'imagedata': topic.imageData()
            ,'ingress':topic.getOccurrenceValue(psis.ingress, ignore=True)
            ,'type_and_date': topic.Type()+', '+context.ZopeTime(topic.created()).strftime('%d.%m.%Y')            
            ,'title_or_id':title
            
    })
if isEditor:
    append({'title_or_id':u'[Rediger listen]'
          ,'absolute_url':latest_global_content_dl.edit_url()    
          ,'imagedata':None
          ,'ingress':''
          ,'type_and_date':''
          
          })          
more_content_url = context.portal_searchtool.constructsearchpageurl(**{'types':[atbsi(psis.article).tm_serial], 'sortindex':'date', 'sort_order':'reverse'})
 

content['priority_content'] = latest_content[:3]
content['latest_content'] = { 'content':latest_content[3:]
                             ,'more_url':more_content_url
                             ,'result_length':result_length

                             }




return content
