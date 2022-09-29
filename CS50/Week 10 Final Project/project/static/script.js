// Show A Load Screen
function loadScreen() {
    setTimeout(function(){
        document.querySelector('body').classList.add('loaded');
    }, 500);
}

// Validate Password While Typing
function verifyPassword() {
    var x = document.getElementById("inputPassword");
    var lower = document.getElementById("lower");
    var upper = document.getElementById("upper");
    var number = document.getElementById("number");
    var length = document.getElementById("length");
    var valid = /(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}/;
    // Control validity while still typing
    if (x.value.length > 0) {
        x.classList.add("is-invalid");
    } else {
        x.classList.remove("is-invalid");
    }
    // Validate lowercase letters
    var lowerCaseLetters = /[a-z]/g;
    if (x.value.match(lowerCaseLetters)) {
        lower.classList.add("invalid-feedback");
    } else {
        lower.classList.remove("invalid-feedback");
    }
    // Validate uppercase letters
    var upperCaseLetters = /[A-Z]/g;
    if (x.value.match(upperCaseLetters)) {
        upper.classList.add("invalid-feedback");
    } else {
        upper.classList.remove("invalid-feedback");
    }
    // Validate numbers
    var numbers = /[0-9]/g;
    if (x.value.match(numbers)) {
        number.classList.add("invalid-feedback");
    } else {
        number.classList.remove("invalid-feedback");
    }
    // Validate length
    if (x.value.length >= 8) {
        length.classList.add("invalid-feedback");
    } else {
        length.classList.remove("invalid-feedback");
    }
    // Validate entire input
    if (x.value.match(valid)) {
        x.classList.remove("is-invalid");
        x.classList.add("is-valid");
    } else {
        x.classList.remove("is-valid");
    }
}//https://www.w3schools.com/howto/howto_js_password_validation.asp


// Toggle password visibility on click of icon
function togglePassword() {
    // The eye icon
    var eye = document.getElementById('togglePassword');
    // The typed password
    var password = document.getElementById('floatingPassword_1');
    // Swap types on click
    var type = password.getAttribute('type') === 'password' ? 'text' : 'password';
    password.setAttribute('type', type);
    // Swap icons on click
    eye.classList.toggle("bi-eye-slash")
    eye.classList.toggle("bi-eye")
}


// Toggle eye icon visibility when typing starts in password field
function toggleIcon() {
    // The eye icon and span container
    var eye = document.getElementById('togglePassword');
    var container = document.getElementById('iconContainer');
    // The typed password
    var password = document.getElementById('floatingPassword_1');
    // Only show eye icon if there is a password to show
    if (password.value.length > 0) {
        eye.style.display = "block";
        container.style.display = "block";
        password.classList.add("pe-5");
    // Else hide icon
    } else {
        eye.style.display = "none";
        container.style.display = "none";
        password.classList.remove("pe-5");
    }
}


// Set modal subtitle and form field to notebook number origin
function setNotebookNumber() {
    var modal = document.getElementById('experimentModal');
    modal.addEventListener('show.bs.modal', function (event) {
        var trigger = event.relatedTarget;
        // Get notebook number
        var target = parseInt(trigger.getAttribute('data-bs-button'));
        // Gather elements by class name
        var elements = document.getElementsByClassName('notebook_no');
        // Get paragraph tag and set inner text
        elements[0].innerText = 'Notebook No. ' + target;
        // Get input field and set value
        elements[1].setAttribute('value', target);
    });
}


// Enable form fields on double click of jumbotron window
function toggleFields(number, exp = null) {
    // For index.html page elements
    if (exp == null) {
        if (document.getElementById('course-' + number).disabled == true) {
            // Enable elements
            document.getElementById('course-' + number).disabled = false;
            document.getElementById('section-' + number).disabled = false;
            document.getElementById('semester-' + number).disabled = false;
            document.getElementById('year-' + number).disabled = false;
            document.getElementById('instructor-' + number).disabled = false;
            // Show save button
            document.getElementById('edit_nb-' + number).style.display = "block";
            // Show delete notebook button
            document.getElementById('deleteNbBtn-' + number).style.display = "block";
            // Show delete experiment buttons
            var exp = document.getElementsByClassName('deleteExpBtn');
            var i;
            // Only show icons for this notebooks experiments
            if (exp.length > 0) {
                for (i = 0; i < exp.length; i++) {
                    let id = (exp[i].id).split("-");
                    if (id[1] == number) {
                         exp[i].style.display = "block"
                    }
                }
            }
            // Show tab's color selector
            document.getElementById('colorMenu-' + number).style.display = "block";
        } else {
            // Disable elements
            document.getElementById('course-' + number).disabled = true;
            document.getElementById('section-' + number).disabled = true;
            document.getElementById('semester-' + number).disabled = true;
            document.getElementById('year-' + number).disabled = true;
            document.getElementById('instructor-' + number).disabled = true;
            // Hide save button
            document.getElementById('edit_nb-' + number).style.display = "none";
            // Hide delete notebook button
            document.getElementById('deleteNbBtn-' + number).style.display = "none";
            // Hide delete experiment buttons
            var exp = document.getElementsByClassName('deleteExpBtn');
            var i;
            // Only hide icons for this notebooks experiments
            if (exp.length > 0) {
                for (i = 0; i < exp.length; i++) {
                    let id = (exp[i].id).split("-");
                    if (id[1] == number) {
                         exp[i].style.display = "none";
                    }
                }
            }// Hide tab's color selector
            document.getElementById('colorMenu-' + number).style.display = "none";
        }
    // For experiment.html page
    } else {
        if (document.getElementById('topic-' + number + '-' + exp).disabled == true) {
            // Enable elements
            document.getElementById('topic-' + number + '-' + exp).disabled = false;
            document.getElementById('partners-' + number + '-' + exp).disabled = false;
            document.getElementById('desk-' + number + '-' + exp).disabled = false;
            // Show save button
            document.getElementById('edit_nb-' + number + '-' + exp).style.display = "block";
        } else {
            // Disable elements
            document.getElementById('topic-' + number + '-' + exp).disabled = true;
            document.getElementById('partners-' + number + '-' + exp).disabled = true;
            document.getElementById('desk-' + number + '-' + exp).disabled = true;
            // Hide save button
            document.getElementById('edit_nb-' + number + '-' + exp).style.display = "none";
        }
    }
}

