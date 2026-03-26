import stripe
from flask import Flask, jsonify, request
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

YOUR_DOMAIN = os.getenv("DOMAIN")  # 👈 important

@app.route("/create-checkout-session", methods=["POST"])
def create_checkout_session():
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                "price_data": {
                    "currency": "usd",
                    "product_data": {
                        "name": "Test Product",
                    },
                    "unit_amount": 1000,
                },
                "quantity": 1,
            }],
            mode="payment",
            success_url=f"{YOUR_DOMAIN}/success.html",
            cancel_url=f"{YOUR_DOMAIN}/cancel.html",
        )

        return jsonify({"id": session.id})

    except Exception as e:
        return jsonify(error=str(e)), 400


@app.route("/")
def home():
    return "Backend running 🚀"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
