from sets import Set
from Globals import InitializeClass
from AccessControl import ClassSecurityInfo

from Acquisition import aq_base, aq_inner, aq_parent

from Products.CMFCore.permissions import View, ModifyPortalContent

from Products.ZTM2.Topic import Topic, addTopic
from Products.ZTM2.Locator import Locator

from zope.component.factory import Factory
from zope.interface import implements

import psis
from Products.ZTM2.psis import zope_id_topicPSI, zope_path_topicPSI

from Products.CMFCore.TypesTool import FactoryTypeInformation
from Products.CMFCore.interfaces import ITypeInformation

class WorkAreaTypeInformation(FactoryTypeInformation):
    """ Allows construction of plain topics. """
    implements(ITypeInformation)
    security = ClassSecurityInfo()
    
    _actions = ( { 'id':'view'
                 , 'title':'View'
                 , 'action':'workarea_view'
                 , 'condition':''
                 , 'permissions':('View',)
                 , 'category':'object'  
                 , 'visible':True
                 }
               , { 'id':'edit'
                 , 'title':'Edit'
                 , 'action':'workarea_view'
                 , 'condition':''
                 , 'permissions':('Modify portal content',)
                 , 'category':'object'
                 , 'visible':True
                 }
               , { 'id':'ztmedit'
                 , 'title':'Topic Edit'
                 , 'action':'workarea_view'
                 , 'condition':''
                 , 'permissions':('Modify topic',)
                 , 'category':'object'
                 , 'visible':False
                 }
               , { 'id':'ztmview'
                 , 'title':'Topic View'
                 , 'action':'workarea_view'
                 , 'condition':''
                 , 'permissions':('View topic',)
                 , 'category':'object'
                 , 'visible':False
                 }
               , { 'id':'folderContents'
                 , 'title':'Folder Contents'
                 , 'action':'history_view'
                 , 'condition':'python:getattr(object, "isPrincipiaFolderish", True)'
                 , 'permissions':('Access folder contents',)
                 , 'category':'object'
                 , 'visible': False
                 }
               )
    _aliases = { 'ztmedit':'workarea_view'
               , 'ztmview':'workarea_view'
               , 'view':'workarea_view'
               , 'edit':'workarea_view'
               , 'gethtml':'workarea_view'
               , 'index.html':'workarea_view'
               }
    
    def __init__(self, id, **kw):
        self._topictype = aq_base(kw['topic'])
        kw['actions'] = self._actions
        kw['aliases'] = self._aliases
        FactoryTypeInformation.__init__(self, id, **kw)
        self.product = ''
        self.factory = 'ksiktforum.workarea'
        self.content_meta_type = 'Topic'
        self.content_icon = 'topic_icon.png'
        self.immediate_view = 'workarea_view'
        self.title = 'workarea'
        self.description = 'Specialized topic that handles access control'
    
    security.declarePrivate('_constructInstance')
    def _constructInstance(self, container, id, *args, **kw):
        topicmap = kw['topicmap'] = self.portal_topicmaps.getTopicMap()  
        ob = FactoryTypeInformation._constructInstance( self
                                                      , container
                                                      , id
                                                      , *args
                                                      , **kw
                                                      )        
        ob.addType(psis.workarea)
        
        
        ob.invokeFactory(id='filer', type_name='CMF BTree Folder')        
        ob.invokeFactory(id='diskusjoner', type_name='CMF BTree Folder')        
        getattr(ob, 'filer').__parent__ = ob
        getattr(ob, 'diskusjoner').__parent__ = ob        
        
        return ob

   

class WorkArea(Topic):
    """ A workarea is a topic with specialized handling of local roles. """
    isObjectManager = True
    isPrincipiaFolderish = True

    meta_type = 'Topic'
    
    isWorkArea = True

    security = ClassSecurityInfo()
    security.declareObjectProtected(View)       
    
    def manage_afterAdd(self, container, item):
        Topic.manage_afterAdd(self, container, item)
        self.updateWorkArea()
    
    def updateWorkArea(self):
        """ Update the local roles. """
        if hasattr(self, '_View_Permission'):
            # Workaround a bug that is either in DCWorkflow, Zope or CMF, It
            # doesn't remember not to acquire roles.
            self._View_Permission = tuple(self._View_Permission)
        
        newroles = {}
        for userid, roles in self.__ac_local_roles__.items():            
            roles = list(Set(roles))
            if 'Owner' in roles:
                roles.remove('Owner')               
            if 'Workarea manager' in roles:
                roles.remove('Workarea manager')
            if roles:
                newroles[userid] = roles
                
        for topic in self.managers(wrap=False):
            # A member may have multiple addresses
            memberid = topic.id
            memberroles = newroles.get(memberid, [])
            if not 'Owner' in memberroles:
                memberroles.append('Owner')
            if not 'Workarea manager' in memberroles:
                memberroles.append('Workarea manager')
            newroles[memberid] = memberroles
 
        self.__ac_local_roles__ = newroles
    
    def managers(self, wrap=True):
        """ The managers of this workarea. """
        
        topics = self.associatedTopicsQuery( otherroletype=psis.workareamanager
                                      , associationtype=psis.workareamembership
                                      , roletype=psis.workarea
                                      , topictype=psis.person
                                      )
        return set(topics)
    
    def reindexObject(self, idxs=[]):
        """ """
        self.updateWorkArea()
        return Topic.reindexObject(self, idxs=idxs)
    
    def workareatopic(self):
        """ The workarea itself. """
        return self.aq_inner

    def fixWorkArea(self):
        """ """
        getattr(self, 'koblinger').__parent__ = self
        getattr(self, 'dokumenter').__parent__ = self
        getattr(self, 'epostarkiv').__parent__ = self
        getattr(self, 'kalender').__parent__ = self

    def _removeAssociationRole(self, role):
        #TODO: Verify that the user is allowed to see the topic.
        Topic._removeAssociationRole(self, role)
        self.updateWorkArea()
    
    def _addAssociationRole(self, role):
        #TODO: Verify that the user is allowed to see the topic.
        Topic._addAssociationRole(self, role)
        self.updateWorkArea()

    def returnToWorkArea(self):
        return '<a href="%s">&laquo; Tilbake til arbeidsrommet</a>'%(self.absolute_url())


    security.declarePrivate('notifyWorkflowCreated')
    def notifyWorkflowCreated(self):
        """
            Notify the workflow that self was just created.
        """
        wftool = self._getWorkflowTool()
        if wftool is not None:
            wftool.notifyCreated(self)
        self._View_Permission = list(self._View_Permission)


InitializeClass(WorkArea)
InitializeClass(WorkAreaTypeInformation)
WorkAreaFactory = Factory(WorkArea)


