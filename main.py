import pygame
import sqlite3
import sys
import random
from database import DB_NAME, create_tables, populate_words, save_session, load_session

pygame.init()
WIDTH, HEIGHT = 800, 600
WHITE, BLACK, GREEN, RED, LIGHT_GRAY, DARK_GRAY = (255,255,255),(0,0,0),(34,177,76),(200,0,0),(230,230,230),(50,50,50)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Language Learning App")
font_large = pygame.font.SysFont("Arial", 40, bold=True)
font = pygame.font.SysFont("Arial", 28)
font_small = pygame.font.SysFont("Arial", 20)
clock = pygame.time.Clock()

current_user = None 

admin_name = "siha"
admin_pass = "9898"

# ---------------- Utility ----------------
def draw_text(text, font, color, surface, x, y, center=False):
    txt = font.render(text, True, color)
    rect = txt.get_rect(center=(x,y)) if center else (x,y)
    surface.blit(txt, rect)

def draw_button(x,y,w,h,text,hover=False):
    color = GREEN if hover else DARK_GRAY
    pygame.draw.rect(screen,color,(x,y,w,h),border_radius=12)
    draw_text(text,font,WHITE,surface=screen,x=x+w//2,y=y+h//2,center=True)

def input_box(prompt, hidden=False):
    text=""
    while True:
        screen.fill(LIGHT_GRAY)
        draw_text(prompt,font_large,BLACK,screen,WIDTH//2,150,center=True)
        masked = "*"*len(text) if hidden else text
        draw_text(masked,font,BLACK,screen,WIDTH//2,230,center=True)
        draw_text("ENTER=confirm  ESC=cancel",font_small,BLACK,screen,WIDTH//2,280,center=True)
        for event in pygame.event.get():
            if event.type==pygame.QUIT: sys.exit()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_RETURN: return text
                elif event.key==pygame.K_ESCAPE: return None
                elif event.key==pygame.K_BACKSPACE: text=text[:-1]
                else: text+=event.unicode
        pygame.display.flip()
        clock.tick(30)

def show_message(msg,duration=1200):
    start=pygame.time.get_ticks()
    while pygame.time.get_ticks()-start<duration:
        screen.fill(LIGHT_GRAY)
        draw_text(msg,font_large,BLACK,screen,WIDTH//2,HEIGHT//2,center=True)
        pygame.display.flip()
        clock.tick(30)

# ---------------- User Management ----------------
def register_user():
    username=input_box("Enter new username:")
    if not username: return None
    password=input_box("Enter new password:",hidden=True)
    if not password: return None

    conn=sqlite3.connect(DB_NAME)
    cursor=conn.cursor()
    # Check duplicate username
    cursor.execute("SELECT * FROM users WHERE username=?", (username,))
    if cursor.fetchone():
        show_message(" Username already exists!")
        conn.close()
        return False

    cursor.execute("INSERT INTO users (username,password,role) VALUES (?,?,?)",(username,password,"user"))
    conn.commit()
    conn.close()
    show_message(" Registration Successful!")
    return True

def login_user():
    username=input_box("Enter username:")
    if not username: return None
    password=input_box("Enter password:",hidden=True)
    if not password: return None

    # Admin fixed
    if username == admin_name and password == admin_pass:
        user = (0, admin_name, "admin")
        save_session(user[0])
        show_message(f"Welcome {username} (Admin)")
        return user

    # Normal user
    conn=sqlite3.connect(DB_NAME)
    cursor=conn.cursor()
    cursor.execute("SELECT id,username,role FROM users WHERE username=? AND password=?",(username,password))
    user=cursor.fetchone()
    conn.close()
    if user:
        save_session(user[0])
        show_message(f"Welcome {username}!")
        return user
    else:
        show_message(" Invalid credentials!")
        return None

# ---------------- Admin Panel ----------------
def admin_panel():
    running=True
    while running:
        screen.fill(LIGHT_GRAY)
        mx,my=pygame.mouse.get_pos()
        click=False
        for event in pygame.event.get():
            if event.type==pygame.QUIT: sys.exit()
            if event.type==pygame.MOUSEBUTTONDOWN: click=True
        buttons = {
            "Populate Words":(250,100,300,50),
            "List Words":(250,180,300,50),
            "Add Word":(250,260,300,50),
            "Delete Word":(250,340,300,50),
            "Exit":(250,420,300,50)
        }
        for text,rect_vals in buttons.items():
            rect=pygame.Rect(rect_vals)
            hover=rect.collidepoint(mx,my)
            draw_button(rect.x,rect.y,rect.w,rect.h,text,hover)
            if hover and click:
                if text=="Populate Words":
                    populate_words()
                    show_message(" Words populated!")
                elif text=="List Words":
                    list_words()
                elif text=="Add Word":
                    add_word()
                    list_words()  
                elif text=="Delete Word":
                    delete_word()
                    list_words()  
                elif text=="Exit":
                    running=False
        pygame.display.flip()
        clock.tick(60)

def list_words():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, english, translated, language FROM words ORDER BY id")
    words = cursor.fetchall()
    conn.close()

    page = 0
    per_page = 12 
    total_pages = (len(words) + per_page - 1) // per_page

    while True:
        screen.fill(LIGHT_GRAY)
        draw_text(" Words List", font_large, BLACK, screen, WIDTH//2, 40, center=True)

        start = page * per_page
        end = min(start + per_page, len(words))
        y = 100
        for word in words[start:end]:
            line = f"{word[0]}. {word[1]} => {word[2]} ({word[3]})"
            draw_text(line, font_small, BLACK, screen, WIDTH//2, y, center=True)
            y += 40

        draw_text(f"Page {page+1}/{total_pages} - Press N for Next, P for Prev, ESC to exit", 
                  font_small, RED, screen, WIDTH//2, HEIGHT-40, center=True)

        pygame.display.flip()
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return
                    elif event.key == pygame.K_n and page < total_pages - 1:
                        page += 1
                        waiting = False
                    elif event.key == pygame.K_p and page > 0:
                        page -= 1
                        waiting = False

def add_word():
    english = input_box("Enter English word:")
    if not english: return
    translated = input_box("Enter Translated word:")
    if not translated: return
    language = input_box("Enter Language:")
    if not language: return
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO words (english,translated,language) VALUES (?,?,?)",
                   (english, translated, language))
    conn.commit()
    conn.close()
    show_message(" Word added!")

def delete_word():
    identifier=input_box("Enter Word ID or English:")
    if not identifier: return
    conn=sqlite3.connect(DB_NAME)
    cursor=conn.cursor()
    if identifier.isdigit(): 
        cursor.execute("DELETE FROM words WHERE id=?",(int(identifier),))
    else: 
        cursor.execute("DELETE FROM words WHERE english=?",(identifier,))
    if cursor.rowcount==0: 
        show_message(" Not found!")
    else: 
        show_message(" Word deleted!")
    conn.commit()
    conn.close()

# ---------------- Quiz ---------------- 
def language_selection():
    selecting=True
    selected_language=None
    buttons={"Spanish":pygame.Rect(220,160,260,60),"Japanese":pygame.Rect(220,230,260,60),"Korean":pygame.Rect(220,300,260,60)}
    while selecting:
        screen.fill(LIGHT_GRAY)
        draw_text("Select Language",font_large,BLACK,screen,WIDTH//2,80,center=True)
        mouse=pygame.mouse.get_pos()
        click=False
        for event in pygame.event.get():
            if event.type==pygame.QUIT: sys.exit()
            if event.type==pygame.MOUSEBUTTONDOWN: click=True
        for lang,rect in buttons.items():
            hover=rect.collidepoint(mouse)
            draw_button(rect.x,rect.y,rect.w,rect.h,lang,hover)
            if hover and click:
                selected_language=lang
                selecting=False
        pygame.display.flip()
        clock.tick(60)
    return selected_language

def get_words(language,limit=20):
    conn=sqlite3.connect(DB_NAME)
    cursor=conn.cursor()
    cursor.execute("SELECT english,translated FROM words WHERE language=?",(language,))
    words=cursor.fetchall()
    conn.close()
    random.shuffle(words)
    return words[:limit]

def quiz(user):
    while True:
        language = language_selection()
        word_pairs = get_words(language, limit=20)
        if not word_pairs:
            show_message(" No words found for this language!")
            return

        all_words_dict = {t: e for e, t in word_pairs}
        current = 0
        score = 0
        feedback = ""
        need_new_choices = True
        selected_option = None
        choices = []

        option_rects = [pygame.Rect(180,220,340,45), pygame.Rect(180,280,340,45), pygame.Rect(180,340,340,45)]
        exit_rect = pygame.Rect(WIDTH-140, HEIGHT-60, 120, 45)
        question_time_limit = 20
        question_start_time = pygame.time.get_ticks()
        waiting_for_key = False

        while True:
            screen.fill(LIGHT_GRAY)
            mouse = pygame.mouse.get_pos()
            click = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN: click = True
                if waiting_for_key and event.type == pygame.KEYDOWN:
                    waiting_for_key = False
                    feedback = ""
                    selected_option = None
                    current += 1
                    need_new_choices = True

            hover_exit = exit_rect.collidepoint(mouse)
            draw_button(exit_rect.x, exit_rect.y, exit_rect.w, exit_rect.h, "Exit", hover_exit)
            if hover_exit and click:
                return

            if current >= len(word_pairs):
                total = len(word_pairs)
                percent = round((score/total)*100)
                draw_text(" Quiz Finished!", font_large, GREEN, screen, WIDTH//2, 150, center=True)
                draw_text(f"Score: {score}/{total}", font, BLACK, screen, WIDTH//2, 210, center=True)
                draw_text(f"Accuracy: {percent}%", font, BLACK, screen, WIDTH//2, 250, center=True)
                draw_text("Press ESC to exit or any key to replay", font_small, BLACK, screen, WIDTH//2, 330, center=True)
                keys = pygame.key.get_pressed()
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        return
                pygame.display.flip()
                clock.tick(60)
                continue

            english, correct_answer = word_pairs[current]

            if need_new_choices:
                choices = [correct_answer]
                while len(choices) < 3:
                    option = random.choice(list(all_words_dict.keys()))
                    if option not in choices: choices.append(option)
                random.shuffle(choices)
                need_new_choices = False
                question_start_time = pygame.time.get_ticks()

            elapsed = (pygame.time.get_ticks() - question_start_time)/1000
            remaining = max(0, int(question_time_limit - elapsed))
            draw_text(f"Time: {remaining}s", font_small, RED, screen, 120, 20)

            if remaining <= 0 and not feedback:
                selected_option = None
                feedback = "Time's up!"
                waiting_for_key = True

            draw_text(f"Translate to {language}", font_small, BLACK, screen, WIDTH//2, 50, center=True)
            draw_text(english, font_large, BLACK, screen, WIDTH//2, 110, center=True)
            draw_text(f"Score: {score}", font_small, BLACK, screen, WIDTH-120, 20)

            if not waiting_for_key:
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
                        waiting_for_key = True

            if feedback:
                color = GREEN if feedback.startswith("Correct") else RED
                draw_text(feedback, font, color, screen, WIDTH//2, 400, center=True)

                y_display = 440
                for opt in choices:
                    english_word = all_words_dict.get(opt, "N/A")
                    draw_text(f"{opt} => {english_word}", font_small, BLACK, screen, WIDTH//2, y_display, center=True)
                    y_display += 30

                draw_text("Press any key for next", font_small, RED, screen, WIDTH//2, y_display+10, center=True)

            pygame.display.flip()
            clock.tick(60)

# ---------------- Main Menu ----------------
def main_menu():
    global current_user
    while True:
        screen.fill(LIGHT_GRAY)
        draw_text(f" Welcome {current_user[1]}", font_large, BLACK, screen, WIDTH//2, 90, center=True)
        buttons = [
            (pygame.Rect(250,180,300,55), "Quiz", lambda: quiz(current_user)),
            (pygame.Rect(250,260,300,55), "Admin Panel", lambda: admin_panel()) if current_user[2]=="admin" else None,
            (pygame.Rect(250,340,300,55), "Logout", lambda: logout())
        ]
        buttons = [b for b in buttons if b]
        mouse=pygame.mouse.get_pos()
        click=False
        for event in pygame.event.get():
            if event.type==pygame.QUIT: sys.exit()
            if event.type==pygame.MOUSEBUTTONDOWN: click=True
        for rect,text,func in buttons:
            hover=rect.collidepoint(mouse)
            draw_button(rect.x,rect.y,rect.w,rect.h,text,hover)
            if hover and click:
                func()
        pygame.display.flip()
        clock.tick(60)

def logout():
    global current_user
    save_session(None)
    current_user = None
    login_register_menu()

# ---------------- Login/Register Menu ----------------
def login_register_menu():
    global current_user
    while not current_user:
        screen.fill(LIGHT_GRAY)
        draw_text(" Login / Register",font_large,BLACK,screen,WIDTH//2,90,center=True)
        login_btn=pygame.Rect(250,180,300,55)
        reg_btn=pygame.Rect(250,260,300,55)
        quit_btn=pygame.Rect(250,340,300,55)
        mouse=pygame.mouse.get_pos()
        click=False
        for event in pygame.event.get():
            if event.type==pygame.QUIT: sys.exit()
            if event.type==pygame.MOUSEBUTTONDOWN: click=True

        buttons=[(login_btn,"Login",login_user),(reg_btn,"Register",register_user),(quit_btn,"Exit",lambda:sys.exit())]

        for rect,text,func in buttons:
            hover=rect.collidepoint(mouse)
            draw_button(rect.x,rect.y,rect.w,rect.h,text,hover)
            if hover and click:
                if func == register_user:
                    success = func()
                    if success:
                        show_message("Please login now!")
                        attempt = login_user()
                        if attempt: current_user = attempt
                else:
                    attempt = func()
                    if attempt: current_user = attempt
        pygame.display.flip()
        clock.tick(60)
    return current_user

# ---------------- Main ----------------
if __name__=="__main__":
    create_tables()
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM words")
    count = cursor.fetchone()[0]
    conn.close()
    if count == 0: populate_words()

    # Auto login
    current_user = load_session()
    if not current_user:
        login_register_menu()

    main_menu()
