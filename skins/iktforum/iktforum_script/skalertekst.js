function setActiveStyleSheet(title, reset) {
    
	  if (!W3CDOM){return false};
    var i, a, main;
    for(i=0; (a = document.getElementsByTagName("link")[i]); i++) {
		  if (a.getAttribute("rel").indexOf("style") != -1 && a.getAttribute("title")) {
            a.disabled = true;
            if (a.getAttribute("title") == title) {
                a.disabled = false;
            }
        }
    }
    if (reset == 1) {
        createCookie("wstyle", title, 365);
    }
    return false;
     
};

var bugRiddenCrashPronePieceOfJunk = (
    navigator.userAgent.indexOf('MSIE 5') != -1
    &&
    navigator.userAgent.indexOf('Mac') != -1
)

var W3CDOM = (!bugRiddenCrashPronePieceOfJunk &&
               document.getElementsByTagName &&
               document.createElement);


function setStyle() {    
    var style = readCookie("wstyle");
    if (style != null) {
        setActiveStyleSheet(style, 0);
    }
};
registerPloneFunction(setStyle);

function registerPloneFunction(func) {
     registerEventListener(window, "load", func);
}


function registerEventListener(elem, event, func) {
    if (elem.addEventListener) {
        elem.addEventListener(event, func, false);
        return true;
    } else if (elem.attachEvent) {
        var result = elem.attachEvent("on"+event, func);
        return result;
    }

    return false;
}


function createCookie(name,value,days) {
    if (days) {
        var date = new Date();
        date.setTime(date.getTime()+(days*24*60*60*1000));
        var expires = "; expires="+date.toGMTString();
    } else {
        expires = "";
    }
    document.cookie = name+"="+escape(value)+expires+"; path=/;";
};

function readCookie(name) {
    var nameEQ = name + "=";
    var ca = document.cookie.split(';');
    for(var i=0;i < ca.length;i++) {
        var c = ca[i];
        while (c.charAt(0)==' ') {
            c = c.substring(1,c.length);
        }
        if (c.indexOf(nameEQ) == 0) {
            return unescape(c.substring(nameEQ.length,c.length));
        }
    }
    return null;
};
