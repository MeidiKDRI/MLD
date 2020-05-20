
/* MAIN JAVASCRIPT SCRIPT FOR DYNAMIC PAGES*/


/* Upload with progressbar */

var progress = document.getElementById('progress');
var progress_wrapper = document.getElementById('progress_wrapper');
var progress_status = document.getElementById('progress_status');

var upload_btn = document.getElementById('upload_btn');

var alert_wrapper = document.getElementById('alert_wrapper');

var input = document.getElementById('file_input');
var file_input_label = document.getElementById('file_input_label');

/* Show the filename inside the custom file input */
function input_filename() {
    file_input_label.innerText = input.files[0].name;
}

/* Upload the file */

function upload(url){

    if (!input.value) {
        return; /* Do nothing for now >>> TODO display an alert */
    }

    progress_wrapper.classList.remove("d-none");

  // request progress handler
  request.upload.addEventListener("progress", function (e) {

    // Get the loaded amount and total filesize (bytes)
    var loaded = e.loaded;
    var total = e.total

    // Calculate percent uploaded
    var percent_complete = (loaded / total) * 100;

    // Update the progress text and progress bar
    progress.setAttribute("style", `width: ${Math.floor(percent_complete)}%`);
    progress_status.innerText = `${Math.floor(percent_complete)}% uploaded`;

  })
}



/* Select input */

/* Display the selection of the select input */
function selected(select_input, selected) {
    var selection = document.getElementById(select_input).value;
    document.getElementById(selected).innerHTML = selection;
    }


/* Checkbox */

/* Display dynamically a box when the checkbox is selected */
function isChecked(checkbox, box) {
    var chboxs = document.getElementsByName(checkbox);
    var display = "none";
    for(var i=0;i<chboxs.length;i++) { 
        if(chboxs[i].checked){
        display = "block";
            break;
        }
    }
    document.getElementById(box).style.display = display;
    }




function drop(){

    document.getElementById('drop_col_selector').value;
    var fd = new FormData(document.forms['droping']);

    var xhr = new XMLHttpRequest({mozSystem: true});
    xhr.open('POST', 'http://127.0.0.1:5000/test', true);

    xhr.onreadystatechange = function(){
        if (xhr.readyState == XMLHttpRequest.DONE) {
            document.getElementById('num').innerHTML = xhr.responseText;
        }

        xhr.onload = function() {
        };
        xhr.send(fd);
    }
}


$(document).ready(function() {
    $('form1').on('submit', function(event) {
        $.ajax({
            data : {
                colonne : $('#drop_col_selector').val(),
            },
            type : 'POST',
            url : '/process'
        })
        .done(function(data) {
            $('#num').text(data.colonne).show();
            
        });
        event.preventDefault();
    });
});