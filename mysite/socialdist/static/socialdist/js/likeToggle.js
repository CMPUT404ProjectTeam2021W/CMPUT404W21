


function likeToggle(postId){
  var elem = document.querySelector("#like-button-" + postId);
  console.log("#like-button-" + postId)
  if (elem.value=="❤ Like"){
    elem.value = "❤ Liked";
    elem.width += "5px";
    var url = $("#like-button-"+postId)[0].getAttribute("url");
    var data = $("#like-button-"+postId)[0].getAttribute("data");
    var likeCount = document.querySelector('#likes-'+data);
    likeCount.textContent = Number(likeCount.textContent)+1;
    console.log(likeCount)
    $.ajax({
        url : url, // the endpoint
        type : "GET", // http method
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
  }
}


function unlikeToggle(postId){
  console.log(postId)
  var elem = document.querySelector("#unlike-button-"+postId);
  if (elem.value == null){
    console.log("whyyy");
  }
  if (elem.value=="❤ Liked"){
    elem.value = "❤ Like";
    elem.width -= "5px";
    var url = $("#unlike-button-"+postId)[0].getAttribute("url");
    var data = $("#unlike-button-"+postId)[0].getAttribute("data");
    var likeCount = document.querySelector('#likes-'+data);
    likeCount.textContent = Number(likeCount.textContent)-1;
    $.ajax({
        url : url, // the endpoint
        type : "GET", // http method
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
  }
}



function shareToggle(postId){
  var elem = document.querySelector("#share-button-" + postId);
  if (elem.value=="🚀 Share"){
    elem.value = "🚀 Shared";
    elem.width += "5px";
    var url = $("#share-button-"+postId)[0].getAttribute("url");
    var data = $("#share-button-"+postId)[0].getAttribute("data");
    $.ajax({
        url : url, // the endpoint
        type : "GET", // http method
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
  }
}


function unshareToggle(postId){
  var elem = document.querySelector("#unshare-button-" + postId);
  if (elem.value=="🚀 Shared"){
    elem.value = "🚀 Share";
    elem.width -= "5px";
    var url = $("#unshare-button-"+postId)[0].getAttribute("url");
    var data = $("#unshare-button-"+postId)[0].getAttribute("data");
    $.ajax({
        url : url, // the endpoint
        type : "GET", // http method
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
  }
}

// function shareToggle(){
//   var elem = document.getElementById("share-button");
//   if (elem.value == null){
//     console.log("whyyy");
//   }
//   if (elem.value=="🚀 Share"){
//     elem.value = "🚀 Shared";
//     elem.width += "5px";
//   }
//   else
//   {
//     elem.value = "🚀 Share";
//   }
// }


// function unshareToggle(){
//   var elem = document.getElementById("share-button");
//   if (elem.value == null){
//     console.log("whyyy");
//   }
//   if (elem.value=="🚀 Shared"){
//     elem.value = "🚀 Share";
//     elem.width -= "5px";
//   }
//   else
//   {
//     elem.value = "🚀 Shared";
//   }
// }
