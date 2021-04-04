function rejectRequestToggle(){
  var elem = document.getElementById("reject-button");
  if (elem.value == null){
    console.log("whyyy");
  }
  if (elem.value==">< Reject"){
    elem.value = "✓ Rejected";
    elem.width += "5px";
  }
  else
  {
    elem.value = ">< Reject";
  }
}
