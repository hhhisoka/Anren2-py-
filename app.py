import os
import json
import logging
from flask import Flask, request, jsonify, render_template, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix

from twilio_integration import process_incoming_message
from game_logic import process_game_command
from utils import save_game_state, load_game_state

# Initialize logging
logger = logging.getLogger(__name__)

# Create database base class
class Base(DeclarativeBase):
    pass

# Initialize SQLAlchemy
db = SQLAlchemy(model_class=Base)

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Configure database
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///rpg_game.db")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}
db.init_app(app)

# Load game state
try:
    game_state = load_game_state()
    logger.info("Game state loaded successfully")
except Exception as e:
    logger.error(f"Failed to load game state: {e}")
    game_state = {
        "players": {},
        "active_battles": {},
        "zones": {},
        "items": {},
        "deities": {}
    }
    save_game_state(game_state)

# Import models after DB initialization
with app.app_context():
    from models import User, Player, Admin
    db.create_all()

# Routes

@app.route("/")
def index():
    """Landing page for the game admin dashboard."""
    return render_template("index.html")

@app.route("/admin", methods=["GET"])
def admin_dashboard():
    """Admin dashboard for game masters/deities."""
    if not session.get("admin_logged_in"):
        return redirect(url_for("index"))
    
    stats = {
        "player_count": len(game_state["players"]),
        "active_battles": len(game_state["active_battles"]),
        "deity_count": len(game_state["deities"])
    }
    
    return render_template("admin_dashboard.html", stats=stats, game_state=game_state)

@app.route("/admin/login", methods=["POST"])
def admin_login():
    """Process admin login."""
    username = request.form.get("username")
    password = request.form.get("password")
    
    admin = Admin.query.filter_by(username=username).first()
    
    if admin and check_password_hash(admin.password_hash, password):
        session["admin_logged_in"] = True
        session["admin_id"] = admin.id
        flash("Login successful!", "success")
        return redirect(url_for("admin_dashboard"))
    
    flash("Invalid credentials", "danger")
    return redirect(url_for("index"))

@app.route("/admin/logout")
def admin_logout():
    """Process admin logout."""
    session.pop("admin_logged_in", None)
    session.pop("admin_id", None)
    flash("You have been logged out", "info")
    return redirect(url_for("index"))

@app.route("/api/webhook", methods=["POST"])
def webhook():
    """Webhook endpoint for Twilio WhatsApp messages."""
    try:
        # Extract message data from Twilio
        message_body = request.values.get("Body", "").strip()
        sender_phone = request.values.get("From", "").strip()
        
        # Process the message
        response = process_incoming_message(message_body, sender_phone, game_state)
        
        # Save game state after processing
        save_game_state(game_state)
        
        return str(response)
    
    except Exception as e:
        logger.error(f"Error processing webhook: {e}")
        return "Error processing message", 500

@app.route("/api/game_state", methods=["GET"])
def get_game_state():
    """API endpoint to get current game state (admin only)."""
    if not session.get("admin_logged_in"):
        return jsonify({"error": "Unauthorized"}), 401
    
    return jsonify(game_state)

@app.route("/api/player/<phone>", methods=["GET"])
def get_player(phone):
    """API endpoint to get player data (admin only)."""
    if not session.get("admin_logged_in"):
        return jsonify({"error": "Unauthorized"}), 401
    
    player = game_state["players"].get(phone)
    if not player:
        return jsonify({"error": "Player not found"}), 404
    
    return jsonify(player)

@app.route("/api/create_deity", methods=["POST"])
def create_deity():
    """API endpoint to create a deity (admin only)."""
    if not session.get("admin_logged_in"):
        return jsonify({"error": "Unauthorized"}), 401
    
    data = request.json
    deity_name = data.get("name")
    phone = data.get("phone")
    
    if not deity_name or not phone or phone not in game_state["players"]:
        return jsonify({"error": "Invalid deity data"}), 400
    
    player = game_state["players"][phone]
    player["is_deity"] = True
    
    if "deities" not in game_state:
        game_state["deities"] = {}
    
    game_state["deities"][phone] = {
        "name": deity_name,
        "player_phone": phone,
        "chosen": []
    }
    
    save_game_state(game_state)
    
    return jsonify({"success": True})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
