var workarea = function(){
    var $ = jQuery
    function initialize(){
      $('#newfile_add_to_queue').bind('click', addFileToUploadQueue);
      $('#existing_file').bind('change', addExistingFileToQueue);
      var id = this.location.hash
      if(id){
        $(id).hide().fadeIn("200");
      }
      
    }    
    
    function addFileToUploadQueue(event){
      event.preventDefault();
      
      var newFileTitle = $("#fileupload #filetitle");
      var newFile = $("#fileupload #newfile");
      
      //validation - must have filename and file
      //TODO: add validation engine      
      if(!validateRequiredValue(newFileTitle, "You must supply a file title")){
        return
      }
      if(!validateRequiredValue(newFile, "You must supply a file")){
        return
      }     
      
      var randomID = Math.floor(Math.random()*1000)           
      newFileTitle.attr('id','nft_'+randomID);
      newFileTitle.addClass("none")
      newFileTitle.after('<input id="filetitle" type="text" name="filetitle:ustring:utf8:list" />')
      
      
      newFile.attr('id', 'nfc_'+randomID);   
      newFile.addClass("none")
      newFile.after('<input id="newfile" type="file" class="file_upload" name="newfile:list" />')
      
       //add to visual upload queue in file-table
      fileTable = $('table#focused');      
      //queueRow = $('<tr class="queued"><td>'+newFileTitle.attr('value')+'</td><td>'+newFile.attr('value')+'</td><td></td></tr>')
      queueRow = $('<tr class="queued"><td>'+newFileTitle.attr('value')+'</td><td></td></tr>')
      queueRow.attr('id', 'qr_'+randomID)
      fileTable.append(queueRow);
      removeFromQueue = $('<a class="icon_small delete" href="#">Remove</a>')
      removeFromQueue.bind('click', function(event){        
        event.preventDefault();                 
        $('#nft_'+randomID).remove();
        $('#nfc_'+randomID).remove();
        $('#qr_'+randomID).remove();
      })
      lastCell = $('td:last', queueRow).append(removeFromQueue);
      //reset input fields
      //newFileTitle.attr('value', '');
      //newFile.attr('value', '');
    }
    function addExistingFileToQueue(event){
      event.preventDefault();           
      var value = this.value;      
      var title = this.options[this.selectedIndex].text;
      
      if(value=='0'){
        return
      }
      
      var uploadqueueContainer = $("#uploadqueue_container");    
      
      var inputField = '<input name="added_existing_files:int:list" type="hidden" value="'+value+'" id="nft_'+value+'">'
      uploadqueueContainer.append(inputField);
      
       //add to visual upload queue in file-table
       var fileTable = $('table#focused');      
       //var queueRow = $('<tr class="queued"><td>'+title+'</td><td></td><td></td></tr>')
       var queueRow = $('<tr class="queued"><td>'+title+'</td><td></td></tr>')
       queueRow.attr('id', 'qr_'+value)
       fileTable.append(queueRow);
       var removeFromQueue = $('<a class="icon_small delete" href="#">Remove</a>')
       removeFromQueue.bind('click', function(event){
        
        event.preventDefault();                 
        $('#nft_'+value).remove();
        $('#qr_'+value).remove();      
        var existing_file = $('#existing_file')[0];
        
        for(var i=0, ilength=existing_file.options.length; i<ilength; i++){   
          elementValue = existing_file.options[i].value;
          
          if(value == elementValue){            
            existing_file.options[i].disabled = false;
          }
        }
        })
        lastCell = $('td:last', queueRow).append(removeFromQueue);
    
      //Disable option
      this.options[this.selectedIndex].disabled = true;
      
      //reset input fields
      this.selectedIndex = 0;     
    
    }
    function validateRequiredValue(obj, errorsmsg){
       //TODO: give better feedback rather than an alert box
       if(!obj.attr('value')){
         alert(errorsmsg);
         return false;
       }
       else{
         return true;
       }      
    }
    
    // return public pointers to the private methods and 
    // properties you want to reveal
    return {
        'initialize':initialize        
    }
}();

$(document).ready(workarea.initialize);





