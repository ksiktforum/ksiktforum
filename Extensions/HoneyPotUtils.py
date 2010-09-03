# -*- coding: utf-8 -*-

import md5
import DateTime
import random

minumumHumanResponseTime =      3 # The minumum time a human would require to fill in a meaningful komment-form
maximumHumanResponseTime =   3600 # The maximum time a human would require to fill in a komment-form
 
 
spinnersecret = "One ping to rule them all" # This is the secret key that is used when creating the spinner value
fieldnamesecret = "and in the dampness bind them" # This is the secret that is used when hashing the fieldnames



def getHashedFieldName(spinnervalue,fieldname):
    """Internal utilityfunction for generating a hashed version of a fieldname.
    """
    ## Note that we must ensure that the fieldname starts with a letter, since it is not legal to have
    ## "for"-attributes in "label"-elements start with anything but a letter.
    return "X" + md5.new( "%s%s%s" % (fieldnamesecret,spinnervalue,fieldname) ).hexdigest()


def getSpinnerValue(timestamp  # the timestamp of when the webpage was served
                    ,ipaddress  # the ipaddress of the client
                    ,entryid    # something that identifies the context of the form. For instance the tm_serial 
                                # of an article that the user is commenting on (via the form where the honeypots are placed)
                    ):
    """internal utilityfunction"
    """
    return md5.new( "%s%s%s%s" % (spinnersecret,timestamp,ipaddress,entryid) ).hexdigest()


def getHoneyPots( timestamp  # the timestamp of when the webpage was served
                    ,ipaddress  # the ipaddress of the client
                    ,entryid    # something that identifies the context of the form. For instance the tm_serial 
                            
                    ,fieldnamesAndCssClasses # A list of (fieldname,cssclass)-tuples. This describes the real fields in the form.
                    ,invisiblecssclasses # The classes to use for the honeypot fiels fields
                    ):
    """This -function is used by forms that want to protect themselves agains spambots.
    
    It works like this: The form contains the following hidden fields:
      timestamp: Contains the time when the webpage was served.
      ipaddress: The ipaddress of the client the webpage was served to.
      entryid:   A value that identifies the context the webpage is related to (For instance an article).
      spinnervalue: An md5-generated hash based on the other three fields and a secret string (stored in the 
                    "spinnersecret" variable in this module.)

      The names of the formal fields (for instance name, email, etc) are encrypted using the spinnervalue and
      another secret string (stored in the "fieldnamesecret" variable in this module). For each real field,
      a number of "honeypot" fields are also created.
      
      
      When the user posts the form, the receiving script calls the checkHoneyPots function to check
      that none of the honeypot fields have been filled.


    """
    spinnervalue = getSpinnerValue(timestamp,ipaddress,entryid)
    
    ## create mappings between the fieldnames and cssstyles and their hashed versions.
    fieldname2hashedfieldname = {}
    hashedfieldname2fieldname = {}
    fieldinfolists = {}
    for fieldname,cssclass in fieldnamesAndCssClasses:
        hashedfieldname = getHashedFieldName(spinnervalue,fieldname)
        fieldname2hashedfieldname[fieldname] = hashedfieldname
        hashedfieldname2fieldname[hashedfieldname] = fieldname

        honeyfieldname = "honeypot_%s" % (fieldname,)
        hashedhoneyfieldname = getHashedFieldName(spinnervalue,honeyfieldname)
        fieldname2hashedfieldname[honeyfieldname] = hashedhoneyfieldname
        hashedfieldname2fieldname[hashedhoneyfieldname] = honeyfieldname
        if invisiblecssclasses:
            ## The user wants the fieldinfo list
            fieldinfolist = [ 
                              ## The real field
                              {"name" : hashedfieldname,
                               "unhashedname" : fieldname,
                               "class": cssclass,
                               "labelclass": "",
                               "ishoneypot":False,
                               },
                              
                              ## The honeypot field
                              {"name" : hashedhoneyfieldname,
                               "unhashedname" : honeyfieldname,
                               "class": random.choice(invisiblecssclasses),
                               "labelclass": random.choice(invisiblecssclasses),
                               "labeltext" : u"Ikke skriv noe i dette feltet",
                               "ishoneypot" : True,
                               }, 
                            ]
        
            random.shuffle(fieldinfolist) # randomize the order of the real field and the honeypot fields
            fieldinfolists[fieldname] = fieldinfolist
    
    ## Add mappings for the hashed version of the standard fields
    for fieldname in ("timestamp","ipaddress","entryid"):
        hashedfieldname = getHashedFieldName(spinnervalue,fieldname)
        fieldname2hashedfieldname[fieldname] = hashedfieldname
        hashedfieldname2fieldname[hashedfieldname] = fieldname        
    
    return {
            "spinnervalue" : spinnervalue,
            "fieldname2hashedfieldname" : fieldname2hashedfieldname,
            "hashedfieldname2fieldname" : hashedfieldname2fieldname,
            "fieldinfolists": fieldinfolists,
            
           }
    
    
       
       



