const dropdown = document.getElementById("dropdownMenu");
const dropdown_items = document.getElementsByClassName("dropdown-item");
dropdown.onclick = function () {
    if (dropdown.getAttribute("aria-expanded") === "false") {
        dropdown.nextElementSibling.classList.remove("d-none");
        dropdown.nextElementSibling.classList.add("d-block");
        dropdown.setAttribute("aria-expanded", "true");
    } else {
        dropdown.nextElementSibling.classList.remove("d-block");
        dropdown.nextElementSibling.classList.add("d-none");
        dropdown.setAttribute("aria-expanded", "false");
    }
};

function click_dropdown() {
    dropdown.click();
}

dropdown_items[0].onclick = function () {
    dropdown.click();
};
dropdown_items[1].onclick = function () {
    dropdown.click();
};
