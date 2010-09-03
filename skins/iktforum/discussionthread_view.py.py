# -*- coding: utf-8 -*-

from DateTime import DateTime
from Products.ksiktforum import psis

"""TODO: 
 get the author, createddate, heading, bodytext of the discussionthread itself
 get the author, createddate and bodytext of all the followups of this thread (sorted by time)
 
 Have a look at ho discussions_view.py.py does it. This will be very similar.
"""

content = {'maintext' : context.getOccurrenceValue(psis.text,ignore=True,default=""),
           'heading'  : context.title_or_id(),
           }


## Get the information about the discussion-thread itself.
authors = context.associatedTopicsQuery(  associationtype = psis.authorship
                                       , roletype   = psis.discussionthread
                                       , otherroletype = psis.author
                                       , topictype  = psis.person
                                       )
authorinfo = {}
for author in authors:
    content['author'] = { "name" : author.title_or_id(),
                          "email": author.getOccurrenceValue(psis.email,ignore=True,default=""),
                          "url"  : author.absolute_url(),
                          }
    break  # there should be only one author.

    

## Get the information about the followups (if any) to this discussion-thread
followups = []
content['followups'] = followups

member = context.portal_membership.getAuthenticatedMember()
roles = member.getRolesInContext(context)

for followup in context.associatedTopicsQuery(associationtype=psis.discussion, topictype=psis.discussionthread, sort='date' ):
    creator = followup.Creator()
    can_edit = False
    if creator == member.id or 'Manager' in roles:
        can_edit = True

    followupinfo = {"url":   followup.absolute_url()
                    ,"tm_serial" : followup.tm_serial
                      ,"heading": followup.title_or_id()
                      ,"maintext":followup.getOccurrenceValue(psis.text,ignore=True,default="")
                      ,"createdtime" : followup.created().strftime("%d.%m.%y %H:%M")
                      ,"title_or_id":followup.title_or_id()
                      ,"can_edit":can_edit
                      }
    followups.append(followupinfo)
    
    authors = followup.associatedTopicsQuery(  associationtype = psis.authorship
                                           , roletype   = psis.discussionthread
                                           , otherroletype = psis.author
                                           , topictype  = psis.person
                                           )

    for author in authors:
        followupinfo['author'] = {  "name" : author.title_or_id(),
                                    "email": author.getOccurrenceValue(psis.email,ignore=True,default=""),
                                    "url"  : author.absolute_url(),
                                 }
        break  # there should be only one author.
    
content['workarea'] = context.workareatopic()

persontopic = context.getAuthenticatedMemberTopic()
subscribers = context.associatedTopicsQuery( associationtype = psis.subscription
                                           , roletype   = psis.subscribed
                                           , otherroletype = psis.discussion_subscriber
                                           , topictype  = psis.person
                                           )
canSubscribe = False                                           
isSubscriber = False
statusText = u'Du har ikke slått på epostvarsling på denne diskusjonen'
subscriptionActionText = u'Slå på epostvarsling'
subscriptionAction = context.absolute_url()+'/discussion_subscribe'

email = persontopic.getOccurrenceValue(psis.email)
if email:
    canSubscribe = True    
else:
    statusText = u'Du må oppgi en epostadresse i din personlige profil før du kan benytte epostvarsling for diskusjoner'

if canSubscribe:
    if persontopic in subscribers:
        isSubscriber = True
        statusText = u'Du følger allerede denne diskusjonen gjennom epostvarsling'
        subscriptionActionText = u'Slå av epostvarsling'
        subscriptionAction = context.absolute_url()+'/discussion_unsubscribe'
    
content['subscription_status'] = {'isSubscriber':isSubscriber
                                 ,'subscriptionActionText':subscriptionActionText
                                 ,'subscriptionAction':subscriptionAction
                                 ,'statusText':statusText
                                 ,'canSubscribe':canSubscribe
                                }
    
return content