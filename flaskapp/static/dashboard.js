$(document).ready(function(){
    $(".form-group").attr("id","")
    $("#addBtn").click(function(){
        var fieldset = ''
        $("form").append(fieldset)
    });
  });