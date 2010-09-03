# -*- coding: utf-8 -*-

from Products.ksiktforum import psis
import DateTime

request = context.REQUEST
response = request.RESPONSE

content = {}
separator   = u"¤¨" # must be the same as used in addComment.py. We should probably put this in some common file...

## Create a list of the comments to the current context.
comments = context.listOccurrences(type=psis.comment)
commentlist = []
for comment in comments:
    #context.removeOccurrence(comment)
    #continue
    ## The entire comment (name, email, heading, commentbody) are stored as a single unicode value,
    ## delimited by a special character sequence.
    commentstring = comment.getValue()
    (name, email, heading, commentbody) = commentstring.split(separator)
    

    created = comment.created().strftime("%d.%m.%y %H:%M")

    ## We return each comment as a dictionary, so that the pagetemplage can easily pick out the
    ## various parts.
    commentlist.append( {"name":name, "email": email, "heading":heading, "comment":commentbody, 
                         "created":created,
                         "tm_serial":comment.tm_serial
                         } )
        
        
## The membersEmail and membersName values can be used to fill the comments-form with default values. 
memberTopic = context.getAuthenticatedMemberTopic()
membersEmail = ''
membersName  = ''
if memberTopic:
    ## yep, the user is a member on the portal.
    membersName  = memberTopic.title_or_id()
    membersEmail = memberTopic.getOccurrenceValue(psis.email,ignore=True,default="")
content['membersName'] = membersName
content['membersEmail'] = membersEmail

content['comments'] = commentlist
content['contenttype'] = context.Type()

## Generate the anti-spam stuff. TODO; perhaps move this to the PageTemplate, where the names of the
## form-fields and the css-styles really belong?
timestamp = DateTime.DateTime()
ipaddress = context.REQUEST.getClientAddr()
entryid   = context.tm_serial
content['commentcount'] = len(commentlist)
content['timestamp']  = timestamp
content['ipaddress'] = ipaddress
content['entryid']    = entryid
content['honeypots'] = context.getHoneyPots(timestamp,ipaddress, entryid,
                                              (('name',   'textInput'),
                                               ('email',  'textInput'),
                                               ('heading','textInput'),
                                               ('comment','textInput'),
                                               ),
                                               ("dn",), ## an invisible css class
                                              )

return content  

