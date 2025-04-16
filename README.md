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

All endpoints return appropriate success and error responses. Below is a list of available routes:

### 🔁 General

- GET /

Displays a sample checkout page to test Pix, Card, or Boleto payments.

#### 🏦 Pix Payments

- GET /pix/

Renders a form to input Pix payment details.

- POST /pix/process_payment/

Processes the Pix payment and returns either a QR Code or an error message.

#### 💸 Boleto Payments

- GET /bill/

Renders a form to input Boleto payment details.

- POST /bill/process_payment/

Processes the Boleto payment and returns the barcode/QR Code or an error message.

#### 💳 Card Payments

- GET /card/

Renders a form to input card payment details.

- POST /card/process_payment/

Processes the card payment and returns the transaction result or an error message.

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

