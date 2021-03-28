function unfriendToggle(){
  var elem = document.getElementById("unfollow-button");
  if (elem.value == null){
    console.log("whyyy");
  }
  if (elem.value=="✓ Following" || !(user in author.following.all())){
    elem.value = "+ Follow";
    elem.width -= "5px";
  }
  else
  {
    elem.value = "✓ Following";
  }
}
