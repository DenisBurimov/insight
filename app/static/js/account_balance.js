document.addEventListener("htmx:afterSwap", function(event) {
    const balanceInput = document.getElementById("balance-input");
    const svgElement = document.getElementById("submit-balance");

    if (balanceInput && svgElement) {
        balanceInput.removeEventListener("keydown", handleEnterPress);

        function handleEnterPress(event) {
            if (event.key === "Enter") {
                event.preventDefault();
                svgElement.dispatchEvent(new Event('click', { bubbles: true }));
            }
        }

        balanceInput.addEventListener("keydown", handleEnterPress);
    }
});
