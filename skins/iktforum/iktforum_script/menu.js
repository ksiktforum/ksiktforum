startList = function() {
	if (document.all&&document.getElementById) {
		navRoot = document.getElementById("midmenu");
		/*alert(navRoot);*/
		for (i=0; i<navRoot.childNodes.length; i++) {
			node = navRoot.childNodes[i];
			if (node.nodeName=="LI") {
				node.onmouseover=function() {
					/*alert("mouseover");*/
					this.className+=" over";
				}
			  node.onmouseout=function() {
				  /*alert("ikke");*/
				  this.className=this.className.replace(" over", "");
		  	  }
	   	}
  		}
 	}
}
window.onload = startList;