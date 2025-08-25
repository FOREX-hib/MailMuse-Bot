"""
Script to run both Telegram bot and Flask web application simultaneously
"""
import asyncio
import threading
import logging
from flask import Flask
from bot import main as bot_main
from app import create_app

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

def run_flask_app():
    """Run Flask application in a separate thread"""
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False)

def run_bot():
    """Run Telegram bot"""
    asyncio.run(bot_main())

if __name__ == "__main__":
    logging.info("Starting Telegram Bot + Flask Web Application...")
    
    # Start Flask app in a separate thread
    flask_thread = threading.Thread(target=run_flask_app, daemon=True)
    flask_thread.start()
    
    logging.info("Flask app started on http://localhost:5000")
    
    # Start bot in main thread
    logging.info("Starting Telegram bot...")
    try:
        run_bot()
    except KeyboardInterrupt:
        logging.info("Applications stopped by user")