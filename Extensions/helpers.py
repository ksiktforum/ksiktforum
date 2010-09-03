from Acquisition import aq_base
    
def setOwner(self, username):
    #note: this assumes that the closest User database houses 'username'
    user = self.acl_users.getUser(username)
    self.changeOwnership(user.__of__(self.acl_users))
    
