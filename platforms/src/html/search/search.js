function convertToId(search)
***REMOVED***
  var result = '';
  for (i=0;i<search.length;i++)
  ***REMOVED***
    var c = search.charAt(i);
    var cn = c.charCodeAt(0);
    if (c.match(/[a-z0-9\u0080-\uFFFF]/))
    ***REMOVED***
      result+=c;
    ***REMOVED***
    else if (cn<16)
    ***REMOVED***
      result+="_0"+cn.toString(16);
    ***REMOVED***
    else
    ***REMOVED***
      result+="_"+cn.toString(16);
    ***REMOVED***
  ***REMOVED***
  return result;
***REMOVED***

function getXPos(item)
***REMOVED***
  var x = 0;
  if (item.offsetWidth)
  ***REMOVED***
    while (item && item!=document.body)
    ***REMOVED***
      x   += item.offsetLeft;
      item = item.offsetParent;
    ***REMOVED***
  ***REMOVED***
  return x;
***REMOVED***

function getYPos(item)
***REMOVED***
  var y = 0;
  if (item.offsetWidth)
  ***REMOVED***
     while (item && item!=document.body)
     ***REMOVED***
       y   += item.offsetTop;
       item = item.offsetParent;
     ***REMOVED***
  ***REMOVED***
  return y;
***REMOVED***

