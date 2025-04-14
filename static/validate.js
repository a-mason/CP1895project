document.addEventListener("DOMContentLoaded", () => {
    let form = document.querySelector("form");

    form.addEventListener("submit", event => {
        let inputs = document.querySelectorAll("input[required]");
        for (let input of inputs) {
            if (input.value == "") {
                event.preventDefault();
                alert("All fields are required.");
                input.focus();
                return;
            }
        }
    });
});