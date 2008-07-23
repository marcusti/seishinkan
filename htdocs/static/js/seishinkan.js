$(document).ready(function(){
  $(":text").focus(function() {
    $(this).select();
  });

  $("#id_username").focus();

  $("#search-clear").click(function() {
    $(":text").val("");
  });

  $("#language").change(function() {
    $("#setlang").submit();
  });

  $("#login-button").click(function() {
    $("#login-button").attr("disabled", "disabled");
    $("#login-form").submit();
  });

});

var RecaptchaOptions = {
    theme : 'white',
    lang : 'de'
};
