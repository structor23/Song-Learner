import sqlite3
from datetime import datetime

def create_connection():
    return sqlite3.connect('songs.db')

def create_tables(conn):
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS songs (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL UNIQUE,
        last_evaluation TEXT,
        overall_rating REAL,
        gesang_textsicherheit REAL,
        gesang_timing REAL,
        gesang_intonation REAL,
        gesang_ausdruck REAL,
        gitarre_arrangement REAL,
        gitarre_technik REAL,
        gitarre_timing REAL,
        gitarre_ausdruck REAL,
        zusammenspiel_timing REAL,
        zusammenspiel_dynamik REAL,
        zusammenspiel_buehnenpraesenz REAL,
        zusammenspiel_performance REAL
    )
    ''')
    conn.commit()

def get_all_songs(conn):
    cursor = conn.cursor()
    cursor.execute("""
    SELECT id, name, 
           (gesang_textsicherheit + gesang_timing + gesang_intonation + gesang_ausdruck) / 4.0 as gesang,
           (gitarre_arrangement + gitarre_technik + gitarre_timing + gitarre_ausdruck) / 4.0 as gitarre,
           (zusammenspiel_timing + zusammenspiel_dynamik + zusammenspiel_buehnenpraesenz + zusammenspiel_performance) / 4.0 as zusammenspiel,
           overall_rating 
    FROM songs
    """)
    songs = cursor.fetchall()
    print(f"Abgerufene Songs: {songs}")  # Debug-Ausgabe
    return songs

def get_song_ratings(conn, song_name):
    cursor = conn.cursor()
    cursor.execute("""
    SELECT gesang_textsicherheit, gesang_timing, gesang_intonation, gesang_ausdruck,
           gitarre_arrangement, gitarre_technik, gitarre_timing, gitarre_ausdruck,
           zusammenspiel_timing, zusammenspiel_dynamik, zusammenspiel_buehnenpraesenz, zusammenspiel_performance,
           overall_rating
    FROM songs WHERE name = ?
    """, (song_name,))
    result = cursor.fetchone()
    if result:
        return {
            "Gesang_Textsicherheit": result[0] or 0,
            "Gesang_Timing": result[1] or 0,
            "Gesang_Intonation": result[2] or 0,
            "Gesang_Ausdruck": result[3] or 0,
            "Gitarre_Arrangement": result[4] or 0,
            "Gitarre_Technik": result[5] or 0,
            "Gitarre_Timing": result[6] or 0,
            "Gitarre_Ausdruck": result[7] or 0,
            "Zusammenspiel_Timing": result[8] or 0,
            "Zusammenspiel_Dynamik": result[9] or 0,
            "Zusammenspiel_Buehnenpraesenz": result[10] or 0,
            "Zusammenspiel_Performance": result[11] or 0,
            "Overall": result[12] or 0
        }
    return {}

def update_song_rating(conn, song_name, overall_rating, subcategory_ratings):
    cursor = conn.cursor()
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
    UPDATE songs
    SET overall_rating = ?, last_evaluation = ?,
        gesang_textsicherheit = ?, gesang_timing = ?, gesang_intonation = ?, gesang_ausdruck = ?,
        gitarre_arrangement = ?, gitarre_technik = ?, gitarre_timing = ?, gitarre_ausdruck = ?,
        zusammenspiel_timing = ?, zusammenspiel_dynamik = ?, zusammenspiel_buehnenpraesenz = ?, zusammenspiel_performance = ?
    WHERE name = ?
    """, (
        overall_rating, current_time,
        subcategory_ratings['Gesang_Textsicherheit'], subcategory_ratings['Gesang_Timing'],
        subcategory_ratings['Gesang_Intonation'], subcategory_ratings['Gesang_Ausdruck'],
        subcategory_ratings['Gitarre_Arrangement'], subcategory_ratings['Gitarre_Technik'],
        subcategory_ratings['Gitarre_Timing'], subcategory_ratings['Gitarre_Ausdruck'],
        subcategory_ratings['Zusammenspiel_Timing'], subcategory_ratings['Zusammenspiel_Dynamik'],
        subcategory_ratings['Zusammenspiel_Buehnenpraesenz'], subcategory_ratings['Zusammenspiel_Performance'],
        song_name
    ))
    conn.commit()

def add_song(conn, song_name):
    cursor = conn.cursor()
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
    INSERT INTO songs (name, last_evaluation, overall_rating,
                       gesang_textsicherheit, gesang_timing, gesang_intonation, gesang_ausdruck,
                       gitarre_arrangement, gitarre_technik, gitarre_timing, gitarre_ausdruck,
                       zusammenspiel_timing, zusammenspiel_dynamik, zusammenspiel_buehnenpraesenz, zusammenspiel_performance)
    VALUES (?, ?, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
    """, (song_name, current_time))
    conn.commit()
    print(f"Song '{song_name}' zur Datenbank hinzugefügt")  # Debug-Ausgabe

def delete_song(conn, song_name):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM songs WHERE name = ?", (song_name,))
    conn.commit()

def check_database_values(conn):
    cursor = conn.cursor()
    cursor.execute("""
    SELECT id, name, overall_rating,
           gesang_textsicherheit, gesang_timing, gesang_intonation, gesang_ausdruck,
           gitarre_arrangement, gitarre_technik, gitarre_timing, gitarre_ausdruck,
           zusammenspiel_timing, zusammenspiel_dynamik, zusammenspiel_buehnenpraesenz, zusammenspiel_performance
    FROM songs
    """)
    rows = cursor.fetchall()
    for row in rows:
        print(f"Song ID: {row[0]}, Name: {row[1]}, Overall: {row[2]}")
        print(f"Gesang: Textsicherheit: {row[3]}, Timing: {row[4]}, Intonation: {row[5]}, Ausdruck: {row[6]}")
        print(f"Gitarre: Arrangement: {row[7]}, Technik: {row[8]}, Timing: {row[9]}, Ausdruck: {row[10]}")
        print(f"Zusammenspiel: Timing: {row[11]}, Dynamik: {row[12]}, Bühnenpräsenz: {row[13]}, Performance: {row[14]}")
        print("---")