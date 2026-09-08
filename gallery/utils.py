import logging
from django.conf import settings

logger = logging.getLogger(__name__)

def send_whatsapp_alert(name, email, phone="", message_text="", form_type="Website Inquiry"):
    """
    Triggers an instant WhatsApp notification via Twilio API for new inquiries/commissions.
    Production-safe & minimal: failures are logged gracefully without breaking form submissions.
    """
    account_sid = getattr(settings, 'TWILIO_ACCOUNT_SID', None)
    auth_token = getattr(settings, 'TWILIO_AUTH_TOKEN', None)
    from_whatsapp = getattr(settings, 'TWILIO_WHATSAPP_NUMBER', None)
    to_whatsapp = getattr(settings, 'MY_PHONE_NUMBER', None)

    if not all([account_sid, auth_token, from_whatsapp, to_whatsapp]):
        logger.warning("Twilio WhatsApp notification skipped: Missing credentials in settings.")
        return False

    try:
        from twilio.rest import Client

        # Format whatsapp: prefix required by Twilio API
        if not from_whatsapp.startswith("whatsapp:"):
            from_whatsapp = f"whatsapp:{from_whatsapp}"
        if not to_whatsapp.startswith("whatsapp:"):
            to_whatsapp = f"whatsapp:{to_whatsapp}"

        body = (
            f"🎨 *New {form_type} on D-Art Studio*\n\n"
            f"👤 *Name:* {name}\n"
            f"📧 *Email:* {email}\n"
            f"📞 *Phone:* {phone if phone else 'N/A'}\n"
            f"💬 *Details:* {message_text}"
        )

        client = Client(account_sid, auth_token)
        msg = client.messages.create(
            from_=from_whatsapp,
            body=body,
            to=to_whatsapp
        )
        logger.info(f"WhatsApp alert sent. SID: {msg.sid}")
        return True
    except Exception as e:
        logger.error(f"Failed to send WhatsApp notification via Twilio: {e}")
        return False
