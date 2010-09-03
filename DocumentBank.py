from sets import Set
from Globals import InitializeClass
from AccessControl import ClassSecurityInfo

from Acquisition import aq_base, aq_inner, aq_parent

from Products.CMFCore.permissions import View, ModifyPortalContent, ManagePortal
 

from Products.ZTM2.Topic import Topic, addTopic
from Products.ZTM2.Locator import Locator

from zope.component.factory import Factory
from zope.interface import implements

from Products.ksiktforum import psis

from Products.ZTM2.psis import zope_id_topicPSI, zope_path_topicPSI

from Products.CMFCore.TypesTool import FactoryTypeInformation
from Products.CMFCore.interfaces import ITypeInformation

from Persistence import Persistent

from BTrees.OOBTree import OOBTree, OOSet
from BTrees.IOBTree import IOBTree

from random import randint

from DateTime import DateTime


filetypes = { 'application/pdf' : 'pdf'
             ,'application/vnd.ms-excel' : 'excel'
             ,'application/vnd.ms-word' : 'word'
             ,'application/msexcel' : 'excel'
             ,'application/msword' : 'word'
             ,'application/mspowerpoint' : 'powerpoint'
             ,'application/vnd.oasis.opendocument.text' : 'odt'
             ,'application/vnd.oasis.opendocument.spreadsheet' : 'ods'             
             ,'image/png' : 'bilde'
             ,'image/jpeg' : 'bilde'
             ,'image/gif' : 'bilde'
            }

fileicons = { 'excel':'xls'
             ,'pdf':'pdf'
             ,'powerpoint':'ppt'
             ,'word':'doc'
             ,'bilde':'gif'
             ,'odt':'odt'
             ,'ods':'ods'
             ,'fil':'txt'
            }

filenames = { 'excel':'Excel-fil'
             ,'pdf':'PDF-fil'
             ,'word':'Word-fil'
             ,'powerpoint':'Powerpoint-fil'
             ,'bilde':'Bildefil'
             ,'odt':'OpenDocument-fil'
             ,'ods':'OpenDocument regneark-fil'
             ,'fil':'Fil'
            }



class AgendaObject(Persistent):
    """ Simple object for. """
    __allow_access_to_unprotected_subobjects__ = 1

    security = ClassSecurityInfo()
    security.declareObjectPublic()    

    def __init__(self, title='No title', ingress='', parent=0):
        self.title = title        
        self.ingress = ingress
        self.serial = randint(1, 1000000)        
        self.parent = parent        
        self.children = []
        self.files = []
        
    def __str__(self):
        return self.serial
        
    def __call__(self):
        return self.__dict__.copy()        
        
    def update(self, kw):        
        for key, value in kw.items():            
            setattr(self, key, value)
        self._p_changed = True
            
    def firstChild(self):        
        if self.children:
            return self.children[0]
        else:
            return 0


InitializeClass(AgendaObject)

