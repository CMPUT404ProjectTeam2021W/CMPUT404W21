function unfriendToggle(){
  var elem = document.getElementById("unfriend-button");
  if (elem.value == null){
    console.log("whyyy");
  }
  if (elem.value==">< Friends"){
    elem.value = "+ Send friend request";
    elem.width += "15px";
  }
  else
  {
    elem.value = ">< Friends";
  }
}
