from Products.ksiktforum.WorkArea import WorkAreaTypeInformation
from Products.ksiktforum.DocumentBank import DocumentBankTypeInformation
from Products.ksiktforum import psis

class WorkAreaTypeInformationAddView(object):
    
    def __call__(self, psi='', submit_add=''):
        # A topic has been submitted.
        topicmap = self.context.portal_topicmaps.getTopicMap()       
        topic = topicmap.getTopic(psis.workarea)
        obj = WorkAreaTypeInformation(id=topic.getId(), topic=topic, topicmap=topicmap)
        self.request.set('add_input_name', topic.getId()) # Should probably use an adapter, but this works as well :-)
        self.context.add(obj)
        self.request.response.redirect(self.context.nextURL())    
        return self.index()
        
class DocumentBankTypeInformationAddView(object):
    
    def __call__(self, psi='', submit_add=''):
        # A topic has been submitted.
        topicmap = self.context.portal_topicmaps.getTopicMap()       
        topic = topicmap.getTopic(psis.documentbank)
        obj = WorkAreaTypeInformation(id=topic.getId(), topic=topic, topicmap=topicmap)
        self.request.set('add_input_name', topic.getId()) # Should probably use an adapter, but this works as well :-)
        self.context.add(obj)
        self.request.response.redirect(self.context.nextURL())    
        return self.index()

class TopicTypeInformationAddView(object):
    def __call__(self):
        # Autocreate a Topic View
        if not 'Topic' in self.context.context.aq_inner.objectIds():
            obj = TopicTypeInformation('Topic')
            self.request.set('add_input_name', 'Topic') # Should probably use an adapter, but this works as well :-)
            self.context.add(obj)
            self.request.response.redirect(self.context.nextURL())
            return ''
        else:
            return "Id 'topic' is already taken"

class TopicMapTypeInformationAddView(object):
    def __call__(self):
        # Autocreate a Topic View
        if not 'TopicMap' in self.context.context.aq_inner.objectIds():
            obj = TopicMapTypeInformation('Topic')
            self.request.set('add_input_name', 'Topic') # Should probably use an adapter, but this works as well :-)
            self.context.add(obj)
            self.request.response.redirect(self.context.nextURL())
            return ''
        else:
            return "Id 'topicmap' is already taken"


