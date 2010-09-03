#Returns the value of the startdate-occurrence. Empty if the occurrence is not present
#used for indexing purposes

from Products.ksiktforum import psis
startdate = context.getOccurrenceValue(psis.startdate, ignore=True, default=None)
if startdate:
    startdate =  context.ZopeTime(startdate) 
return startdate
