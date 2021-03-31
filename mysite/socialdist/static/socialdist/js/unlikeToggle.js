function unlikeToggle(){
  var elem = document.getElementById("unlike-button");
  if (elem.value == null){
    console.log("whyyy");
  }
  if (elem.value=="✓ Liked"){
    elem.value = "+ Like";
    elem.width -= "5px";
  }
  else
  {
    elem.value = "✓ Liked";
  }
}
