# -*- coding: utf-8 -*-
from Products.ksiktforum import psis

content = {}
occurrenceMapping = {    'work': psis.work        
                       , 'department':psis.department
                       , 'workplace':psis.workplace
                       , 'visitaddress':psis.visitaddress
                       , 'phone':psis.phone
                       , 'mobilephone':psis.mobilephone
                       , 'email':psis.email
                       , 'workareas':psis.workareas
                       , 'qualifications':psis.qualifications            
                   }

topicmap = context.getTopicMap()
gtbs = topicmap.getTopicBySerial
            
persontopic = context.getAuthenticatedMemberTopic()

if not persontopic:
    return None

profile = {}
for key, psi in occurrenceMapping.items():
    profile[key] = persontopic.getOccurrenceValue(psi, ignore=True)
profile['title'] = persontopic.title_or_id()
content['profile'] = profile


## Get a list of all the content this user has created
works = []
#for work in context.associatedTopicsQuery(associationtype=psis.authorship,
#                                                     roletype=psis.author
#                                                     ):
member = context.portal_membership.getAuthenticatedMember()
lazymap = context.portal_catalog(types=[psis.activity,psis.article], Creator=member.getUserName(), sort_on="Date", sort_order="reverse")
for brain in lazymap:
    try:
        work = brain.getObject()
        works.append({"url":   work.absolute_url(),
                          "title": work.title_or_id(),
                          "contenttype": work.Type(),
                          "modifiedtime" : work.modified(),
                          "tm_serial" : work.tm_serial,
                          "review_state"    : context.portal_workflow.getInfoFor(work, "review_state"),
                          
                          })
    except:
        pass
content['works'] = works

mydrafts = context.portal_wizard.getPersonalDrafts()
drafts = []
append = drafts.append

for draft in mydrafts:
    draftattributes = draft()
    title = draftattributes.get('title', draftattributes.get('serial'))
    topictypeserial = draftattributes.get('topictype', None)
    serial = draftattributes.get('serial','')
    edit_url = ''
    if topictypeserial:
        topic = gtbs(topictypeserial)
        edit_url = topic.absolute_url()+"/veiviser?state.serial:int:record="+str(serial)
        
    append({'title':draftattributes.get('title', title)
           ,'serial':serial
           ,'edit_url':edit_url
    })
content['drafts'] = drafts

workareas = []
append = workareas.append
lazy = context.portal_catalog(portal_type=['workarea'], sort_by="Title")
#temp fix. somehow the Title-property of the brain is empty
for brain in lazy:
    append(brain.getObject())
content['workareas'] = workareas
    

return content





