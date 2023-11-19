import tkinter as tk
from tkinter import ttk
from sqlalchemy.orm import sessionmaker
from models import engine

Session = sessionmaker(bind=engine)
session = Session()


class Reader(tk.Frame):
    FONT_TYPES = ["Times New Roman", "Arial", "Verdana"]

    def __init__(self, master=None, book_path=None, book_id=None):
        super().__init__(master)
        self.master = master
        self.book_path = book_path
        self.book_id = book_id
        self.current_theme = "light"
        self.current_font = "Times New Roman"
        self.init_ui()

    def init_ui(self):
        self.master.title("Skaityklė")
        self.master.geometry("600x500+200+50")
        self.master.config(bg="white")
        self.master.resizable(False, False)

        self.text_frame = tk.Frame(self.master, bg="white")
        self.text_frame.pack(fill=tk.BOTH, expand=True)

        self.scrollbar = tk.Scrollbar(self.text_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.text_box = tk.Text(self.text_frame, yscrollcommand=self.scrollbar.set, bg="white", fg="black",
                                font=(self.current_font, 12))
        self.text_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        with open(self.book_path, "r", encoding='utf-8') as f:
            contents = f.read()
            self.text_box.insert(tk.END, contents)

        self.scrollbar.config(command=self.text_box.yview)

        self.button_frame = tk.Frame(self.master, bg="white")
        self.button_frame.pack(fill=tk.X)

        self.theme_button = tk.Button(self.button_frame, width=12, pady=7,
                                      bg="pink", fg="white", border=1,
                                      text="Keisti Temą",
                                      command=self.switch_theme)
        self.theme_button.pack(side=tk.LEFT)

        self.search_label = tk.Label(self.button_frame, text="Search:", bg="white")
        self.search_label.pack(side=tk.LEFT)

        self.search_entry = tk.Entry(self.button_frame, bg="white")
        self.search_entry.pack(side=tk.LEFT)

        self.search_button = tk.Button(self.button_frame, text="Search", command=self.search_text)
        self.search_button.pack(side=tk.LEFT)

        self.font_label = tk.Label(self.button_frame, text="Font:", bg="white")
        self.font_label.pack(side=tk.LEFT)

        self.font_combobox = ttk.Combobox(self.button_frame, values=self.FONT_TYPES, state="readonly")
        self.font_combobox.pack(side=tk.LEFT)
        self.font_combobox.current(0)
        self.font_combobox.bind("<<ComboboxSelected>>", self.change_font)

    def change_font(self, event):
        self.current_font = self.font_combobox.get()
        self.text_box.config(font=(self.current_font, 12))

    def switch_theme(self):
        if self.current_theme == "light":
            self.current_theme = "dark"
        else:
            self.current_theme = "light"
        self.set_theme()

    def set_theme(self):
        if self.current_theme == "light":
            self.bg_color = "white"
            self.fg_color = "black"
        else:
            self.bg_color = "black"
            self.fg_color = "white"

        self.text_frame.config(bg=self.bg_color)
        self.text_box.config(bg=self.bg_color, fg=self.fg_color)
        self.button_frame.config(bg=self.bg_color)

    def search_text(self):
        query = self.search_entry.get().strip()
        if query:
            self.text_box.tag_remove("paieška", "1.0", tk.END)
            start = "1.0"
            while True:
                start = self.text_box.search(query, start, tk.END)
                if not start:
                    break
                end = f"{start}+{len(query)}c"
                self.text_box.tag_add("paieška", start, end)
                start = end
            self.text_box.tag_config("paieška", background="yellow")


if __name__ == '__main__':
    root = tk.Tk()
    app = Reader(root)
    root.mainloop()
