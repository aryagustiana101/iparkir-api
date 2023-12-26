import json
from datetime import datetime
from flask import jsonify, request
from app.libs.stripe import stripe

from app.services import reservations
from app.libs.constants import STRIPE_WEBHOOK_SECRET


def stripe_webhook():
    event = None
    payload = request.data

    try:
        event = json.loads(payload)
    except json.decoder.JSONDecodeError as e:
        print(f"Webhook error while parsing basic request\n{str(e)}")

        return jsonify({"success": False})

    sig_header = request.headers.get("stripe-signature")

    try:
        event = stripe.Webhook.construct_event(
            payload=payload,
            sig_header=sig_header,
            secret=STRIPE_WEBHOOK_SECRET
        )
    except stripe.SignatureVerificationError as e:
        print(f"Webhook signature verification failed\n{str(e)}")

        return jsonify({"success": False})

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]

        reservation = reservations.get_reservation(
            user_id="ADMIN",
            id=session["id"],
            by_payment_id=True,
            is_admin_user=True,
        ).get("data")

        if reservation and reservation["payment"]["status"] == "unpaid":
            reservations.update_reservation(
                id=reservation["id"],
                payment={
                    **reservation["payment"],
                    "status": session["payment_status"],
                    "paid_at": datetime.now().isoformat(),
                },
            )

            print(session)

        if not reservation:
            print(f"Reservation not found for payment id {session['id']}")
    else:
        print(f"Unhandled event type {event["type"]}")

    return jsonify({"success": True})
