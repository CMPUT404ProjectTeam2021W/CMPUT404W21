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
