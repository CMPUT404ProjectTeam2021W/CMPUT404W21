function likeToggle(){
  var elem = document.getElementById("like-button");
  if (elem.value == null){
    console.log("whyyy");
  }
  if (elem.value=="+ Like"){
    elem.value = "✓ Liked";
    elem.width += "5px";
  }
  else
  {
    elem.value = "+ Like";
  }
}