/* A class handling everything associated with the search panel.

   Parameters:
   name - The name of the global variable that will be
          storing this instance.  Is needed to be able to set timeouts.
   resultPath - path to use for external files
*/
function SearchBox(name, resultsPath, inFrame, label)
***REMOVED***
  if (!name || !resultsPath) ***REMOVED***  alert("Missing parameters to SearchBox."); ***REMOVED***

  // ---------- Instance variables
  this.name                  = name;
  this.resultsPath           = resultsPath;
  this.keyTimeout            = 0;
  this.keyTimeoutLength      = 500;
  this.closeSelectionTimeout = 300;
  this.lastSearchValue       = "";
  this.lastResultsPage       = "";
  this.hideTimeout           = 0;
  this.searchIndex           = 0;
  this.searchActive          = false;
  this.insideFrame           = inFrame;
  this.searchLabel           = label;

  // ----------- DOM Elements

  this.DOMSearchField = function()
  ***REMOVED***  return document.getElementById("MSearchField");  ***REMOVED***

  this.DOMSearchSelect = function()
  ***REMOVED***  return document.getElementById("MSearchSelect");  ***REMOVED***

  this.DOMSearchSelectWindow = function()
  ***REMOVED***  return document.getElementById("MSearchSelectWindow");  ***REMOVED***

  this.DOMPopupSearchResults = function()
  ***REMOVED***  return document.getElementById("MSearchResults");  ***REMOVED***

  this.DOMPopupSearchResultsWindow = function()
  ***REMOVED***  return document.getElementById("MSearchResultsWindow");  ***REMOVED***

  this.DOMSearchClose = function()
  ***REMOVED***  return document.getElementById("MSearchClose"); ***REMOVED***

  this.DOMSearchBox = function()
  ***REMOVED***  return document.getElementById("MSearchBox");  ***REMOVED***

  // ------------ Event Handlers

  // Called when focus is added or removed from the search field.
  this.OnSearchFieldFocus = function(isActive)
  ***REMOVED***
    this.Activate(isActive);
  ***REMOVED***

  this.OnSearchSelectShow = function()
  ***REMOVED***
    var searchSelectWindow = this.DOMSearchSelectWindow();
    var searchField        = this.DOMSearchSelect();

    if (this.insideFrame)
    ***REMOVED***
      var left = getXPos(searchField);
      var top  = getYPos(searchField);
      left += searchField.offsetWidth + 6;
      top += searchField.offsetHeight;

      // show search selection popup
      searchSelectWindow.style.display='block';
      left -= searchSelectWindow.offsetWidth;
      searchSelectWindow.style.left =  left + 'px';
      searchSelectWindow.style.top  =  top  + 'px';
    ***REMOVED***
    else
    ***REMOVED***
      var left = getXPos(searchField);
      var top  = getYPos(searchField);
      top += searchField.offsetHeight;

      // show search selection popup
      searchSelectWindow.style.display='block';
      searchSelectWindow.style.left =  left + 'px';
      searchSelectWindow.style.top  =  top  + 'px';
    ***REMOVED***

    // stop selection hide timer
    if (this.hideTimeout)
    ***REMOVED***
      clearTimeout(this.hideTimeout);
      this.hideTimeout=0;
    ***REMOVED***
    return false; // to avoid "image drag" default event
  ***REMOVED***

  this.OnSearchSelectHide = function()
  ***REMOVED***
    this.hideTimeout = setTimeout(this.name +".CloseSelectionWindow()",
                                  this.closeSelectionTimeout);
  ***REMOVED***

  // Called when the content of the search field is changed.
  this.OnSearchFieldChange = function(evt)
  ***REMOVED***
    if (this.keyTimeout) // kill running timer
    ***REMOVED***
      clearTimeout(this.keyTimeout);
      this.keyTimeout = 0;
    ***REMOVED***

    var e  = (evt) ? evt : window.event; // for IE
    if (e.keyCode==40 || e.keyCode==13)
    ***REMOVED***
      if (e.shiftKey==1)
      ***REMOVED***
        this.OnSearchSelectShow();
        var win=this.DOMSearchSelectWindow();
        for (i=0;i<win.childNodes.length;i++)
        ***REMOVED***
          var child = win.childNodes[i]; // get span within a
          if (child.className=='SelectItem')
          ***REMOVED***
            child.focus();
            return;
          ***REMOVED***
        ***REMOVED***
        return;
      ***REMOVED***
      else if (window.frames.MSearchResults.searchResults)
      ***REMOVED***
        var elem = window.frames.MSearchResults.searchResults.NavNext(0);
        if (elem) elem.focus();
      ***REMOVED***
    ***REMOVED***
    else if (e.keyCode==27) // Escape out of the search field
    ***REMOVED***
      this.DOMSearchField().blur();
      this.DOMPopupSearchResultsWindow().style.display = 'none';
      this.DOMSearchClose().style.display = 'none';
      this.lastSearchValue = '';
      this.Activate(false);
      return;
    ***REMOVED***

    // strip whitespaces
    var searchValue = this.DOMSearchField().value.replace(/ +/g, "");

    if (searchValue != this.lastSearchValue) // search value has changed
    ***REMOVED***
      if (searchValue != "") // non-empty search
      ***REMOVED***
        // set timer for search update
        this.keyTimeout = setTimeout(this.name + '.Search()',
                                     this.keyTimeoutLength);
      ***REMOVED***
      else // empty search field
      ***REMOVED***
        this.DOMPopupSearchResultsWindow().style.display = 'none';
        this.DOMSearchClose().style.display = 'none';
        this.lastSearchValue = '';
      ***REMOVED***
    ***REMOVED***
  ***REMOVED***

  this.SelectItemCount = function(id)
  ***REMOVED***
    var count=0;
    var win=this.DOMSearchSelectWindow();
    for (i=0;i<win.childNodes.length;i++)
    ***REMOVED***
      var child = win.childNodes[i]; // get span within a
      if (child.className=='SelectItem')
      ***REMOVED***
        count++;
      ***REMOVED***
    ***REMOVED***
    return count;
  ***REMOVED***

  this.SelectItemSet = function(id)
  ***REMOVED***
    var i,j=0;
    var win=this.DOMSearchSelectWindow();
    for (i=0;i<win.childNodes.length;i++)
    ***REMOVED***
      var child = win.childNodes[i]; // get span within a
      if (child.className=='SelectItem')
      ***REMOVED***
        var node = child.firstChild;
        if (j==id)
        ***REMOVED***
          node.innerHTML='&#8226;';
        ***REMOVED***
        else
        ***REMOVED***
          node.innerHTML='&#160;';
        ***REMOVED***
        j++;
      ***REMOVED***
    ***REMOVED***
  ***REMOVED***

  // Called when an search filter selection is made.
  // set item with index id as the active item
  this.OnSelectItem = function(id)
  ***REMOVED***
    this.searchIndex = id;
    this.SelectItemSet(id);
    var searchValue = this.DOMSearchField().value.replace(/ +/g, "");
    if (searchValue!="" && this.searchActive) // something was found -> do a search
    ***REMOVED***
      this.Search();
    ***REMOVED***
  ***REMOVED***

  this.OnSearchSelectKey = function(evt)
  ***REMOVED***
    var e = (evt) ? evt : window.event; // for IE
    if (e.keyCode==40 && this.searchIndex<this.SelectItemCount()) // Down
    ***REMOVED***
      this.searchIndex++;
      this.OnSelectItem(this.searchIndex);
    ***REMOVED***
    else if (e.keyCode==38 && this.searchIndex>0) // Up
    ***REMOVED***
      this.searchIndex--;
      this.OnSelectItem(this.searchIndex);
    ***REMOVED***
    else if (e.keyCode==13 || e.keyCode==27)
    ***REMOVED***
      this.OnSelectItem(this.searchIndex);
      this.CloseSelectionWindow();
      this.DOMSearchField().focus();
    ***REMOVED***
    return false;
  ***REMOVED***

  // --------- Actions

  // Closes the results window.
  this.CloseResultsWindow = function()
  ***REMOVED***
    this.DOMPopupSearchResultsWindow().style.display = 'none';
    this.DOMSearchClose().style.display = 'none';
    this.Activate(false);
  ***REMOVED***

  this.CloseSelectionWindow = function()
  ***REMOVED***
    this.DOMSearchSelectWindow().style.display = 'none';
  ***REMOVED***

  // Performs a search.
  this.Search = function()
  ***REMOVED***
    this.keyTimeout = 0;

    // strip leading whitespace
    var searchValue = this.DOMSearchField().value.replace(/^ +/, "");

    var code = searchValue.toLowerCase().charCodeAt(0);
    var idxChar = searchValue.substr(0, 1).toLowerCase();
    if ( 0xD800 <= code && code <= 0xDBFF && searchValue > 1) // surrogate pair
    ***REMOVED***
      idxChar = searchValue.substr(0, 2);
    ***REMOVED***

    var resultsPage;
    var resultsPageWithSearch;
    var hasResultsPage;

    var idx = indexSectionsWithContent[this.searchIndex].indexOf(idxChar);
    if (idx!=-1)
    ***REMOVED***
       var hexCode=idx.toString(16);
       resultsPage = this.resultsPath + '/' + indexSectionNames[this.searchIndex] + '_' + hexCode + '.html';
       resultsPageWithSearch = resultsPage+'?'+escape(searchValue);
       hasResultsPage = true;
    ***REMOVED***
    else // nothing available for this search term
    ***REMOVED***
       resultsPage = this.resultsPath + '/nomatches.html';
       resultsPageWithSearch = resultsPage;
       hasResultsPage = false;
    ***REMOVED***

    window.frames.MSearchResults.location = resultsPageWithSearch;
    var domPopupSearchResultsWindow = this.DOMPopupSearchResultsWindow();

    if (domPopupSearchResultsWindow.style.display!='block')
    ***REMOVED***
       var domSearchBox = this.DOMSearchBox();
       this.DOMSearchClose().style.display = 'inline';
       if (this.insideFrame)
       ***REMOVED***
         var domPopupSearchResults = this.DOMPopupSearchResults();
         domPopupSearchResultsWindow.style.position = 'relative';
         domPopupSearchResultsWindow.style.display  = 'block';
         var width = document.body.clientWidth - 8; // the -8 is for IE :-(
         domPopupSearchResultsWindow.style.width    = width + 'px';
         domPopupSearchResults.style.width          = width + 'px';
       ***REMOVED***
       else
       ***REMOVED***
         var domPopupSearchResults = this.DOMPopupSearchResults();
         var left = getXPos(domSearchBox) + 150; // domSearchBox.offsetWidth;
         var top  = getYPos(domSearchBox) + 20;  // domSearchBox.offsetHeight + 1;
         domPopupSearchResultsWindow.style.display = 'block';
         left -= domPopupSearchResults.offsetWidth;
         domPopupSearchResultsWindow.style.top     = top  + 'px';
         domPopupSearchResultsWindow.style.left    = left + 'px';
       ***REMOVED***
    ***REMOVED***

    this.lastSearchValue = searchValue;
    this.lastResultsPage = resultsPage;
  ***REMOVED***

  // -------- Activation Functions

  // Activates or deactivates the search panel, resetting things to
  // their default values if necessary.
  this.Activate = function(isActive)
  ***REMOVED***
    if (isActive || // open it
        this.DOMPopupSearchResultsWindow().style.display == 'block'
       )
    ***REMOVED***
      this.DOMSearchBox().className = 'MSearchBoxActive';

      var searchField = this.DOMSearchField();

      if (searchField.value == this.searchLabel) // clear "Search" term upon entry
      ***REMOVED***
        searchField.value = '';
        this.searchActive = true;
      ***REMOVED***
    ***REMOVED***
    else if (!isActive) // directly remove the panel
    ***REMOVED***
      this.DOMSearchBox().className = 'MSearchBoxInactive';
      this.DOMSearchField().value   = this.searchLabel;
      this.searchActive             = false;
      this.lastSearchValue          = ''
      this.lastResultsPage          = '';
    ***REMOVED***
  ***REMOVED***
