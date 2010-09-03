# -*- coding: utf-8 -*-
#
# Copyright KSIKT-Forum and Bouvet
from Products.CMFCore.utils import initializeBasesPhase1, initializeBasesPhase2, ToolInit, ContentInit
from Products.CMFCore.DirectoryView import registerDirectory
from Products.CMFCore.permissions import AddPortalContent


# Make the skins available as DirectoryViews
registerDirectory('skins/iktforum', globals(), subdirs=True)

from AccessControl.SecurityInfo import ModuleSecurityInfo                                                                                  
#ModuleSecurityInfo('Products.IKTForum').declarePublic('psis')
ModuleSecurityInfo('Products.ksiktforum').declarePublic('psis')
#ModuleSecurityInfo('Products').declarePublic('ksiktforum')

import sys
this_module = sys.modules[ __name__ ]

import patches

import psis
from Products.ZTM2.Topic import DESCRIPTIONPSIS
DESCRIPTIONPSIS.append(psis.ingress)

def initialize(context):
    
    ContentInit(u'IKTForum Content'
               , content_types = ()
               , permission = AddPortalContent               
               ).initialize(context)

            
#vim:encoding=utf-8:fileencoding=utf-8:bomb:et:sts=4:ts=4:sw=4
