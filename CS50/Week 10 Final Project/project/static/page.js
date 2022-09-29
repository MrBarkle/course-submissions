// Declare and initialize global variables for page event handling

// The page that preceeds the curr
var prev =  null;
// The page currently in focus
var curr = document.getElementById('page-1');
// Set focus to initial page-1
curr.focus();
// The page that follows curr
var next = null;
// The last known position of the caret cursor inside of curr
var pos = 0;
// The last known selection range inside of curr
var globalRange = null;

// Initialize page-1 with event listeners
curr.addEventListener('keyup', getCaretIndex); // Key movement
curr.addEventListener('mouseup', getCaretIndex); // Click release
curr.addEventListener('paste', getCaretIndex); // Clipboard actions
curr.addEventListener('cut', getCaretIndex);
curr.addEventListener('select', getCaretIndex); // Some browsers support this event
curr.addEventListener('selectstart', getCaretIndex); // Some browsers support this event


// Copy inner text of element and notify user
function copyText(td) {
    // Copy text
    navigator.clipboard.writeText(td.textContent);
    // Save old text
    var old = td.textContent;
    // Notify user with class styling
    td.classList.add('copied');
    // Change text to copied
    td.textContent = "Copied!"
    // Wait 1 second
    setTimeout(function(){
        // Change text back
        td.textContent = old;
        // Remove styling class
        td.classList.remove('copied');
    }, 1000)
}

function submit(type) {
    // Get key strokes
    var key = event.keyCode || event.charCode || event.key;
    // Look for 'enter' key press
    if (key == 13) {
        // If inside linkModal
        if (type == 'link') {
            // Get modal
            var linkModal = document.getElementById('linkModal');
            // Get current instance of modal
            var instance = bootstrap.Modal.getInstance(linkModal);
            // Insert link
            insertLink();
            // hide modal
            instance.hide();
        } else if (type == 'table') {
            // Get modal
            var tableModal = document.getElementById('tableModal');
            // Get current instance of modal
            var instance = bootstrap.Modal.getInstance(tableModal);
            // Insert table
            insertTable();
            // hide modal
            instance.hide();
        }
    }
}


// Format document based on input
function formatDoc(commandName, valueArgument) {
    document.execCommand(commandName, false, valueArgument);
}// Adapted from https://developer.mozilla.org/en-US/docs/Web/Guide/HTML/Editable_content


// Insert html element at caret point
function pasteHtmlAtCaret(html_element) {
    var sel
    if (window.getSelection) {
        sel = window.getSelection();
        if (sel.getRangeAt && sel.rangeCount && globalRange) {
            globalRange.deleteContents();

            var frag = document.createDocumentFragment(), lastNode;
            lastNode = frag.appendChild(html_element);

            globalRange.insertNode(frag);

            // Preserve the selection
            if (lastNode) {
                globalRange = globalRange.cloneRange();
                globalRange.setStartAfter(lastNode);
                globalRange.collapse(true);
                sel.removeAllRanges();
                sel.addRange(globalRange);
            }
        }
    }
}// Adapted from: https://jsfiddle.net/Xeoncross/4tUDk


// Insert link
function insertLink() {

    // Create link tags
    var a = document.createElement('a');

    // Get link input from user
    var link = document.getElementById('floatingLink').value;

    // If link destination matches criteria
    if (link && link !='' && link != 'http://') {

        // Set href to link
        a.href = link;

        // Set on hover display title text
        a.title = link;
    }

    // Link text
    var linkText;

    // If text was highlighted
    if (globalRange && globalRange.toString() != '') {

        // Get link text as highlighted text
        linkText = document.createTextNode(globalRange.toString());

        // Set link text
        a.appendChild(linkText);

    // If text wasn't highlighted
    } else {
        // Get link text as user input url
        linkText = document.createTextNode(link);

        // Set link text
        a.appendChild(linkText);
    }

    // Clear field input for next use
    document.getElementById('floatingLink').value = 'http://';

    // Place link in document
    pasteHtmlAtCaret(a);
}


