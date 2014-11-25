var hashtagLookup = {
  /**
   * URL for searching a test hashtag, just to demonstrate functionaality. 
   *
   * @type {string}
   * @private
   */
  searchHashtag_: 'http://127.0.0.1:5000/' +
      'query='+ encodeURIComponent("#HelloWorld")

  /**
   * Sends an XHR GET request to grab hashtag reference urls. The
   * XHR's 'onload' event is hooks up to the 'displayResults_' method.
   *
   * @public
   */
  requestReferences: function() {
    var req = new XMLHttpRequest();
    req.open("GET", this.searchHashtag_, true);
    req.onload = this.showRefernces_.bind(this);
    req.send(null);
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
    for (var i = 0; i < references.length; i++) {
      var ref = document.createElement('div');
      ref.innerHTML = references[i];
      document.body.appendChild(ref);
    }
  }
};

// Run our script as soon as the document's DOM is ready.
document.addEventListener('DOMContentLoaded', function () {
  hashtagLookup.requestReferences();
});
