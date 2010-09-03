## Script (Python) "templateCacheHeaders"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##

anon = context.portal_membership.isAnonymousUser()

from DateTime import DateTime
import time
togmt = context.rfc1123_date

now = DateTime()

request = context.REQUEST

response = request.RESPONSE

modified = context.modified()

delta = now-modified

if delta <= 7:
  # New content, only cache it for a few hours
  cache_time = 3
elif delta > 7 and delta <= 14:
  # Semi-new content, cache it for a day
  cache_time = 24
elif delta > 14 and delta <= 30:
  # Semi-new content, cache it for three days
  cache_time = 3 * 24
elif delta > 30 and delta <= 60:
  # Semi-old content, cache it for five days
  cache_time = 5 * 24
else:
  # Really old content, cache it for two weeks
  cache_time = 14 * 24

  
  
expires = now# + float(cache_time) / 24.0

setHeader = response.setHeader

setHeader('Content-Type', 'text/html;charset=utf-8')
setHeader('Last-Modified', togmt(now.timeTime()))

#if not anon:
setHeader('Cache-Control', 'no-cache, no-store')
setHeader('Pragma', 'no-cache')
setHeader('Expires', '0')
#else:
#  setHeader('Cache-Control', 'max-age='+ str(cache_time * 3600))
#  setHeader('Expires', togmt(expires.timeTime()))

return None