// Insert Table
function insertTable() {

    // Check if a table has been created
    if (typeof tableCount !== 'undefined') {
        // Increment global count
        tableCount += 1;
    // If other tables exist
    } else {
        // Increment global count BASE ON OTHER EXISTING TABLES FOR BEST PRACTICES
        globalThis.tableCount = 1;
    }

    // Create table tags
    var table = document.createElement('table');

    // Get dimensions from users
    var col = document.getElementById('floatingCol').value;
    var row = document.getElementById('floatingRow').value;

    // Add bootstrap styling
    table.classList.add('table', 'table-bordered', 'table-hover', 'position-relative');

    // Set dynamic table id
    table.setAttribute('id', 'table-' + tableCount);

    // Loop through adding rows
    for (i = 0; i < Number(row); i++) {
        var tr = table.insertRow();
        tr.setAttribute('id', 'table-' + tableCount + '-row-' + (Number(i) + 1));

        // Set a default height for rows
        tr.style.height = '41px';

        // Loop through adding columns
        for (j = 0; j < Number(col); j++) {
            var td = tr.insertCell();
            td.setAttribute('onclick', 'toggleTableOptions();')
            td.setAttribute('id', 'table-' + tableCount + '-row-' + (Number(i) + 1) + '-col-' + (Number(j) + 1));
            //td.style.resize = 'horizontal';
            //td.style.overflow = 'auto';
        }
    }// Adapted from: https://stackoverflow.com/questions/14643617/create-table-using-javascript

    // Insert table into document at desired location
    pasteHtmlAtCaret(table);
}


// Table options on focus of table
function toggleTableOptions(table) {
    var toolbar = document.getElementById('tableToolbar');
    toolbar.classList.remove('visually-hidden');

    var parent = globalRange.commonAncestorContainer.parentElement;
    var tagName = 'tr';

    // Loop until desired row is found
    while (parent) {
        // If row tags found
        if (parent.tagName && parent.tagName.toLowerCase() == tagName) {
            var rowIndex = parent.rowIndex;
            // Set toolbar location
            toolbar.style.top = 68 + (41 * rowIndex) + 'px';
            return;
        // Keep looping
        } else {
            // Move to next parent
            parent = parent.parentElement;
        }
    }
}

// table toolbar functions
function tableFunction(commandName) {
    var colTag = 'td';
    var table = globalRange.commonAncestorContainer;
    var tableCount = 0;

    // Loop until table is identified
    while (table) {
        // If table found
        if (table.tagName && table.tagName.toLowerCase() == colTag) {
            // Get table id and count number
            tableCount = Number(table.id.split('-')[1]);
            var tableID = 'table-' + tableCount;
            table = document.getElementById(tableID);
            break;
        // Keep looping
        } else {
            // Move to next parent
            table = table.parentElement;
        }
    }

    // Get table col and row counts
    var colCount = table.rows[0].cells.length;
    var rowCount = table.rows.length;

    // Insert blank row
    if (commandName == "add_row") {
        var row = table.insertRow(-1);
        row.style.height = '41px';
        row.setAttribute('id', 'table-' + tableCount + '-row-' + (Number(rowCount) + 1));
        // Iterate over cell count filling entire new row
        for (i = 0; i < colCount; i++) {
            var cell = row.insertCell(i);
            cell.setAttribute('onclick', 'toggleTableOptions();');
            cell.setAttribute('id', 'table-' + tableCount + '-row-' + (Number(rowCount) + 1) + '-col-' + (Number(i) + 1));
        }

    // Insert blank column
    } else if (commandName == "add_col") {
        // Iterate over existing rows
        for (i = 0; i < rowCount; i++){
            // Insert one cell to each row
            var row = table.rows[i];
            var cell = row.insertCell(-1);
            cell.setAttribute('onclick', 'toggleTableOptions();');
            cell.setAttribute('id', 'table-' + tableCount + '-row-' + (Number(i) + 1) + '-col-' + (Number(colCount) + 1));
        }

    // Add header to table
    } else if (commandName == "head") {
        var header = table.createTHead();
        var row = header.insertRow(0);
        row.style.height = '41px';
        // Create entire header row
        for (i = 0; i < colCount; i++) {
            var headerCell = document.createElement("th");
            headerCell.setAttribute('onclick', 'toggleTableOptions();');
            row.appendChild(headerCell);
        }

    // Delete active row
    } else if (commandName == "del_row") {
        // Start with the cell that was last clicked
        var parent = globalRange.commonAncestorContainer.parentElement;
        var tagName = 'tr';

        // Loop until desired row is found
        while (parent) {
            // If row tags found
            if (parent.tagName && parent.tagName.toLowerCase() == tagName) {
                // Get row index
                var rowIndex = parent.rowIndex;
                // Delete row
                table.deleteRow(rowIndex);
                return;
            // Keep looping
            } else {
                console.log("parent was " + parent);
                // Move to next parent
                parent = parent.parentElement;
                console.log("parent is now " + parent);
            }
        }

    // Delete active column
    } else if (commandName == "del_col") {

        // This may be <td> or some form of text
        var parent = globalRange.commonAncestorContainer;
        var headColTag = 'th';
        while (parent) {
            // If column tags found for header or main table body
            if ((parent.tagName && parent.tagName.toLowerCase() == colTag) || (parent.tagName && parent.tagName.toLowerCase() == headColTag)) {
                // Get column index
                var colIndex = parent.cellIndex;
                // Loop over each row, deleting the specified cell index
                for (i = 0; i < rowCount; i++) {
                    var row = table.rows[i]
                    row.deleteCell(colIndex);
                }
                return;
            } else {
                parent = parent.parentElement;
                console.log(parent.tagName);
            }
        }

    }
}


