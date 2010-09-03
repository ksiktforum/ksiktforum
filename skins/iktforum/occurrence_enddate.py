#Returns the value of the endadate-occurrence. Empty if the occurrence is not present
#used for indexing purposes

from Products.ksiktforum import psis
enddate = context.getOccurrenceValue(psis.enddate, ignore=True, default=None)
if enddate:
    enddate =  context.ZopeTime(enddate) 
return enddate
