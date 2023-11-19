import tkinter as tk
from tkinter import messagebox, filedialog
from sqlalchemy.orm import sessionmaker
from models import engine, User, Book
import sys
from PIL import ImageTk, Image
import os
from sqlalchemy.exc import SQLAlchemyError
from reader import Reader

Session = sessionmaker(bind=engine)
session = Session()


class Profile(tk.Frame):
    def __init__(self, master=None, user=None):
        super().__init__(master)
        self.master = master
        self.master.title("Profilis - {}".format(user.username))
        self.master.geometry("450x500+300+70")
        self.master.config(bg="white")
        self.master.resizable(False, False)
        self.user = user

        if not user:
            messagebox.showerror("Error", "No user provided")
            self.master.destroy()
            return

        self.name = user.name
        self.surname = user.surname
        self.grade = user.grade
        self.email = user.email
        self.total_points = user.total_points
        self.profile_picture = user.profile_picture

        self.profile_picture = "profile_folder"
        if self.user.profile_picture is not None:
            img_path = self.user.profile_picture
        else:
            img_path = "default_profile.png"

        img = Image.open(img_path).resize((150, 150))
        self.img = ImageTk.PhotoImage(img)
        self.img_label = tk.Label(self.master, image=self.img, border=0, bg="white")
        self.img_label.image = self.img
        self.img_label.place(x=30, y=30)

        change_profile_picture_button = tk.Button(self.master, width=20, text="Pakeisti paveiksliuka", border=0,
                                                  bg="white", cursor="hand2",
                                                  fg="#57a1f8", command=self.change_picture)
        change_profile_picture_button.place(x=40, y=220)

        frame = tk.Frame(self.master, width=170, height=200, bg="white")
        frame.place(x=250, y=30)

        heading = tk.Label(frame, text="Apie Jus:", fg="#57a1f8", bg="white",
                           font=('Microsoft Yahei UI Light', 14, 'bold'))
        heading.place(x=15, y=5)

        name_label = tk.Label(frame, text=f"Vardas: {self.name}", fg="black", bg="white", font=("Arial", 12))
        name_label.place(x=15, y=40)

        surname_label = tk.Label(frame, text=f"Pavardė: {self.surname}", fg="black", bg="white", font=('Arial', 12))
        surname_label.place(x=15, y=70)

        grade_label = tk.Label(frame, text=f"Klasė: {self.grade}", fg="black", bg="white", font=('Arial', 12))
        grade_label.place(x=15, y=100)

        total_points_label = tk.Label(frame, text=f"Taškai: {self.total_points}", fg="black", bg="white",
                                      font=('Arial', 12))
        total_points_label.place(x=15, y=130)

        separator = tk.Frame(self.master, height=2, bg="#d9d9d9")
        separator.place(x=0, y=250, width=450)

        book_cover_1 = Image.open(
            "C:\\Users\\malgo\\PycharmProjects\\Baigiamasis\\knygos\\virselis\\mazasis_princas.png")
        book_cover_1 = book_cover_1.resize((70, 100), Image.ANTIALIAS)
        self.cover_image = ImageTk.PhotoImage(book_cover_1)

        self.read_button_1 = tk.Button(self.master, image=self.cover_image, cursor="hand2",
                                       command=lambda: self.read_book(book_id=1))
        self.read_button_1.place(x=20, y=270)

        book_cover_2 = Image.open("C:\\Users\\malgo\\PycharmProjects\\Baigiamasis\\knygos\\virselis\\book_cover2.png")
        book_cover_2 = book_cover_2.resize((70, 100), Image.ANTIALIAS)
        self.cover_image_2 = ImageTk.PhotoImage(book_cover_2)

        self.read_button_2 = tk.Button(self.master, image=self.cover_image_2, cursor="hand2",
                                       command=lambda: self.read_book(book_id=2))
        self.read_button_2.place(x=110, y=270)

        menu_bar = tk.Menu(self.master)
        self.master.config(menu=menu_bar)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Atsijungti", command=self.log_off)
        menu_bar.add_cascade(label="Menu", menu=file_menu)

        edit_menu = tk.Menu(menu_bar, tearoff=0)
        edit_menu.add_command(label="Keisti vardą", command=self.edit_name)
        edit_menu.add_command(label="Keisti pavardę", command=self.edit_surname)
        edit_menu.add_command(label="Keisti klasę", command=self.edit_grade)
        edit_menu.add_command(label="Keisti el. paštą", command=self.edit_email)
        menu_bar.add_cascade(label="Redaguoti", menu=edit_menu)

        about_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Failas", menu=about_menu)
        about_menu.add_command(label="Apie", command=self.show_readme)

        self.pack()

    def change_picture(self):
        filename = filedialog.askopenfilename(initialdir="/", title="Select Image",
                                              filetypes=(("Image Files", "*.png"), ("All Files", "*.*")))
        if filename:
            img = Image.open(filename).resize((150, 150))
            self.img = ImageTk.PhotoImage(img)
            self.img_label.config(image=self.img)
            self.img_label.image = self.img

            if not os.path.exists("profile_folder"):
                os.mkdir("profile_folder")

            path = f"profile_folder/{self.user.username}.png"
            img.save(path)

            try:
                user = session.query(User).filter_by(username=self.user.username).first()
                user.profile_picture = path
                session.commit()
                messagebox.showinfo("Info", "Profilio nuotrauka pakeista sėkmingai")
            except SQLAlchemyError as e:
                session.rollback()
                messagebox.showerror("Klaida", f"Nepavyko pakeisti profilio nuotraukos: {e}")

    def log_off(self):
        sys.exit(self)

    def edit_name(self):
        name_change_window = tk.Toplevel(self.master)
        name_change_window.title("Keisti vardą")
        name_change_window.geometry("300x150")
        name_change_window.config(bg="white")

        name_label = tk.Label(name_change_window, text="Naujas vardas:", font=("Arial", 12), bg="white")
        name_label.place(x=20, y=20)
        name_entry = tk.Entry(name_change_window, font=("Arial", 12), width=20)
        name_entry.place(x=130, y=20)

        save_button = tk.Button(name_change_window, text="Išsaugoti", font=("Arial", 12), bg="#57a1f8", fg="white",
                                cursor="hand2", command=lambda: self.save_name(name_entry.get(), name_change_window))
        save_button.place(x=120, y=80)

    def save_name(self, new_name, window):
        if not new_name:
            messagebox.showerror("Error", "Neįvestas naujas vardas")
            return

        try:
            user = session.query(User).filter_by(username=self.user.username).first()
            user.name = new_name
            session.commit()
            self.user= user
            messagebox.showinfo("Info", "Vardas pakeistas sėkmingai")
        except SQLAlchemyError as e:
            session.rollback()
            messagebox.showerror("Error", f"Klaida: {e}")
        window.destroy()

    def edit_surname(self):
        surname_change_window = tk.Toplevel(self.master)
        surname_change_window.title("Keisti pavardę")
        surname_change_window.geometry("300x150")
        surname_change_window.config(bg="white")

        surname_label = tk.Label(surname_change_window, text="Nauja pavardė:", font=("Arial", 12), bg="white")
        surname_label.place(x=20, y=20)
        surname_entry = tk.Entry(surname_change_window, font=("Arial", 12), width=20)
        surname_entry.place(x=130, y=20)

        save_button = tk.Button(surname_change_window, text="Išsaugoti", font=("Arial", 12), bg="#57a1f8", fg="white",
                                cursor="hand2",
                                command=lambda: self.save_surname(surname_entry.get(), surname_change_window))
        save_button.place(x=120, y=80)

    def save_surname(self, new_surname, window):
        if not new_surname:
            messagebox.showerror("Error", "Neįvesta nauja pavardė")
            return

        try:
            user = session.query(User).filter_by(username=self.user.username).first()
            user.surname = new_surname
            session.commit()
            self.user = user
            messagebox.showinfo("Info", "Pavardė pakeista sėkmingai")
        except SQLAlchemyError as e:
            session.rollback()
            messagebox.showerror("Error", f"Klaida: {e}")
        window.destroy()

    def edit_grade(self):
        grade_change_window = tk.Toplevel(self.master)
        grade_change_window.title("Keisti klasę")
        grade_change_window.geometry("300x150")
        grade_change_window.config(bg="white")

        grade_label = tk.Label(grade_change_window, text="Nauja klasė:", font=("Arial", 12), bg="white")
        grade_label.place(x=20, y=20)
        grade_entry = tk.Entry(grade_change_window, font=("Arial", 12), width=20)
        grade_entry.place(x=130, y=20)

        save_button = tk.Button(grade_change_window, text="Išsaugoti", font=("Arial", 12), bg="#57a1f8", fg="white",
                                cursor="hand2", command=lambda: self.save_grade(grade_entry.get(), grade_change_window))
        save_button.place(x=120, y=80)

    def save_grade(self, new_grade, window):
        if not new_grade:
            messagebox.showerror("Error", "Neįvesta nauja klasė")
            return
        try:
            user = session.query(User).filter_by(username=self.user.username).first()
            user.grade = new_grade
            session.commit()
            messagebox.showinfo("Info", "Klasė pakeista sėkmingai")
        except SQLAlchemyError as e:
            session.rollback()
            messagebox.showerror("Error", f"Klaida: {e}")
        window.destroy()

    def edit_email(self):
        email_change_window = tk.Toplevel(self.master)
        email_change_window.title("Keisti el. paštą")
        email_change_window.geometry("300x150")
        email_change_window.config(bg="white")

        email_label = tk.Label(email_change_window, text="Naujas el. paštas:", font=("Arial", 12), bg="white")
        email_label.place(x=20, y=20)
        email_entry = tk.Entry(email_change_window, font=("Arial", 12), width=20)
        email_entry.place(x=130, y=20)

        save_button = tk.Button(email_change_window, text="Išsaugoti", font=("Arial", 12), bg="#57a1f8", fg="white",
                                cursor="hand2", command=lambda: self.save_email(email_entry.get(), email_change_window))
        save_button.place(x=120, y=80)

    def save_email(self, new_email, window):
        if not new_email:
            messagebox.showerror("Error", "Neįvestas naujas el. paštas")
            return
        try:
            user = session.query(User).filter_by(username=self.user.username).first()
            user.email = new_email
            session.commit()
            messagebox.showinfo("Info", "El. paštas pakeistas sėkmingai")
        except SQLAlchemyError as e:
            session.rollback()
            messagebox.showerror("Error", f"Klaida: {e}")
        window.destroy()

    def show_readme(self):
        with open("readme.txt", "r", encoding='utf-8') as f:
            contents = f.read()
            messagebox.showinfo("Apie programą", contents)

    def read_book(self, book_id):
        book = session.query(Book).filter_by(id=book_id).first()
        book_path = f"knygos/tekstai/chapter_{book_id}.txt"
        reader_window = tk.Toplevel(self.master)
        Reader(reader_window, book_path)


if __name__ == '__main__':
    root = tk.Tk()
    user = session.query(User).filter_by(username="username", password="password").first()
    app = Profile(root, user=user)
    root.mainloop()
