import sqlite3

DATABASE_FILE = "music_catalog.db"

def get_db_connection():
    """Устанавливает соединение с базой данных."""
    connection = None
    try:
        connection = sqlite3.connect(DATABASE_FILE)
        connection.row_factory = sqlite3.Row
        return connection
    except sqlite3.Error as e:
        print(f"Ошибка подключения к базе данных: {e}")
        if connection:
            connection.close()
        return None

def create_database(db_name):
    try:
        connection = sqlite3.connect(db_name)
        cursor = connection.cursor()

        # Таблица artists
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS artists (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                biography TEXT
            )
        ''')

        # Таблица genres
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS genres (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT
            )
        ''')

        # Таблица albums
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS albums (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                artist_id INTEGER NOT NULL,
                description TEXT,
                FOREIGN KEY (artist_id) REFERENCES artists(id)
            )
        ''')

        # Таблица songs (с добавленным album_id)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS songs (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                artist_id INTEGER NOT NULL,
                genre_id INTEGER,
                album_id INTEGER,
                year INTEGER NOT NULL,
                FOREIGN KEY (artist_id) REFERENCES artists(id),
                FOREIGN KEY (genre_id) REFERENCES genres(id),
                FOREIGN KEY (album_id) REFERENCES albums(id)
            )
        ''')

        connection.commit()
        print("Таблицы artists, genres, albums и songs созданы успешно.")
    except sqlite3.Error as e:
        print(f"Ошибка при создании таблиц: {e}")
    finally:
        if connection:
            connection.close()
