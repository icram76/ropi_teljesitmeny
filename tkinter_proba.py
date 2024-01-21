import tkinter as tk

class TextWidgetManager:

    def __init__(self, root):
        self.root = root
        self.data = []  # Tömb adatainak tárolására
        self.text_widgets = []

        # Text widget-ek létrehozása és adataik hozzáadása a "data" tömbhöz
        for i in range(5):
            text_widget = tk.Text(root, height=1, width=30)
            text_widget.pack(pady=1)
            self.data.append(f'Text Widget {i + 1}')
            text_widget.insert(tk.END, self.data[i])
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

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Text Widgets")

    text_manager = TextWidgetManager(root)
    
    # Adataink módosítása és frissítése
    text_manager.data = ["Elem 1", "Elem 2", "Elem 3" , "Elem 4", "Elem 5", "Elem 6", "Elem 7", "Elem 8", "Elem 9"]
    text_manager.update_widgets()

    root.mainloop()