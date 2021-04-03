function followToggle(){
  var elem = document.getElementById("follow-button");
  if (elem.value == null){
    console.log("whyyy");
  }
  if (elem.value=="+ Follow"){
    elem.value = "✓ Following";
    elem.width += "5px";
  }
  else
  {
    elem.value = "+ Follow";
  }
}

function unfollowToggle(){
  var elem = document.getElementById("unfollow-button");
  if (elem.value == null){
    console.log("whyyy");
  }
  if (elem.value=="✓ Following"){
    elem.value = "+ Follow";
    elem.width -= "5px";
  }
  else
  {
    elem.value = "✓ Following";
  }
}
