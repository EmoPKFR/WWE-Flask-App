// Get the input element
const expiryDateInput = document.getElementById("expiry_date");

// Listen for input events
expiryDateInput.addEventListener("input", function () {
    const value = this.value;

    // Remove any non-digit characters from the input
    const cleanedValue = value.replace(/\D/g, "");

    // Format the input as MM/YY
    if (cleanedValue.length >= 2) {
        const formattedValue = cleanedValue.slice(0, 2) + "/" + cleanedValue.slice(2);
        this.value = formattedValue;
    } else {
        this.value = cleanedValue;
    }
});