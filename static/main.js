
/* MAIN JAVASCRIPT SCRIPT FOR DYNAMIC PAGES*/

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

