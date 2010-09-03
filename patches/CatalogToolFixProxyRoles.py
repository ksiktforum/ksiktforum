from Products.CMFCore.CatalogTool import CatalogTool
from AccessControl import getSecurityManager

def _listAllowedRolesAndUsers(self, user):
    
    effective_roles = user.getRoles()
    sm = getSecurityManager()    
    if sm.calledByExecutable():
        eo = sm._context.stack[-1]
        proxy_roles = getattr(eo, '_proxy_roles', None)   
        if proxy_roles:
            effective_roles = proxy_roles
    result = list( effective_roles )
    result.append( 'Anonymous' )
    result.append( 'user:%s' % user.getId() )    
    return result
    
CatalogTool._listAllowedRolesAndUsers = _listAllowedRolesAndUsers