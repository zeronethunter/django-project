const login_modal_dialog = document.getElementById("loginModal");
const login_modal_btn = document.getElementById("loginBtn");
const signup_modal_dialog = document.getElementById("signupModal");
const signup_modal_btn = document.getElementById("signupBtn");

window.addEventListener('click', function (e) {
    if (e.target.id === "loginBtn" || e.target.id === "signupBtn") {
        return
    }
    if (login_modal_dialog.classList.contains('open')) {
        if (!login_modal_dialog.contains(e.target)) {
            hide_all_modals();
        }
    }
    if (signup_modal_dialog.classList.contains('open')) {
        if (!signup_modal_dialog.contains(e.target)) {
            hide_all_modals();
        }
    }
});

function hide_all_modals() {
    display_none(login_modal_dialog);
    display_none(signup_modal_dialog);
}

function display_none(block) {
    if (block.classList.contains('open')) {
        block.classList.remove('open');
    }
}

login_modal_btn.onclick = function () {
    hide_all_modals();
    login_modal_dialog.classList.add('open');
}

signup_modal_btn.onclick = function () {
    hide_all_modals();
    signup_modal_dialog.classList.add('open');
}
