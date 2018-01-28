editing = false;
var start;
var end;
var comments = "";

var content = document.getElementById("contents");

document.getElementById("edit").onclick = function(e) {
    editing = !editing;
    if (editing) {
        var ta = document.createElement("TEXTAREA");
        ta.value = content.innerHTML;
        var numlines = ta.value.split("\n").length;
        ta.onselect = function(e) {
            start = e.originalTarget.selectionStart;
            end = e.originalTarget.selectionEnd;
            console.log(ta.value.substring(start, end))

        }
        content.innerHTML = "";
        ta.setAttribute("rows", numlines);
        ta.style.border = "none";
        content.appendChild(ta);
    } else {
        content.innerHTML = content.firstChild.value;
    }
}

