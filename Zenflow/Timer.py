import customtkinter as ctk
import pygame
from PIL import Image

# using pygame mixer for sounds
pygame.mixer.init()

# purple theme colors
PRIMARY = "#5b2872"
HOVER = "#a064c9"
BACK_COLOR = "#2A1045"
LABEL_COLOR = "#3c1e5d"
BORDER = "#a855f7"

#global variable
timeApp=None
#main function 
def open_timer(parent): 
    global timeApp
    if timeApp and timeApp.winfo_exists():
        timeApp.destroy()
        timeApp=None
        return
        
    WORK_TIME = 25
    SHORT_BREAK_TIME = 5
    LONG_BREAK_TIME = 10

    current_mode = "Pomodoro"
    time_left = WORK_TIME * 60
    is_running = False
    pomodoro_count = 0
    timer_id = None
    settings_win = None

    #converting time form seconds to minutes and seconds format
    def format_time(seconds):
        mins, secs = divmod(seconds, 60)
        return f"{mins:02d}:{secs:02d}"
    
    #switching between modes
    def switch_mode(mode):
        nonlocal current_mode, is_running, timer_id
        current_mode = mode
        is_running = False
        if timer_id:
            timeApp.after_cancel(timer_id)
        start_btn.configure(text="Start")
        update_timer_display()
        update_mode_indicator()

        
    #updates timer after every switch    
    def update_timer_display():
        nonlocal time_left
        if current_mode == "Pomodoro":
            time_left = WORK_TIME * 60
        elif current_mode == "Short Break":
            time_left = SHORT_BREAK_TIME * 60
        elif current_mode == "Long Break":
            time_left = LONG_BREAK_TIME * 60
        timer_label.configure(text=format_time(time_left))
        highlight_mode()
    
    #for timer end sound
    def play_sound(file):
        pygame.mixer.music.stop() #always stops before starting a new one
        pygame.mixer.music.load(file)
        pygame.mixer.music.play()

    #start button functionality(pause/start)
    def start_timer():
        nonlocal is_running
        if not is_running:
            is_running = True
            start_btn.configure(text="Pause")
            countdown()
        else:
            is_running = False
            start_btn.configure(text="Start")
            pygame.mixer.music.stop()
    #decreses time by 1 sec per 1 sec
    def countdown():
        nonlocal time_left, is_running, timer_id
        if is_running and time_left > 0:
            time_left -= 1
            timer_label.configure(text=format_time(time_left))
            #adding sound for pomodoro mode
            if time_left == 5 and current_mode == "Pomodoro":
                play_sound("alarm.mp3")
            timer_id = timeApp.after(1000, countdown)
        elif time_left == 0:
            start_btn.configure(text="Start")
            handle_completion()
    #switching mode after time completion
    def handle_completion():
        nonlocal pomodoro_count
        #adding sound for short and long breaks
        if current_mode=="Short Break": 
            play_sound("Twinkle.mp3")
        elif current_mode=="Long Break":
            play_sound("Twinkle.mp3")
        else:
            pygame.mixer.music.stop()
        #mode switching
        if current_mode == "Pomodoro":
            pomodoro_count += 1
            loop_label.configure(text=f"{pomodoro_count % 4}/4")
            if pomodoro_count % 4 == 0:
                switch_mode("Long Break")
            else:
                switch_mode("Short Break")
        else:
            switch_mode("Pomodoro")
        start_timer()
    #skipping time
    def skip_timer():
        nonlocal is_running, timer_id
        if timer_id:
            timeApp.after_cancel(timer_id)
        is_running = False
        start_btn.configure(text="Start")
        handle_completion()

    def open_settings():#opens the settings option
        nonlocal settings_win, WORK_TIME, SHORT_BREAK_TIME, LONG_BREAK_TIME

        if settings_win and settings_win.winfo_exists():
            settings_win.destroy()
            settings_win = None
            return

        def save_settings(event=None):# saves the time for different modes in the settings
            nonlocal WORK_TIME, SHORT_BREAK_TIME, LONG_BREAK_TIME
            try:
                WORK_TIME = int(work_time_entry.get())
                SHORT_BREAK_TIME = int(short_break_time_entry.get())
                LONG_BREAK_TIME = int(long_break_time_entry.get())
                update_timer_display()
                settings_win.destroy()
            except ValueError:
                print("Please enter valid integers")
        #the settings page creation using CTk hehe
        settings_win = ctk.CTkToplevel(timeApp)
        settings_win.title("Settings")
        settings_win.geometry("250x280+654+30")
        settings_win.configure(fg_color=BACK_COLOR)
        settings_win.wm_overrideredirect(True)
        settings_win.bind("<Return>", save_settings)#saves time by pressing enter key

        ctk.CTkLabel(settings_win, text="Pomodoro:").pack(pady=(10, 5))
        work_time_entry = ctk.CTkEntry(settings_win, fg_color=LABEL_COLOR, border_color=BORDER,width=100)
        work_time_entry.insert(0, str(WORK_TIME))
        work_time_entry.pack()

        ctk.CTkLabel(settings_win, text="Short Break:").pack(pady=(10, 5))
        short_break_time_entry = ctk.CTkEntry(settings_win, fg_color=LABEL_COLOR,border_color=BORDER, width=100)
        short_break_time_entry.insert(0, str(SHORT_BREAK_TIME))
        short_break_time_entry.pack()

        ctk.CTkLabel(settings_win, text="Long Break:").pack(pady=(10, 5))
        long_break_time_entry = ctk.CTkEntry(settings_win, fg_color=LABEL_COLOR, border_color=BORDER, width=100)
        long_break_time_entry.insert(0, str(LONG_BREAK_TIME))
        long_break_time_entry.pack()

        ctk.CTkButton(settings_win, text="Save", command=save_settings, fg_color=PRIMARY, hover_color=HOVER, border_color=BORDER).pack(pady=15)
        #keeps the settings window on top(TopLevel)
        settings_win.lift()
        settings_win.attributes('-topmost', True)
        #settings_win.after_idle(settings_win.attributes, '-topmost', False)
        settings_win.focus_force()
    #color of the running mode button
    def highlight_mode():
        pomodoro_btn.configure(fg_color="transparent")
        short_break_btn.configure(fg_color="transparent")
        long_break_btn.configure(fg_color="transparent")

        if current_mode == "Pomodoro":
            pomodoro_btn.configure(fg_color=PRIMARY)
        elif current_mode == "Short Break":
            short_break_btn.configure(fg_color=PRIMARY)
        elif current_mode == "Long Break":
            long_break_btn.configure(fg_color=PRIMARY)
    #Changes the color of the modes
    def update_mode_indicator():
        if current_mode == "Pomodoro":
            mode_label.configure(text="Pomodoro Time ⏲", text_color="#be38e3")
        elif current_mode == "Short Break":
            mode_label.configure(text="Short Break 💤", text_color="#d2afff")
        elif current_mode == "Long Break":
            mode_label.configure(text="Long Break 😴", text_color="#38bbe3")

    #UI Setuo
    timeApp = ctk.CTkToplevel(parent)
    timeApp.title("Timer")
    timeApp.geometry("450x280+905+30")
    timeApp.configure(fg_color=BACK_COLOR)
    timeApp.wm_overrideredirect(True)

    refresh_icon = ctk.CTkImage(Image.open("refresh.png"), size=(22, 22))
    settings_icon = ctk.CTkImage(Image.open("settings.png"), size=(23, 23))

    top_frame = ctk.CTkFrame(timeApp, fg_color=LABEL_COLOR)
    top_frame.pack(pady=10, fill="x", padx=10)

    loop_label = ctk.CTkLabel(top_frame, text="0/4", font=("Segoe UI", 18))
    loop_label.pack(side="left", padx=10)

    ctk.CTkButton(top_frame, text="", image=settings_icon, width=35, command=open_settings, fg_color=PRIMARY, hover_color=HOVER, border_color=BORDER).pack(side="right")

    mode_label = ctk.CTkLabel(timeApp, text="", font=("Segoe UI", 16))
    mode_label.pack()
    update_mode_indicator()

    timer_label = ctk.CTkLabel(timeApp, text=format_time(time_left), font=("Segoe UI", 48))
    timer_label.pack(pady=10)

    button_frame = ctk.CTkFrame(timeApp, fg_color="transparent")
    button_frame.pack(pady=10)

    start_btn = ctk.CTkButton(button_frame, text="  Start", command=start_timer, width=140, fg_color=PRIMARY, hover_color=HOVER, border_color=BORDER, border_width=1)
    start_btn.pack(side="left", padx=3)

    skip_btn = ctk.CTkButton(button_frame, text="", image=refresh_icon, command=skip_timer, width=40, fg_color=PRIMARY, hover_color=HOVER, border_color=BORDER, border_width=1)
    skip_btn.pack(side="left", padx=2)

    mode_frame = ctk.CTkFrame(timeApp, fg_color="transparent")
    mode_frame.pack(pady=10)

    pomodoro_btn = ctk.CTkButton(mode_frame, text="Pomodoro", command=lambda: switch_mode("Pomodoro"), width=90, fg_color="transparent", hover_color=HOVER, border_color=BORDER, border_width=1)
    pomodoro_btn.grid(row=0, column=0, padx=5)

    short_break_btn = ctk.CTkButton(mode_frame, text="Short Break", command=lambda: switch_mode("Short Break"), width=90, fg_color="transparent", hover_color=HOVER, border_color=BORDER, border_width=1)
    short_break_btn.grid(row=0, column=1, padx=5)

    long_break_btn = ctk.CTkButton(mode_frame, text="Long Break", command=lambda: switch_mode("Long Break"), width=90, fg_color="transparent", hover_color=HOVER, border_color=BORDER, border_width=1)
    long_break_btn.grid(row=0, column=2, padx=5)

    highlight_mode()
    timeApp.lift()
    timeApp.attributes('-topmost', True)
    timeApp.focus_force()