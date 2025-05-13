import os
import logging
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse

from game_logic import process_game_command

# Initialize logging
logger = logging.getLogger(__name__)

# Twilio credentials
TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.environ.get("TWILIO_PHONE_NUMBER")

def send_whatsapp_message(to_phone: str, message: str) -> None:
    """Send a WhatsApp message using Twilio"""
    if not TWILIO_ACCOUNT_SID or not TWILIO_AUTH_TOKEN or not TWILIO_PHONE_NUMBER:
        logger.error("Twilio credentials not properly configured")
        return
    
    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        
        # Format to WhatsApp format if needed
        if not to_phone.startswith("whatsapp:"):
            to_phone = f"whatsapp:{to_phone}"
        
        if not TWILIO_PHONE_NUMBER.startswith("whatsapp:"):
            from_phone = f"whatsapp:{TWILIO_PHONE_NUMBER}"
        else:
            from_phone = TWILIO_PHONE_NUMBER
        
        # Send message
        message = client.messages.create(
            body=message,
            from_=from_phone,
            to=to_phone
        )
        
        logger.info(f"Message sent with SID: {message.sid}")
    
    except Exception as e:
        logger.error(f"Error sending WhatsApp message: {e}")

def process_incoming_message(message_body: str, sender_phone: str, game_state: dict) -> MessagingResponse:
    """Process an incoming WhatsApp message and return a TwiML response"""
    try:
        # Clean up phone format if needed
        if sender_phone.startswith("whatsapp:"):
            sender_phone = sender_phone[9:]  # Remove "whatsapp:" prefix
        
        # Process the game command
        response_text = process_game_command(message_body, sender_phone, game_state)
        
        # Create TwiML response
        resp = MessagingResponse()
        resp.message(response_text)
        
        return resp
    
    except Exception as e:
        logger.error(f"Error processing incoming message: {e}")
        
        # Create error response
        resp = MessagingResponse()
        resp.message("Sorry, an error occurred. Please try again later.")
        
        return resp
