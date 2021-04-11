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
  var new_title = $("<form method=\"POST\" id=\"post-form\"> <textarea class=\"form-control editTitle\" style=\"resize: none;overflow: hidden;\"oninput=\"auto_grow(this)\"/>");
  new_title.val(title_original);
  $('.post-title').replaceWith(new_title);

  var original_text = $('.editable_text').text();
  var new_input = $("<textarea class=\"form-control editArea\" style=\"resize: none;overflow: hidden;\"oninput=\"auto_grow(this)\"/>");
  new_input.val(original_text);
  $('.editable_text').replaceWith(new_input);

  var pass_data = $('#editButton')[0].getAttribute("data");
  const url = $('#editButton')[0].getAttribute("url");
  var new_button = $("<input type =\"submit\" class=\"btn btn-primary saveButton\" value =\"🖬 Save\"/>");
  $('#editButton').replaceWith(new_button)
  $('.saveButton')[0].setAttribute("data", pass_data)
  $('.saveButton')[0].setAttribute("url", url)
  new_input.focus();
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


$(document).on("click", ".saveButton", function() {
  var post_id = $('.saveButton')[0].getAttribute("data");
  var url = $('.saveButton')[0].getAttribute("url");
  var new_input = $('.editArea').val();
  var updated_text = $("<span class=\"editable_text\">");
  updated_text.text(new_input);
  $('.editArea').replaceWith(updated_text);

  var new_title = $('.editTitle').val();
  var updated_title = $("<span class=\"post-title\">");
  updated_title.text(new_title);
  $('.editTitle').replaceWith(updated_title);

  var new_button = $(" <input class=\"btn btn-primary\" type=\"button\" value =\"✎ Edit\" id = \"editButton\"/>");

  $('.saveButton').replaceWith(new_button);
  $('#editButton')[0].setAttribute("data", post_id);
  create_post(post_id, url, new_title, new_input)
});

function auto_grow(element) {
    element.style.height = "5px";
    element.style.height = (element.scrollHeight)+"px";
}


function create_post(post_id, url, new_title, new_input) {
  console.log(new_title)
  const csrftoken = getCookie('csrftoken');
  $.ajax({
      url : url, // the endpoint
      type : "POST", // http method
      headers: {'X-CSRFToken': csrftoken},
      data : {
            // csrfmiddlewaretoken:$('[name=csrfmiddlewaretoken]').val(),
            action: 'post',
            post_id: post_id,
            title : new_title,
            description: new_input }, // data sent with the post request

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
