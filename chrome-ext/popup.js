/**
 * Credit to google's chrome extension starter code and
 * Mark Ashley Bell's tutorial/code, respectively:
 * https://developer.chrome.com/extensions/getstarted
 * http://markashleybell.com/building-a-simple-google-chrome-extension.html
 */
var hashtagLookup = {
  /**
   * Sends an XHR GET request to grab hashtag reference urls. The
   * XHR's 'onload' event is hooks up to the 'displayResults_' method.
   *
   * @public
   */
  requestReferences: function(event) {
    var req = new XMLHttpRequest();
    var hashtag =  document.getElementById('query-field').value;
    query =  'http://127.0.0.1:5000/query/' + encodeURIComponent(hashtag);
    req.open("GET", query, true); //true for a-synchronous
    console.log(req.responseText)
    req.onload = hashtagLookup.showReferences_;
    req.send(null);
    event.preventDefault(); //Keeps page from re-loading and aborting api call
  },

  /**
   * Handle the 'onload' event of our kitten XHR request, generated in
   * 'requestReferences', by generating 'div' elements, and appending them
   *
   * @param {ProgressEvent} e The XHR ProgressEvent.
   * @private
   */
  showReferences_: function (e) {
    var references = JSON && JSON.parse(e.target.responseText)
    var result, results, title, link;
    var listId = "results", titleId = "title";

    //delete any existing results block
    results = document.getElementById(listId);
    if (results) {
      console.log("Remove existing results");
      results.parentNode.removeChild(results);
      title = document.getElementById(titleId);
      title.parentNode.removeChild(title);
    }

    results = document.createElement("div");
    results.id = listId;
    title = document.createElement("div");
    title.id = titleId;
    title.innerHTML = "Results:";
    document.body.appendChild(title);

    for (var i = 0; i < references.length; i++) {
      result = document.createElement("div");
      link = document.createElement('a');
      link.href = references[i];
      link.innerHTML = "- " + references[i];
      result.appendChild(link);
      results.appendChild(result);
    }

    console.log("Appending results");
    document.body.appendChild(results);
  }
};

// Run our script as soon as the document's DOM is ready.
document.addEventListener('DOMContentLoaded', function () {
  // Handle the lookup button submit event
  document.getElementById('query-form').addEventListener('submit', hashtagLookup.requestReferences);
});
