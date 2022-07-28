//widged variables declarations
var input_text_radiobutton = document.getElementById("customRadioInline1");
var input_file_radiobutton = document.getElementById("customRadioInline2");
var load_button_label = document.getElementById('load_button_label');
var load_button = document.getElementById('load_button');
var start_button = document.getElementById('start_button');
var user_text = document.getElementById('exampleFormControlTextarea1');
var loaded_text_label = document.getElementById('loaded_text_label');
var results_label = document.getElementById('results_label');
var the_spinner = document.getElementById('the_spinner');


//radiobuttons functionality START
//////////////////////////////////
input_file_radiobutton.addEventListener('click', function (e) {
  if (input_file_radiobutton.checked) {
    load_button_label.className = "btn btn-primary btn-sm";
    load_button.disabled = false;
    user_text.value = "";
  }
})

input_text_radiobutton.addEventListener('click', function (e) {
  if (input_text_radiobutton.checked) {
    load_button_label.className = "btn btn-secondary btn-sm";
    load_button.disabled = true;
    user_text.value = "";
    loaded_text_label.innerText = "";

  }
})
//radiobuttons functionality ENDED
//////////////////////////////////



// load button functionality START
//////////////////////////////////

// this function clears the value kept in the button so that
// a file is loaded each time, not only when a new file is chose
load_button.addEventListener('click', function (e) {
  load_button.value = "";
});


var openFile = function(event) {
  var input = event.target;
  var reader = new FileReader();
  reader.onload = function(){
    var text = reader.result;
    var fileName = document.getElementById('load_button').files[0].name;
    user_text.value = text;
    loaded_text_label.innerText = "Loaded: " + fileName;
  };
  reader.readAsText(input.files[0]);
};


// load button functionality ENDED
//////////////////////////////////



// start button functionality START
///////////////////////////////////
start_button.addEventListener('click', function (e) {
  let xhr = new XMLHttpRequest();

  xhr.onreadystatechange = function (e) {
    if (xhr.readyState == 4 && xhr.status == 200) {
      // obtaining the json response
      let json_response = xhr.responseText;
      // transforming the json response to js object
      let response_object = JSON.parse(json_response);
      let converted_file_name = response_object.result;

      results_label.style.visibility = 'hidden';
      the_spinner.style.visibility = 'hidden';

      // creating and activating the download link
      let link = document.createElement('a');
      link.href = '/media/' + converted_file_name;
      link.download = converted_file_name;
      document.body.appendChild(link);
      link.click();
    };
  };

  var user_text_with_punctuation = user_text.value;
  var user_text_without_punctuation = user_text_with_punctuation.match(/[^_\W]+/g).join(' ');

  results_label.style.visibility = 'visible';
  the_spinner.style.visibility = 'visible';


  xhr.open('POST', '/convert_user_text/', true);
  xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8');
  var data = 'user_text=' + user_text_without_punctuation;
  xhr.send(data);

})
// start button functionality ENDED
///////////////////////////////////
