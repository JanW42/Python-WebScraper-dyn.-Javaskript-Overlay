#Python Version 3.10.5
import customtkinter as ctk
from datetime import datetime, timedelta
import time
import threading
from tkinter import font  # Füge diese Zeile hinzu
import pygetwindow as gw
from PIL import Image, ImageTk, ImageDraw
import keyboard
from icecream import ic

from crawler import crawler
from crawler2 import crawler2
from Settings import Settings


class GUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        #-Title--------------------------------------------------------------------------------------------------------------------------------------------------------#
        title_label = ctk.CTkLabel(self, text="here_Heading", corner_radius=8, font=Settings.title_font, fg_color=Settings.fg_color, text_color= Settings.group_orange)
        title_label.pack(pady=10, anchor="e", padx=10)

        #-Marktwerte---------------------------------------------------------------------------------------------------------------------------------------------------#
        # Erstelle eine Instanz der crawler-Klasse
        self.crawler_instance = crawler("name")
        self.crawler2_instance = crawler2("name")

        self.price_vars = []
        self.labels = []

        for i in range(14):
            price_var = ctk.StringVar()
            label = ctk.CTkLabel(self, textvariable=price_var, corner_radius=8, font=Settings.price_font, fg_color=Settings.fg_color, anchor="e", text_color="White")
            label.pack(pady=1, anchor="e", padx=10)
            self.price_vars.append(price_var)
            self.labels.append(label)

        # -Gangcount-------------------------------------------------------------------------------------------------------------------------------------------------#
        self.gangcount_label1 = ctk.CTkLabel(self, text="", corner_radius=8, font=Settings.gang_font, fg_color=Settings.blue, text_color="White")
        self.gangcount_label1.pack(pady=10, anchor="e", padx=10)

        self.gangcount_label2 = ctk.CTkLabel(self, text="", corner_radius=8, font=Settings.gang_font, fg_color=Settings.blue, text_color="White")
        self.gangcount_label2.pack(pady=(1, 10), anchor="e", padx=10)
        
        for i in range(3, 11):
            label = ctk.CTkLabel(self, text="", corner_radius=8, font=Settings.gang_font, fg_color=Settings.fg_color, text_color="White")
            label.pack(pady=1, anchor="e", padx=10)
            setattr(self, f"gangcount_label{i}", label)
        # -Gangcount-------------------------------------------------------------------------------------------------------------------------------------------------#

        #-Button-----------------------------------------------------------------------------------------------------------------------------------------------------#
        quit_button = ctk.CTkButton(self, text ="Programm Beenden", corner_radius=8, fg_color=Settings.fg_color, command=self.destroy, hover_color=Settings.group_orange, text_color="White", font=Settings.button_font)
        quit_button.pack(pady=10, anchor="e", padx=10)

         # Starten der Timer für die Preisaktualisierung und Uhrzeit
        self.start_timers()

    def start_timers(self):
        threading.Thread(target=self.update_prices, daemon=True).start()

        threading.Thread(target=self.update_gang, daemon=True).start()

    
    def update_prices(self):
        # Rufe die main-Funktion der crawler-Instanz auf
        result, result1 = self.crawler_instance.main()

        for i in range(14):
            self.price_vars[i].set(result[i])
            self.labels[i].configure(text_color=result1[i])

        self.update_idletasks()  # Aktualisiere das Label sofort
        
        # Die update_prices-Methode wird erneut nach der neuen timer_duration aufgerufen
        current_time = datetime.now()
        minutes_to_next_step = Settings.faktortimebismarke - (current_time.minute % Settings.faktortimebismarke)
        next_step_time = current_time + timedelta(minutes=minutes_to_next_step)
        timer_duration_backend = (next_step_time - current_time).total_seconds()
        ic(timer_duration_backend)
        timer_duration_backend += Settings.warteaufwebsite
        timer_duration_backend += Settings.warteaufwebsite
        ic(timer_duration_backend)
        ic("jetzt am ende update prices")
        ic()
        self.after(int(timer_duration_backend * 1000), self.update_prices)

    def update_gang(self):
        while True:
            keyboard.wait("shift+G")
            ic("Shift+G wurde gedrückt")
            ic()
            combined_list = self.crawler2_instance.main()
            for i in range(9):
                getattr(self, f"gangcount_label{i+1}").configure(text=f"{combined_list[i]}")
            self.update()

if __name__ == "__main__":
    app = GUI()
    app.title("Marktpreise")
    bg = Settings.bg
    app.configure(fg_color=bg)
    # Starte das Fenster im Vordergrund und mit Transparenz
    app.wm_attributes("-topmost", 1)
    app.wm_attributes("-transparentcolor", app["bg"])
    app.overrideredirect(True)
    screen_width = app.winfo_screenwidth()
    screen_height = app.winfo_screenheight()
    window_width = 275
    window_height = 950
    x_position = screen_width - window_width
    y_position = 140
    app.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
    app.mainloop()
   