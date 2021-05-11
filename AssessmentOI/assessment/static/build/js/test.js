var currentTab = 0; // Current tab is set to be the first tab (0)
var modal = document.getElementById("myModal");
var span = document.getElementsByClassName("close")[0];

showTab(currentTab); // Display the current tab

function showTab(n) {
  // This function will display the specified tab of the form ...
  var x = document.getElementsByClassName("tab");

  x[n].style.display = "block";
  // ... and fix the Previous/Next buttons:
  if (n == 0) {
    document.getElementById("prevBtn").style.display = "none";
//    document.getElementById("prevBtn").innerHTML = "Previous";
  } else if (n == (x.length - 1)) {
    document.getElementById("prevBtn").innerHTML = "Test";
  }
  else {
    document.getElementById("prevBtn").innerHTML = "Previous";
    document.getElementById("prevBtn").style.display = "inline";
  }
  if (n == (x.length - 1)) {


    document.getElementById("nextBtn").innerHTML = "Submit";
  } else if (n == (x.length - 2)) {
    document.getElementById("nextBtn").innerHTML = "Summary";
  }else {
    document.getElementById("nextBtn").innerHTML = "Next";
  }
  // ... and run a function that displays the correct step indicator:
  fixStepIndicator(n)
}

function nextPrev(n) {

  // This function will figure out which tab to display
  var x = document.getElementsByClassName("tab");
  // Exit the function if any field in the current tab is invalid:
  if (n == 1 && !validateForm()) {

    modal.style.display = "block";

    document.getElementById('message').innerHTML =
        '\r\nSelect ' + document.getElementById('selection'+(parseInt(currentTab)+1)).innerHTML + ' option(s)'
    return false;
  }

  // Hide the current tab:
  x[currentTab].style.display = "none";
  // Increase or decrease the current tab by 1:
  currentTab = currentTab + n;
  // if you have reached the end of the form... :
  if (currentTab >= x.length) {
    //...the form gets submitted:
    debugger
    document.getElementById("regForm").submit();
    return false;
  }
  // Otherwise, display the correct tab:
  showTab(currentTab);
}

function validateForm() {
  // This function deals with validation of the form fields
  // update accordingly
  var x, y, i, valid = true;

  x = document.getElementsByClassName("tab");
  y = x[currentTab].getElementsByTagName("input");
  // A loop that checks every input field in the current tab:

  //  check the type of question (single or multiple) if it is not he summary tab
  if(currentTab == x.length-1){
    valid = true
    return valid
  }
  number_of_selections = document.getElementById("selection"+(parseInt(currentTab)+1)).innerText;

  count_selected = 0;
  answers = ""
//  the test for the length is modified as there is an additional input for the review flat
  for (i = 0; i < y.length-1; i++) {
    // If a field is empty...
    if (y[i].checked == true) {
      // add an "invalid" class to the field:
      count_selected = count_selected + 1
      // and set the current valid status to false:
        answers = answers + 'A' + (parseInt(i)+1) + ', '
    }
  }

  if(count_selected != parseInt(number_of_selections)){
        valid = false;
  }

  // If the valid status is true, mark the step as finished and valid:
  if (valid) {
    document.getElementsByClassName("step")[currentTab].className += " finish";
    document.getElementsByName('answers_question_'+ parseInt(currentTab+1))[0].innerHTML = answers
  }



  return valid; // return the valid status
}

function recordResult(){
        debugger
//        document.getElementsByName('answers_question_'+ parseInt(currentTab+1))[0].innerHTML = answers
}

function fixStepIndicator(n) {
  // This function removes the "active" class of all steps...
  var i, x = document.getElementsByClassName("step");
  for (i = 0; i < x.length; i++) {
    x[i].className = x[i].className.replace(" active", "");
  }
  //... and adds the "active" class to the current step:
  if(n >= x.length){
      document.getElementById("question_summary").style.display = "contents";
  }else{
    x[n].className += " active";
  }

}

function jumpToQuestion(question_number) {
        var x = document.getElementsByClassName("tab");
        x[currentTab].style.display = "none";
        currentTab  = question_number
        showTab(question_number);
}

function jumpToQuestionFromTable(question_number) {
        var x = document.getElementsByClassName("tab");
        x[currentTab].style.display = "none";
        currentTab  = question_number - 1
        showTab(question_number - 1);
}

function flagForReview(question_number){


        if (validateForm()){
            span_element = document.getElementsByName('span'+ (parseInt(question_number)-1))[0]
            review_element = document.getElementsByName('review_question_'+ parseInt(question_number))[0]
            current_colour = span_element.style.backgroundColor
            if (current_colour == "red") {
             span_element.style.backgroundColor = "#04AA6D"
             review_element.innerHTML = ''

            }

            else {
                span_element.style.backgroundColor = "red"
                review_element.innerHTML = 'Yes'
            }
        }

        else{
            modal.style.display = "block";


            document.getElementById('message').innerHTML =
                '\r\nSelect ' + document.getElementById('selection'+(parseInt(currentTab)+1)).innerHTML + ' option(s)'
            debugger
            document.getElementById('optionsSelectionX' + (parseInt(currentTab)+1)).checked = false

        }




}

function resetEntry(){
//reset any selection (the select option has a default solution )

    select_options = document.querySelectorAll('input')
    for (i = 0; i < select_options.length; i++){

        if(select_options[i].type == 'radio'){
            select_options[i].checked = false
        }
    }
//    checked
}

function startTimer(duration, display) {
    var timer = duration, minutes, seconds;
    setInterval(function () {
        minutes = parseInt(timer / 60, 10);
        seconds = parseInt(timer % 60, 10);

        minutes = minutes < 10 ? "0" + minutes : minutes;
        seconds = seconds < 10 ? "0" + seconds : seconds;

        display.textContent = minutes + ":" + seconds;

        if (--timer < 0) {
            timer = duration;
        }
    }, 1000);
}

window.onload = function () {
    var fiveMinutes = 60 * 1,
        display = document.querySelector('#time');
    resetEntry()
    startTimer(fiveMinutes, display);
};

// When the user clicks on <span> (x), close the modal
span.onclick = function() {
  modal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}


