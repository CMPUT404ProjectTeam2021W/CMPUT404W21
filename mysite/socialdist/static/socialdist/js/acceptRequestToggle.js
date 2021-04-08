function acceptRequestToggle(){
  var elem = document.getElementById("accept-button");
  if (elem.value == null){
    console.log("whyyy");
  }
  if (elem.value=="+ Accept"){
    elem.value = "✓ Accepted";
    elem.width += "5px";
  }
  else
  {
    elem.value = "+ Accept";
  }
}
