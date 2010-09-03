if not context.portal_membership.isAnonymousUser():    
    member = context.portal_membership.getAuthenticatedMember()
    return getattr(context.portal_url.personer, member.getId(), None)
else: 
    return None

