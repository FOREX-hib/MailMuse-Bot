"""
Flask routes
"""
from flask import current_app, jsonify, request
from extensions import db
from models import User, Message


@current_app.route('/')
def index():
    """Main page"""
    return jsonify({
        'status': 'ok',
        'message': 'Flask app is running',
        'users_count': User.query.count(),
        'messages_count': Message.query.count()
    })


@current_app.route('/health')
def health():
    """Health check endpoint"""
    try:
        # Test database connection
        db.session.execute(db.text('SELECT 1'))
        return jsonify({'status': 'healthy', 'database': 'connected'}), 200
    except Exception as e:
        return jsonify({'status': 'unhealthy', 'error': str(e)}), 500


@current_app.route('/users', methods=['GET'])
def get_users():
    """Get all users"""
    users = User.query.all()
    return jsonify([{
        'id': user.id,
        'telegram_id': user.telegram_id,
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'created_at': user.created_at.isoformat(),
        'is_active': user.is_active
    } for user in users])


@current_app.route('/users', methods=['POST'])
def create_user():
    """Create a new user"""
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
    
    try:
        db.session.add(user)
        db.session.commit()
        return jsonify({
            'id': user.id,
            'telegram_id': user.telegram_id,
            'message': 'User created successfully'
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500