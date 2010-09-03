# -*- coding: utf-8 -*-


## ksiktforum_login_form_target"
## This is the script that is called when a user is logging onto the portal. It is called in two
## different cases: 
##  1: When a new user has clicked on an invitation-link to the acceptMemberInvite.py
##     script. In this case the acceptMemberInvite.py script will create a form with 
##     hidden "__ac_name" and "__ac_password" fields (among others).
##  2: When an existing user has entered his username and password in the login-form
##     on one of the portal-pages (this form is defined in content_view.pt).


mtool = context.portal_membership
isAnon = mtool.isAnonymousUser()
member = mtool.getAuthenticatedMember()


redirecturl = context.REQUEST.URL1 # context.portal_url()

messages = []
errors   = []


# First we check to see if the user is a valid member of the portal.
if isAnon:
    context.REQUEST.RESPONSE.expireCookie('__ac', path='/')
    #context.REQUEST.REQUEST.set('error_message', 'Login failed')
    errors.append(u'Kunne ikke logge deg på: feil brukernavn eller passord.') 
    #return context.login_form(context.REQUEST, context.REQUEST.RESPONSE)
else:
    if 'usersworkspaceurl' in context.REQUEST:
        ## This page is called from the acceptMemberInvite.py script, so we want to add some more specific
        ## welcoming messages.
        redirecturl = context.REQUEST['usersworkspaceurl']
        username = context.REQUEST['username']
        password = context.REQUEST['password']        
        messages.append(u"Velkommen som ny bruker av KSIKT-Forum!") 
        messages.append(u"""Ditt brukernavn er "%s" og ditt passord er "%s". Denne informasjonen er også sendt til deg på epost""" % (username,password))
        messages.append(u'Det første du bør gjøre som medlem av KSIKT-Forum er å fylle ut personlig informasjon. Dette gjøres i skjemaet du finner i høyre marg av denne siden.')
        messages.append(u'Siden du nå står på er din personlige arbeidsflate. Du vil alltid kunne komme tilbake hit via lenken øverst til høyre på siden')
    else:
        #http://zopedev.bouvet.no/portal/personer/knut.johannessen7/workspace_view?status.errors:record:ustring:utf8:list=error1&status.errors:record:ustring:utf8:list=error2  
        memberTopic = context.getAuthenticatedMemberTopic()
        if not memberTopic:
            errors.append(u'Hmm. Du er logget på, men context.getAuthenticatedMemberTopic() returnerte ingenting. Er du logget på med en bruker som er laget manuellt av portal-administratoren?')
        else:
            # t
            # TODO: should we redirect the user to his workarea here? If so, uncomment the next line.
            redirecturl = memberTopic.absolute_url() + "/workspace_view"
            messages.append(u'Du er nå logget inn som ' + memberTopic.title_or_id())


## Pack errors and messages into the url string, so that they will be displayed on the page.
params = ""
for message in messages:    
    params += "status.messages:record:ustring:utf8:list=%s&" % (message.encode("utf-8"),)
for error in errors:
    redirecturl = redirecturl.replace('https','http')
    params += "status.errors:record:ustring:utf8:list=%s&" % (error.encode("utf-8"),)
if params:
    params = "?" + params



context.REQUEST.RESPONSE.redirect(redirecturl+ params)
        
