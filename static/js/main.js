document.addEventListener('DOMContentLoaded', function () {
  const productTitle = document.getElementById('productTitle');
  const productPrice = document.getElementById('productPrice');
  const productImage = document.getElementById('productImage');
  const totalPriceElement = document.getElementById('totalPrice'); // Get the total price element
  const hiddenTotalPriceInput = document.getElementById('hiddenTotalPrice');
  const hiddenUnitPriceInput = document.getElementById('hiddenUnitPrice');

  // Initialize unitPrice and quantity
  let unitPrice = 9.19;
  let quantity = 1;

  // Set the initial total price based on unitPrice and quantity
  const initialTotalPrice = unitPrice * quantity;
  hiddenTotalPriceInput.value = initialTotalPrice.toFixed(2);

  // Get references to the button and the product list section
  const toggleProductListBtn = document.getElementById("toggleProductListBtn");
  const productListSection = document.getElementById("productListSection");

  // Add a click event listener to the button
  toggleProductListBtn.addEventListener("click", function () {
    // Toggle the display property of the product list section
    if (productListSection.style.display === "none") {
      productListSection.style.display = "block";
    } else {
      productListSection.style.display = "none";
    }
  });

  // Get all "Cart" buttons
  const cartButtons = document.querySelectorAll('.cart-button');

  cartButtons.forEach(function (button) {
    button.addEventListener('click', function () {
      // Get the product details from data attributes
      const title = button.getAttribute('data-title');
      let price = button.getAttribute('data-price'); // Get the price as a string
      const imageSrc = button.getAttribute('data-image');

      // Remove all currency symbols, extra characters, and whitespace
      price = price.replace(/[^\d.]/g, '').trim();

      // Update the offcanvas content
      productTitle.textContent = title;
      productPrice.textContent = '£' + price; // Add the currency symbol back

      // Set unitPrice based on the product's price
      unitPrice = parseFloat(price);

      productImage.src = imageSrc;

      // Initialize quantity to 1 when a new product is selected
      quantity = 1;

      // Call updateTotalPrice to update the total price
      updateTotalPrice();
    });
  });

  // Get references to the "+" and "-" buttons, the quantity element
  const decreaseQuantityBtn = document.getElementById("decreaseQuantityBtn");
  const increaseQuantityBtn = document.getElementById("increaseQuantityBtn");
  const quantityElement = document.getElementById("quantity");
  const hiddenQuantityInput = document.getElementById('hiddenQuantity');

  // Function to update the quantity element and the total price
  function updateQuantity() {
    quantityElement.textContent = quantity;
    updateTotalPrice();
  }

  // Add click event listeners to the "+" and "-" buttons
  decreaseQuantityBtn.addEventListener("click", function () {
    if (quantity > 1) {
      quantity--; // Decrease the quantity, but ensure it doesn't go below 1
      updateQuantity();
    }
  });

  increaseQuantityBtn.addEventListener("click", function () {
    quantity++; // Increase the quantity
    updateQuantity();
  });

  // Function to update the total price
function updateTotalPrice() {
  const totalPrice = quantity * unitPrice; // Calculate the total price
  totalPriceElement.textContent = '$' + totalPrice.toFixed(2); // Format as currency with the currency symbol

  // Set the total price in the hidden input field
  document.getElementById('hiddenTotalPrice').value = totalPrice.toFixed(2);
}

  // Set total price and unit price as data attributes on the form
const form = document.querySelector('form');
hiddenUnitPriceInput.value = unitPrice.toFixed(2);

// Call updateTotalPrice initially to set the correct total price
updateTotalPrice();

// Add an event listener to the button buy stripe card
document.getElementById('redirectButton').addEventListener('click', function () {
  // Redirect the user to the desired URL
  window.location.href = 'https://buy.stripe.com/test_28og0u7BB4mKbAsbIJ';
});
});
