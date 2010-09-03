var IKTforum = {};
IKTforum.UI = {};
IKTforum.Event = {};
IKTforum.DOM = {};

 
/*
Event handling
*/
IKTforum.Event.attachEventHandler = function(obj, eventType, eventHandler){  
  if(obj.attachEvent){       
    obj.attachEvent(eventType, eventHandler);
  }
  else if(obj.addEventListener){  
    obj.addEventListener(eventType.substr(2), eventHandler, false);      
  }
};


IKTforum.DOM.getElementsByTagAndClassName = function (tagName, className, parent) {    
    if (typeof(tagName) == 'undefined' || tagName === null) {
      tagName = '*';
    }
    if (typeof(parent) == 'undefined' || parent === null) {
      parent = document;
    }        
    var children = (parent.getElementsByTagName(tagName) || self._document.all);        
    var elements = [];
    for (var i = 0; i < children.length; i++) {
      var child = children[i];
      var cls = child.className;
      if (!cls) {
        continue;
      }
      var classNames = cls.split(' ');
      for (var j = 0; j < classNames.length; j++) {
        if (classNames[j] == className) {
            elements.push(child);
            break;
        }
      }
    }
    return elements;
  };
IKTforum.DOM.addElementClass = function (obj, className) {
        var cls = obj.className;
        // trivial case, no className yet
        if (cls === undefined || cls.length === 0) {
            obj.className = className;
            return true;
        }
        // the other trivial case, already set as the only class
        if (cls == className) {
            return false;
        }
        var classes = cls.split(" ");
        for (var i = 0; i < classes.length; i++) {
            // already present
            if (classes[i] == className) {
                return false;
            }
        }
        // append class
        obj.className = cls + " " + className;
        return true;
    };

    
IKTforum.DOM.removeElementClass = function (obj, className) {
        var cls = obj.className;
        // trivial case, no className yet
        if (cls === undefined || cls.length === 0) {
            return false;
        }        
        var classes = cls.split(" ");
        for (var i = 0; i < classes.length; i++) {
            // already present
            if (classes[i] == className) {
                // only check sane case where the class is used once
                classes.splice(i, 1);
                obj.className =  classes.join(" ");
                return true;
            }
        }
        // not found
        return false;
    };

IKTforum.DOM.hasElementClass =  function (obj, className/*...*/) {
        var classes = obj.className.split(" ");
        for (var i = 1; i < arguments.length; i++) {
            var good = false;
            for (var j = 0; j < classes.length; j++) {
                if (classes[j] == arguments[i]) {
                    good = true;
                    break;
                }
            }
            if (!good) {
                return false;
            }
        }
        return true;
    };
    
