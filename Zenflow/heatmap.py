import customtkinter as ctk
import sqlite3
from datetime import datetime, timedelta

# CustomTkinter setup
ctk.set_appearance_mode("dark")

# Constants
CELL_SIZE = 20
BG_COLOR = "#522682"
HEAT_COLOR = "#a855f7"
FUTURE_COLOR = "#765f8b"
BORDER_COLOR="#cd7aeb"
PRIMARY = "#5b2872"
GRID_HOVER="#8c46ba"
HOVER = "#a064c9"
BACK_COLOR = "#2A1045"

heatmap=None
show_first_half = True

def hmap(parent):
    global heatmap
    if heatmap and heatmap.winfo_exists():
        heatmap.destroy()
        heatmap=None
        return
    

    # SQLite setup
    conn = sqlite3.connect("calendar.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS contributions (
        date TEXT PRIMARY KEY,
        level INTEGER
    )
    """)
    conn.commit()

    # Globals
    cells = {}
    
    start_date = datetime(datetime.now().year, 1, 1)
    today = datetime.now()
    today_str = today.strftime("%Y-%m-%d")

    # Main heatmap
    #heatmap = ctk.CTk()
    heatmap = ctk.CTkToplevel(parent)
    heatmap.wm_overrideredirect(True)
    heatmap.title("Half-Year Contribution Calendar")
    heatmap.geometry("920x300+9+420")
    heatmap.configure(fg_color=BACK_COLOR)

    # Frame
    grid_frame = ctk.CTkFrame(heatmap, fg_color=BACK_COLOR)
    grid_frame.grid(row=0, column=0, sticky="nsew")


    def get_level(date_str):
        cursor.execute("SELECT 1 FROM contributions WHERE date = ?", (date_str,))
        return cursor.fetchone() is not None


    def toggle_contribution(date_str):
        if get_level(date_str):
            cursor.execute("DELETE FROM contributions WHERE date = ?", (date_str,))
            cells[date_str].configure(fg_color=BG_COLOR)
        else:
            cursor.execute("INSERT INTO contributions (date, level) VALUES (?, 1)", (date_str,))
            cells[date_str].configure(fg_color=HEAT_COLOR)
        conn.commit()


    def build_grid():
        for widget in grid_frame.winfo_children():
            widget.destroy()
        cells.clear()

        weekdays = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
        for i, day in enumerate(weekdays):
            lbl = ctk.CTkLabel(grid_frame, text=day, width=30)
            lbl.grid(row=i + 1, column=0, padx=2, pady=2, sticky="e")

        date = start_date
        col = 1
        month_positions = {}

        while date.year == start_date.year:
            if show_first_half and date.month > 6:
                break
            if not show_first_half and date.month <= 6:
                date += timedelta(days=1)
                continue

            weekday = date.weekday()
            row = (weekday + 1) % 7
            date_str = date.strftime("%Y-%m-%d")
            contributed = get_level(date_str)
            is_future = date > today

            cell = ctk.CTkButton(
                grid_frame,
                width=CELL_SIZE + 10,
                height=CELL_SIZE + 5,
                fg_color=FUTURE_COLOR if is_future else (HEAT_COLOR if contributed else BG_COLOR),
                hover_color=GRID_HOVER,
                text=str(date.day),
                font=ctk.CTkFont(size=10),
                text_color="gray" if is_future else "white",
                state="disabled" if is_future else "normal",
                command=(lambda d=date_str: toggle_contribution(d)) if not is_future else None
            )

            if date_str == today_str:
                cell.configure(border_width=2, border_color=BORDER_COLOR)

            cell.grid(row=row + 1, column=col, padx=1, pady=1)
            cells[date_str] = cell

            if date.day <= 7 and date.strftime("%b") not in month_positions:
                month_positions[date.strftime("%b")] = col

            date += timedelta(days=1)
            if date.weekday() == 6:
                col += 1

        for name, col_pos in month_positions.items():
            label = ctk.CTkLabel(grid_frame, text=name)
            label.grid(row=0, column=col_pos, padx=2, pady=2)


    def toggle_half():
        global show_first_half
        show_first_half = not show_first_half
        build_grid()


    def log_today():
        if not get_level(today_str):
            cursor.execute("INSERT INTO contributions (date, level) VALUES (?, 1)", (today_str,))
            conn.commit()
        build_grid()


    # Toggle Button
    toggle_btn = ctk.CTkButton(heatmap, text="Show Jul–Dec", command=None, fg_color=PRIMARY, hover_color=HOVER)
    toggle_btn.grid(row=8, column=0, padx=(0, 200), pady=(10, 0))

    # Log Today Button
    log_today_btn = ctk.CTkButton(heatmap, text="Log Today", command=log_today, fg_color=PRIMARY, hover_color=HOVER)
    log_today_btn.grid(row=8, column=0, padx=(200, 0), pady=(10, 0))


    def update_button():
        toggle_half()
        if show_first_half:
            toggle_btn.configure(text="Show Jul–Dec")
        else:
            toggle_btn.configure(text="Show Jan–Jun")


    toggle_btn.configure(command=update_button)

    # Initial draw
    build_grid()

    #top
    heatmap.lift()
    heatmap.attributes('-topmost', True)

    # Run
    #heatmap.mainloop()

