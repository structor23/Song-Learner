import sqlite3
from datetime import datetime

def add_song(conn, song_name):
    cursor = conn.cursor()
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
    INSERT INTO songs (name, overall_rating, last_evaluation)
    VALUES (?, 0, ?)
    """, (song_name, current_time))
    
    cursor.execute("""
    INSERT INTO song_ratings (song_id, category, subcategory, rating)
    SELECT last_insert_rowid(), category, subcategory, 0
    FROM (
        SELECT 'Gesang' as category, 'Textsicherheit' as subcategory
        UNION ALL SELECT 'Gesang', 'Timing'
        UNION ALL SELECT 'Gesang', 'Intonation'
        UNION ALL SELECT 'Gesang', 'Ausdruck'
        UNION ALL SELECT 'Gitarre', 'Arrangement'
        UNION ALL SELECT 'Gitarre', 'Technik'
        UNION ALL SELECT 'Gitarre', 'Timing'
        UNION ALL SELECT 'Gitarre', 'Ausdruck'
        UNION ALL SELECT 'Zusammenspiel', 'Timing'
        UNION ALL SELECT 'Zusammenspiel', 'Dynamik'
        UNION ALL SELECT 'Zusammenspiel', 'Buehnenpraesenz'
        UNION ALL SELECT 'Zusammenspiel', 'Performance'
    )
    """)
    
    conn.commit()

def delete_song(conn, song_name):
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM songs WHERE name = ?", (song_name,))
    song_id = cursor.fetchone()
    
    if song_id:
        song_id = song_id[0]
        cursor.execute("DELETE FROM song_ratings WHERE song_id = ?", (song_id,))
        cursor.execute("DELETE FROM songs WHERE id = ?", (song_id,))
        conn.commit()

def get_all_songs(conn):
    cursor = conn.cursor()
    cursor.execute("""
    SELECT s.name, 
           COALESCE(s.overall_rating, 0) as overall_rating,
           COALESCE(AVG(CASE WHEN sr.category = 'Gesang' THEN sr.rating ELSE NULL END), 0) as gesang,
           COALESCE(AVG(CASE WHEN sr.category = 'Gitarre' THEN sr.rating ELSE NULL END), 0) as gitarre,
           COALESCE(AVG(CASE WHEN sr.category = 'Zusammenspiel' THEN sr.rating ELSE NULL END), 0) as zusammenspiel,
           s.last_evaluation
    FROM songs s
    LEFT JOIN song_ratings sr ON s.id = sr.song_id
    GROUP BY s.id
    ORDER BY s.name
    """)
    return cursor.fetchall()

def update_song_rating(conn, song_name, overall_rating, subcategory_ratings):
    cursor = conn.cursor()
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
    UPDATE songs
    SET overall_rating = ?, last_evaluation = ?
    WHERE name = ?
    """, (overall_rating, current_time, song_name))

    cursor.execute("SELECT id FROM songs WHERE name = ?", (song_name,))
    song_id = cursor.fetchone()[0]

    for category_subcategory, rating in subcategory_ratings.items():
        category, subcategory = category_subcategory.split('_')
        cursor.execute("""
        UPDATE song_ratings
        SET rating = ?
        WHERE song_id = ? AND category = ? AND subcategory = ?
        """, (rating, song_id, category, subcategory))

    conn.commit()

def get_song_ratings(conn, song_name):
    cursor = conn.cursor()
    cursor.execute("""
    SELECT sr.category, sr.subcategory, sr.rating
    FROM song_ratings sr
    JOIN songs s ON sr.song_id = s.id
    WHERE s.name = ?
    """, (song_name,))
    ratings = cursor.fetchall()
    
    return {f"{category}_{subcategory}": rating for category, subcategory, rating in ratings}

# Exportiere alle Funktionen
__all__ = ['add_song', 'delete_song', 'get_all_songs', 'update_song_rating', 'get_song_ratings']