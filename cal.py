import customtkinter as ctk
from PIL import Image, ImageTk
ctk.set_appearance_mode("dark")

#ctk.set_default_color_theme("blue")

HOVER = "#5b2872"
PRIMARY = "#a064c9"
ENTRY= "#B382E7"
TEXT_COLOR = "#3c1e5d"
BORDER = "#9833f8"
BACK_COLOR="#b597d1"

calcApp=None
result_displayed=[False]

def calc(parent):
    global calcApp
    if calcApp and calcApp.winfo_exists():
        calcApp.destroy()
        calcApp=None
        return
    
    calcApp = ctk.CTkToplevel(parent)
    calcApp.wm_overrideredirect(True)
    calcApp.title("Calculator")
    calcApp.geometry("350x500+80+40")
    calcApp.configure(fg_color=BACK_COLOR)
    del_im=ctk.CTkImage(Image.open("del.png"),size=(22,22))

    # Display
    display = ctk.CTkEntry(
        calcApp, font=("Segeo UI", 30),justify="right", height=60,
        width=315, corner_radius=25, fg_color=ENTRY, text_color="white"
    )
    display.insert(0, "0")
    display.place(x=20, y=20)

    # Logic functions
    def append(char):
    # If a result was just displayed
        if result_displayed[0]:
            if char.isdigit() or char == ".":
                # New calculation: clear the field
                display.delete(0, ctk.END)
                result_displayed[0] = False
            else:
                # Continue calculation: keep result
                result_displayed[0] = False  # Still reset flag to allow further inputs
        elif display.get() in ("0", "Error"):
            display.delete(0, ctk.END)

        display.insert(ctk.END, char)


    def clear():
        display.delete(0, ctk.END)
        display.insert(0, "0")
        result_displayed[0]=False

    def delete():
        content = display.get()
        if len(content) > 1:
            display.delete(len(content) - 1, ctk.END)
        else:
            display.delete(0, ctk.END)
            display.insert(0, "0")

    def calculate():
        try:
            result = str(eval(display.get()))
            display.delete(0, ctk.END)
            display.insert(0, result)
            result_displayed[0]=True
        except:
            display.delete(0, ctk.END)
            display.insert(0, "Error")
    
    def key_handler(event):
        char = event.char
        if char in "0123456789.+-*/%":
            append(char)
        elif event.keysym == "Return":
            calculate()
        elif event.keysym == "BackSpace":
            delete()
        elif event.keysym == "Escape":
            clear()

    calcApp.bind("<Key>", key_handler)


    # Button sizee and spacing
    sizee = 50
    pad = 32
    x0, y0 = 20, 100

    # Row 1
    ctk.CTkButton(calcApp, text="Clr", command=clear, width=30, height=50,corner_radius=25, fg_color=PRIMARY,hover_color=HOVER,border_width=2,border_color=BORDER, text_color=TEXT_COLOR, font=("Segoe UI", 16, "bold")
    ).place(x=x0 + 0*(sizee+pad), y=y0)

    ctk.CTkButton(calcApp, text="", image=del_im, command=delete, width=48, height=48,corner_radius=24, fg_color=PRIMARY,hover_color=HOVER,border_color=BORDER, border_width=2,text_color=TEXT_COLOR, font=("Segoe UI", 16, "bold")
    ).place(x=x0 + 1*(sizee+pad), y=y0)

    ctk.CTkButton(calcApp, text="%", command=lambda: append("%"), width=sizee, height=sizee,corner_radius=30, fg_color=PRIMARY,hover_color=HOVER, border_width=2, border_color=BORDER, text_color=TEXT_COLOR, font=("Segoe UI", 18, "bold")
    ).place(x=x0 + 2*(sizee+pad), y=y0)

    ctk.CTkButton(calcApp, text="/", command=lambda: append("/"), width=sizee, height=sizee,corner_radius=30, fg_color=PRIMARY,hover_color=HOVER, border_width=2, border_color=BORDER, text_color=TEXT_COLOR,font=("Segoe UI", 18, "bold")
    ).place(x=x0 + 3*(sizee+pad), y=y0)

    # Row 2
    ctk.CTkButton(calcApp, text="7", command=lambda: append("7"), width=sizee, height=sizee,corner_radius=30, fg_color=PRIMARY,hover_color=HOVER, border_width=2, border_color=BORDER, text_color=TEXT_COLOR,font=("Segoe UI", 18, "bold")
    ).place(x=x0 + 0*(sizee+pad), y=y0 + 1*(sizee+pad))

    ctk.CTkButton(calcApp, text="8", command=lambda: append("8"), width=sizee, height=sizee,corner_radius=30, fg_color=PRIMARY,hover_color=HOVER, border_width=2, border_color=BORDER, text_color=TEXT_COLOR,font=("Segoe UI", 18, "bold")
    ).place(x=x0 + 1*(sizee+pad), y=y0 + 1*(sizee+pad))

    ctk.CTkButton(calcApp, text="9", command=lambda: append("9"), width=sizee, height=sizee,corner_radius=30, fg_color=PRIMARY,hover_color=HOVER, border_width=2, border_color=BORDER, text_color=TEXT_COLOR,font=("Segoe UI", 18, "bold")
    ).place(x=x0 + 2*(sizee+pad), y=y0 + 1*(sizee+pad))

    ctk.CTkButton(calcApp, text="*", command=lambda: append("*"), width=sizee, height=sizee,corner_radius=30, fg_color=PRIMARY,hover_color=HOVER, border_width=2, border_color=BORDER, text_color=TEXT_COLOR,font=("Segoe UI", 18, "bold")
    ).place(x=x0 + 3*(sizee+pad), y=y0 + 1*(sizee+pad))

    # Row 3
    ctk.CTkButton(calcApp, text="4", command=lambda: append("4"), width=sizee, height=sizee,corner_radius=30, fg_color=PRIMARY,hover_color=HOVER, border_width=2, border_color=BORDER, text_color=TEXT_COLOR,font=("Segoe UI", 18, "bold")
    ).place(x=x0 + 0*(sizee+pad), y=y0 + 2*(sizee+pad))

    ctk.CTkButton(calcApp, text="5", command=lambda: append("5"), width=sizee, height=sizee,corner_radius=30, fg_color=PRIMARY,hover_color=HOVER, border_width=2, border_color=BORDER, text_color=TEXT_COLOR,font=("Segoe UI", 18, "bold")
    ).place(x=x0 + 1*(sizee+pad), y=y0 + 2*(sizee+pad))

    ctk.CTkButton(calcApp, text="6", command=lambda: append("6"), width=sizee, height=sizee, corner_radius=30, fg_color=PRIMARY,hover_color=HOVER, border_width=2, border_color=BORDER, text_color=TEXT_COLOR,font=("Segoe UI", 18, "bold")
    ).place(x=x0 + 2*(sizee+pad), y=y0 + 2*(sizee+pad))

    ctk.CTkButton(calcApp, text="-", command=lambda: append("-"), width=sizee, height=sizee, corner_radius=30, fg_color=PRIMARY,hover_color=HOVER, border_width=2, border_color=BORDER, text_color=TEXT_COLOR,font=("Segoe UI", 18, "bold")
    ).place(x=x0 + 3*(sizee+pad), y=y0 + 2*(sizee+pad))

    # Row 4
    ctk.CTkButton(calcApp, text="1", command=lambda: append("1"), width=sizee, height=sizee, corner_radius=30, fg_color=PRIMARY,hover_color=HOVER, border_width=2, border_color=BORDER, text_color=TEXT_COLOR,font=("Segoe UI", 18, "bold")
    ).place(x=x0 + 0*(sizee+pad), y=y0 + 3*(sizee+pad))

    ctk.CTkButton(calcApp, text="2", command=lambda: append("2"), width=sizee, height=sizee, corner_radius=30, fg_color=PRIMARY,hover_color=HOVER, border_width=2, border_color=BORDER, text_color=TEXT_COLOR,font=("Segoe UI", 18, "bold")
    ).place(x=x0 + 1*(sizee+pad), y=y0 + 3*(sizee+pad))

    ctk.CTkButton(calcApp, text="3", command=lambda: append("3"), width=sizee, height=sizee, corner_radius=30, fg_color=PRIMARY,hover_color=HOVER, border_width=2, border_color=BORDER, text_color=TEXT_COLOR,font=("Segoe UI", 18, "bold")
    ).place(x=x0 + 2*(sizee+pad), y=y0 + 3*(sizee+pad))

    ctk.CTkButton(calcApp, text="+", command=lambda: append("+"), width=sizee, height=sizee, corner_radius=30, fg_color=PRIMARY,hover_color=HOVER, border_width=2, border_color=BORDER, text_color=TEXT_COLOR,font=("Segoe UI", 18, "bold")
    ).place(x=x0 + 3*(sizee+pad), y=y0 + 3*(sizee+pad))

    # Row 5
    ctk.CTkButton(calcApp, text="0", command=lambda: append("0"), width=sizee, height=sizee, corner_radius=30, fg_color=PRIMARY,hover_color=HOVER, border_width=2, border_color=BORDER, text_color=TEXT_COLOR,font=("Segoe UI", 18, "bold")
    ).place(x=x0 + 0*(sizee+pad), y=y0 + 4*(sizee+pad))

    ctk.CTkButton(calcApp, text=".", command=lambda: append("."), width=sizee, height=sizee, corner_radius=30, fg_color=PRIMARY,hover_color=HOVER, border_width=2, border_color=BORDER, text_color=TEXT_COLOR,font=("Segoe UI", 18, "bold")
    ).place(x=x0 + 1*(sizee+pad), y=y0 + 4*(sizee+pad))

    ctk.CTkButton(calcApp, text="=", command=calculate, width=130, height=sizee, corner_radius=30, fg_color=PRIMARY,hover_color=HOVER,border_color=BORDER,border_width=2, text_color="white",font=("Segoe UI", 18, "bold")
    ).place(x=x0 + 2*(sizee+pad), y=y0 + 4*(sizee+pad))

    calcApp.lift()
    calcApp.attributes('-topmost', True)
    calcApp.focus_force()
#     calcApp.mainloop()
# calc(None)

