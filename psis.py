__allow_access_to_unprotected_subobjects__ = 1

from Products.ZTMDefault.psis import dc_description
from Products.ZTMSearch.psis import category, categorization, categorized, taxonomy, generalization, specialization
from Products.ZTMPhoto.psis import photographer, original
from Products.DisplayList.psis import displaylist

def __setattr__(self, name, value):
    raise AssertionError("Please to not overwrite these constants")

contenttype = u'http://psi.emnekart.no/ztm/default/contenttype'
#Contenttypes            
article = u'http://psi.ksikt-forum.no/ontology/article'
image = u'http://psi.emnekart.no/ztm/ztmphoto/#image'
file = u'http://psi.emnekart.no/ztm/ztmdefault/#file'
person = u'http://psi.ksikt-forum.no/ontology/person'
subject = u'http://psi.ksikt-forum.no/ontology/subject'
activity = u'http://psi.ksikt-forum.no/ontology/activity'
faq = u'http://psi.ksikt-forum.no/ontology/faq'
plural = u'http://psi.ontopia.net/xtm/basename/plural'
campaign = u'http://psi.ksikt-forum.no/ontology/campaign'
frontpage = u'http://psi.ksikt-forum.no/ontology/frontpage'
external_link = u'http://psi.ksikt-forum.no/ontology/external_link'
seminar = u'http://psi.ksikt-forum.no/ontology/seminar'
discussionthread = u'http://psi.ksikt-forum.no/ontology/discussionthread'
discussionthreadfollowup  = u'http://psi.ksikt-forum.no/ontology/discussionthreadfollowup'
section = u'http://psi.ksikt-forum.no/ontology/section' 
concept = u'http://psi.ksikt-forum.no/ontology/concept'
handbook = u'http://psi.ksikt-forum.no/ontology/handbook'
documentbank = u'http://psi.ksikt-forum.no/ontology/documentbank'

resource = u'http://psi.emnekart.no/ztm/ztmphoto/#resource'
decoration = u'http://psi.emnekart.no/ztm/ztmphoto/#decoration'

service = u'http://psi.ksikt-forum.no/ontology/service'
servicetreatement = u'http://psi.ksikt-forum.no/ontology/servicetreatment'

#occurrencetypewidgets
text = u'http://psi.ksikt-forum.no/ontology/text'

ingress = u'http://psi.ksikt-forum.no/ontology/ingress'
phone = u'http://psi.ksikt-forum.no/ontology/phone'
address = u'http://psi.ksikt-forum.no/ontology/address'
email = u'http://psi.ksikt-forum.no/ontology/email'
workareas = u'http://psi.ksikt-forum.no/ontology/workareas'
visitaddress = u'http://psi.ksikt-forum.no/ontology/visitaddress'
edittemplate = 'http://psi.ksikt-forum.no/ontology/edittemplate'
mobilephone = u'http://psi.ksikt-forum.no/ontology/mobilephone'
startdate = u'http://psi.ksikt-forum.no/ontology/startdate'
enddate = u'http://psi.ksikt-forum.no/ontology/enddate'
edittemplate = u'http://psi.ksikt-forum.no/ontology/edittemplate'
structuredmarker = u'http://psi.ksikt-forum.no/ontology/structuredmarker'
creation_path = u'http://psi.emnekart.no/ztm/content/creation_path'
link = u'http://psi.ksikt-forum.no/ontology/link'
work = u'http://psi.ksikt-forum.no/ontology/work'
department = u'http://psi.ksikt-forum.no/ontology/department'
workplace = u'http://psi.ksikt-forum.no/ontology/workplace'
qualifications = u'http://psi.ksikt-forum.no/ontology/qualifications'
answer = u'http://psi.ksikt-forum.no/ontology/answer'
question = u'http://psi.ksikt-forum.no/ontology/question'
press_release = u'http://psi.ksikt-forum.no/ontology/press_release'
location = u'http://psi.ksikt-forum.no/ontology/location'
registration_start_date = u'http://psi.ksikt-forum.no/ontology/registration_start_date'
registration_end_date = u'http://psi.ksikt-forum.no/ontology/registration_end_date'
registration_options = u'http://psi.ksikt-forum.no/ontology/registration_options'
max_attendees = u'http://psi.ksikt-forum.no/ontology/max_attendees'
imagetext = u'http://psi.ksikt-forum.no/ontology/imagetext'
arrangor = u'http://psi.ksikt-forum.no/ontology/arrangor'
alert_on_add_newmember = u'http://psi.ksikt-forum.no/ontology/alert_on_add_newmember'

