# -*- coding: utf-8 -*-

topicmap = context.getTopicMap()
contentlist = context.REQUEST.get('selectedContent',[])
#person      =  context.REQUEST.get('person',0)
#personTopic = topicmap.getTopicBySerial(person)
personTopic = context.getAuthenticatedMemberTopic()
if not personTopic:
    return "invalid 'person' value! request:",request # This should never happen

selectedcount = 0
successcount = 0
messages = []
errors = []
for tm_serial in contentlist:
    topic = topicmap.getTopicBySerial(tm_serial)
    if topic:
        selectedcount += 1
        try:
            context.portal_workflow.doActionFor(topic,'retract') 
            successcount += 1
        except Exception,e: # happens if the user tries an unsupported workflow action (like retracting an already published element)
            errors.append(u"""Kunne ikke trekke tilbake "%s". Feilmeldingen fra systemet var: "%s" """ % (topic.title_or_id(),e,))

if successcount > 0:
    messages.append('%d element(er) ble trukket tilbake' % (successcount,))
else:
    if selectedcount == 0:
        errors.append(u'Ingen elementer var valgt.')
        

return personTopic.workspace_view(status={'errors':errors,'messages':messages})

