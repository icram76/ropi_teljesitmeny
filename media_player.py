import tkinter as tk
import vlc
from tkinter import filedialog
from datetime import timedelta
from pynput import keyboard
import ropi_esemeny_feldolgozo as r
import tomb_mentes_olvasas as tmo
import os

def on_press(key):
    global app
       
    if key.keysym == 'Left':
        app.rewind()
    
    if key.keysym == 'Right':
        app.fast_forward()
    
    if key.keysym == 'space':
        app.pause_video()
        
    if key.keysym == 'F1':
        print ("esemenyek")
        print(r.esemenyek)
    
    if key.keysym == 'F2':
        print ("labda_menet")
        print(r.labda_menet)
    
    if key.keysym == 'F3':
        print(r.labdamenetek)

    if key.keysym == 'F5':
        r.labda_menet = []

    r.key_press_handler(key,app.media_player.get_time())

    if len(r.esemeny) == 0 and len(r.esemenyek) > 0:
        app.esemenyek_text.delete('0', tk.END)
        app.esemenyek_text.insert('0', " ".join(r.esemenyek[-1]) )
        app.text_menetek.data = r.esemenyek
        app.text_menetek.update_widgets()   
               
    #eredmény frissítése
    if  len(r.labdamenetek) >0: 
        app.eredmeny_text.delete('0', tk.END)
        app.eredmeny_text.insert('0', r.labdamenetek[-1].get('pont'))

def on_release(key):
    if key == keyboard.Key.esc:
        print("Kilépés")
        return False


class TextWidgetManager:

    def __init__(self, root):
        self.root = root
        self.data = []  # Tömb adatainak tárolására
        self.text_widgets = []

        # Text widget-ek létrehozása és adataik hozzáadása a "data" tömbhöz
        for i in range(5):
            text_widget = tk.Text(root, height=1, width=30)
            text_widget.pack(pady=1)
            #self.data.append(f'Text Widget {i + 1}')
            #text_widget.insert(tk.END, self.data[i])
            text_widget.config(state=tk.DISABLED)
            self.text_widgets.append(text_widget)

    def update_widgets(self):
        # Az utolsó 5 elem beállítása az utolsó 5 Text widget-re
        for i in range(5):
            text_widget_index = len(self.data) - i - 1 #fent van az utolsó
            text_widget_index = len(self.data) - (abs(i - 5)) # lent van az utolsó
            text_widget = self.text_widgets[i]
            text_widget.config(state=tk.NORMAL)
            text_widget.delete(1.0, tk.END)
            if text_widget_index >= 0:
                text_widget.insert(tk.END, self.data[text_widget_index])
                text_widget.config(state=tk.DISABLED)
    
    def delete(self):
        for i in range(5):
            self.text_widgets[i].delete(1.0, tk.END)

