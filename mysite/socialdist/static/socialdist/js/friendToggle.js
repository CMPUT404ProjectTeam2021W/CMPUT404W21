function friendToggle(){
  var elem = document.getElementById("follow-button");
  if (elem.value == null){
    console.log("whyyy");
  }
  if (elem.value=="+ Follow" || (user in author.following.all())){
    elem.value = "✓ Following";
    elem.width += "5px";
  }
  else
  {
    elem.value = "+ Follow";
  }
}