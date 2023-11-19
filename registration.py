import re
import tkinter as tk
from tkinter import messagebox
from sqlalchemy.orm import sessionmaker
from models import engine, User

Session = sessionmaker(bind=engine)
session = Session()


class Register(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master.title("Registracija")
        self.master.geometry("350x500+300+70")
        self.master.config(bg="white")
        self.master.resizable(False, False)

        self.name = tk.StringVar()
        self.surname = tk.StringVar()
        self.email = tk.StringVar()
        self.grade = tk.StringVar()
        self.username = tk.StringVar()
        self.password = tk.StringVar()
        self.agree_to_terms = tk.BooleanVar()

        frame = tk.Frame(self.master, width=300, height=480, bg="white")
        frame.place(x=0, y=30)

        heading = tk.Label(frame, text="Registracija", fg="#57a1f8", bg="white",
                           font=('Microsoft Yahei UI Light', 23, 'bold'))
        heading.place(x=70, y=5)

        def on_enter_name(i):
            name.delete(0, "end")

        def on_leave_name(i):
            if name.get() == "":
                name.insert(0, "Vardas")

        name = tk.Entry(frame, width=25, fg="black", border=0, bg="white", font=("Microsoft Yahei UI Light", 12),
                        textvariable=self.name)
        name.place(x=30, y=90)
        name.insert(0, "Vardas")
        name.bind("<FocusIn>", on_enter_name)
        name.bind("<FocusOut>", on_leave_name)

        name_middle = tk.Frame(frame, width=295, height=1, bg="black")
        name_middle.place(x=25, y=117)

        def on_enter_surname(i):
            surname.delete(0, "end")

        def on_leave_surname(i):
            if surname.get() == "":
                surname.insert(0, "Pavardė")

        surname = tk.Entry(frame, width=25, fg="black", border=0, bg="white", font=("Microsoft Yahei UI Light", 12),
                           textvariable=self.surname)
        surname.place(x=30, y=140)
        surname.insert(0, "Pavardė")
        surname.bind("<FocusIn>", on_enter_surname)
        surname.bind("<FocusOut>", on_leave_surname)

        surname_middle = tk.Frame(frame, width=295, height=1, bg="black")
        surname_middle.place(x=25, y=167)

        def on_enter_email(i):
            email.delete(0, "end")

        def on_leave_email(i):
            if email.get() == "":
                email.insert(0, "El. paštas")

        email = tk.Entry(frame, width=25, fg="black", border=0, bg="white", font=("Microsoft Yahei UI Light", 12),
                         textvariable=self.email)
        email.place(x=30, y=190)
        email.insert(0, "El. paštas")
        email.bind("<FocusIn>", on_enter_email)
        email.bind("<FocusOut>", on_leave_email)

        email_middle = tk.Frame(frame, width=295, height=1, bg="black")
        email_middle.place(x=25, y=217)

        def on_enter_grade(i):
            grade.delete(0, "end")

        def on_leave_grade(i):
            if grade.get() == "":
                grade.insert(0, "Klasė")

        grade = tk.Entry(frame, width=25, fg="black", border=0, bg="white", font=("Microsoft Yahei UI Light", 12),
                         textvariable=self.grade)
        grade.place(x=30, y=240)
        grade.insert(0, "Klasė")
        grade.bind("<FocusIn>", on_enter_grade)
        grade.bind("<FocusOut>", on_leave_grade)

        grade_middle = tk.Frame(frame, width=295, height=1, bg="black")
        grade_middle.place(x=25, y=267)

        def on_enter_username(i):
            username.delete(0, "end")

        def on_leave_username(i):
            if username.get() == "":
                username.insert(0, "Prisijungimo vardas")

        username = tk.Entry(frame, width=25, fg="black", border=0, bg="white", font=("Microsoft Yahei UI Light", 12),
                            textvariable=self.username)
        username.place(x=30, y=290)
        username.insert(0, "Prisijungimo vardas")
        username.bind("<FocusIn>", on_enter_username)
        username.bind("<FocusOut>", on_leave_username)

        username_middle = tk.Frame(frame, width=295, height=1, bg="black")
        username_middle.place(x=25, y=317)

        def on_enter_password(i):
            if password.get() == "Slaptažodis":
                password.delete(0, "end")
            password.config(show="*")

        def on_leave_password(i):
            if password.get() == "":
                password.insert(0, "Slaptažodis")

        password = tk.Entry(frame, width=25, fg="black", border=0, bg="white", font=("Microsoft Yahei UI Light", 12),
                            textvariable=self.password)
        password.place(x=30, y=340)
        password.insert(0, "Slaptažodis")
        password.bind("<FocusIn>", on_enter_password)
        password.bind("<FocusOut>", on_leave_password)

        password_middle = tk.Frame(frame, width=295, height=1, bg="black")
        password_middle.place(x=25, y=367)

        agree_to_terms_checkbox = tk.Checkbutton(frame, text="I agree to Terms", variable=self.agree_to_terms,
                                                 bg="white")
        agree_to_terms_checkbox.place(x=50, y=400)

        register_button = tk.Button(frame, text="Registracija", width=10, command=self.register_user)
        register_button.place(x=170, y=400)

        self.pack()

    def register_user(self):
        name = self.name.get()
        surname = self.surname.get()
        email = self.email.get()
        grade = self.grade.get()
        username = self.username.get()
        password = self.password.get()

        user = session.query(User).filter_by(username=username).first()
        if user:
            messagebox.showerror("Error", "Vartotojo vardas uzimtas.")
            return

        if not re.match("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d@$!%*#?&^~-]{8,}$", password):
            messagebox.showerror("Error",
                                 "Slaptazodyje turi buti nors vienas skaicius, nors viena didzioji raide,"
                                 "nors viena mazoji raide, ir maziausiai 8 zenklai!"
                                 "@$!%*#?&^~- simboliu naudoti negalima!")
            return

        if not self.agree_to_terms.get():
            messagebox.showerror("Error", "You must agree to the terms and conditions.")
            return

        new_user = User(name=name, surname=surname, email=email, grade=grade, username=username, password=password)
        try:
            session.add(new_user)
            session.commit()
            session.close()
            messagebox.showinfo("Success", "Registration successful.")
            self.master.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add user: {e}")

        return


if __name__ == '__main__':
    root = tk.Tk()
    app = Register(root)
    root.mainloop()
