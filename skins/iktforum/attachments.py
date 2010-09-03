## Script (Python) "attachments.py"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters= assocpsi = None
##title=Get dictionary of attachements related to a topic
##
from Products.ksiktforum import psis

filetypes = { 'application/pdf' : 'pdf'
             ,'application/vnd.ms-excel' : 'excel'
             ,'application/vnd.ms-word' : 'word'
             ,'application/msexcel' : 'excel'
             ,'application/msword' : 'word'
             ,'application/mspowerpoint' : 'powerpoint'
             ,'application/vnd.oasis.opendocument.text' : 'odt'
             ,'application/vnd.oasis.opendocument.spreadsheet' : 'ods'             
             ,'image/png' : 'bilde'
             ,'image/jpeg' : 'bilde'
             ,'image/gif' : 'bilde'
            }

fileicons = { 'excel':'xls'
             ,'pdf':'pdf'
             ,'powerpoint':'ppt'
             ,'word':'doc'
             ,'bilde':'gif'
             ,'odt':'odt'
             ,'ods':'ods'
             ,'fil':'txt'
            }

filenames = { 'excel':'Excel-fil'
             ,'pdf':'PDF-fil'
             ,'word':'Word-fil'
             ,'powerpoint':'Powerpoint-fil'
             ,'bilde':'Bildefil'
             ,'odt':'OpenDocument-fil'
             ,'ods':'OpenDocument regneark-fil'
             ,'fil':'Fil'
            }


relatedattachements = list(context.associatedTopicsQuery(associationtype=psis.attachment, sort='title'))
#raise AssertionError(list(relatedattachements))
attachements = []
append = attachements.append
ft = []
for attachement in relatedattachements:
    if attachement:
        fileobject = attachement.resource_object()
        content_type = fileobject and fileobject.content_type or ""
        
        ft.append(content_type)      
        filetype = filetypes.has_key(content_type) and filetypes[content_type] or "fil"
                
        file_icon = fileicons[filetype]
        file_type = filenames[filetype]
        append({  'attachment' : attachement
                , 'title': attachement.title_or_id()
                , 'url' : attachement.resource_url()
                , 'iconclass' : file_icon
                , 'type': file_type
                })


return attachements
