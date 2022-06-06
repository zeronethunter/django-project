import {getCookie} from "./vote.js"

var csrftoken = getCookie('csrftoken');

$(".is-right-btn").on('click', function (ev) {
    const $this = $(this);

    const request = new Request(
        "http://127.0.0.1:8000/is_right/",
        {
            method: 'post',
            headers: {
                'X-CSRFToken': csrftoken,
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: 'answer_id=' + $this.data('id')
        }
    );
    fetch(request).then(function (response) {
        $this.addClass("d-none");
        var right = document.createElement('h3');
        right.classList.add("text-success ms-auto");
        right.innerHTML = "✔";
        $("div.before-right").parent().appendChild(right);
    })
})
