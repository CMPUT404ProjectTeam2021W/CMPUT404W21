function likeToggle(){
  var elem = document.getElementById("like-button");
  if (elem.value == null){
    console.log("whyyy");
  }
  if (elem.value=="❤ Like"){
    elem.value = "❤ Liked";
    elem.width += "5px";
  }
  else
  {
    elem.value = "+ Like";
  }
}

function shareToggle(){
  var elem = document.getElementById("share-button");
  if (elem.value == null){
    console.log("whyyy");
  }
  if (elem.value=="🚀 Share"){
    elem.value = "🚀 Shared";
    elem.width += "5px";
  }
  else
  {
    elem.value = "🚀 Share";
  }
}
