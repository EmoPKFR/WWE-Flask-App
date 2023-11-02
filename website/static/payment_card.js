// Function to format card number with spaces
function formatCardNumber() {
    const cardNumberInput = document.getElementById("card_number");
    let cardNumber = cardNumberInput.value.replace(/\D/g, ''); // Remove non-numeric characters
    let formattedCardNumber = '';
    // Add spaces every 4 digits
    for (let i = 0; i < cardNumber.length; i++) {
        if (i > 0 && i % 4 === 0) {
        formattedCardNumber += ' ';
        }
        formattedCardNumber += cardNumber[i];
    }
    cardNumberInput.value = formattedCardNumber;
    }  
    // Attach the formatCardNumber function to the input's input event
    document.getElementById("card_number").addEventListener("input", formatCardNumber);
    

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


// Function to allow only numeric input for CVV
document.getElementById("cvv").addEventListener("input", function (e) {
    const input = e.target;
    const value = input.value;
    const newValue = value.replace(/\D/g, ''); // Remove non-numeric characters
    if (value !== newValue) {
      input.value = newValue; // Update the input value to contain only numeric characters
    }
  });