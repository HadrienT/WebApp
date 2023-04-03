// Example starter JavaScript for disabling form submissions if there are invalid fields
(function () {
  'use strict'

  // Fetch all the forms we want to apply custom Bootstrap validation styles to
  var forms = document.querySelectorAll('.needs-validation')

  // Loop over them and prevent submission
  Array.prototype.slice.call(forms)
    .forEach(function (form) {
      form.addEventListener('submit', function (event) {
        event.preventDefault(); // Move this line outside the if block

        if (!form.checkValidity()) {
          event.stopPropagation();
        }

        form.classList.add('was-validated');
      }, false)
    })

})()


const planId = "{{planId}}"; // Get the planId from the server-side rendering

let initialPriceElement;
if (planId === "private") {
  initialPriceElement = document.getElementById("initial-price-private");
} else if (planId === "professional") {
  initialPriceElement = document.getElementById("initial-price-professional");
}

const initialPrice = parseFloat(initialPriceElement.textContent.slice(1));

const promoForm = document.getElementById('promo-form');
const promoInput = document.getElementById('promo-input');
const promoDisplay = document.getElementById('promo-display');
const promoCodeDesc = document.getElementById('promo-code-desc');
const promoDiscount = document.getElementById('promo-discount');
const totalPrice = document.getElementById('total-price');

let totalAmount = initialPrice; // Set the initial total amount

promoForm.addEventListener('submit', (event) => {
  event.preventDefault(); // Prevent the form from submitting

  const promoCode = promoInput.value.trim(); // Get the entered promo code

  // Validate the promo code (Replace this with an API call or other validation logic)
  if (promoCode === 'FREE') {
    const discount = totalAmount; // Set the discount value for this promo code

    // Update the promo code information display
    promoCodeDesc.innerText = promoCode;
    promoDiscount.innerText = `−$${discount}`;
    promoDisplay.style.display = 'block';

    // Update the total price with the discount
    totalAmount -= discount;
    totalPrice.innerText = `$${totalAmount}`;
  } else {
    alert('Invalid promo code');
  }
});
