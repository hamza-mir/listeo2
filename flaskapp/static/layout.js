$(document).ready(function(){
  $("div#regis").hide();
  $("button#login").addClass("red");
  $("button#login").click(function(){
    $("div#login").show();
    $("div#regis").hide();
    $("button#login").addClass("red");
    $("button#regis").removeClass("red");
  });
  $("button#regis").click(function(){
    $("div#regis").show();
    $("div#login").hide();
    $("button#regis").addClass("red");
    $("button#login").removeClass("red");
  });
  $(".btn-wishlist-add").click(function(e){
      var eventid = $(this).data('rep');
      console.log(eventid);
      var urlid = '/addwishlist/' + eventid;
      console.log(urlid);
      e.preventDefault();
      $.ajax({
          type:'POST',
          url:urlid,
          data:{eventid:eventid},
          success:function()
            {
              changeaddbtn(eventid);
              showwishaddalert();
            },
          error: function(error) {
                console.log(error);
            }
      })
  });
  $(".btn-wishlist-rem").click(function(e){
      var eventid = $(this).data('rep');
      console.log(eventid);
      var urlid = '/remwishlist/' + eventid;
      console.log(urlid);
      e.preventDefault();
      $.ajax({
          type:'POST',
          url:urlid,
          data:{eventid:eventid},
          success:function()
            {
              changerembtn(eventid);
              showwishremalert();
            },
          error: function(error) {
                console.log(error);
            }
      })
  });
  $(".btn-booking").click(function(e){
      var eventid = $(this).data('rep');
      console.log(eventid);
      var urlid = '/addtocart/' + eventid;
      console.log(urlid);
      e.preventDefault();
      $.ajax({
          type:'POST',
          url:urlid,
          data:{eventid:eventid},
          success:function()
            {
              console.log('Event added to cart!');
              location.href = 'https://testsite09.pythonanywhere.com/cart';
            },
          error: function(error) {
                console.log(error);
            }
      })
  });
  $(".btn-cart").click(function(e){
      var eventid = $(this).data('rep');
      console.log(eventid);
      var urlid = '/addtocart/' + eventid;
      console.log(urlid);
      e.preventDefault();
      $.ajax({
          type:'POST',
          url:urlid,
          data:{eventid:eventid},
          success:function()
            {
              showcartalert();
            },
          error: function(error) {
                console.log(error);
            }
      })
  });
});
function showwishremalert() {
    $('.alert-row').remove()
    var alertrow = "<div class='row alert-row'></div>"
    var alertcol = "<div class='col-lg-4 offset-lg-4 alert-col'></div>"
    var alertbar = "<div class='alert-bar alert-msg-bar'></div>"
    var alertmain = "<div class='alert alert-success alert-dismissible fade show alert-main' role='alert'></div>"
    var alertmsg = "<b>Event Removed from Wishlist</b>"
    var alertclosebutton = "<button type='button' class='btn-close btn-alert-close' data-bs-dismiss='alert' aria-label='Close'></button>"
    $('.cart-alert').append(alertrow);
    $('.alert-row').fadeIn();
    $('.alert-row').append(alertcol);
    $('.alert-col').append(alertbar);
    $('.alert-msg-bar').append(alertmain);
    $('.alert-main').append(alertmsg);
    $('.alert-main').append(alertclosebutton);
    $('.btn-close').click(function(){
        $('.alert-row').remove(1000);
    });
}
function showwishaddalert() {
    $('.alert-row').remove()
    var alertrow = "<div class='row alert-row'></div>"
    var alertcol = "<div class='col-lg-4 offset-lg-4 alert-col'></div>"
    var alertbar = "<div class='alert-bar alert-msg-bar'></div>"
    var alertmain = "<div class='alert alert-success alert-dismissible fade show alert-main' role='alert'></div>"
    var alertmsg = "<b>Event added to Wishlist</b>"
    var alertclosebutton = "<button type='button' class='btn-close btn-alert-close' data-bs-dismiss='alert' aria-label='Close'></button>"
    $('.cart-alert').append(alertrow);
    $('.alert-row').fadeIn();
    $('.alert-row').append(alertcol);
    $('.alert-col').append(alertbar);
    $('.alert-msg-bar').append(alertmain);
    $('.alert-main').append(alertmsg);
    $('.alert-main').append(alertclosebutton);
    $('.btn-close').click(function(){
        $('.alert-row').remove(1000);
    });
}
function showcartalert() {
    $('.alert-row').remove()
    var alertrow = "<div class='row alert-row'></div>"
    var alertcol = "<div class='col-lg-4 offset-lg-4 alert-col'></div>"
    var alertbar = "<div class='alert-bar alert-msg-bar'></div>"
    var alertmain = "<div class='alert alert-success alert-dismissible fade show alert-main' role='alert'></div>"
    var alertmsg = "<b>Event added to cart</b>"
    var alertclosebutton = "<button type='button' class='btn-close btn-alert-close' data-bs-dismiss='alert' aria-label='Close'></button>"
    $('.cart-alert').append(alertrow);
    $('.alert-row').append(alertcol);
    $('.alert-col').append(alertbar);
    $('.alert-msg-bar').append(alertmain);
    $('.alert-main').append(alertmsg);
    $('.alert-main').append(alertclosebutton);
    $('.btn-close').click(function(){
        $('.alert-row').remove(1000);
    });
}
function changerembtn(eventid) {
    console.log('changerembtn called')
    var eventselector = '.btn-wishlist-' + eventid;
    $(eventselector).removeClass('btn-wishlist-rem');
    $(eventselector).addClass('btn-wishlist-add');
    $(eventselector).children("i").removeClass('fa-heart');
    $(eventselector).children("i").addClass('fa-heart-o');
    $(eventselector).off("click");
    $(eventselector).click(function(e) {
      var eventid = $(this).data('rep');
      console.log(eventid);
      var urlid = '/addwishlist/' + eventid;
      console.log(urlid);
      e.preventDefault();
      $.ajax({
          type:'POST',
          url:urlid,
          data:{eventid:eventid},
          success:function()
            {
              changeaddbtn(eventid);
              alert('Event added in wishlist!');
            },
          error: function(error) {
                console.log(error);
            }
      })
    });
}
function changeaddbtn(eventid) {
    console.log('changeaddbtn called')
    var eventselector = '.btn-wishlist-' + eventid;
    $(eventselector).removeClass('btn-wishlist-add');
    $(eventselector).addClass('btn-wishlist-rem');
    $(eventselector).children("i").removeClass('fa-heart-o');
    $(eventselector).children("i").addClass('fa-heart');
    $(eventselector).off("click");
    $(eventselector).click(function(e) {
      var eventid = $(this).data('rep');
      console.log(eventid);
      var urlid = '/remwishlist/' + eventid;
      console.log(urlid);
      e.preventDefault();
      $.ajax({
          type:'POST',
          url:urlid,
          data:{eventid:eventid},
          success:function()
            {
              changerembtn(eventid);
              alert('Event removed from wishlist!');
            },
          error: function(error) {
                console.log(error);
            }
      })
    });
}