# 💳 PaymentApp

PaymentApp is a microservice designed to handle payments through Pix, Card, and Boleto, using the Mercado Pago payment gateway. This service provides secure and reliable payment processing, including data integrity verification using cryptographic hashes.

## 🧾 Features

✅ Payment through Pix, Credit Card, and Boleto

🔒 Hash-based verification to ensure payment data integrity

📦 RESTful endpoints for payment processing

🧪 Sample checkout page for testing

🧾 Automatic QR code generation for Pix and Boleto

## 📁 Project Structure

**PaymentApp/** <br>
├── **integrations/** *Integrations with external services (e.g., Mercado Pago API)* <br>
├── **models/** *Data models and validation logic* <br>
├── **routes/** *Route definitions and controllers* <br> 
│ ├── **pix.py** <br> 
│ ├── **card.py** <br> 
│ ├── **bill.py** <br> 
│ └── **checkout.py** <br> 
├── **static/** *Static assets (CSS, JS, images)* <br> 
├── **templates/** *HTML templates (Jinja2)* <br>
├── **.env** *Environment variables (not committed)* <br> 
└── **init.py** *App factory and setup* <br> 


## ⚙️ Environment Setup

Before running the application, create a .env file or export the following environment variables:

```
PAYMENT_PRIVATE_KEY="PRIVATE KEY USED TO CREATE THE HASH"
PAYMENT_PUBLIC_KEY="PUBLIC KEY USED TO VALIDATE THE HASH"
PAYMENT_MP_PRIVATE_KEY="YOUR MERCADO PAGO ACCESS TOKEN"
PAYMENT_MP_PUBLIC_KEY="YOUR MERCADO PAGO PUBLIC KEY"
```

*You can generate PAYMENT_PRIVATE_KEY and PAYMENT_PUBLIC_KEY using the utils.py file.*

*PAYMENT_MP_PRIVATE_KEY and PAYMENT_MP_PUBLIC_KEY can be generated in your Mercado Pago Developer Account.*

## 📡 API Endpoints

---

### 🔁 Checkout

Below are the main REST endpoints available for each payment method:

---

### 🔁 Checkout

- `GET /`  
  Displays the main checkout page with links to Pix, Boleto, and Card payments.

---

### 🏦 Pix (Instant Payment)

- `POST /pix/`  
  Renders the form for Pix payment with encrypted `purchase_identification`.

- `POST /pix/process_payment/`  
  Processes the Pix payment using the Mercado Pago API.  
  Returns a base64 QR Code and a copy-and-paste code string.

---

### 💸 Boleto (Bank Slip)

- `POST /bill/`  
  Renders the form for Boleto payment with encrypted `purchase_identification`.

- `POST /bill/process_payment/`  
  Processes the Boleto payment and returns the digitable line or an error message.

---

### 💳 Credit Card

- `POST /card/`  
  Renders the form for credit card payment with encrypted `purchase_identification`.

- `POST /card/process_payment/`  
  Processes the card payment and returns the transaction status (approved, rejected, etc.).

- `GET /card/payment_successful/`  
  Success page for approved card payments.

- `GET /card/payment_error/`  
  Error page for rejected card payments.

- `GET | POST /card/register/`  
  Registers a new card for an existing customer.

- `GET /card/<customer_id>/<card_id>/`  
  Retrieves information for a specific saved card.

- `POST /card/<customer_id>/<card_id>/`  
  Updates information for a saved card.

- `GET /card/<customer_id>/<card_id>/delete/`  
  Deletes a saved card.

- `GET | POST /card/search/`  
  Searches for saved cards using the customer's email.

---

### 👤 Clients

- `GET | POST /client/register/`  
  Registers a new client (customer).

- `GET | POST /client/<client_id>/update/`  
  Updates an existing client’s information.

- `GET | POST /client/search/`  
  Searches for clients by email.

- `GET /client/<client_id>/`  
  Retrieves details of a specific client.

---

### 📅 Subscription Plans

- `GET | POST /plan/register/`  
  Registers a new recurring subscription plan.

- `GET | POST /plan/<plan_id>/update/`  
  Updates an existing subscription plan.

- `GET /plan/`  
  Lists all available subscription plans.

- `GET /plan/<plan_id>/`  
  Retrieves information for a specific subscription plan.

---

### 🔄 Subscription Signatures

- `GET | POST /signature/register/`  
  Registers a new subscription (signature) under an existing plan using card data.

- `GET | POST /signature/`  
  Searches for all active subscriptions by the payer's email.

- `GET /signature/<signature_id>/`  
  Retrieves detailed information for a specific subscription.

---

> 🛡️ **Note:** All endpoints for payment use encrypted `purchase_identification` and secure hash validation with `x-idempotency-key`, ensuring data integrity and preventing duplicate charges.

### 🧠 How It Works

1. The client fills a payment form (Pix, Card, or Boleto).

2. The frontend sends the required data to the backend.

3. A hash is created using PAYMENT_PRIVATE_KEY and the key fields (amount, email, description).

4. This hash ensures that the data remains untampered between steps.

5. The Mercado Pago API is called to process the payment and generate a QR code or return transaction data.

### 🔐 Security

- All payment requests include an x-idempotency-key generated from the hash.

- This prevents duplicated charges and ensures consistent payment validation.

### 📦 Dependencies

- Python 3.12
- Mercado Pago Python SDK
- Flask
- dotenv
- pycryptodome

#### Install with:

    pip install mercadopago python-dotenv flask pycryptodome

