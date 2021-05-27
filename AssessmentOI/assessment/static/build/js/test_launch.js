var currentTab = 0; // Current tab is set to be the first tab (0)

var modal2 = document.getElementById("myModalTaC");
var span2 = document.getElementById("span2");


// When the user clicks on <span> (x), close the modal
span2.onclick = function() {
  modal2.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == modal2) {
    modal2.style.display = "none";
  }
}

function terms_and_conditions(){
  modal2.style.display = "block";
}

function activate_deactivate_start(){
  debugger
  start_button = document.getElementById("startButton");
  if (start_button.disabled) {
    start_button.disabled = false
  }
  else {
    start_button.disabled = true
  }

}

