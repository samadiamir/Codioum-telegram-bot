"""
Database module.
Provides SQLite connection and table creation.
"""

import sqlite3
import os
from utils.constants import Emojis
from utils.logger import log_info, log_error, log_debug, log_warning

# Path to the database file
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "bot_data.db")


def get_connection():
    """Create and return a database connection."""
    try:
        connection = sqlite3.connect(DB_PATH)
        connection.row_factory = sqlite3.Row  # This lets you access columns by name
        return connection
    except Exception as e:
        log_error("Failed to connect to database", e)
        return None


def init_db():
    """Create tables if they don't exist."""
    try:
        conn = get_connection()
        log_info("Getting connection to the database.")
        
        if conn is None:
            return
        
        cursor = conn.cursor()
        
        # Columns: id, user_id, role, content, event_type, timestamp
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                role TEXT,
                content TEXT,
                event_type TEXT,
                timestamp TEXT
            )
        """)
        
        # Columns: user_id, latitude, longitude, saved_at
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_locations (
                user_id INTEGER PRIMARY KEY,
                latitude REAL,
                longitude REAL,
                saved_at TEXT
            )
        """)

        # Creating a table for adding a id for each session and message in ai chat
        # Columns: id, user_id, name, created_at
        log_debug("Creating a new table for saving each session id in 'ai chat' ")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                name TEXT,
                created_at TEXT
            )
        """)

        # Bookmark table
        # Columns: id, user_id, content, saved_at
        log_debug(f"{Emojis.BOOK} Creating a table for saving each bookmark.")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS bookmarks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                content TEXT,
                saved_at TEXT
            )
        """)
        
        try:
            log_debug("Adding a new column to messages table.")
            cursor.execute("""
                ALTER TABLE messages ADD COLUMN session_id INTEGER
            """)
        except Exception as e :
            log_warning(f"An expected error happened: {e}")
            
        conn.commit()
        conn.close()
        
        log_info("Database initialized successfully.")
    except Exception as e:
        log_error("Failed to initialize database", e)