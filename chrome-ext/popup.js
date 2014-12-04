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
    req.onload = hashtagLookup.showResults_;
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
  showResults_: function (e) {
    var references = JSON && JSON.parse(e.target.responseText)['references'];
    var similarTags = JSON && JSON.parse(e.target.responseText)['similar-tags'];
    var tagdefSummary = JSON && JSON.parse(e.target.responseText)['tagdef-summary'];
    var result, results, resultsTitle, link, similarTagsTitle;
    var listId = "results", resultsTitleId = "results-title", 
        simTagsId = "sim-tags", simTagsTitleId = "sim-tags-title",
        tagdefId = "tagdef";

    //delete any existing results block
    results = document.getElementById(listId);
    if (results) {
      console.log("Remove existing results");
      results.parentNode.removeChild(results); //references
      resultsTitle = document.getElementById(resultsTitleId);
      resultsTitle.parentNode.removeChild(resultsTitle); //references title
      results = document.getElemenetById(simTagsId);
      results.parentNode.removeChild(results); //similar HashTags
      resultsTitle = document.getElementById(simTagsTitleId);
      resultsTitle.parentNode.removeChild(resultsTitle); //similar HashTags title
      resultsTitle = document.getElementById(tagdefId);
      resultsTitle.parentNode.removeChild(resultsTitle); //tagdef summary
    }

    console.log("Appending results");

    //append tagdef summary
    result = document.createElement("div");
    result.id = tagdefId;
    result.innerHTML = "TagDef.com summary: " + tagdefSummary;
    document.body.appendChild(result);

    //append similar hashtags title
    resultsTitle = document.createElement("div");
    resultsTitle.id = simTagsTitleId;
    resultsTitle.innerHTML = "Related HashTags:"
    document.body.appendChild(resultsTitle);

    //append similar hashtags
    results = document.createElement("div");
    results.id = simTagsId;
    for(var i = 0; i < similarTags.length; i++) {
      results.innerHTML += "#" + similarTags[i] + " "
    }
    document.body.appendChild(results);

    //append reference links
    results = document.createElement("div");
    results.id = listId;
    resultsTitle = document.createElement("div");
    resultsTitle.id = resultsTitleId;
    resultsTitle.innerHTML = "References:";
    document.body.appendChild(resultsTitle);

    for (var i = 0; i < references.length; i++) {
      result = document.createElement("div");
      link = document.createElement('a');
      link.href = references[i];
      link.innerHTML = "- " + references[i];
      result.appendChild(link);
      results.appendChild(result);
    }
    document.body.appendChild(results);
  }
};

// Run our script as soon as the document's DOM is ready.
document.addEventListener('DOMContentLoaded', function () {
  // Handle the lookup button submit event
  document.getElementById('query-form').addEventListener('submit', hashtagLookup.requestReferences);
});
