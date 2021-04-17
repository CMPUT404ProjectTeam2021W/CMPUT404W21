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

function unshareToggle(){
  var elem = document.getElementById("share-button");
  if (elem.value == null){
    console.log("whyyy");
  }
  if (elem.value=="🚀 Shared"){
    elem.value = "🚀 Share";
    elem.width -= "5px";
  }
  else
  {
    elem.value = "🚀 Shared";
  }
}
