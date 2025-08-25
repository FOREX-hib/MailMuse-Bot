"""
Integration utilities for connecting Telegram bot with Flask app
"""
import requests
from models import User, Message
from extensions import db


class BotWebhookHandler:
    """Handler for bot-web integration"""
    
    def __init__(self, flask_app_url="http://localhost:5000"):
        self.flask_app_url = flask_app_url
    
    def register_user(self, telegram_user):
        """Register or update user in the database via Flask API"""
        user_data = {
            'telegram_id': telegram_user.id,
            'username': telegram_user.username,
            'first_name': telegram_user.first_name,
            'last_name': telegram_user.last_name
        }
        
        try:
            response = requests.post(
                f"{self.flask_app_url}/api/users",
                json=user_data,
                timeout=5
            )
            if response.status_code in [200, 201, 409]:  # 409 = user already exists
                return True
        except Exception as e:
            print(f"Error registering user: {e}")
        
        return False
    
    def log_message(self, user_id, message_text, message_type='text'):
        """Log message to database via Flask API"""
        message_data = {
            'user_id': user_id,
            'message_text': message_text,
            'message_type': message_type
        }
        
        try:
            response = requests.post(
                f"{self.flask_app_url}/api/messages",
                json=message_data,
                timeout=5
            )
            return response.status_code == 201
        except Exception as e:
            print(f"Error logging message: {e}")
        
        return False


def register_user_from_bot(telegram_user):
    """Direct database registration (when running in same process)"""
    try:
        # Check if user already exists
        existing_user = User.query.filter_by(telegram_id=telegram_user.id).first()
        
        if existing_user:
            # Update existing user
            existing_user.username = telegram_user.username
            existing_user.first_name = telegram_user.first_name
            existing_user.last_name = telegram_user.last_name
            db.session.commit()
            return existing_user
        else:
            # Create new user
            new_user = User(
                telegram_id=telegram_user.id,
                username=telegram_user.username,
                first_name=telegram_user.first_name,
                last_name=telegram_user.last_name
            )
            db.session.add(new_user)
            db.session.commit()
            return new_user
            
    except Exception as e:
        print(f"Error in register_user_from_bot: {e}")
        db.session.rollback()
        return None


def log_message_from_bot(telegram_user_id, message_text, message_type='text'):
    """Direct database message logging (when running in same process)"""
    try:
        # Find user
        user = User.query.filter_by(telegram_id=telegram_user_id).first()
        if not user:
            return False
        
        # Create message
        message = Message(
            user_id=user.id,
            message_text=message_text,
            message_type=message_type
        )
        db.session.add(message)
        db.session.commit()
        return True
        
    except Exception as e:
        print(f"Error in log_message_from_bot: {e}")
        db.session.rollback()
        return False