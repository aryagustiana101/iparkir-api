import stripe

from app.libs.constants import STRIPE_SECRET_KEY

stripe.api_key = STRIPE_SECRET_KEY
