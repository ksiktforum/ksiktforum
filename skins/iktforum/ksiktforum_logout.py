# -*- coding: utf-8 -*-


## This script is called when the user clicks the "Logg ut" link on any of the pages of the
## KSIKT portal.

REQUEST = context.REQUEST
if REQUEST.has_key('portal_skin'):
   context.portal_skins.clearSkinCookie()
REQUEST.RESPONSE.expireCookie('__ac', path='/')


redirecturl = context.index_html.absolute_url()

if REQUEST.has_key('came_from'):
    redirecturl = REQUEST['came_from']

messages = []
messages.append(u'Du er nå logget ut.')
params = "?"
for message in messages:
    params += "status.messages:record:ustring:utf8:list=%s&" % (message.encode("utf-8"),)


context.REQUEST.RESPONSE.redirect(redirecturl + params)
        