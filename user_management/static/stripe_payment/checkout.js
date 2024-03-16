// This is your test publishable API key.
const stripe = Stripe("pk_test_51OqqVHF29svWAwWrIqX5Udn4ko02NwNJSMkD6wqzkfMbsINrpIelI7egEASJyyaj16v0lA7GslqPg8ot1P63tpgD007L8Nxn59");

initialize();

// Create a Checkout Session as soon as the page loads
async function initialize() {
  const response = await fetch("/create-checkout-session", {
    method: "POST",
  });

  const { clientSecret } = await response.json();

  const checkout = await stripe.initEmbeddedCheckout({
    clientSecret,
  });

  // Mount Checkout
  checkout.mount('#checkout');
}