***REMOVED***

// -----------------------------------------------------------------------

// The class that handles everything on the search results page.
function SearchResults(name)
***REMOVED***
    // The number of matches from the last run of <Search()>.
    this.lastMatchCount = 0;
    this.lastKey = 0;
    this.repeatOn = false;

    // Toggles the visibility of the passed element ID.
    this.FindChildElement = function(id)
    ***REMOVED***
      var parentElement = document.getElementById(id);
      var element = parentElement.firstChild;

      while (element && element!=parentElement)
      ***REMOVED***
        if (element.nodeName == 'DIV' && element.className == 'SRChildren')
        ***REMOVED***
          return element;
        ***REMOVED***

        if (element.nodeName == 'DIV' && element.hasChildNodes())
        ***REMOVED***
           element = element.firstChild;
        ***REMOVED***
        else if (element.nextSibling)
        ***REMOVED***
           element = element.nextSibling;
        ***REMOVED***
        else
        ***REMOVED***
          do
          ***REMOVED***
            element = element.parentNode;
          ***REMOVED***
          while (element && element!=parentElement && !element.nextSibling);

          if (element && element!=parentElement)
          ***REMOVED***
            element = element.nextSibling;
          ***REMOVED***
        ***REMOVED***
      ***REMOVED***
    ***REMOVED***

    this.Toggle = function(id)
    ***REMOVED***
      var element = this.FindChildElement(id);
      if (element)
      ***REMOVED***
        if (element.style.display == 'block')
        ***REMOVED***
          element.style.display = 'none';
        ***REMOVED***
        else
        ***REMOVED***
          element.style.display = 'block';
        ***REMOVED***
      ***REMOVED***
    ***REMOVED***

    // Searches for the passed string.  If there is no parameter,
    // it takes it from the URL query.
    //
    // Always returns true, since other documents may try to call it
    // and that may or may not be possible.
    this.Search = function(search)
    ***REMOVED***
      if (!search) // get search word from URL
      ***REMOVED***
        search = window.location.search;
        search = search.substring(1);  // Remove the leading '?'
        search = unescape(search);
      ***REMOVED***

      search = search.replace(/^ +/, ""); // strip leading spaces
      search = search.replace(/ +$/, ""); // strip trailing spaces
      search = search.toLowerCase();
      search = convertToId(search);

      var resultRows = document.getElementsByTagName("div");
      var matches = 0;

      var i = 0;
      while (i < resultRows.length)
      ***REMOVED***
        var row = resultRows.item(i);
        if (row.className == "SRResult")
        ***REMOVED***
          var rowMatchName = row.id.toLowerCase();
          rowMatchName = rowMatchName.replace(/^sr\d*_/, ''); // strip 'sr123_'

          if (search.length<=rowMatchName.length &&
             rowMatchName.substr(0, search.length)==search)
          ***REMOVED***
            row.style.display = 'block';
            matches++;
          ***REMOVED***
          else
          ***REMOVED***
            row.style.display = 'none';
          ***REMOVED***
        ***REMOVED***
        i++;
      ***REMOVED***
      document.getElementById("Searching").style.display='none';
      if (matches == 0) // no results
      ***REMOVED***
        document.getElementById("NoMatches").style.display='block';
      ***REMOVED***
      else // at least one result
      ***REMOVED***
        document.getElementById("NoMatches").style.display='none';
      ***REMOVED***
      this.lastMatchCount = matches;
      return true;
    ***REMOVED***

    // return the first item with index index or higher that is visible
    this.NavNext = function(index)
    ***REMOVED***
      var focusItem;
      while (1)
      ***REMOVED***
        var focusName = 'Item'+index;
        focusItem = document.getElementById(focusName);
        if (focusItem && focusItem.parentNode.parentNode.style.display=='block')
        ***REMOVED***
          break;
        ***REMOVED***
        else if (!focusItem) // last element
        ***REMOVED***
          break;
        ***REMOVED***
        focusItem=null;
        index++;
      ***REMOVED***
      return focusItem;
    ***REMOVED***

    this.NavPrev = function(index)
    ***REMOVED***
      var focusItem;
      while (1)
      ***REMOVED***
        var focusName = 'Item'+index;
        focusItem = document.getElementById(focusName);
        if (focusItem && focusItem.parentNode.parentNode.style.display=='block')
        ***REMOVED***
          break;
        ***REMOVED***
        else if (!focusItem) // last element
        ***REMOVED***
          break;
        ***REMOVED***
        focusItem=null;
        index--;
      ***REMOVED***
      return focusItem;
    ***REMOVED***

    this.ProcessKeys = function(e)
    ***REMOVED***
      if (e.type == "keydown")
      ***REMOVED***
        this.repeatOn = false;
        this.lastKey = e.keyCode;
      ***REMOVED***
      else if (e.type == "keypress")
      ***REMOVED***
        if (!this.repeatOn)
        ***REMOVED***
          if (this.lastKey) this.repeatOn = true;
          return false; // ignore first keypress after keydown
        ***REMOVED***
      ***REMOVED***
      else if (e.type == "keyup")
      ***REMOVED***
        this.lastKey = 0;
        this.repeatOn = false;
      ***REMOVED***
      return this.lastKey!=0;
    ***REMOVED***

    this.Nav = function(evt,itemIndex)
    ***REMOVED***
      var e  = (evt) ? evt : window.event; // for IE
      if (e.keyCode==13) return true;
      if (!this.ProcessKeys(e)) return false;

      if (this.lastKey==38) // Up
      ***REMOVED***
        var newIndex = itemIndex-1;
        var focusItem = this.NavPrev(newIndex);
        if (focusItem)
        ***REMOVED***
          var child = this.FindChildElement(focusItem.parentNode.parentNode.id);
          if (child && child.style.display == 'block') // children visible
          ***REMOVED***
            var n=0;
            var tmpElem;
            while (1) // search for last child
            ***REMOVED***
              tmpElem = document.getElementById('Item'+newIndex+'_c'+n);
              if (tmpElem)
              ***REMOVED***
                focusItem = tmpElem;
              ***REMOVED***
              else // found it!
              ***REMOVED***
                break;
              ***REMOVED***
              n++;
            ***REMOVED***
          ***REMOVED***
        ***REMOVED***
        if (focusItem)
        ***REMOVED***
          focusItem.focus();
        ***REMOVED***
        else // return focus to search field
        ***REMOVED***
           parent.document.getElementById("MSearchField").focus();
        ***REMOVED***
      ***REMOVED***
      else if (this.lastKey==40) // Down
      ***REMOVED***
        var newIndex = itemIndex+1;
        var focusItem;
        var item = document.getElementById('Item'+itemIndex);
        var elem = this.FindChildElement(item.parentNode.parentNode.id);
        if (elem && elem.style.display == 'block') // children visible
        ***REMOVED***
          focusItem = document.getElementById('Item'+itemIndex+'_c0');
        ***REMOVED***
        if (!focusItem) focusItem = this.NavNext(newIndex);
        if (focusItem)  focusItem.focus();
      ***REMOVED***
      else if (this.lastKey==39) // Right
      ***REMOVED***
        var item = document.getElementById('Item'+itemIndex);
        var elem = this.FindChildElement(item.parentNode.parentNode.id);
        if (elem) elem.style.display = 'block';
      ***REMOVED***
      else if (this.lastKey==37) // Left
      ***REMOVED***
        var item = document.getElementById('Item'+itemIndex);
        var elem = this.FindChildElement(item.parentNode.parentNode.id);
        if (elem) elem.style.display = 'none';
      ***REMOVED***
      else if (this.lastKey==27) // Escape
      ***REMOVED***
        parent.searchBox.CloseResultsWindow();
        parent.document.getElementById("MSearchField").focus();
      ***REMOVED***
      else if (this.lastKey==13) // Enter
      ***REMOVED***
        return true;
      ***REMOVED***
      return false;
    ***REMOVED***

    this.NavChild = function(evt,itemIndex,childIndex)
    ***REMOVED***
      var e  = (evt) ? evt : window.event; // for IE
      if (e.keyCode==13) return true;
      if (!this.ProcessKeys(e)) return false;

      if (this.lastKey==38) // Up
      ***REMOVED***
        if (childIndex>0)
        ***REMOVED***
          var newIndex = childIndex-1;
          document.getElementById('Item'+itemIndex+'_c'+newIndex).focus();
        ***REMOVED***
        else // already at first child, jump to parent
        ***REMOVED***
          document.getElementById('Item'+itemIndex).focus();
        ***REMOVED***
      ***REMOVED***
      else if (this.lastKey==40) // Down
      ***REMOVED***
        var newIndex = childIndex+1;
        var elem = document.getElementById('Item'+itemIndex+'_c'+newIndex);
        if (!elem) // last child, jump to parent next parent
        ***REMOVED***
          elem = this.NavNext(itemIndex+1);
        ***REMOVED***
        if (elem)
        ***REMOVED***
          elem.focus();
        ***REMOVED***
      ***REMOVED***
      else if (this.lastKey==27) // Escape
      ***REMOVED***
        parent.searchBox.CloseResultsWindow();
        parent.document.getElementById("MSearchField").focus();
      ***REMOVED***
      else if (this.lastKey==13) // Enter
      ***REMOVED***
        return true;
      ***REMOVED***
      return false;
    ***REMOVED***
