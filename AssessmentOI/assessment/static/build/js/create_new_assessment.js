var currentTab = 0; // Current tab is set to be the first tab (0)
// var modal = document.getElementById("myModal");
// var span = document.getElementsByClassName("close")[0];


showTab(currentTab); // Display the current tab
// selectedNumberOfAnswers('single')

function showTab(n) {
  // This function will display the specified tab of the form ...
  var x = document.getElementsByClassName("tab");

  x[n].style.display = "block";
  // ... and fix the Previous/Next buttons:
  if (n == 0) {
    document.getElementById("prevBtn").style.display = "none";
//    document.getElementById("prevBtn").innerHTML = "Previous";
  } else if (n == (x.length - 1)) {
    document.getElementById("prevBtn").innerHTML = "Previous";
  }
  else {
    document.getElementById("prevBtn").innerHTML = "Previous";
    document.getElementById("prevBtn").style.display = "inline";
  }
  if (n == (x.length - 1)) {


    document.getElementById("nextBtn").innerHTML = "Submit";
  }
  else if (n == (x.length - 2)) {
    document.getElementById("nextBtn").innerHTML = "Next";
  }
  else {
    document.getElementById("nextBtn").innerHTML = "Next";
  }
  // ... and run a function that displays the correct step indicator:
  fixStepIndicator(n)
}

function nextPrev(n) {
    debugger
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

    document.getElementById("question_form").submit();
    return false;
  }
  // Otherwise, display the correct tab:
  //   TODO: calculate time based on number of questions

    // to be launched when in the correct tab
if (currentTab == x.length-2) {
    debugger
    all_input = document.getElementById("table").getElementsByClassName("flat")
    all_input_selected = []
    for(i=0;i<all_input.length;i++){
        if (all_input[i].checked){
            all_input_selected.push(all_input[i].name.split("_")[2])
        }
    }
    console.log(all_input_selected)
    document.getElementById("questions_selected_summary").innerHTML = all_input_selected
    numbers_of_selected_answers = Math.ceil(all_input_selected.length * 2)
    document.getElementById("duration_summary").innerHTML = numbers_of_selected_answers
    document.getElementsByName("duration")[0].value = numbers_of_selected_answers
}

  showTab(currentTab);
}

function validateForm() {
  // This function deals with validation of the form fields
  // update accordingly
  var x, y, i, valid = true;

//   x = document.getElementsByClassName("tab");
//   y = x[currentTab].getElementsByTagName("input");
//   // A loop that checks every input field in the current tab:
//
//   //  check the type of question (single or multiple) if it is not he summary tab
//   if(currentTab == x.length-1){
//     valid = true
//     return valid
//   }
//   number_of_selections = document.getElementById("selection"+(parseInt(currentTab)+1)).innerText;
//
//   count_selected = 0;
//   answers = ""
// //  the test for the length is modified as there is an additional input for the review flat
//   for (i = 0; i < y.length-1; i++) {
//     // If a field is empty...
//     if (y[i].checked == true) {
//       // add an "invalid" class to the field:
//       count_selected = count_selected + 1
//       // and set the current valid status to false:
//         answers = answers + 'A' + (parseInt(i)+1) + ', '
//     }
//   }
//
//   if(count_selected != parseInt(number_of_selections)){
//         valid = false;
//   }
//
//   // If the valid status is true, mark the step as finished and valid:
//   if (valid) {
//     document.getElementsByClassName("step")[currentTab].className += " finish";
//     document.getElementsByName('answers_question_'+ parseInt(currentTab+1))[0].innerHTML = answers
//   }
//


  return valid; // return the valid status
}