// Change alginment button image on click of dropdown item
function changeImage(buttonName, source) {
    if (buttonName == "align") {
        var button = document.getElementById("dynamic_align");
        if (source == "left") {
            button.innerHTML = '<i class="fas fa-align-left mr-2"></i> ';
        } else if (source == "right") {
            button.innerHTML = '<i class="fas fa-align-right mr-2"></i> ';
        } else if (source == "center") {
            button.innerHTML = '<i class="fas fa-align-center mr-2"></i> ';
        } else if (source == "justify") {
            button.innerHTML = '<i class="fas fa-align-justify mr-2"></i> ';
        }
    } else if (buttonName == "style") {
        var button = document.getElementById("dynamic_style");
        if (source == "p") {
            button.innerText = "Paragraph ";
        } else if (source == "h1") {
            button.innerText = "Heading 1 ";
        } else if (source == "h2") {
            button.innerText = "Heading 2 ";
        } else if (source == "h3") {
            button.innerText = "Heading 3 ";
        } else if (source == "h4") {
            button.innerText = "Heading 4 ";
        } else if (source == "h5") {
            button.innerText = "Heading 5 ";
        } else if (source == "h6") {
            button.innerText = "Heading 6 ";
        }
    } else if (buttonName == "font") {
        var button = document.getElementById("dynamic_font");
        if (source == "1") {
            button.innerText = "Arial";
        } else if (source == "2") {
            button.innerText = "Arial Black";
        } else if (source == "3") {
            button.innerText = "Brush Script MT";
        } else if (source == "4") {
            button.innerText = "Courier New";
        } else if (source == "5") {
            button.innerText = "Garamond";
        } else if (source == "6") {
            button.innerText = "Georgia";
        } else if (source == "7") {
            button.innerText = "Helvetica";
        } else if (source == "8") {
            button.innerText = "Tahoma";
        } else if (source == "9") {
            button.innerText = "Times New Roman";
        } else if (source == "10") {
            button.innerText = "Trebuchet MS";
        } else if (source == "11") {
            button.innerText = "Verdana";
        }
    }
}


// On focus of page, update global variables
function onFocus(element) {
    // Set page currently in focus
    curr = element;
    // If the current page in focus has a predecessor
    if (curr.previousElementSibling != null) {
        // Set prev to that page
        prev = curr.previousElementSibling;
    // If not, the first page is in focus
    } else {
        // Set prev to null
        prev = null;
    }
    // If the current page is not followed by any other pages
    if (curr.nextElementSibling != null) {
        // Set next to that page
        next = curr.nextElementSibling;
    // If not, the last page is in focus
    } else {

        // Set next to null
        next = null;
    }
}

/*
// Add a new contentEditable div page to the document
function createPage(attrs) {
    // Create the page
    var page = document.createElement('div');
    // Get the container that holds contentEditable pages
    var parent = document.getElementById('outerTextBox');
    // Set page attributes
    for (var key in attrs) {
        if (attrs.hasOwnProperty(key)) {
            page.setAttribute(key, attrs[key]);
        }
    }
    // Set id to next page number
    page.id = 'page-' + (parent.childElementCount + 1);
    if (parent) {
        parent.appendChild(page);
    }

    // This next section taken from: https://stackoverflow.com/questions/53999384/javascript-execute-when-textarea-caret-is-moved

    // When caret moves by any action, call function to update global variable position
    const target = document.getElementById(page.id);
    target.addEventListener('keyup', getCaretIndex); // Key movement
    target.addEventListener('mouseup', getCaretIndex); // Click release
    target.addEventListener('paste', getCaretIndex); // Clipboard actions
    target.addEventListener('cut', getCaretIndex);
    target.addEventListener('select', getCaretIndex); // Some browsers support this event
    target.addEventListener('selectstart', getCaretIndex); // Some browsers support this event

    // Set focus to new page, updating globals
    page.focus();

}*/

