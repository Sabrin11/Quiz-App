import sqlite3


DB_NAME = "words.db"


def create_tables():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()


    # Drop and recreate words table
    cursor.execute("DROP TABLE IF EXISTS words")
    cursor.execute("""
        CREATE TABLE words (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            english TEXT NOT NULL,
            translated TEXT NOT NULL,
            language TEXT NOT NULL
        )
    """)


    # Single-user table to store highest score
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_score (
            id INTEGER PRIMARY KEY,
            highest_score INTEGER DEFAULT 0
        )
    """)


    # Insert default user if not exists
    cursor.execute("INSERT OR IGNORE INTO user_score (id, highest_score) VALUES (1, 0)")
   
    conn.commit()
    conn.close()
    print("✅ Tables created successfully.")


# ------------------- Words management -------------------
def populate_words():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()


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


    spanish_words = [(en, tr, "Spanish") for en, tr in spanish_data]
    japanese_words = [(en, tr, "Japanese") for en, tr in japanese_data]
    korean_words = [(en, tr, "Korean") for en, tr in korean_data]


    cursor.executemany("INSERT INTO words (english, translated, language) VALUES (?, ?, ?)",
                       spanish_words + japanese_words + korean_words)


    conn.commit()
    conn.close()
    print("✅ Words populated.")


def list_words():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, english, translated, language FROM words ORDER BY id")
    for row in cursor.fetchall():
        print(f"{row[0]}. {row[1]} => {row[2]} ({row[3]})")
    conn.close()


def add_word():
    english = input("Enter English word: ").strip()
    translated = input("Enter Translated word: ").strip()
    language = input("Enter language: ").strip()
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO words (english, translated, language) VALUES (?, ?, ?)",
                   (english, translated, language))
    conn.commit()
    conn.close()
    print("✅ Word added.")


def delete_word():
    identifier = input("Enter word ID or English word to delete: ").strip()
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    if identifier.isdigit():
        cursor.execute("DELETE FROM words WHERE id = ?", (int(identifier),))
    else:
        cursor.execute("DELETE FROM words WHERE english = ?", (identifier,))
    if cursor.rowcount == 0:
        print("❌ No matching word found.")
    else:
        print("✅ Word deleted.")
    conn.commit()
    conn.close()


# ------------------- Highest Score -------------------
def show_highest_score():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT highest_score FROM user_score WHERE id=1")
    score = cursor.fetchone()[0]
    print(f"🏆 Highest Score: {score}")
    conn.close()


def update_highest_score():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    score = int(input("Enter new score: "))
    cursor.execute("SELECT highest_score FROM user_score WHERE id=1")
    highest = cursor.fetchone()[0]
    if score > highest:
        cursor.execute("UPDATE user_score SET highest_score=? WHERE id=1", (score,))
        conn.commit()
        print(f"✅ New highest score saved: {score}")
    else:
        print("ℹ️ Score not higher than current highest.")
    conn.close()


# ------------------- Menu -------------------
def menu():
    create_tables()
    while True:
        print("\n📘 Language Word Manager")
        print("1. Populate words")
        print("2. List all words")
        print("3. Add a new word")
        print("4. Delete a word")
        print("5. Show highest score")
        print("6. Update highest score")
        print("7. Exit")


        choice = input("Choose an option: ").strip()
        if choice == '1':
            populate_words()
        elif choice == '2':
            list_words()
        elif choice == '3':
            add_word()
        elif choice == '4':
            delete_word()
        elif choice == '5':
            show_highest_score()
        elif choice == '6':
            update_highest_score()
        elif choice == '7':
            break
        else:
            print("❌ Invalid choice. Try again.")


if __name__ == "__main__":
    menu()