class DocumentBankTypeInformation(FactoryTypeInformation):
    """ Allows construction of plain topics. """
    implements(ITypeInformation)
    security = ClassSecurityInfo()
    
    _actions = ( { 'id':'view'
                 , 'title':'View'
                 , 'action':'documentbank_view'
                 , 'condition':''
                 , 'permissions':('View',)
                 , 'category':'object'  
                 , 'visible':True
                 }
               , { 'id':'edit'
                 , 'title':'Edit'
                 , 'action':'documentbank_view'
                 , 'condition':''
                 , 'permissions':('Modify portal content',)
                 , 'category':'object'
                 , 'visible':True
                 }
               , { 'id':'ztmedit'
                 , 'title':'Topic Edit'
                 , 'action':'documentbank_view'
                 , 'condition':''
                 , 'permissions':('Modify topic',)
                 , 'category':'object'
                 , 'visible':False
                 }
               , { 'id':'ztmview'
                 , 'title':'Topic View'
                 , 'action':'documentbank_view'
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
    _aliases = { 'ztmedit':'documentbank_view'
               , 'ztmview':'documentbank_view'
               , 'view':'documentbank_view'
               , 'edit':'documentbank_view'
               , 'gethtml':'documentbank_view'
               , 'index.html':'documentbank_view'
               }
    
    def __init__(self, id, **kw):
        self._topictype = aq_base(kw['topic'])
        kw['actions'] = self._actions
        kw['aliases'] = self._aliases
        FactoryTypeInformation.__init__(self, id, **kw)
        self.product = ''
        self.factory = 'ksiktforum.documentbank'
        self.content_meta_type = 'Topic'
        self.content_icon = 'topic_icon.png'
        self.immediate_view = 'documentbank_view'
        self.title = 'documentbank'
        self.description = 'Specialized topic that can organize content under self chose labels'
           
    
    security.declarePrivate('_constructInstance')
    def _constructInstance(self, container, id, *args, **kw):
        topicmap = kw['topicmap'] = self.portal_topicmaps.getTopicMap()  
        ob = FactoryTypeInformation._constructInstance( self
                                                      , container
                                                      , id
                                                      , *args
                                                      , **kw
                                                      )        
        ob.addType(psis.documentbank)
        
        
        #ob.invokeFactory(id='filearchive', type_name='CMF BTree Folder')        
        #ob.invokeFactory(id='discussion', type_name='CMF BTree Folder')        
        #getattr(ob, 'filearchive').__parent__ = ob
        #getattr(ob, 'discussion').__parent__ = ob        
        
        return ob

   

class DocumentBank(Topic):
    """ A documentbank is a topic where you are able to arrange attachments in an hierarchical way. """
    isObjectManager = True
    isPrincipiaFolderish = True

    meta_type = 'Topic'
    
    security = ClassSecurityInfo()
    security.declareObjectProtected(View)       
    
    
    def __init__(self, topicid, *args, **kw):
        self.agendaManager = IOBTree()
        self.agendaTopLevel = []
        Topic.__init__(self, topicid, *args, **kw)
    
    
    def manage_afterAdd(self, container, item):
        Topic.manage_afterAdd(self, container, item)        
        
        
    def documentbanktopic(self):
        """ The documentbank itself. """
        return self.aq_inner
        
    security.declarePrivate('notifyWorkflowCreated')
    def notifyWorkflowCreated(self):
        """
            Notify the workflow that self was just created.
        """       
        wftool = self._getWorkflowTool()
        if wftool is not None:
            wftool.notifyCreated(self)
        #self._View_Permission = ['Editor', 'Manager']#list(self._View_Permission)

    def addAgendaObject(self, title, ingress, invokedOn=0, level=0):        
        invokedOnAgendaNode =  self.agendaManager.get(invokedOn, None)       
        agendaNode = None    
        if invokedOnAgendaNode:                    
            if level == 0:
                #same level
                agendaNode = AgendaObject(title, ingress, parent=invokedOnAgendaNode.parent)
                children = self.agendaTopLevel
                if invokedOnAgendaNode.parent:
                    parent = self.agendaManager.get(invokedOnAgendaNode.parent, None)
                    parent.p_modified = True
                    children = parent.children
                else:
                    self.p_modified = True
                    
                index = 0                
                
                for serial in children:
                    if serial == invokedOn:
                        children.insert(index+1, agendaNode.serial)
                        break;
                    index = index + 1
                
            elif level == 1:
                #level below                
                parent = invokedOnAgendaNode.serial                                                                
                agendaNode = AgendaObject(title, ingress, parent=parent)
                invokedOnAgendaNode.children.append(agendaNode.serial)
                invokedOnAgendaNode._p_changed = True                
        #bootstrap
        else:
            agendaNode = AgendaObject(title, ingress, parent=0)
            self.agendaTopLevel.append(agendaNode.serial)
        
        if agendaNode:
            self.agendaManager.insert(agendaNode.serial, agendaNode)            
        self._p_changed = True        
        
    def removeAgendaObject(self, invokedOn):
        invokedOnNode = self.agendaManager.get(invokedOn, None)
        if invokedOnNode:
            parentNode = self.agendaManager.get(invokedOnNode.parent, None)
            siblings = self.agendaTopLevel
            if parentNode:
                siblings = parentNode.children
                parentNode._p_changed = True
            else:
                self._p_changed = True
                
            children = invokedOnNode.children
            
            
            def recursiveRemove(children):          
                for child in children:
                    try:
                        recursiveRemove(self.agendaManager.get(child, None).children)
                    except AttributeError:
                        pass                        
                    del(self.agendaManager[child])                    
            #Remove all children from the node we want to remove as well.
            recursiveRemove(children)
            
                    
            siblings.remove(invokedOn)
            del(self.agendaManager[invokedOn])
            
                
        
    def indentAgendaObject(self, invokedOn):
        invokedOnNode = self.agendaManager.get(invokedOn, None)
        if invokedOnNode:
            parentNode = self.agendaManager.get(invokedOnNode.parent, None)
            children = self.agendaTopLevel
            if parentNode:
                children = parentNode.children
                parentNode._p_changed = True
            else:
                self._p_changed = True
            index = 0
            for serial in children:
                if serial == invokedOnNode.serial:                    
                    if index == 0:
                        raise AssertionError, "can't indent"
                    #get previous node
                    prevSibling = self.agendaManager.get(children[index-1], None)                    
                    #make previous node parent
                    invokedOnNode.parent = prevSibling.serial
                    #add node to new parent children
                    prevSibling.children.append(invokedOn)
                    prevSibling._p_changed = True
                    #remove node from current parent                    
                    children.remove(invokedOnNode.serial)
                    break
                index = index+1            
        
        
        return True
        
                        
        
    def outdentAgendaObject(self, invokedOn):
        invokedOnNode = self.agendaManager.get(invokedOn, None)
        if invokedOnNode:
            parentNode = self.agendaManager.get(invokedOnNode.parent, None)            
            if not parentNode:                
                raise SyntaxError, "can't outdent"            
            parentNode.children.remove(invokedOn)
            parentNode._p_changed = True
            grandparentNode = self.agendaManager.get(parentNode.parent, None)
            children = self.agendaTopLevel
            if grandparentNode:
                children = grandparentNode.children
                grandparentNode._p_changed = True
            else:
                self._p_changed = True
            
            index = 0
            for serial in children:
                if serial == parentNode.serial:
                    children.insert(index+1, invokedOn)
                    break
                index = index+1                
            #set new parent
            invokedOnNode.parent = parentNode.parent
        
        return True
        
    
    def moveAgendaObjectUp(self, invokedOn):
        invokedOnNode = self.agendaManager.get(invokedOn, None)
        if invokedOnNode:
            parentNode = self.agendaManager.get(invokedOnNode.parent, None)
            children = self.agendaTopLevel
            if parentNode:
                children = parentNode.children
                parentNode._p_changed = True
            else:
                self._p_changed = True
            index = 0
            for serial in children:
                if serial == invokedOnNode.serial:                    
                    if index == 0:
                        raise AssertionError, "on the top"
                    else:
                        children.remove(invokedOnNode.serial)
                        children.insert(index-1, invokedOnNode.serial)
                    break
                index = index+1            
        
        
        return True
        
        
    def moveAgendaObjectDown(self, invokedOn):
        invokedOnNode = self.agendaManager.get(invokedOn, None)
        if invokedOnNode:
            parentNode = self.agendaManager.get(invokedOnNode.parent, None)
            children = self.agendaTopLevel
            if parentNode:
                children = parentNode.children
                parentNode._p_changed = True
            else:
                self._p_changed = True
            index = 0
            for serial in children:
                if serial == invokedOnNode.serial:                    
                    if index == len(children)-1:
                        raise AssertionError, "on the bottom"
                    else:
                        children.remove(invokedOnNode.serial)
                        children.insert(index+1, invokedOnNode.serial)
                    break
                index = index+1
        
        
        return True
                
        
    security.declareProtected(View, 'getAgendaNode')
    def getAgendaNode(self, serial):        
        return self.agendaManager.get(serial, None)
    
    def getAgenda(self):    
        return self.agendaTopLevel

    security.declareProtected(ModifyPortalContent, 'uploadFile')
    def uploadFile(self, fileObject, title, overwrite=False):
        topicmap = self.portal_topicmaps.getTopicMap()
        atbsi = topicmap.assertTopicBySubjectIdentifier              
        filetopictype = atbsi(psis.file)

        #TODO: get path
        creationpath = getattr(self, 'filearchive')

        filename = altTopicTitle = self.portal_topicmanagement.extractFilename(unicode(fileObject.filename, 'utf8'))
        
        origname = filename = self.portal_topicmanagement.normalizeid(filename)

        counter = 1

        
        idIsAvailable = creationpath.checkIdAvailable(filename)
        topicid = filename+".topic"
        if not idIsAvailable:
            if overwrite and getattr(creationpath, topicid, False):
                #delete file.      
                creationpath.manage_delObjects([filename])                
                filetopic = getattr(creationpath, topicid)
                #update title if set
                if title:                    
                    filetopic.setTitleAndName(title)
                idIsAvailable = True
            else:
                raise AssertionError, "%s already exists. If you want to overwrite this file you must check the checkbox titled 'Overwrite existing file'"%title
            
        checkIdAvailable = creationpath.checkIdAvailable
        while not idIsAvailable:
            filename = origname[0:origname.rindex('.')]+'_'+str(counter)+'_'+origname[origname.rindex('.'):]
            counter += 1        
            idIsAvailable = checkIdAvailable(filename)    
            if counter >= 50:
                raise AssertionError, "You entered an endless loop during fileupload. This should not have happened. Please write down the steps you used to trigger this bug and report it to the ZTM developers."

        if not title:
            title = altTopicTitle            
        
        self.REQUEST.set('type_name', 'File')
        creationpath.invokeFactory(type_name='File', id=filename)
        newfile = getattr(creationpath, filename)
        newfile.manage_upload(fileObject)
            
        
        #create file topic. set file as subjectlocatior    
        if not getattr(creationpath, topicid, False):                    
            self.REQUEST.set('type_name', 'file')
            creationpath.invokeFactory(type_name='file', id=topicid)
            filetopic = getattr(creationpath, topicid)    
            filetopic.setTitleAndName(title)
            filetopic.addSubjectLocator('x-zope-path:' + '/'.join(newfile.getPhysicalPath()))            
        else:
            if overwrite:
                #overwrite file clear subject locators:            
                filetopic = getattr(creationpath, topicid)
                for locator in filetopic.getSubjectLocators():
                    filetopic.removeSubjectLocator(locator)
                #set new subject locator
                filetopic.addSubjectLocator('x-zope-path:' + '/'.join(newfile.getPhysicalPath()))            
            
        filetopic.reindexObject()  
        return filetopic.tm_serial
       
    security.declareProtected(ModifyPortalContent, 'openForAnonymousUsers')
    def openForAnonymousUsers(self, topic=None):
          #topic not given, open up the documentbank itself
        if not topic:
            topic = self
        allowedToAccessContent = list(getattr(topic, '_Access_contents_information_Permission', []))    
        if 'Anonymous' not in allowedToAccessContent:
            allowedToAccessContent.append('Anonymous')        
        topic.manage_permission("Access contents information", allowedToAccessContent, acquire=0)
        
        allowedToViewContent = list(getattr(topic, '_View_Permission', []))    
        if 'Anonymous' not in allowedToViewContent:
            allowedToViewContent.append('Anonymous')        
        topic.manage_permission("View", allowedToViewContent, acquire=0)        
        
    security.declareProtected(ModifyPortalContent, 'closeForAnonymousUsers')
    def closeForAnonymousUsers(self, topic=None):
        #topic not given, close down the documentbank itself
        if not topic:
            lazy = self.portal_catalog(path='/'.join(self.getPhysicalPath()), types=[psis.file], sort_on='modified', sort_order='Reverse')
            for brain in lazy:
                topic = brain.getObject()
                self.closeForAnonymousUsers(topic)            
            topic = self
            
        allowedToAccessContent = list(getattr(topic, '_Access_contents_information_Permission', []))        
        for user in allowedToAccessContent:
            if user == 'Anonymous':
                allowedToAccessContent.remove(user)
        topic.manage_permission("Access contents information",allowedToAccessContent, acquire=0)
        
        allowedToViewContent = list(getattr(topic, '_View_Permission', []))    
        for user in allowedToViewContent:
            if user == 'Anonymous':
                allowedToViewContent.remove(user)   
        topic.manage_permission("View", allowedToViewContent, acquire=0)   
           
    security.declareProtected(View, 'isOpen')
    def isOpen(self):
        allowedToAccessContent = list(getattr(self, '_Access_contents_information_Permission', []))       
        allowedToViewContent = list(getattr(self, '_View_Permission', []))
        
        if 'Anonymous' in allowedToAccessContent and 'Anonymous' in allowedToViewContent:
            return True
        else:
            return False
    
    security.declareProtected(View, 'fileArchiveContents')
    def fileArchiveContents(self):
        return {} #mark
        files = []
        append = files.append
        lazy = self.portal_catalog(path='/'.join(self.filearchive.getPhysicalPath()), types=[psis.file], sort_on='modified', sort_order='Reverse')
        for brain in lazy:
            topic = brain.getObject()    
            fileobject = topic.resource_object()
            content_type = fileobject and fileobject.content_type or ""           
            filetype = filetypes.has_key(content_type) and filetypes[content_type] or "fil"                
            file_icon = fileicons[filetype]
            file_type = filenames[filetype]    
    
            allowedToAccessContent = list(getattr(topic, '_Access_contents_information_Permission', []))       
            allowedToViewContent = list(getattr(topic, '_View_Permission', []))
            is_open = bool('Anonymous' in allowedToAccessContent and 'Anonymous' in allowedToViewContent)
    
    
            append({'title':topic.title_or_id()
            ,'filetitle':fileobject.title_or_id()
            ,'Creator':topic.Creator
            ,'iconclass':file_icon
            ,'modified': DateTime(topic.modified()).strftime('%d.%m.%Y %H:%M')
            ,'tm_serial':topic.tm_serial
            ,'url':fileobject.absolute_url()
            ,'is_open':is_open
                
            })
            
        files = [(x['title_or_id'],x) for x in files]
	files.sort()
	files = [y for (x,y) in files]

        return files     
        
    security.declareProtected(ModifyPortalContent, 'publishFiles')
    def publishFiles(self, tm_serials):
        topicmap = self.getTopicMap()
        gtbs = topicmap.getTopicBySerial
        for tm_serial in tm_serials:
            
            try:            
                topic = gtbs(tm_serial)
                self.openForAnonymousUsers(topic) 
                topic.reindexObject()
            except KeyError:
                pass
                
    security.declareProtected(ModifyPortalContent, 'retractFiles')
    def retractFiles(self, tm_serials):
        topicmap = self.getTopicMap()
        gtbs = topicmap.getTopicBySerial
        for tm_serial in tm_serials:
            try:
                topic = gtbs(tm_serial)
                self.closeForAnonymousUsers(topic)
                topic.unindexObject()
                topic.indexObject()
            except KeyError:
                pass
                
InitializeClass(DocumentBank)
InitializeClass(DocumentBankTypeInformation)
DocumentBankFactory = Factory(DocumentBank)

