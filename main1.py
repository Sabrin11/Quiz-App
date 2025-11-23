import pygame
import sqlite3
import sys
import random

pygame.init()
WIDTH, HEIGHT = 700, 500
WHITE, BLACK, GREEN, RED, LIGHT_GRAY, DARK_GRAY = (255,255,255), (0,0,0), (34,177,76), (200,0,0), (230,230,230), (50,50,50)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Language Learning App")
font_large = pygame.font.SysFont("Arial", 40, bold=True)
font = pygame.font.SysFont("Arial", 28)
font_small = pygame.font.SysFont("Arial", 20)
clock = pygame.time.Clock()


# ---------------- Database Setup ----------------
def init_db():
    conn = sqlite3.connect("words.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        highest_score INTEGER DEFAULT 0
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

    conn.commit()
    conn.close()


# ---------------- Utility Functions ----------------
def draw_text(text, font, color, surface, x, y, center=False):
    txt = font.render(text, True, color)
    rect = txt.get_rect(center=(x, y)) if center else (x, y)
    surface.blit(txt, rect)


def draw_button(x, y, w, h, text, hover=False):
    color = GREEN if hover else DARK_GRAY
    pygame.draw.rect(screen, color, (x, y, w, h), border_radius=12)
    draw_text(text, font, WHITE, screen, x + w//2, y + h//2, center=True)


def input_box(prompt, hidden=False):
    text = ""
    while True:
        screen.fill(LIGHT_GRAY)
        draw_text(prompt, font_large, BLACK, screen, WIDTH//2, 150, center=True)
        masked = "*" * len(text) if hidden else text
        draw_text(masked, font, BLACK, screen, WIDTH//2, 230, center=True)
        draw_text("ENTER = confirm  |  ESC = cancel", font_small, BLACK, screen, WIDTH//2, 280, center=True)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return text
                elif event.key == pygame.K_ESCAPE:
                    return None
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode

        pygame.display.flip()
        clock.tick(30)


def show_message(msg, duration=1200):
    start = pygame.time.get_ticks()
    while pygame.time.get_ticks() - start < duration:
        screen.fill(LIGHT_GRAY)
        draw_text(msg, font_large, BLACK, screen, WIDTH//2, HEIGHT//2, center=True)
        pygame.display.flip()
        clock.tick(30)


# ---------------- User Management ----------------
def register_user():
    username = input_box("Enter new username:")
    if not username:
        return None

    password = input_box("Enter new password:", hidden=True)
    if not password:
        return None

    conn = sqlite3.connect("words.db")
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        show_message("✅ Registration Successful!")
        conn.close()
        return True
    except sqlite3.IntegrityError:
        show_message("❌ Username already exists!")
        conn.close()
        return False


def login_user():
    username = input_box("Enter username:")
    if not username:
        return None

    password = input_box("Enter password:", hidden=True)
    if not password:
        return None

    conn = sqlite3.connect("words.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, password, highest_score FROM users WHERE username=? AND password=?",
                   (username, password))
    user = cursor.fetchone()
    conn.close()

    if user:
        show_message(f"Welcome {username}!")
        return user
    else:
        show_message("❌ Invalid credentials!")
        return None


def login_menu():
    user = None
    while not user:
        screen.fill(LIGHT_GRAY)
        draw_text("🔐 Login or Register", font_large, BLACK, screen, WIDTH//2, 90, center=True)

        login_btn = pygame.Rect(190, 180, 320, 55)
        reg_btn = pygame.Rect(190, 260, 320, 55)
        quit_btn = pygame.Rect(190, 340, 320, 55)

        mouse = pygame.mouse.get_pos()
        click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True

        buttons = [
            (login_btn, "Login", login_user),
            (reg_btn, "Register", register_user),
            (quit_btn, "Exit", lambda: sys.exit()),
        ]

        for rect, text, func in buttons:
            hover = rect.collidepoint(mouse)
            draw_button(rect.x, rect.y, rect.w, rect.h, text, hover)
            if hover and click:
                attempt = func()
                if attempt:
                    user = attempt

        pygame.display.flip()
        clock.tick(60)

    return user


# ---------------- Pre Quiz ----------------
def pre_quiz_welcome(user):
    running = True
    while running:
        screen.fill(LIGHT_GRAY)
        draw_text(f"Welcome {user[1]}!", font_large, GREEN, screen, WIDTH//2, 120, center=True)
        draw_text("Start your Quiz Adventure ✨", font, BLACK, screen, WIDTH//2, 170, center=True)

        start_btn = pygame.Rect(WIDTH//2 - 130, 280, 260, 70)

        mouse = pygame.mouse.get_pos()
        click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True

        hover = start_btn.collidepoint(mouse)
        draw_button(start_btn.x, start_btn.y, start_btn.w, start_btn.h, "Start Quiz", hover)

        if hover and click:
            return

        pygame.display.flip()
        clock.tick(60)


# ---------------- Language Selection ----------------
def language_selection():
    selecting = True
    selected_language = None

    buttons = {
        "Spanish": pygame.Rect(220, 160, 260, 60),
        "Japanese": pygame.Rect(220, 230, 260, 60),
        "Korean": pygame.Rect(220, 300, 260, 60),
    }

    while selecting:
        screen.fill(LIGHT_GRAY)
        draw_text("Select a Language", font_large, BLACK, screen, WIDTH//2, 80, center=True)
        draw_text("20 seconds per quiz", font_small, BLACK, screen, WIDTH//2, 120, center=True)

        mouse = pygame.mouse.get_pos()
        click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True

        for lang, rect in buttons.items():
            hover = rect.collidepoint(mouse)
            draw_button(rect.x, rect.y, rect.w, rect.h, lang, hover)

            if hover and click:
                selected_language = lang
                selecting = False

        pygame.display.flip()
        clock.tick(60)

    return selected_language


# ---------------- Load Words ----------------
def get_words(language):
    conn = sqlite3.connect("words.db")
    cursor = conn.cursor()
    cursor.execute("SELECT english, translated FROM words WHERE language=?", (language,))
    words = cursor.fetchall()
    conn.close()
    random.shuffle(words)
    return words


def get_choices(correct, all_words):
    choices = [correct]
    while len(choices) < 3:
        option = random.choice(all_words)
        if option != correct and option not in choices:
            choices.append(option)
    random.shuffle(choices)
    return choices


# ---------------- Quiz ----------------
def main(user):
    language = language_selection()
    word_pairs = get_words(language)

    all_translations = [pair[1] for pair in word_pairs]

    current = 0
    score = 0

    feedback = ""
    feedback_timer = 0
    need_new_choices = True
    selected_option = None
    choices = []

    option_rects = [
        pygame.Rect(180, 220, 340, 45),
        pygame.Rect(180, 280, 340, 45),
        pygame.Rect(180, 340, 340, 45),
    ]

    while True:
        screen.fill(LIGHT_GRAY)

        mouse = pygame.mouse.get_pos()
        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True

        # ---------------- END OF QUIZ ----------------
        if current >= len(word_pairs):
            total = len(word_pairs)
            percent = round((score / total) * 100) if total > 0 else 0

            draw_text("🎉 All Done!", font_large, GREEN, screen, WIDTH//2, 150, center=True)
            draw_text(f"Score: {score}/{total}", font, BLACK, screen, WIDTH//2, 210, center=True)
            draw_text(f"Accuracy: {percent}%", font, BLACK, screen, WIDTH//2, 250, center=True)

            # Update high score
            if score > user[3]:
                conn = sqlite3.connect("words.db")
                cursor = conn.cursor()
                cursor.execute("UPDATE users SET highest_score=? WHERE id=?", (score, user[0]))
                conn.commit()
                conn.close()
                draw_text("🎯 NEW HIGH SCORE!", font, RED, screen, WIDTH//2, 290, center=True)

            draw_text("Press ESC to exit", font_small, BLACK, screen, WIDTH//2, 330, center=True)

            if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                sys.exit()

        else:
            english, correct_answer = word_pairs[current]

            if need_new_choices:
                choices = get_choices(correct_answer, all_translations)
                need_new_choices = False

            draw_text(f"Translate to {language}", font_small, BLACK, screen, WIDTH//2, 50, center=True)
            draw_text(english, font_large, BLACK, screen, WIDTH//2, 110, center=True)
            draw_text(f"Score: {score}", font_small, BLACK, screen, WIDTH - 120, 20)

            # --- Option Buttons ---
            for i, rect in enumerate(option_rects):
                hover = rect.collidepoint(mouse)
                draw_button(rect.x, rect.y, rect.w, rect.h, choices[i], hover)

                if hover and click and not feedback:
                    selected_option = choices[i]
                    if selected_option == correct_answer:
                        feedback = "Correct!"
                        score += 1
                    else:
                        feedback = "Wrong!"

                    feedback_timer = pygame.time.get_ticks()

            # --- FEEDBACK BLOCK (SAFE VERSION) ---
            if feedback:
                color = GREEN if feedback == "Correct!" else RED
                draw_text(feedback, font, color, screen, WIDTH//2, 405, center=True)

                y = 440
                for opt in choices:
                    if opt == correct_answer:
                        msg = f"{opt}  ✓ Correct"
                        col = GREEN
                    elif opt == selected_option:
                        msg = f"{opt}  ✗ Wrong"
                        col = RED
                    else:
                        msg = opt
                        col = BLACK

                    draw_text(msg, font_small, col, screen, WIDTH//2, y, center=True)
                    y += 25

                if pygame.time.get_ticks() - feedback_timer > 1800:
                    feedback = ""
                    selected_option = None
                    current += 1
                    need_new_choices = True

        pygame.display.flip()
        clock.tick(60)


# ---------------- Main ----------------
if __name__ == "__main__":
    init_db()
    user = login_menu()
    pre_quiz_welcome(user)
    main(user)
