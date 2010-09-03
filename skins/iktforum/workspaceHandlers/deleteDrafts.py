# -*- coding: utf-8 -*-

request = context.REQUEST
response = request.RESPONSE

persontopic = context.getAuthenticatedMemberTopic()
draft_serials = request.get('draft_serial', [])
for draft_serial in draft_serials:    
    context.portal_wizard.removeDraft(draft_serial)
    
return persontopic.workspace_view(status={'messages':[u'Merkede kladder er slettet']})
