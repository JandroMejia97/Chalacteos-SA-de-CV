/*  url = "La url como la declara DJANGo";
     $.ajax({
      url: url,
      type: 'POST',
      data: {'variable': valor },
    }).done(function(respuesta) {

    }).fail(function() {
      console.log("error");
    }).always(function() {
      console.log("complete");
*/

/*
url = "/ajax/borrar/invernadero/";
return $.ajax({
  url: url,
  type: 'POST',
  data: {
    'id_invernadero': id_invernadero,
  },
  dataType: 'json'
}).done(function(respuesta) {
  alert(respuesta['message']);
    $('#'+id_invernadero).remove();
}).fail(function() {
  console.log("error");
  alert(respuesta['message']);
}).always(function() {
  console.log("complete");
});
 */

 $(function () {
  $.ajaxSetup({
      headers: { "X-CSRFToken": getCookie("csrftoken") }
  });
});