/*
// Delete a contentEditable div page from document and set focus to previous existing page
function deletePage(parent) {
    // Delete current page
    parent.removeChild(curr);
    // Set focus to fallback page, updating globals
    prev.focus();
    // Set cursor to end caret position if text is present on previous (now curr) page
    if (curr.lastChild) {
        // Create a range
        var range = document.createRange();
        // Get selection
        var selection = window.getSelection();
        // Place caret to end position
        range.setStart(curr.lastChild, 0);
        range.collapse(true);
        selection.removeAllRanges();
        selection.addRange(range);
    }
}*/

/*
// Handle creation and deletion of new pages based on typing
function pageHandler(element) {
    // The container that holds contentEditable pages
    var parent = document.getElementById("outerTextBox");
    // Get all of the text on current page by element
    var children = document.getElementById(element.id).children;
    // Keep track of total element heights on page
    var totalHeight = 0;
    // Listen for specific key press
    var key = event.keyCode || event.charCode || event.key;

    // If backspace is pressed and cursor is at page start
    if (key == 8 && getCaretIndex() == 0) {
        // Check if there is another page to fall back on
        if (element.previousElementSibling != null) {
            // Get previous page and page number
            var prevNumber = Number(element.id.split("-")[1]) - 1;
            var prevPage = document.getElementById("page-" + prevNumber);
            // Make sure there is not text on current page
            if (element.childNodes.length == 0) {
                // Delete current page
                deletePage(parent);
            // If there is text on current page
            } else {
                console.log("need to push text backward word by word");
                // Take 'word' from next and place it on prev
                // replacing one 'character' at a time for each
                // 'character' in 'word'
            }
        }

    // On any other document altering key press
    } else if ((key >= 48 && key <= 57) || (key >= 65 && key <= 90) || (key >= 97 && key <= 122) || (key == 13) || (key == 32)) {
        // Keep track of text on page, making sure it does not exceed margins
        for (i = 0; i < children.length; i++) {
            let style = getComputedStyle(children[i]);
            let marginBottom = parseInt(style.marginBottom);
            totalHeight += Number(children[i].clientHeight + marginBottom);
        }
        // If page margin is reached
        if (totalHeight == 960) {


        // If text goes over page margin
        } else if (totalHeight > 960) {
            // If next sibling page does not exist
            if (document.getElementById('page-' + Number(element.id + 1)) != true) {
                // Get next page's number
                var nextNumber = Number(element.id.split("-")[1]) + 1;
                // Create next page
                createPage({'class': 'm-3 p-5 mx-auto shadow border border-light experiment-text-box', 'contentEditable': 'true', 'onkeydown': 'pageHandler(this);', 'onfocus': 'onFocus(this);'});
                // Get next page
                var nextPage = document.getElementById('page-' + nextNumber);
                // Set new previous page
                prevPage = element;
                // Set new current page
                element = nextPage;
                // Point nextPage to null
                nextPage = null;
            }
        }

    } else {
        // Arrow keys should be able to move focus between pages
    }
} */


// Get index position of caret
function getCaretIndex() {
    let position = 0;
    const isSupported = typeof window.getSelection !== "undefined";
    if (isSupported) {
        // Determine if text is highlighted
        const selection = window.getSelection();
        // Check if there is a text selection (i.e. cursor in place)
        if (selection.rangeCount !== 0) {
            // Store the original range
            const range = window.getSelection().getRangeAt(0);
            // Set global variable
            globalRange = range;
            // Clone the range
            const preCaretRange = range.cloneRange();
            // Select all textual contents from the contenteditable element
            preCaretRange.selectNodeContents(curr);
            // And set the range end to the original clicked position
            preCaretRange.setEnd(range.endContainer, range.endOffset);
            // Return the text length from contenteditable start to the range end
            position = preCaretRange.toString().trim().length;
            // White space also trimmed as additional modification to original JS
        }
    }
    // Set global variable for caret position
    pos = position;
    // Return Position
    return position;
}// Modification of Konstantin Münster's JS at
 // https://javascript.plainenglish.io/how-to-find-the-caret-inside-a-contenteditable-element-955a5ad9bf81


// https://stackoverflow.com/questions/6247702/using-html5-how-do-i-use-contenteditable-fields-in-a-form-submission
function copyContent () {
    document.getElementById("experimentContent").value =
        document.getElementById("page-1").innerHTML;
    return true;
}