// Show new badge on create notebook button
function showNotice(type) {
    if (type == 'notebook') {
        document.getElementById('newNotice-Nb').style.display = "block";
    } else if (type == 'experiment') {
        document.getElementById('newNotice-Exp').style.display = "block";
    }
}

// Change notebook tab color and associated elements
function changeColor(number, color) {

    // Set last clicked color for submission
    document.getElementById("lastClickedColor_nb-" + number).setAttribute('value', color["id"]);
    // Change color picker button icon color
    document.getElementById("changeColor-" + number).style.backgroundColor = "#" + color["base_hex"];

    // Initialize
    var tab = document.getElementById("notebook-" + number + "-tab");
    var toc = document.getElementById("toc_header_nb-" + number);
    var tbl_header = document.getElementById("table_header_nb-" + number);
    var nb = document.getElementById("notebook-" + number);
    var tbl = document.getElementById("table_nb-" + number);
    var srtBtn = document.getElementById("sortMenu-" + number);
    var edtBtn = document.getElementById("edit_nb-" + number);
    var colorBtn = document.getElementById("colorMenu-" + number);
    var addExpBtn = document.getElementById("add_exp_nb-" + number);

    // Tab Colors
    tab.style.backgroundColor = "#" + color["base_hex"];
    tab.style.color = "#" + color["text"];
    tab.style.borderColor = "#" + color["base_hex"];

    // Table of contents header and experiements table header colors
    toc.style.setProperty("background-color", "#" + color["header"], "important");
    toc.style.color = "#" + color["text"];
    tbl_header.style.setProperty("background-color", "#" + color["header"], "important");
    tbl_header.style.color = "#" + color["text"];

    // Notebook Background
    nb.style.backgroundColor = "#" + color["base_hex"];

    // All enabled form field colors and borders
    for (var i = 0; i < 8; i++) {
        toc.querySelectorAll("input")[i].style.backgroundColor = "#" + color["enabled"];
        toc.querySelectorAll("input")[i].style.color = "#" + color["text"];
        toc.querySelectorAll("input")[i].style.borderColor = "#" + color["border"];
    }
    for (var i = 0; i < 2; i++) {
        toc.querySelectorAll("select")[i].style.backgroundColor = "#" + color["enabled"];
        toc.querySelectorAll("select")[i].style.color = "#" + color["text"];
        toc.querySelectorAll("select")[i].style.borderColor = "#" + color["border"];
    }

    // All disabled form fields colors and borders
    for (var i = 0; i < 8; i++) {
        toc.querySelectorAll("span")[i].style.backgroundColor = "#" + color["disabled"];
        toc.querySelectorAll("span")[i].style.color = "#" + color["text"];
        toc.querySelectorAll("span")[i].style.borderColor = "#" + color["border"];
    }
    for (var i = 0; i < 3; i++) {
        toc.querySelectorAll("input[disabled]")[i].style.backgroundColor = "#" + color["disabled"];
        toc.querySelectorAll("input[disabled]")[i].style.color = "#" + color["text"];
    }

    // Buttons
    edtBtn.style.borderColor = "#" + color["button"];
    colorBtn.style.borderColor = "#" + color["button"];
    addExpBtn.style.borderColor = "#" + color["button"];
    srtBtn.style.borderColor = "#" + color["button"];

    edtBtn.style.backgroundColor = "#" + color["button"];
    colorBtn.style.backgroundColor = "#" + color["button"];
    addExpBtn.style.backgroundColor = "#" + color["button"];
    srtBtn.style.backgroundColor = "#" + color["button"];

    edtBtn.style.color = "#" + color["text"];
    colorBtn.style.color = "#" + color["text"];
    addExpBtn.style.color = "#" + color["text"];
    srtBtn.style.color = "#" + color["text"];

    // Table
    tbl.style.color = "#" + color["text"];
    tbl.style.backgroundColor = "#" + color["disabled"];
    tbl.style.borderColor = "#" + color["border"];

}