***REMOVED***

function setKeyActions(elem,action)
***REMOVED***
  elem.setAttribute('onkeydown',action);
  elem.setAttribute('onkeypress',action);
  elem.setAttribute('onkeyup',action);
***REMOVED***

function setClassAttr(elem,attr)
***REMOVED***
  elem.setAttribute('class',attr);
  elem.setAttribute('className',attr);
***REMOVED***

function createResults()
***REMOVED***
  var results = document.getElementById("SRResults");
  for (var e=0; e<searchData.length; e++)
  ***REMOVED***
    var id = searchData[e][0];
    var srResult = document.createElement('div');
    srResult.setAttribute('id','SR_'+id);
    setClassAttr(srResult,'SRResult');
    var srEntry = document.createElement('div');
    setClassAttr(srEntry,'SREntry');
    var srLink = document.createElement('a');
    srLink.setAttribute('id','Item'+e);
    setKeyActions(srLink,'return searchResults.Nav(event,'+e+')');
    setClassAttr(srLink,'SRSymbol');
    srLink.innerHTML = searchData[e][1][0];
    srEntry.appendChild(srLink);
    if (searchData[e][1].length==2) // single result
    ***REMOVED***
      srLink.setAttribute('href',searchData[e][1][1][0]);
      if (searchData[e][1][1][1])
      ***REMOVED***
       srLink.setAttribute('target','_parent');
      ***REMOVED***
      var srScope = document.createElement('span');
      setClassAttr(srScope,'SRScope');
      srScope.innerHTML = searchData[e][1][1][2];
      srEntry.appendChild(srScope);
    ***REMOVED***
    else // multiple results
    ***REMOVED***
      srLink.setAttribute('href','javascript:searchResults.Toggle("SR_'+id+'")');
      var srChildren = document.createElement('div');
      setClassAttr(srChildren,'SRChildren');
      for (var c=0; c<searchData[e][1].length-1; c++)
      ***REMOVED***
        var srChild = document.createElement('a');
        srChild.setAttribute('id','Item'+e+'_c'+c);
        setKeyActions(srChild,'return searchResults.NavChild(event,'+e+','+c+')');
        setClassAttr(srChild,'SRScope');
        srChild.setAttribute('href',searchData[e][1][c+1][0]);
        if (searchData[e][1][c+1][1])
        ***REMOVED***
         srChild.setAttribute('target','_parent');
        ***REMOVED***
        srChild.innerHTML = searchData[e][1][c+1][2];
        srChildren.appendChild(srChild);
      ***REMOVED***
      srEntry.appendChild(srChildren);
    ***REMOVED***
    srResult.appendChild(srEntry);
    results.appendChild(srResult);
  ***REMOVED***
***REMOVED***

function init_search()
***REMOVED***
  var results = document.getElementById("MSearchSelectWindow");
  for (var key in indexSectionLabels)
  ***REMOVED***
    var link = document.createElement('a');
    link.setAttribute('class','SelectItem');
    link.setAttribute('onclick','searchBox.OnSelectItem('+key+')');
    link.href='javascript:void(0)';
    link.innerHTML='<span class="SelectionMark">&#160;</span>'+indexSectionLabels[key];
    results.appendChild(link);
  ***REMOVED***
  searchBox.OnSelectItem(0);
***REMOVED***