class MediaPlayerApp(tk.Tk):

    file_path = ""

    def __init__(self):
        super().__init__()

        self.title("Media Player")
        self.geometry("800x700")
        self.configure(bg="#f0f0f0")
        self.initialize_player()

        self.bind('<KeyPress>',on_press)
        self.bind('<KeyRelease>',on_release)

    def initialize_player(self):
        self.instance = vlc.Instance()
        self.media_player = self.instance.media_player_new()
        self.current_file = None
        self.playing_video = False
        self.video_paused = False
        self.create_widgets()
    
    def create_widgets(self):
        self.media_canvas = tk.Canvas(self, bg="black", width=800, height=400)
        self.media_canvas.pack(pady=10, fill=tk.BOTH, expand=True)
        self.select_file_button = tk.Button(
            self,
            text="Select File",
            font=("Arial", 12, "bold"),
            command=self.select_file,
        )
        self.select_file_button.pack(pady=1)
        self.time_label = tk.Label(
            self,
            text="00:00:00 / 00:00:00",
            font=("Arial", 12, "bold"),
            fg="#555555",
            bg="#f0f0f0",
        )
        self.time_label.pack(pady=5)
        self.control_buttons_frame = tk.Frame(self, bg="#f0f0f0")
        self.control_buttons_frame.pack(pady=5)
    
        self.play_button = tk.Button(
            self.control_buttons_frame,
            text="Play",
            font=("Arial", 12, "bold"),
            bg="#4CAF50",
            fg="white",
            command=self.play_video,
        )
        self.play_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.pause_button = tk.Button(
            self.control_buttons_frame,
            text="Pause",
            font=("Arial", 12, "bold"),
            bg="#FF9800",
            fg="white",
            command=self.pause_video,
        )
        self.pause_button.pack(side=tk.LEFT, padx=10, pady=5)
        self.stop_button = tk.Button(
            self.control_buttons_frame,
            text="Stop",
            font=("Arial", 12, "bold"),
            bg="#F44336",
            fg="white",
            command=self.stop,
        )
        self.stop_button.pack(side=tk.LEFT, pady=5)
        self.fast_forward_button = tk.Button(
            self.control_buttons_frame,
            text="Fast Forward",
            font=("Arial", 12, "bold"),
            bg="#2196F3",
            fg="white",
            command=self.fast_forward,
        )
        self.fast_forward_button.pack(side=tk.LEFT, padx=10, pady=5)
        self.rewind_button = tk.Button(
            self.control_buttons_frame,
            text="Rewind",
            font=("Arial", 12, "bold"),
            bg="#2196F3",
            fg="white",
            command=self.rewind,
        )
        self.rewind_button.pack(side=tk.LEFT, pady=5)
        self.jump_last_button = tk.Button(
            self.control_buttons_frame,
            text="Jump",
            font=("Arial", 12, "bold"),
            bg="#2196F3",
            fg="white",
            command=self.jump,
        )
        self.jump_last_button.pack(side=tk.LEFT, pady=5)
        self.progress_bar = VideoProgressBar(
            self, self.set_video_position, bg="#e0e0e0", highlightthickness=0 
        )
        self.progress_bar.pack(fill=tk.X, padx=10, pady=2)
        
        self.info_text_frame = tk.Frame(self, bg="#f0f0f0")
        
        self.info_text_frame.pack(side=tk.LEFT)
        
        self.esemenyek_text = tk.Entry(
                                      self.info_text_frame,  
                                      width= 20,
                                      state=tk.DISABLED)
        self.esemenyek_text.pack(side=tk.LEFT, padx= 5)
        self.scroll = tk.Scrollbar()        
        
        self.eredmeny_label = tk.Label(self.info_text_frame, text="Eredmény:")
        self.eredmeny_label.pack(side=tk.LEFT, padx=3)
        self.eredmeny_text = tk.Entry(self.info_text_frame,
                                      width=5)
        self.eredmeny_text.pack(side=tk.LEFT)

        self.text_menetek = TextWidgetManager(self.info_text_frame)     
    
    def select_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Media Files", "*.mp4 *.avi")]
        )
        if file_path:
            self.current_file = file_path
            self.time_label.config(text="00:00:00 / " + self.get_duration_str())
            self.play_video()
    
    def get_duration_str(self):
        if self.playing_video:
            total_duration = self.media_player.get_length()
            total_duration_str = str(timedelta(milliseconds=total_duration))[:-3]
            return total_duration_str
        return "00:00:00"

    def play_video(self):
        if not self.playing_video:
            media = self.instance.media_new(self.current_file)
            self.media_player.set_media(media)
            self.media_player.set_hwnd(self.media_canvas.winfo_id())
            self.media_player.play()
            self.playing_video = True
    
    def fast_forward(self):
        if self.playing_video:
            current_time = self.media_player.get_time() + 10000
            self.media_player.set_time(current_time)

    def rewind(self):
        if self.playing_video:
            current_time = self.media_player.get_time() - 10000
            self.media_player.set_time(current_time)
    
    def jump(self):
        if self.playing_video:
            if r.labdamenetek:
                if r.labdamenetek[-1]["ido"] != -1:
                    self.media_player.set_time(r.labdamenetek[-1]["ido"])

    def pause_video(self):
        if self.playing_video:
            if self.video_paused:
                self.media_player.play()
                self.video_paused = False
                self.pause_button.config(text="Pause")
            else:
                self.media_player.pause()
                self.video_paused = True
                self.pause_button.config(text="Resume")
    
    def stop(self):
        if self.playing_video:
            self.media_player.stop()
            self.playing_video = False
        self.time_label.config(text="00:00:00 / " + self.get_duration_str())
        print('Stop video')

    def set_video_position(self, value):
        if self.playing_video:
            total_duration = self.media_player.get_length()
            position = int((float(value) / 100) * total_duration)
            self.media_player.set_time(position)
    
    def update_video_progress(self):
        if self.playing_video:
            total_duration = self.media_player.get_length()
            current_time = self.media_player.get_time()
            progress_percentage = (current_time / total_duration) * 100
            self.progress_bar.set(progress_percentage)
            current_time_str = str(timedelta(milliseconds=current_time))[:-3]
            total_duration_str = str(timedelta(milliseconds=total_duration))[:-3]
            self.time_label.config(text=f"{current_time_str}/{total_duration_str}")
        self.after(1000, self.update_video_progress)

class VideoProgressBar(tk.Scale):
    def __init__(self, master, command, **kwargs):
        kwargs["showvalue"] = False
        super().__init__(
            master,
            from_=0,
            to=100,
            orient=tk.HORIZONTAL,
            length=800,
            command=command,
            **kwargs,
        )
        self.bind("<Button-1>", self.on_click)

    def on_click(self, event):
        if self.cget("state") == tk.NORMAL:
            value = (event.x / self.winfo_width()) * 100
            self.set(value)
    
if __name__ == "__main__":

    filename = "labda_menet.json"

    if os.path.isfile(filename):
        r.labdamenetek = tmo.file_to_json(filename)
        print("labda_menet feltöltve")
        print(r.labdamenetek)
        if r.labdamenetek:
            r.a_pont = int(r.labdamenetek[-1]['pont'].split(sep=':')[0])
            r.b_pont = int(r.labdamenetek[-1]['pont'].split(sep=':')[1])
            print(f"Beolvasott eredmény: {r.a_pont}:{r.b_pont}")
    app = MediaPlayerApp()
    app.update_video_progress()
    app.mainloop()
    print(r.labda_menet)
    #tmo.tomb_to_file(r.labda_menet, filename)
    #tmo.tomb_mentese_allomanyba(r.labda_menet,filename)
    tmo.json_to_file(r.labdamenetek, filename)
    r.kiertekel()
    
    
    