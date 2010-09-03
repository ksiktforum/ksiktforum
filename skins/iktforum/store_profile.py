# -*- coding: utf-8 -*-
#Updates the persons personal data

from Products.ksiktforum import psis

request = context.REQUEST
response = request.RESPONSE

persontopic = context.getAuthenticatedMemberTopic()
if persontopic:    
    options = {}
    options['status'] = {}
    messages = []
    errors = []
    
    
    personaldata = request.get('profile', {})
    occurrenceMapping = {'work': psis.work        
                       , 'department':psis.department
                       , 'workplace':psis.workplace
                       , 'visitaddress':psis.visitaddress
                       , 'phone':psis.phone
                       , 'mobilephone':psis.mobilephone
                       , 'email':psis.email
                       , 'workareas':psis.workareas
                       , 'qualifications':psis.qualifications            
                       }    
    new_password = personaldata.get('new_password','')
    confirm_password = personaldata.get('confirm_password','')
    if personaldata:        
        if new_password != u'passord' and confirm_password != u'passord':
            if new_password == confirm_password:                
                user = context.portal_membership.getAuthenticatedMember()
                name = user.getUserName() 
                roles = user.getRoles()
                domains = user.getDomains()
                userfolder = getattr(context, 'acl_users') 
                
                user_info = { 
                            'name' : name,
                            'password' : new_password,
                            'confirm' : confirm_password,
                            'roles' : roles,
                            'domains' : domains
                        }
                userfolder.manage_users(submit='Change', REQUEST=user_info)
            else:
                errors.append(u'De to passordene du oppgav stemte ikke overens')
        
        
        #set occurrencevalues        
        title = personaldata.get('name','')
        persontopic.setTitleAndName(title)        
        for key, psi in occurrenceMapping.items():
            updatevalue = personaldata.get(key,'')
            persontopic.setOccurrence(updatevalue, psi)   
        #check remove picture option
        if personaldata.get('removeimage', False):
            persontopic.portal_images.removeDecoration(psis.portraitimage, psis.resource, psis.decoration)                        
        
        portraitimage = personaldata.get('image', None)         
        if portraitimage:
            #upload image and set as personal picture
            imagetopic = context.portal_images.uploadImage(portraitimage)
            imagetopic.setTitleAndName(u'portrettbilde av '+persontopic.title_or_id())                                
            persontopic.portal_images.redecorateTopic(persontopic, imagetopic, psis.portraitimage, psis.resource, psis.decoration)            
        
        options['status']['errors'] = errors    
        if not errors:
            messages.append(u'Din personlige profil ble oppdatert.')
            options['status']['messages'] = messages
        
        return context.workspace_view(**options)
