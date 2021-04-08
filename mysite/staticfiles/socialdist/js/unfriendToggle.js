function unfriendToggle(){
  var elem = document.getElementById("unfriend-button");
  if (elem.value == null){
    console.log("whyyy");
  }
  if (elem.value==">< Friends"){
    elem.value = "+ Follow";
    elem.width -= "5px";
  }
  else
  {
    elem.value = ">< Friends";
  }
}
