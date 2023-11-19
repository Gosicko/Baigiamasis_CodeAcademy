import tkinter as tk
from tkinter import PhotoImage, messagebox
from sqlalchemy.orm import sessionmaker
from models import engine, User
from registration import Register
from profile import Profile
import traceback


Session = sessionmaker(bind=engine)
session = Session()


class Login(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Prisijungimas")
        self.master.geometry("600x350+300+200")
        self.master.config(bg="white")
        self.master.resizable(False, False)

        self.username = tk.StringVar()
        self.password = tk.StringVar()

        img = PhotoImage(file="login.png")
        img = img.subsample(2)
        img_label = tk.Label(self.master, image=img, border=0, bg="white")
        img_label.image = img
        img_label.place(x=30, y=40)

        frame = tk.Frame(self.master, width=270, height=300, bg="white")
        frame.place(x=300, y=30)

        heading = tk.Label(frame, text="Prisijungimas", fg="#57a1f8", bg="white",
                           font=('Microsoft Yahei UI Light', 23, 'bold'))
        heading.place(x=37, y=5)

        def on_enter_username(i):
            self.username.delete(0, "end")

        def on_leave_username(i):
            if self.username.get() == "":
                self.username.insert(0, "Prisijungimo vardas")

        self.username = tk.Entry(frame, width=25, fg="black", border=0, bg="white",
                                 font=("Microsoft Yahei UI Light", 12))
        self.username.place(x=30, y=90)
        self.username.insert(0, "Prisijungimo vardas")
        self.username.bind("<FocusIn>", on_enter_username)
        self.username.bind("<FocusOut>", on_leave_username)

        username_middle = tk.Frame(frame, width=295, height=1, bg="black")
        username_middle.place(x=25, y=117)

        def on_enter_password(i):
            if self.password.get() == "Slaptažodis":
                self.password.delete(0, "end")
            self.password.config(show="*")

        def on_leave_password(i):
            if self.password.get() == "":
                self.password.insert(0, "Slaptažodis")

        self.password = tk.Entry(frame, width=25, fg="black", border=0, bg="white",
                                 font=("Microsoft Yahei UI Light", 12))
        self.password.place(x=30, y=160)
        self.password.insert(0, "Slaptažodis")
        self.password.bind("<FocusIn>", on_enter_password)
        self.password.bind("<FocusOut>", on_leave_password)

        password_middle = tk.Frame(frame, width=295, height=1, bg="black")
        password_middle.place(x=25, y=187)

        login_button = tk.Button(frame, width=35, pady=7, text="Prisijungti", bg="#57a1f8", fg="white", border=0,
                                 command=self.login_button_pressed)
        login_button.place(x=25, y=200)

        register_label = tk.Label(frame, text="Neturi paskiros?", fg="black", bg="white",
                                  font=("Microsoft Yahei UI Light", 9))
        register_label.place(x=50, y=240)

        register_button = tk.Button(frame, width=10, text="Registruokis", border=0, bg="white", cursor="hand2",
                                    fg="#57a1f8", command=self.open_register_window)
        register_button.place(x=140, y=240)

        self.pack()

    def open_register_window(self):
        register_window = tk.Toplevel(self.master)
        register_form = Register(register_window)
        register_form.wait_window()

    def login_button_pressed(self):
        username = self.username.get()
        password = self.password.get()
        user = session.query(User).filter_by(username=username, password=password).first()

        if user:
            messagebox.showinfo("Sekmingai!", "Jus prisijungete sekmingai!")
            self.master.destroy()
            profile_window = tk.Tk()
            try:
                Profile(profile_window, user)
            except Exception as e:
                traceback.print_exc()
                messagebox.showerror("Error", str(e))
            profile_window.mainloop()
        else:
            messagebox.showerror("Nesekme!", "Prisijungimo vardas ir/arba slaptazodis neteisingi!")


if __name__ == '__main__':
    root = tk.Tk()
    app = Login(root)
    root.mainloop()
