document.addEventListener("htmx:afterSwap", function(event) {
    const nameInput = document.getElementById("name-input");
    const svgElement = document.getElementById("submit-name");

    if (nameInput && svgElement) {
        nameInput.removeEventListener("keydown", handleEnterPress);

        function handleEnterPress(event) {
            if (event.key === "Enter") {
                event.preventDefault();
                svgElement.dispatchEvent(new Event('click', { bubbles: true }));
            }
        }

        nameInput.addEventListener("keydown", handleEnterPress);
    }
});
