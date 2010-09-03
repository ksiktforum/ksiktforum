import DateTime
from Products.ksiktforum import psis

content = {}
activities = []


## We must find the position of the first activity that starts today or later,
## since that will be the default startpoint in the list that we display to the user.
## The user can then use the "next" and "previous" links to move to activities further
## in the future or the past.


last_midnight = DateTime.DateTime().earliestTime()-2


future_activites = context.portal_catalog(types=[psis.activity, psis.seminar], 
                                      occurrence_enddate=(last_midnight, ),
                                      occurrence_enddate_usage='range:min',                                    
                                      sort_on='occurrence_enddate',
                                      sort_order='Ascending')

past_activities = context.portal_catalog(types=[psis.activity, psis.seminar], 
                                      occurrence_enddate=(last_midnight, ),
                                      sort_on='occurrence_enddate',
                                      occurrence_enddate_usage='range:max',
                                      sort_order='Descending')

content["future_activities"] = future_activites
content["past_activities"] = past_activities
return content