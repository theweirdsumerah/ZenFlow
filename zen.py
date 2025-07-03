import customtkinter as ctk
import tkinter as tk                    
from tkinter import ttk                 
from tkinter import messagebox            
import sqlite3 as sql 
from PIL import Image, ImageTk, ImageSequence
from Timer import open_timer
from List import list
from heatmap import hmap
from cal import calc

ctk.set_appearance_mode("dark")

BG_COLOR = "#2a1045"
BUTTON_COLOR = "#5b2872"
BUTTON_HOVER = "#a064c9"
BORDER = "#a855f7"

root = ctk.CTk()
root.title("Zenflow")
root.geometry("1920x1080+0+0")
bck_im=ctk.CTkImage(Image.open("wrld.png"), size=(23,23))
clock=ctk.CTkImage(Image.open("clock.png"),size=(20,20))
map_im=ctk.CTkImage(Image.open("heatmap.png"),size=(20,20))
list_im=ctk.CTkImage(Image.open("list.png"),size=(22,22))
calc_im=ctk.CTkImage(Image.open("calculator.png"),size=(20,20))

canvas = tk.Canvas(root, highlightthickness=0)
canvas.place(x=0, y=0, relwidth=1, relheight=1)
canvas_image_id = None

gif_paths = {
    "Radio": "Radio.gif",
    "Keyboard": "keyboard.gif",
    "Study": "study.gif"
}

frames = []
resized_frames = []
frame_count = 0
current_frame = 0

def load_gif(path):
    global frames, resized_frames, frame_count, current_frame
    gif = Image.open(path)
    frames = [frame.copy().convert("RGBA") for frame in ImageSequence.Iterator(gif)]
    frame_count = len(frames)
    current_frame = 0
    resized_frames = resize_frames(root.winfo_width(), root.winfo_height())

def resize_frames(width, height):
    return [ImageTk.PhotoImage(frame.resize((width, height), Image.LANCZOS)) for frame in frames]

def animate_gif():
    global current_frame, canvas_image_id
    if not resized_frames or not root.winfo_exists():
        return
    canvas.delete("all")
    canvas_image_id = canvas.create_image(0, 0, anchor="nw", image=resized_frames[current_frame])
    current_frame = (current_frame + 1) % frame_count
    root.after(100, animate_gif)

def on_resize(event):
    global resized_frames
    if frames:
        resized_frames = resize_frames(event.width, event.height)

root.bind("<Configure>", on_resize)

gif_win=None

#gif menu
def gif():
    global gif_win
    if gif_win and gif_win.winfo_exists():
        gif_win.destroy()
        gif_win=None
        return

    gif_win = ctk.CTkToplevel(root)
    gif_win.wm_overrideredirect(True)
    gif_win.configure(fg_color=BG_COLOR)

    x = bck_btn.winfo_rootx()
    y = bck_btn.winfo_rooty() + bck_btn.winfo_height()
    gif_win.geometry(f"+{x}+{y}")

    for name, path in gif_paths.items():
            gif_btn = ctk.CTkButton(gif_win, text=name, command=lambda p=path, w=gif_win: [load_gif(p), w.destroy()], fg_color=BUTTON_COLOR, hover_color=BUTTON_HOVER)
            gif_btn.pack(pady=5, padx=10, fill="x")
 

button_frame=ctk.CTkFrame(root, fg_color=BUTTON_COLOR,height=300, width=54)
button_frame.place(x=10, y=15)

bck_btn = ctk.CTkButton(button_frame, image=bck_im, text=" Spaces ",font=("Segoe UI",10,"bold"),width=45,height=40, command=gif,fg_color=BUTTON_COLOR,hover_color=BUTTON_HOVER, compound="top" )
bck_btn.place(x=2,y=2)

timer_btn=ctk.CTkButton(button_frame, image=clock, text=" Timer ",font=("Segoe UI",11,"bold"),width=45,height=40, command=lambda:open_timer(root),fg_color=BUTTON_COLOR, hover_color=BUTTON_HOVER,compound="top")
timer_btn.place(x=1,y=55)

map_btn=ctk.CTkButton(button_frame, image=map_im, text=" Habit \nLog",font=("Segoe UI",11,"bold"),width=45,height=40, command=lambda:hmap(root),fg_color=BUTTON_COLOR, hover_color=BUTTON_HOVER,compound="top")
map_btn.place(x=2,y=110)

list_btn=ctk.CTkButton(button_frame, image=list_im, text=" Task \nList",font=("Segoe UI",11,"bold"),width=45,height=40, command=lambda:list(),fg_color=BUTTON_COLOR, hover_color=BUTTON_HOVER,compound="top")
list_btn.place(x=4,y=178)

calc_btn=ctk.CTkButton(button_frame, image=calc_im, text="Calculator",font=("Segoe UI",10,"bold"),width=45,height=40, command=lambda:calc(root),fg_color=BUTTON_COLOR, hover_color=BUTTON_HOVER,compound="top")
calc_btn.place(x=-4,y=245)
# --- Start ---
load_gif(gif_paths["Radio"])
animate_gif()

root.mainloop()