function setTheme(number, base, id, disabled, enabled, border, text, rgb, exp=null) {
    // Set notebook themes on index.html
    if (exp == null) {
        // Change color picker button icon color
        document.getElementById("changeColor-" + number).style.backgroundColor = "#" + base;
        // Set last clicked color for submission
        document.getElementById("lastClickedColor_nb-" + number).setAttribute('value', id);
        // If there is a theme set
        if (id != 0) {
            // Initialize HTML element
            var style = document.createElement('style');
            // Create new style sheet for additional technical theme changes
            style.innerHTML =
                '#notebook-' + number + '-tab:hover {' +
                    'background-image: var(--bs-gradient);' +
                '}' +
                '#first-' + number + ':disabled, #last-' + number + ':disabled, #course-' + number +
                ':disabled, #section-' + number + ':disabled, #semester-' + number + ':disabled, #year-' + number +
                ':disabled, #instructor-' + number + ':disabled, #partners-' + number + '{' +
                    'background-color: #' + disabled + ';' +
                    'color: #' + text + ';' +
                    'border-color: #' + border + ';' +
                '}' +
                '#course-' + number + ', #section-' + number + ', #semester-' + number +
                ', #year-' + number + ', #instructor-' + number + '{' +
                    'background-color: #' + enabled + ';' +
                    'color: #' + text + ';' +
                    'border-color: #' + border + ';' +
                '}' +
                '#course-' + number + ':focus, #section-' + number + ':focus, #semester-' + number +
                ':focus, #year-' + number + ':focus, #instructor-' + number + ':focus{' +
                    'box-shadow: 0 0 0 0.25rem rgba(' + rgb + ',0.5);' +
                '}' +
                '#table_nb-' + number + ' tbody tr:hover td {' +
                    'background: #' + enabled + ';' +
                    'color: #' + text + ';' +
                    'box-shadow: none;' +
                '}' +
                '#sort_nb-' + number + ' .dropdown-menu.dropdown-item:focus, #sort_nb-' + number +
                ' .dropdown-item:hover {' +
                    'background: #' + disabled + ';' +
                    'color: #' + text + ';' +
                '}' +
                '#sort_nb-' + number + ' .dropdown-menu {' +
                    'background-color: #' + enabled + ';' +
                '}' +
                '#sort_nb-' + number + ' .dropdown-menu .dropdown-item {' +
                    'color: #' + text + ';' +
                '}' +
                '#sortMenu-' + number + ':hover, #edit_nb-' + number + ':hover, #colorMenu-' + number +
                ':hover, #add_exp_nb-' + number + ':hover {' +
                    'background-color: #' + disabled + '!important;' +
                    'border-color: #' + disabled + '!important;' +
                '}';
        // Get script tag that called this function
        var ref = document.querySelector("script[id$=setStyle_nb-" + number + "]");
        // Insert new styles before desired script tag
        ref.parentNode.insertBefore(style, ref);
        }
    // Set experiment header theme on experiment.html page
    } else {
        // If there is a theme set
        if (id != 0) {
            // Initialize HTML element
            var style = document.createElement('style');
            // Create new style sheets using obnoxious method to alter disabled and enabled CSS properties individually
            // as well as focus and active styles per new notebook created
            style.innerHTML =
                '#topic-' + number + '-' + exp + ':disabled, #date-' + number + '-' + exp + ':disabled, #course-' + number + '-' + exp +
                ':disabled, #section-' + number + '-' + exp + ':disabled, #partners-' + number + '-' + exp + ':disabled, #first-' + number + '-' + exp +
                ':disabled, #last-' + number + '-' + exp + ':disabled, #desk-' + number + '-' + exp + ':disabled {' +
                    'background-color: #' + disabled + ';' +
                    'color: #' + text + ';' +
                    'border-color: #' + border + ';' +
                '}' +
                '#topic-' + number + '-' + exp + ', #partners-' + number + '-' + exp + ', #desk-' + number + '-' + exp + '{' +
                    'background-color: #' + enabled + ';' +
                    'color: #' + text + ';' +
                    'border-color: #' + border + ';' +
                '}' +
                '#topic-' + number + '-' + exp + ':focus, #partners-' + number + '-' + exp + ':focus, #desk-' + number + '-' + exp + ':focus{' +
                    'box-shadow: 0 0 0 0.25rem rgba(' + rgb + ',0.5);' +
                '}' +
                '#edit_nb-' + number + '-' + exp + ':hover {' +
                    'background-color: #' + disabled + ';' +
                    'border-color: #' + disabled + ';' +
                '}';
        // Get script tag that called this function
        var ref = document.querySelector("script[id$=setStyle-" + number + '-' + exp + "]");
        // Insert new styles before desired script tag
        ref.parentNode.insertBefore(style, ref);
        }
    }
}