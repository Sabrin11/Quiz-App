import sqlite3

DB_NAME = "data.db"

def create_tables():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS words (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            english TEXT NOT NULL,
            translated TEXT NOT NULL,
            language TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_score (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            highest_score INTEGER DEFAULT 0,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS session (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER
        )
    """)
    cursor.execute("INSERT OR IGNORE INTO users (id, username, password, role) VALUES (1, 'admin', 'admin', 'admin')")

    conn.commit()
    conn.close()
    print("✅ Database initialized.")

def populate_words():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Spanish words
    spanish_data = [
        ("Hello", "Hola"), ("Goodbye", "Adios"), ("Thank you", "Gracias"),
        ("Dog", "Perro"), ("Cat", "Gato"), ("Love", "Amor"),
        ("Water", "Agua"), ("Food", "Comida"), ("Book", "Libro"),
        ("Pen", "Pluma"), ("Chair", "Silla"), ("Table", "Mesa"),
        ("Window", "Ventana"), ("Door", "Puerta"), ("Friend", "Amigo"),
        ("Family", "Familia"), ("Money", "Dinero"), ("School", "Escuela"),
        ("Teacher", "Maestro"), ("Student", "Estudiante"), ("House", "Casa"),
        ("Car", "Coche"), ("Bus", "Autobús"), ("Train", "Tren"),
        ("Plane", "Avión"), ("Street", "Calle"), ("City", "Ciudad"),
        ("Country", "País"), ("World", "Mundo"), ("Happy", "Feliz"),
        ("Sad", "Triste"), ("Angry", "Enojado"), ("Tired", "Cansado"),
        ("Beautiful", "Hermoso"), ("Ugly", "Feo"), ("Big", "Grande"),
        ("Small", "Pequeño"), ("Fast", "Rápido"), ("Slow", "Lento"),
        ("Hot", "Caliente"), ("Cold", "Frío"), ("Morning", "Mañana"),
        ("Night", "Noche"), ("Day", "Día"), ("Week", "Semana"),
        ("Month", "Mes"), ("Year", "Año"), ("Today", "Hoy"),
        ("Tomorrow", "Mañana"), ("Yesterday", "Ayer"), ("Yes", "Sí"),
        ("No", "No"), ("Maybe", "Quizás"), ("Always", "Siempre"),
        ("Never", "Nunca"), ("Sometimes", "A veces"), ("Now", "Ahora"),
        ("Later", "Luego"), ("Before", "Antes"), ("After", "Después"),
        ("Easy", "Fácil"), ("Hard", "Difícil"), ("Question", "Pregunta"),
        ("Answer", "Respuesta"), ("Problem", "Problema"), ("Solution", "Solución"),
        ("Work", "Trabajo"), ("Job", "Empleo"), ("Computer", "Computadora"),
        ("Phone", "Teléfono"), ("Internet", "Internet"), ("Music", "Música"),
        ("Movie", "Película"), ("Game", "Juego"), ("Sport", "Deporte"),
        ("Run", "Correr"), ("Walk", "Caminar"), ("Eat", "Comer"),
        ("Drink", "Beber"), ("Sleep", "Dormir"), ("Wake", "Despertar"),
        ("Read", "Leer"), ("Write", "Escribir"), ("Speak", "Hablar"),
        ("Listen", "Escuchar"), ("Look", "Mirar"), ("See", "Ver"),
        ("Buy", "Comprar"), ("Sell", "Vender"), ("Open", "Abrir"),
        ("Close", "Cerrar"), ("Start", "Empezar"), ("Stop", "Detener"),
        ("Win", "Ganar"), ("Lose", "Perder"), ("Help", "Ayuda"),
        ("Need", "Necesitar"), ("Want", "Querer"), ("Like", "Gustar"),
        ("Hate", "Odiar"), ("Live", "Vivir"), ("Die", "Morir")
    ]

    # Japanese words
    japanese_data = [
        ("Hello", "Konnichiwa"), ("Goodbye", "Sayonara"), ("Thank you", "Arigatou"),
        ("Dog", "Inu"), ("Cat", "Neko"), ("Love", "Ai"),
        ("Water", "Mizu"), ("Food", "Tabemono"), ("Book", "Hon"),
        ("Pen", "Pen"), ("Chair", "Isu"), ("Table", "Tēburu"),
        ("Window", "Mado"), ("Door", "Doa"), ("Friend", "Tomodachi"),
        ("Family", "Kazoku"), ("Money", "Okane"), ("School", "Gakkou"),
        ("Teacher", "Sensei"), ("Student", "Seito"), ("House", "Ie"),
        ("Car", "Kuruma"), ("Bus", "Basu"), ("Train", "Densha"),
        ("Plane", "Hikouki"), ("Street", "Michi"), ("City", "Toshi"),
        ("Country", "Kuni"), ("World", "Sekai"), ("Happy", "Ureshii"),
        ("Sad", "Kanashii"), ("Angry", "Okotteiru"), ("Tired", "Tsukareta"),
        ("Beautiful", "Utsukushii"), ("Ugly", "Minikui"), ("Big", "Ōkii"),
        ("Small", "Chiisai"), ("Fast", "Hayai"), ("Slow", "Osoi"),
        ("Hot", "Atsui"), ("Cold", "Samui"), ("Morning", "Asa"),
        ("Night", "Yoru"), ("Day", "Hi"), ("Week", "Shūkan"),
        ("Month", "Tsuki"), ("Year", "Toshi"), ("Today", "Kyou"),
        ("Tomorrow", "Ashita"), ("Yesterday", "Kinou"), ("Yes", "Hai"),
        ("No", "Iie"), ("Maybe", "Tabun"), ("Always", "Itsumo"),
        ("Never", "Zettai ni nai"), ("Sometimes", "Tokidoki"), ("Now", "Ima"),
        ("Later", "Ato de"), ("Before", "Mae ni"), ("After", "Ato"),
        ("Easy", "Kantan"), ("Hard", "Muzukashii"), ("Question", "Shitsumon"),
        ("Answer", "Kotae"), ("Problem", "Mondai"), ("Solution", "Kaiketsu"),
        ("Work", "Shigoto"), ("Job", "Shigoto"), ("Computer", "Konpyuutaa"),
        ("Phone", "Denwa"), ("Internet", "Intānetto"), ("Music", "Ongaku"),
        ("Movie", "Eiga"), ("Game", "Gēmu"), ("Sport", "Supōtsu"),
        ("Run", "Hashiru"), ("Walk", "Aruku"), ("Eat", "Taberu"),
        ("Drink", "Nomu"), ("Sleep", "Neru"), ("Wake", "Okiru"),
        ("Read", "Yomu"), ("Write", "Kaku"), ("Speak", "Hanasu"),
        ("Listen", "Kiku"), ("Look", "Miru"), ("See", "Miru"),
        ("Buy", "Kau"), ("Sell", "Uru"), ("Open", "Akeru"),
        ("Close", "Shimeru"), ("Start", "Hajimeru"), ("Stop", "Tomeru"),
        ("Win", "Katsu"), ("Lose", "Makeru"), ("Help", "Tetsudau"),
        ("Need", "Hitsuyou"), ("Want", "Hoshii"), ("Like", "Suki"),
        ("Hate", "Kirai"), ("Live", "Ikiru"), ("Die", "Shinu")
    ]

    # Korean words
    korean_data = [
        ("Hello", "Annyeonghaseyo"), ("Goodbye", "Annyeonghi gaseyo"), ("Thank you", "Gamsahamnida"),
        ("Dog", "Gae"), ("Cat", "Goyangi"), ("Love", "Sarang"),
        ("Water", "Mul"), ("Food", "Eumsik"), ("Book", "Chaek"),
        ("Pen", "Pen"), ("Chair", "Uija"), ("Table", "Teibeul"),
        ("Window", "Changmun"), ("Door", "Mun"), ("Friend", "Chingu"),
        ("Family", "Gajok"), ("Money", "Don"), ("School", "Hakgyo"),
        ("Teacher", "Seonsaengnim"), ("Student", "Haksaeng"), ("House", "Jip"),
        ("Car", "Jadongcha"), ("Bus", "Beoseu"), ("Train", "Gicha"),
        ("Plane", "Bihaenggi"), ("Street", "Geori"), ("City", "Dosi"),
        ("Country", "Nara"), ("World", "Segye"), ("Happy", "Haengbokhan"),
        ("Sad", "Seulpeun"), ("Angry", "Hwanan"), ("Tired", "Pigonan"),
        ("Beautiful", "Areumdawoon"), ("Ugly", "Motsaenggin"), ("Big", "Keun"),
        ("Small", "Jageun"), ("Fast", "Ppareun"), ("Slow", "Neurin"),
        ("Hot", "Tteugeoun"), ("Cold", "Chuun"), ("Morning", "Achim"),
        ("Night", "Bam"), ("Day", "Naj"), ("Week", "Ju"),
        ("Month", "Wol"), ("Year", "Nyeon"), ("Today", "Oneul"),
        ("Tomorrow", "Naeil"), ("Yesterday", "Eoje"), ("Yes", "Ne"),
        ("No", "Aniyo"), ("Maybe", "Amado"), ("Always", "Hangsang"),
        ("Never", "Jeoldae"), ("Sometimes", "Gakkeum"), ("Now", "Jigeum"),
        ("Later", "Najunge"), ("Before", "Jeone"), ("After", "Hue"),
        ("Easy", "Swiun"), ("Hard", "Eoryeoun"), ("Question", "Jilmun"),
        ("Answer", "Dap"), ("Problem", "Munje"), ("Solution", "Haegyeol"),
        ("Work", "Il"), ("Job", "Jigeop"), ("Computer", "Keompyuteo"),
        ("Phone", "Jeonhwagi"), ("Internet", "Inteonet"), ("Music", "Eumak"),
        ("Movie", "Yeonghwa"), ("Game", "Geim"), ("Sport", "Seupocheu"),
        ("Run", "Dallida"), ("Walk", "Geotda"), ("Eat", "Meokda"),
        ("Drink", "Masida"), ("Sleep", "Jada"), ("Wake", "Kkaeda"),
        ("Read", "Ikda"), ("Write", "Sseuda"), ("Speak", "Malhada"),
        ("Listen", "Deutda"), ("Look", "Boda"), ("See", "Boda"),
        ("Buy", "Sada"), ("Sell", "Palda"), ("Open", "Yeolda"),
        ("Close", "Dadda"), ("Start", "Sijakada"), ("Stop", "Meomchuda"),
        ("Win", "Igida"), ("Lose", "Jida"), ("Help", "Dopda"),
        ("Need", "Piryohada"), ("Want", "Wonhada"), ("Like", "Joahada"),
        ("Hate", "Silheohada"), ("Live", "Salda"), ("Die", "Jukda")
    ]

    all_words = [(e,t,"Spanish") for e,t in spanish_data] + \
                [(e,t,"Japanese") for e,t in japanese_data] + \
                [(e,t,"Korean") for e,t in korean_data]

    cursor.executemany("INSERT INTO words (english, translated, language) VALUES (?, ?, ?)", all_words)
    conn.commit()
    conn.close()
    print(f"✅ Words populated ({len(all_words)} total).")

def save_session(user_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM session") 
    if user_id:
        cursor.execute("INSERT INTO session (user_id) VALUES (?)", (user_id,))
    conn.commit()
    conn.close()

def load_session():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT user_id FROM session LIMIT 1")
    row = cursor.fetchone()
    conn.close()
    if row:
        user_id = row[0]
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, role FROM users WHERE id=?", (user_id,))
        user = cursor.fetchone()
        conn.close()
        return user
    return None
