
from flask import Blueprint, request, jsonify
import stripe
from app import db
from app.models import User
from flask_login import login_required, current_user

bp = Blueprint('subscription', __name__, url_prefix='/subscription')

# Stripe secret key (ka saka naka daga dashboard)
stripe.api_key = "sk_test_your_secret_key"

@bp.route('/create-checkout-session', methods=['POST'])
@login_required
def create_checkout_session():
    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price': 'price_your_stripe_price_id',  # ka saka price ID daga Stripe
                'quantity': 1,
            }],
            mode='subscription',
            success_url='http://localhost:5000/success',
            cancel_url='http://localhost:5000/cancel',
            customer_email=current_user.username  # assuming username = email
        )
        return jsonify({'checkout_url': checkout_session.url})
    except Exception as e:
        return jsonify(error=str(e)), 400

@bp.route('/webhook', methods=['POST'])
def stripe_webhook():
    payload = request.data
    sig_header = request.headers.get('Stripe-Signature')
    endpoint_secret = "whsec_your_webhook_secret"

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except Exception as e:
        return jsonify(error=str(e)), 400

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        user = User.query.filter_by(username=session['customer_email']).first()
        if user:
            user.subscription_status = "active"
            db.session.commit()

    return jsonify(success=True)