def checkHoneyPots(context,fieldnames):
    """This functions checks that the anti-spambot honeypots looks clean.
    
    returns: A tuple of the honeypot-info (as returned by the getHoneyPots()-funciton) and an error-message string.
             The errorm-message string will be empty if all is well. Otherwise a if will contain a human-readable 
             errormessage. 
             
             
      When the form with the honeypot fields is submitted, the receiving script will call this function
      to check that the honeypots are empty.
      A number of checks are done:
        * The spinnervalue is re-calculated based on the form-data in the http-request and checked to see if
          it matches the spinnervalue in the form-data. 
          
        * The timestamp in the formdata is checked to make sure that it isn't too recent or too old. If
          it is too recent, it probably means that the form was submitted by a (inhumanly fast) spambot.
          If it is too old, it was probably submittet by a spambot using stored form-data.
          
        * The honeypot-fields are checked to see if they contain any data. If they do, we know that the
          form was submitted by a spambot.             
          
          
          
        TODO: Add support for record-type fieldnames (name="commentform.email:record"). 
    """
    formErrorMsg = ""    
    honeypots = None
    
    ## First use the spinnervalue in the request to calculate the hashed names of the "timestamp", 
    ## "ipaddress" and "entryid" fields and check that they exist. If they don't it probably means
    ## that the spinnervalue has been tampered with.
    spinnervalue = context.REQUEST.spinnervalue
    (hashedtimestampFieldname, hashedipaddressFieldname ,hashedentryidFieldname) = [getHashedFieldName(spinnervalue,fieldname) for fieldname in ("timestamp","ipaddress","entryid")]
    for requiredfieldname in  (hashedtimestampFieldname, hashedipaddressFieldname ,hashedentryidFieldname):
        if not requiredfieldname in context.REQUEST:
            formErrorMsg = u"SPAMMER! required field %s not found. Either the field is missing, or the spinnervalue has been tampered with." % (requiredfieldname,)
        
    if not formErrorMsg:
        ## Recalculate the spinnervalue to check that none of the fields have been tampered with
        timestamp = context.REQUEST[hashedtimestampFieldname]
        ipaddress = context.REQUEST[hashedipaddressFieldname]
        entryid   = context.REQUEST[hashedentryidFieldname]
        fieldnamesAndCssClasses = [(fieldname,"") for fieldname in fieldnames] ## When the getHoneyPots is called from the page that renders the form, 
                                                                               ## the css-classes are required. We just need dummies here.
        honeypots = context.getHoneyPots(timestamp,ipaddress, entryid,
                                                    fieldnamesAndCssClasses,
                                                       ("",),
                                                      )

    ## Check that the spinner hasn't been tampered with.
    if not formErrorMsg:
        if context.REQUEST.spinnervalue != honeypots['spinnervalue']:
            formErrorMsg = u"SPAMMER! (context.REQUEST.spinnervalue(%s) != honeypots['spinnervalue'](%s))" % (context.REQUEST.spinnervalue, honeypots['spinnervalue'])
   

    ## Check that the ipaddress stored in the form-data matches the ipaddress of the current client
    if not formErrorMsg:
        if context.REQUEST.getClientAddr() != ipaddress:
            formErrorMsg = u"SPAMMER! (context.REQUEST.getClientAddr() != context.REQUEST.ipaddress)"
    
    ## Check that the request refers to the correct context
    if not formErrorMsg:
        ## Check that the entryid in the formdata matches the id of the current context
        if str(context.tm_serial) != entryid:
            formErrorMsg =  u"SPAMMER! (context.REQUEST.entryid(%s) != context.tm_serial(%s))" % (context.REQUEST.entryid,context.tm_serial)
    
    
    if not formErrorMsg:
        ## Check that the timestamp:
        ## * isn't in the future.  (which shouldn't be possible, unless the system clock has been modified recently, or someone has cracked the encryption).
        ## * isn't too close to the present.  (which could indicate a spam-bot reading the formpage and immediately posting a reply)
        ## * isn't too far in the pasat. (which could indicate a spambot using stored form-data)
        currentTime = DateTime.DateTime().timeTime()
        formTimeStamp = DateTime.DateTime(timestamp).timeTime()
        
        if (currentTime-formTimeStamp) < minumumHumanResponseTime:
            ## This could also happen to a legitimate human user, so we must write a friendly response here
            #formErrorMsg = u"SPAMMER! (currentTime-formTimeStamp)(%s) < minumumHumanResponseTime(%s)" % (currentTime-formTimeStamp, minumumHumanResponseTime)
            formErrorMsg = u"Systemet synes at du fylte inn skjemaet og postet det for raskt (Hvis du bruker for liten tid vil systemet tro at du er en spam-bot). Vent noen sekunder og prøv igjen."        
        elif (currentTime-formTimeStamp) > maximumHumanResponseTime:
            ## This could also happen to a legitimate human user, so we must write a friendly response here.
            #formErrorMsg =  u"SPAMMER! (currentTime-formTimeStamp)(%s) > maximumHumanResponseTime(%s)" % (currentTime-formTimeStamp, maximumHumanResponseTime)
            formErrorMsg = u"Systemet synes at du brukte for lang tid til å fylle inn skjemaet og poste det (Hvis du bruker for lang tid vil systemet tro at du er en spam-bot.). Vent noen sekunder og prøv igjen."        
       
    if not formErrorMsg: 
        ## check that all the honeypot fields are empty
        for fieldname,hashedfieldname in honeypots['fieldname2hashedfieldname'].items():
            if fieldname.startswith("honeypot_"):
                if context.REQUEST.get(hashedfieldname) != "":
                    formErrorMsg =  u"SPAMMER! The honeypot field %s(%s) contains data!" % (hashedfieldname,fieldname) 
                    break

    return (honeypots,formErrorMsg)
    
    