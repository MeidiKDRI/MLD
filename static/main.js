
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
    let selection = document.getElementById(select_input).value;
    document.getElementById(selected).innerHTML = selection;
    }


/* Checkbox */

/* Display dynamically a box when the checkbox is selected */
function isChecked(checkbox, box) {
    let chboxs = document.getElementsByName(checkbox);
    let display = "none";
    for(let i=0;i<chboxs.length;i++) { 
        if(chboxs[i].checked){
        display = "block";
            break;
        }
    }
    document.getElementById(box).style.display = display;
    }



jQuery(function() {
    jQuery("#varia").change(function() {
        var firstName = $(this).val();
        jQuery.ajax({
        url: "/process",
        type: "GET",
        data: {
            "firstName": String(firstName)
            
        },
        dataType: "html",
        success: function(data) {

            jQuery("#output").html(data);
        }
        });
    });
    console.log(firstName)

    });