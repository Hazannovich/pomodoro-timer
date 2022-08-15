import math
from tkinter import *

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 1
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
SECS_IN_MIN = 60
g_reps = 1
g_timer = None
g_paused = 2
g_count = 2


# ---------------------------- TIMER RESET ------------------------------- #
def pause_timer():
    global g_reps
    global g_paused
    global g_timer
    global g_count
    try:
        if g_paused == 2 or g_paused == 0:
            win.after_cancel(str(g_timer))
            timer_label.config(text="Pause", fg=RED)
            pause_btn.config(text="Play", fg=RED)
            g_paused = 1
        else:
            g_paused = 0
            i = g_reps % 8
            if i == 2 or i == 4 or i == 6:
                timer_label.config(text="Break", fg=PINK)
            elif i == 0:
                timer_label.config(text="Break", fg=RED)
            else:
                timer_label.config(text="Work", fg=GREEN)
            pause_btn.config(text="Pause", fg=RED)
            count_down(g_count)
    except ValueError:
        pass
    finally:
        pass


# ---------------------------- TIMER RESET ------------------------------- #
def reset_timer():
    global g_reps
    global g_paused
    try:
        win.after_cancel(str(g_timer))
        timer_label.config(text="Timer", fg=GREEN)
        start_btn.config(state=NORMAL)
        canvas.itemconfig(timer_text, text=f"{WORK_MIN}:00")
        check_marks.config(text="")
        pause_btn.config(text="Pause")
        g_paused = 2
        g_reps = 1
    except ValueError:
        pass
    finally:
        pass


# ---------------------------- TIMER MECHANISM ------------------------------- #
def start_timer():
    global g_reps
    global g_count
    global g_paused
    i = g_reps % 8
    start_btn.config(state=DISABLED)
    if g_paused == 2:
        win.attributes('-topmost', 0)
        if i == 2 or i == 4 or i == 6:
            g_count = SHORT_BREAK_MIN * SECS_IN_MIN
            timer_label.config(text="Break", fg=PINK)
            count_down(g_count)
        elif i == 0:
            g_count = LONG_BREAK_MIN * SECS_IN_MIN
            timer_label.config(text="Break", fg=RED)
            count_down(g_count)
        else:
            g_count = WORK_MIN * SECS_IN_MIN
            timer_label.config(text="Work", fg=GREEN)
            count_down(g_count)


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def count_down(count):
    global g_reps
    global g_count
    global g_paused
    g_paused = 0
    g_count = count
    minutes = math.floor(count / SECS_IN_MIN)
    seconds = count % SECS_IN_MIN
    canvas.itemconfig(timer_text, text=f"{minutes:02d}:{seconds:02d}")
    if count > 0:
        global g_timer
        g_timer = win.after(1000, count_down, count - 1)
    else:
        win.attributes('-topmost', 1)
        marks = ""
        work_sessions = math.floor(g_reps / 2)
        g_reps += 1
        for _ in range(work_sessions):
            marks += "✔"
        check_marks.config(text=marks)
        g_paused = 2
        start_timer()


# ---------------------------- UI SETUP ------------------------------- #
# Window Config
win = Tk()
win.title("Pomodoro")
win.config(padx=100, pady=50, bg=YELLOW)

# Background Config
canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
tomato_img = PhotoImage(file="tomato.png")
canvas.create_image(100, 112, image=tomato_img)
timer_text = canvas.create_text(103, 130, text=f"{WORK_MIN}:00", fill="white", font=(FONT_NAME, 35, "bold"))
canvas.grid(column=1, row=1)

# Labels
timer_label = Label(fg=GREEN, text="Timer", bg=YELLOW, font=(FONT_NAME, 50))
timer_label.grid(column=1, row=0)
check_marks = Label(fg=GREEN, bg=YELLOW)
check_marks.grid(column=1, row=3)

# Buttons
start_btn = Button(text="Start", fg=RED, highlightbackground=YELLOW, command=start_timer)
reset_btn = Button(text="Reset", fg=RED, highlightbackground=YELLOW, command=reset_timer)
reset_btn.grid(column=2, row=2)
start_btn.grid(column=0, row=2)
pause_btn = Button(text="Pause", fg=RED, highlightbackground=YELLOW, command=pause_timer)
pause_btn.grid(column=1, row=2)

win.mainloop()
