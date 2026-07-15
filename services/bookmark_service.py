from utils.database import get_connection
from utils.logger import log_debug, log_error, log_info
from utils.constants import Emojis
from datetime import datetime, timezone

# Adding bookmark func
def add_bookmark(user_id: int, content: str) :
    
    utc_time = datetime.now(timezone.utc).isoformat() + "Z"

    conn = get_connection()
    
    if not conn:
        log_error(f"{Emojis.ERROR} Failed to connect to database for creating session.")
        return None

    try:
        cursor = conn.cursor()
        log_debug(f"{Emojis.BOOK} Creating bookmark for user {user_id}")

        cursor.execute("""
            INSERT INTO bookmarks(user_id, content, saved_at)
            VALUES (?, ?, ?)

        """, (user_id, content, utc_time))
        conn.commit()

        bookmark_id = cursor.lastrowid
        log_info(f"{Emojis.SUCCESS} Bookmark id saved successfully for user {user_id}")
        return bookmark_id
        
    except Exception as add_bookmark_error:
        log_error(f"{Emojis.ERROR} Failed to add bookmark for user {user_id}", add_bookmark_error)
        return None

    finally:
        conn.close()


# Getting bookmark func
def get_user_bookmarks(user_id: int):
    
    conn = get_connection()
    
    if not conn:
        log_error(f"{Emojis.ERROR} Failed to connect to database for getting bookmark.")
        return None

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT content, id FROM bookmarks WHERE user_id = ? ORDER BY id ASC", (user_id, ))
        bookmarks = cursor.fetchall()
        return bookmarks

    except Exception as getting_bookmark_error:
        log_error(f"{Emojis.ERROR} Failed to get bookmark", getting_bookmark_error)

    finally:
        conn.close()


# Deleting bookmark func
def delete_bookmark(bookmark_id: int, user_id: int) -> None:
    
    conn = get_connection()

    if not conn:
        log_error(f"{Emojis.ERROR} Failed to connect to database for deleting bookmark.")
        return None

    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM bookmarks WHERE user_id = ? AND id = ?", (user_id, bookmark_id))
        conn.commit()

    except Exception as deleting_bookmark_error:
        log_error(f"{Emojis.ERROR} Failed to delete bookmark", deleting_bookmark_error)

    finally:
        conn.close()
        
    