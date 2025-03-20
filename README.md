# PaymentApp

This project consists of creating a microservice for payment processing, making payment available via Pix, Card and boleto. The checkout endpoint is an example of which fields you must pass to the Payment WebSite. These fields are mandatory as they will be used to create a hash that will identify the payment in the Mercado Pago system (x-idempotency-key) and will ensure that fields such as amount, email, description are not changed during one step or another.

## Environment

Before using this project, you will need to define some environment variables as described below. The first two variables can be generated through the utils.py file and will be used to create the hash that guarantees data integrity during an endpoint and others. The last two must be generated on the Mercado Pago website and will be used to generate the forms and record payments.

```
PAYMENT_PRIVATE_KEY="PRIVATE KEY USED TO CREATE THE HASH"
PAYMENT_PUBLIC_KEY="PUBLIC KEY USED TO VALIDATE THE HASE"
PAYMENT_MP_PRIVATE_KEY="KEY TO COMUNICATE WITH MERCADO PAGO API AND REGISTER PAYMENTS"
PAYMENT_MP_PUBLIC_KEY="MERCADO PAGO PUBLIC KEY"
```

## Endpoints

### / 
### /pix/
### /pix/process_payment/
### /bill/
### /bill/process_payment/
### /card/
### /card/process_payment/
### /card/payment_successful/
### /card/payment_error/

