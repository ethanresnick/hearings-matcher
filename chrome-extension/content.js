(function() {
  var url = "http://127.0.0.1:5000/matches?for=" + encodeURIComponent(window.location.href);
  $.ajax(url, {
    success: function(data) {
      $(function() {
        $("body").prepend(JSON.stringify(data));
      });
    }
  });
}());

