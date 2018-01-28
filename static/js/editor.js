editing = false;
var start;
var end;
var comments = [];
var loc = window.location.href;
if (loc.indexOf("#") != -1) {
    loc = loc.substring(0, loc.indexOf("#"));
}
var page = Number(loc.substring(loc.lastIndexOf("/") + 1));

var content = document.getElementById("contents");
var editbtn = document.getElementById("edit");
editbtn.onclick = function(e) {
    editing = !editing;
    if (editing) {
        editbtn.innerText = "Cancel Editing";
        var ta = document.createElement("TEXTAREA");
        ta.value = content.innerHTML;
        var numlines = ta.value.split("\n").length;
        ta.onselect = function(e) {
            start = e.originalTarget.selectionStart;
            end = e.originalTarget.selectionEnd;
            console.log(ta.value.substring(start, end));
            var commentdiv = document.getElementById("blank");
            commentdiv.innerHTML = "";
            var header = document.createElement("H3");
            header.innerText = "Create a comment"
            var subheader = document.createElement("H5");
            subheader.innerText = "What would you like to comment on " + ta.value.substring(start, end);
            var comment = document.createElement("INPUT");
            comment.type = "text";
            comment.id = "comment";
            var addcommentbutton = document.createElement("BUTTON");
            //addcommentbutton.value = "ADD COMMENT";
            addcommentbutton.innerText = "ADD COMMENT";
            addcommentbutton.onclick = function(e) {
                if (comment.value.length > 0) {
                    comments.push({start:start, end:end, content:comment.value, page:page});
                    start = 0;
                    end = 0;
                    commentdiv.innerHTML = "";
                    commentdiv.innerHTML = "";
                    editbtn.innerText = "Submit " + comments.length + " edits";
                }
            };
            commentdiv.appendChild(header);
            commentdiv.appendChild(subheader);
            commentdiv.appendChild(comment);
            commentdiv.appendChild(document.createElement("BR"));
            commentdiv.appendChild(addcommentbutton);
        }
        content.innerHTML = "";
        ta.setAttribute("rows", numlines);
        ta.style.border = "none";
        content.appendChild(ta);
    } else {
        editbtn.innerText = "Edit";
        if (comments.length > 0) {
            submitComments();
        }
        content.innerHTML = content.firstChild.value;
    }
}

var submitComments = function() {
    var xhr = new XMLHttpRequest();
    xhr.open('POST', "/addcomments", true);
    xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
    xhr.onload = function() {
    };
    xhr.send("data=" + JSON.stringify(comments));
}
