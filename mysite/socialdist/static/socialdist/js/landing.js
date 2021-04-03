$(document).ready(function() {
  setTimeout(function() {
    $('.hermes-big').animate({
      marginTop: "-=15vh",
      opacity: 1
    }, 250);
  },400);
  setTimeout(function() {
    $('.big-marker').animate({
      opacity: 1
    }, 250);
  },500);

  setTimeout(function() {
    $('.friendly-reminder').animate({
      opacity: 1
    }, 250);
  },700);

  setTimeout(function() {
    $('.link-box').animate({
      opacity: 1,
      display: "visible"
    }, 250);
  },900);
});


$(document).on("click", "#editButton", function() {
  var title_original = $('.post-title').text()
  var new_title = $("<textarea class=\"form-control editTitle\" style=\"resize: none;overflow: hidden;\"oninput=\"auto_grow(this)\"/>");
  new_title.val(title_original);
  $('.post-title').replaceWith(new_title);

  var original_text = $('.editable_text').text();
  var new_input = $("<textarea class=\"form-control editArea\" style=\"resize: none;overflow: hidden;\"oninput=\"auto_grow(this)\"/>");
  new_input.val(original_text);
  $('.editable_text').replaceWith(new_input);

  var pass_data = $('#editButton')[0].getAttribute("data");
  var new_button = $("<input type =\"submit\" class=\"btn btn-primary saveButton\" value =\"🖬 Save\"/>");
  $('#editButton').replaceWith(new_button)
  $('.saveButton')[0].setAttribute("data", pass_data)
  answer = $('.saveButton')[0].getAttribute("data");
  new_input.focus();
});

$(document).on("click", ".saveButton", function() {

  var new_input = $('.editArea').val();
  var updated_text = $("<span class=\"editable_text\">");
  updated_text.text(new_input);
  $('.editArea').replaceWith(updated_text);

  var new_title = $('.editTitle').val();
  var updated_title = $("<span class=\"post-title\">");
  updated_title.text(new_title);
  $('.editTitle').replaceWith(updated_title);


  var new_button = $(" <input class=\"btn btn-primary\" type=\"button\" value =\"✎ Edit\" id = \"editButton\"/>");
  var pass_data = $('.saveButton')[0].getAttribute("data");
  $('.saveButton').replaceWith(new_button);
  $('#editButton')[0].setAttribute("data", pass_data);
  create_post(pass_data);

});

function auto_grow(element) {
    element.style.height = "5px";
    element.style.height = (element.scrollHeight)+"px";
}


function create_post(post_id) {
    console.log("create post is working!") // sanity check
    console.log(post_id);
    $.ajax({
        // url : "", // the endpoint
        type : "POST", // http method
        data : { title : $('.post-title').val(), post: $('.editable_text').val() }, // data sent with the post request

        // handle a successful response
        success : function(json) {
            console.log(json); // log the returned json to the console
            console.log("success"); // another sanity check
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
};