IKTforum.UI.EnhanceListItems = {};
IKTforum.UI.EnhanceListItems.init = function(){
  var lists = IKTforum.DOM.getElementsByTagAndClassName('ol', 'enhanced');
  for(var i=0,ilength=lists.length; i<ilength;i++){
    var list = lists[i];
    var listitems = list.getElementsByTagName('li');   
    for(var j=0,jlength=listitems.length; j<jlength; j++){      
      var listitem = listitems[j];
      var pNode = listitem.parentNode;       
      if(list == pNode){       
        var links = IKTforum.DOM.getElementsByTagAndClassName('a', 'hideme', listitem);
        if(links.length>0){        
          var link = links[0];
            IKTforum.DOM.addElementClass(link, 'hidden');                
        }        
        IKTforum.Event.attachEventHandler(listitem, 'onclick', IKTforum.UI.EnhanceListItems.onclickHandler);
        IKTforum.Event.attachEventHandler(listitem, 'onmouseover', IKTforum.UI.EnhanceListItems.onMouseoverHandler);
        IKTforum.Event.attachEventHandler(listitem, 'onmouseout', IKTforum.UI.EnhanceListItems.onMouseoutHandler);
      }
    }
  }  
};
IKTforum.UI.EnhanceListItems.onclickHandler = function(e){
  var listElement = e.target || e.srcElement;
  while(listElement.tagName != 'LI'){
    listElement = listElement.parentNode;
  }
  var links = listElement.getElementsByTagName('a');
  if(links){
    var link = links[0];
    location.href = link;    
  }
};
IKTforum.UI.EnhanceListItems.onMouseoverHandler = function(e){  
  var listElement = e.target || e.srcElement;  
  //while(listElement.parentNode.className != 'LI' && IKTforum.DOM.hasElementClass(listElement.parentNode.parentNode, 'enhanced')){
  while(!IKTforum.DOM.hasElementClass(listElement.parentNode, 'contentlisting')){        
    listElement = listElement.parentNode;
  }    
  IKTforum.DOM.addElementClass(listElement, 'enhanced');
  
};
IKTforum.UI.EnhanceListItems.onMouseoutHandler = function(e){
  var listElement = e.target || e.srcElement;
  while(!IKTforum.DOM.hasElementClass(listElement.parentNode, 'contentlisting')){    
    listElement = listElement.parentNode;
  }   
  IKTforum.DOM.removeElementClass(listElement, 'enhanced');
};
IKTforum.UI.InputValueTogglers = {};
IKTforum.UI.InputValueTogglers.init = function(){
  var inputs = IKTforum.DOM.getElementsByTagAndClassName('input', 'toggler');
  for(var i=0,ilength=inputs.length; i<ilength;i++){
    var input = inputs[i];
    IKTforum.Event.attachEventHandler(input, 'onfocus', IKTforum.UI.InputValueTogglers.onfocusHandler);
    IKTforum.Event.attachEventHandler(input, 'onblur', IKTforum.UI.InputValueTogglers.onblurHandler);
  }
};
IKTforum.UI.InputValueTogglers.onfocusHandler = function(e){
  var src = e.target || e.srcElement;  
  if(src.value == src.alt){
    src.value = "";
  }
  
};
IKTforum.UI.InputValueTogglers.onblurHandler = function(e){
  var src = e.target || e.srcElement;
  if(!src.value){
    src.value = src.alt;  
  }  
};
IKTforum.UI.SectionToggler = {};
IKTforum.UI.SectionToggler.init = function(){
  var sections = IKTforum.DOM.getElementsByTagAndClassName('div', 'toggler');
  for(var i=0,ilength=sections.length;i<ilength;i++){
    var section = sections[i];
    IKTforum.DOM.addElementClass(section, 'dn');
    var gpNode = section.parentNode.parentNode;
    var pnode = section.parentNode;
    var openlink = document.createElement('a');
    openlink.section = section;   
    IKTforum.DOM.addElementClass(openlink, 'arrow');
    IKTforum.DOM.addElementClass(openlink, 'arrow_003365');
    IKTforum.DOM.addElementClass(openlink, 'marginbottom');
    IKTforum.DOM.addElementClass(openlink, 'block');
    openlink.innerHTML = section.title;
    pnode.appendChild(openlink);
    pnode.insertBefore(openlink, section);
    IKTforum.Event.attachEventHandler(openlink, 'onclick', IKTforum.UI.SectionToggler.onclickHandler);    
  }  
};
IKTforum.UI.SectionToggler.onclickHandler = function(e){  
  if (!e){ 
    e = window.event;     
    e.cancelBubble = true;
  }
  if (e.stopPropagation){    
    e.stopPropagation();
  } 
  var src = e.target || e.srcElement;

  IKTforum.DOM.addElementClass(src, 'dn');
  IKTforum.DOM.removeElementClass(src, 'block');
  var section = src.section;
  if(section){
    IKTforum.DOM.removeElementClass(section, 'dn');
  }
  return false;
};

(function(i) {var u =navigator.userAgent;var e=/*@cc_on!@*/false; var st =
setTimeout;if(/webkit/i.test(u)){st(function(){var dr=document.readyState;
if(dr=="loaded"||dr=="complete"){i()}else{st(arguments.callee,10);}},10);}
else if((/mozilla/i.test(u)&&!/(compati)/.test(u)) || (/opera/i.test(u))){
document.addEventListener("DOMContentLoaded",i,false); } else if(e){     (
function(){var t=document.createElement('doc:rdy');try{t.doScroll('left');
i();t=null;}catch(e){st(arguments.callee,0);}})();}else{window.onload=i;}})(
  function(){
     IKTforum.UI.EnhanceListItems.init();
     IKTforum.UI.InputValueTogglers.init();
     IKTforum.UI.SectionToggler.init();
  }
)


//registerEventListener(window, "load", IKTforum.UI.EnhanceListItems.init);
//registerEventListener(window, "load", IKTforum.UI.InputValueTogglers.init);
//registerEventListener(window, "load", IKTforum.UI.SectionToggler.init);