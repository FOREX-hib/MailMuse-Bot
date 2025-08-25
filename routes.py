"""
Flask routes for the web application
"""
from flask import request, jsonify, render_template_string
from extensions import db
from models import User, Message


def register_routes(app):
    """Register all routes with the Flask app"""
    
    @app.route('/')
    def index():
        """Main page"""
        html_template = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Telegram Bot Dashboard</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; }
                .container { max-width: 800px; margin: 0 auto; }
                .stats { display: flex; gap: 20px; margin: 20px 0; }
                .stat-card { 
                    background: #f0f0f0; 
                    padding: 20px; 
                    border-radius: 8px; 
                    flex: 1;
                    text-align: center;
                }
                .stat-number { font-size: 2em; font-weight: bold; color: #007bff; }
                .stat-label { color: #666; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🤖 Telegram Bot Dashboard</h1>
                <div class="stats">
                    <div class="stat-card">
                        <div class="stat-number">{{ users_count }}</div>
                        <div class="stat-label">Total Users</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">{{ messages_count }}</div>
                        <div class="stat-label">Total Messages</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">{{ active_users }}</div>
                        <div class="stat-label">Active Users</div>
                    </div>
                </div>
                <p><strong>Bot Status:</strong> 🟢 Running</p>
                <h3>API Endpoints:</h3>
                <ul>
                    <li><a href="/api/users">/api/users</a> - Get all users</li>
                    <li><a href="/api/messages">/api/messages</a> - Get all messages</li>
                    <li><a href="/api/stats">/api/stats</a> - Get statistics</li>
                </ul>
            </div>
        </body>
        </html>
        """
        
        users_count = User.query.count()
        messages_count = Message.query.count()
        active_users = User.query.filter_by(is_active=True).count()
        
        return render_template_string(
            html_template,
            users_count=users_count,
            messages_count=messages_count,
            active_users=active_users
        )
    
    @app.route('/api/users', methods=['GET'])
    def get_users():
        """Get all users"""
        users = User.query.all()
        return jsonify([user.to_dict() for user in users])
    
    @app.route('/api/users/<int:user_id>', methods=['GET'])
    def get_user(user_id):
        """Get specific user"""
        user = User.query.get_or_404(user_id)
        return jsonify(user.to_dict())
    
    @app.route('/api/users', methods=['POST'])
    def create_user():
        """Create new user"""
        data = request.get_json()
        
        if not data or 'telegram_id' not in data:
            return jsonify({'error': 'telegram_id is required'}), 400
        
        # Check if user already exists
        existing_user = User.query.filter_by(telegram_id=data['telegram_id']).first()
        if existing_user:
            return jsonify({'error': 'User already exists'}), 409
        
        user = User(
            telegram_id=data['telegram_id'],
            username=data.get('username'),
            first_name=data.get('first_name'),
            last_name=data.get('last_name')
        )
        
        db.session.add(user)
        db.session.commit()
        
        return jsonify(user.to_dict()), 201
    
    @app.route('/api/messages', methods=['GET'])
    def get_messages():
        """Get all messages"""
        messages = Message.query.order_by(Message.created_at.desc()).limit(100).all()
        return jsonify([message.to_dict() for message in messages])
    
    @app.route('/api/messages', methods=['POST'])
    def create_message():
        """Create new message"""
        data = request.get_json()
        
        if not data or 'user_id' not in data:
            return jsonify({'error': 'user_id is required'}), 400
        
        message = Message(
            user_id=data['user_id'],
            message_text=data.get('message_text'),
            message_type=data.get('message_type', 'text')
        )
        
        db.session.add(message)
        db.session.commit()
        
        return jsonify(message.to_dict()), 201
    
    @app.route('/api/stats', methods=['GET'])
    def get_stats():
        """Get bot statistics"""
        stats = {
            'total_users': User.query.count(),
            'active_users': User.query.filter_by(is_active=True).count(),
            'total_messages': Message.query.count(),
            'messages_today': Message.query.filter(
                Message.created_at >= db.func.current_date()
            ).count()
        }
        return jsonify(stats)
    
    @app.route('/health', methods=['GET'])
    def health_check():
        """Health check endpoint"""
        return jsonify({'status': 'healthy', 'service': 'telegram-bot-api'})