#occurrencetypes
structuredmarker = u'http://psi.ksikt-forum.no/ontology/structuredmarker'
comment = u'http://psi.ksikt-forum.no/ontology/comment'
attendee = u'http://psi.ksikt-forum.no/ontology/attendee'
comments_allowed = u'http://psi.ksikt-forum.no/ontology/comments_allowed'
typeweight = u'http://psi.emnekart.no/ztm/search/typeweight'

#assoctypes
authorship = u'http://psi.ksikt-forum.no/ontology/authorship'
authored = 'http://psi.emnekart.no/ztm/authored'
attachment = u'http://psi.ksikt-forum.no/ontology/attachement'
caseimage = u'http://psi.ksikt-forum.no/ontology/caseimage'
responsibility = u'http://psi.ksikt-forum.no/ontology/responsibility'
relevancy = u'http://psi.ksikt-forum.no/ontology/relevancy'
portraitimage = u'http://psi.ksikt-forum.no/ontology/frontpage'
campaignimage = u'http://psi.ksikt-forum.no/ontology/campaignimage'
campaign = u'http://psi.ksikt-forum.no/ontology/campaign'
discussion = u'http://psi.ksikt-forum.no/ontology/discussion'         # between discussionthreads and 'arbeids rom'.
subscription = u'http://psi.ksikt-forum.no/ontology/subscription'  
has_chapter = u'http://psi.ksikt-forum.no/ontology/has_chapter'  
servicecategorization = 'http://psi.ksikt-forum.no/ontology/servicecategorization'
servicetreatementcategorization = 'http://psi.ksikt-forum.no/ontology/servicetreatmentcategorization'

#rolestypes
maincampaign = u'http://psi.ksikt-forum.no/ontology/maincampaign'
author = u'http://psi.emnekart.no/ztm/author'
contactperson = u'http://psi.ksikt-forum.no/ontology/contactperson'
relevant = u'http://psi.ksikt-forum.no/ontology/relevant'
discussion_subscriber = u'http://psi.ksikt-forum.no/ontology/discussion_subscriber'
subscribed = u'http://psi.ksikt-forum.no/ontology/subscribed'
discussion_contribution= u"http://psi.ksikt-forum.no/ontology/discussion_contribution"
chapter = u"http://psi.ksikt-forum.no/ontology/chapter"
workarea_subscriber = u'http://psi.ksikt-forum.no/ontology/workarea_subscriber'

# Image sizes
originalimage = u'http://psi.ksikt-forum.no/ontology/originalimage'
thumbnailimage = u'http://psi.emnekart.no/ztm/ztmphoto/#thumbnail'
ingressimage = u'http://psi.ksikt-forum.no/ontology/ingressimage'
subjectimage = u'http://psi.ksikt-forum.no/ontology/subjectimage'
frontpageimage = u'http://psi.ksikt-forum.no/ontology/forsidetoppsakbilde'
portraitimage = u'http://psi.ksikt-forum.no/ontology/portraitimage'
campaignimage = u'http://psi.ksikt-forum.no/ontology/campaignimage'

#lists                          
latest_global_content = u'http://psi.ksikt-forum.no/lists/latest_global_content'
latest_categorized_content = u'http://psi.ksikt-forum.no/lists/latest_categorized_content'
link_list = u'http://psi.ksikt-forum.no/lists/link_list'
concept_list = u'http://psi.ksikt-forum.no/lists/concept_list'

#Extranet
workarea = u'http://psi.ksikt-forum.no/ontology/workarea'
workareamanager = u'http://psi.ksikt-forum.no/ontology/workareamanager'
workareamembership = u'http://psi.ksikt-forum.no/ontology/workareamembership'
              