function fixStepIndicator(n) {
  // This function removes the "active" class of all steps...
  var i, x = document.getElementsByClassName("step");
  for (i = 0; i < x.length; i++) {
    x[i].className = x[i].className.replace(" active", "");
  }
  //... and adds the "active" class to the current step:
  if(n >= x.length){
      // document.getElementById("question_summary").style.display = "contents";
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

// function selectedNumberOfAnswers(radio_check_text){
//
//     check_max_of_correct_answer()
//     if (radio_check_text == undefined){
//         // check what option is selected: single, multi, text
//         radio_options = document.getElementsByName("radio")
//         for (i=0;i<radio_options.length;i++){
//                 if (radio_options[i].checked){
//                     radio_check_text = radio_options[i].value
//                 }
//         }
//     }
//
//     debugger
//     number_of_answers = parseInt(document.querySelector("#number_of_answers").value)
//     if(radio_check_text=='single'){
//         answers = document.getElementsByName("answer_radio")
//     }
//     else if(radio_check_text=='multi'){
//         answers = document.getElementsByName("answer_check")
//     }
//     else{
//         answers = document.getElementsByName("answer_text")
//     }
//
//     debugger
//     for (i=0;i<5;i++){
//         debugger
//         if (i<number_of_answers){
//         answers[i].hidden = false;
//         }
//         else{
//         answers[i].hidden = true;
//         }
//
//     }
//
// }

// function type_of_question(type) {
//     debugger
//     number_of_answers = document.getElementById("number_of_answers")
//     number_of_correct_answers = document.getElementById("number_of_correct_answers")
//
//     if (type == "single"){
//         number_of_answers.disabled = false
//         number_of_correct_answers.selectedIndex = 0
//         number_of_correct_answers.disabled = true
//         document.getElementById("radio_row").hidden = false
//         document.getElementById("check_row").hidden = true
//         document.getElementById("text_row").hidden = true
//         selectedNumberOfAnswers('single')
//     }
//     else if(type == "multi"){
//         number_of_correct_answers.disabled = false
//         number_of_answers.disabled = false
//         number_of_correct_answers.selectedIndex = 1
//         number_of_answers.selectedIndex = 1
//         document.getElementById("radio_row").hidden = true
//         document.getElementById("check_row").hidden = false
//         document.getElementById("text_row").hidden = true
//         selectedNumberOfAnswers('multi')
//     }
//     else{
//
//         number_of_correct_answers.selectedIndex = 0
//         number_of_correct_answers.disabled = true
//
//         number_of_answers.selectedIndex = 0
//         number_of_answers.disabled = true
//         document.getElementById("radio_row").hidden = true
//         document.getElementById("check_row").hidden = true
//         document.getElementById("text_row").hidden = false
//         selectedNumberOfAnswers('text')
//
//     }
//
// }
//
// function check_max_of_correct_answer(){
//     debugger
//     correct_answers = document.getElementById("number_of_correct_answers")
//     answers = document.getElementById("number_of_answers")
//     number_of_correct_answers_selected = parseInt(correct_answers[correct_answers.selectedIndex].value)
//     number_of_answers_selected = parseInt(answers[answers.selectedIndex].value)
//
//     radio_options = document.getElementsByName("radio")
//     for (i=0;i<radio_options.length;i++){
//             if (radio_options[i].checked){
//                 radio_check_text = radio_options[i].value
//             }
//     }
//
//     if(radio_check_text == "multi"){
//         if (number_of_correct_answers_selected >= number_of_answers_selected){
//             // cannot be
//             document.getElementById("number_of_answers").selectedIndex = number_of_answers_selected - 1
//             document.getElementById("error_message").hidden = false
//             startTimer(10)
//         }
//     }
//
//
// }
//
// function startTimer(duration) {
//     var timer = duration, minutes, seconds;
//     setInterval(function () {
//         minutes = parseInt(timer / 60, 10);
//         seconds = parseInt(timer % 60, 10);
//
//         minutes = minutes < 10 ? "0" + minutes : minutes;
//         seconds = seconds < 10 ? "0" + seconds : seconds;
//
//         if (--timer < 0) {
//             // timer = duration;
//             // setAlert()
//             document.getElementById("error_message").hidden = true
//         }
//     }, 1000);
// }

function recordSelection(input){
    debugger
    switch (input){
        case 'test_name':
            document.getElementById("test_name_summary").innerHTML = document.getElementsByName(input)[0].value
            break;
        case 'candidate_name':
            document.getElementById("candidate_name_summary").innerHTML = document.getElementsByName(input)[0].value
            break;
        case 'candidate_surname':
            document.getElementById("candidate_surname_summary").innerHTML = document.getElementsByName(input)[0].value

            break;
        case 'candidate_email':
            document.getElementById("candidate_email_summary").innerHTML = document.getElementsByName(input)[0].value

            break;
        case 'token':
            document.getElementById("token_summary").innerHTML = document.getElementsByName(input)[0].value

            break;
        case 'duration':
            document.getElementById("duration_summary").innerHTML = document.getElementsByName(input)[0].value

            break;
        default:
    }
    console.log(input)
}

function temp(ele){
    console.log("pippo")
}

function generate_token(length){
    //edit the token allowed characters
    var a = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890".split("");
    var b = [];
    for (var i=0; i<length; i++) {
        var j = (Math.random() * (a.length-1)).toFixed(0);
        b[i] = a[j];
    }
    return b.join("");
}



