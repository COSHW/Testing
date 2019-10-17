# coding=utf8
from tkinter import *
from tkinter import ttk
import backend
import re
import tkinter.scrolledtext
import random
import analysis
from tkinter.messagebox import showerror, showwarning
import ctypes


database = backend.Database_user()
current_email = ""
current_level = ""
subject = ""
admin_subject = ""


class A(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.wm_title("Тестирование")
        self.resizable(width=False, height=False)
        self.protocol("WM_DELETE_WINDOW", close)
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('mycompany.myproduct.subproduct.version')
        self.iconbitmap(default=r'D:\Projects\PythonProjects\Testing2\images\education_icon_Jj5_icon.ico')
        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        list1 = (Login, Register, Choice, Levels, Administrator, Calibration, Test_window)

        for F in list1:
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(Login)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


"""
todo: 
"""


class Login(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        global canvas1
        canvas1 = Canvas(self, bg='#d9d9d9', width=1100, height=700)
        canvas1.grid()

        self.l1 = ttk.Label(self, text="Добро пожаловать!")
        self.l1.place(x=400, y=60)

        self.l2 = ttk.Label(self, text="Вход")
        self.l2.place(x=470, y=90)

        self.l5 = ttk.Label(self, text="Email")
        self.l5.place(x=300, y=197)

        self.email = StringVar()
        self.e1 = ttk.Entry(self, textvariable=self.email)
        self.e1.place(width=200, x=400, y=200)

        self.l4 = ttk.Label(self, text="Пароль")
        self.l4.place(x=300, y=247)

        self.password = StringVar()
        self.e2 = ttk.Entry(self, textvariable=self.password, show="*")
        self.e2.place(width=200, x=400, y=250)

        self.l3 = ttk.Label(self, text="", font=("Times", 12))
        self.l3.place(x=377, y=285)

        self.b1 = ttk.Button(self, text="Войти", width=20,
                             command=lambda: self.check_user(database, self.email.get(), self.password.get()))
        self.b1.place(height=40, width=200, x=400, y=320)

        self.b2 = ttk.Button(self, text="Регистрация", width=20, command=lambda: self.reg())
        self.b2.place(height=40, width=200, x=400, y=370)

        self.b3 = ttk.Button(self, text="Выход", width=20, command=lambda: close())
        self.b3.place(height=40, width=200, x=400, y=470)

        self.bpop = ttk.Button(self, text="Информация", width=20, command=lambda: popup(
            "На этой странице, вы можете зайти в свой профиль, либо зарегистрироваться в системе, нажав на кнопку регистрации."))
        self.bpop.place(height=40, width=200, x=720, y=65)

        self.e1.bind('<Return>', self.check_user_enter_func)
        self.e2.bind('<Return>', self.check_user_enter_func)

    def check_user_enter_func(self, event):
        self.check_user(database, self.email.get(), self.password.get())

    def check_user(self, database, email, password):
        pattern = r"([\w\.-]+)@([\w\.-]+)(\.[\w\.]+)"
        match = re.search(pattern, email)
        result = backend.Database_user.check(database, email, password)
        if match:
            if self.password.get() == "":
                self.l3.config(text="Пожалуйста, введите свой пароль!")
            elif len(result) == 0:
                self.l3.config(text="Неправильный логин или пароль!")
            elif len(result) == 1:
                if result[0][7] == "admin":
                    self.e1.delete(0, END)
                    self.e2.delete(0, END)
                    self.controller.show_frame(Administrator)
                else:
                    global current_email
                    current_email = email
                    self.e1.delete(0, END)
                    self.e2.delete(0, END)
                    app.frames[Choice].update_points()
                    self.controller.show_frame(Choice)

        else:
            self.l3.config(text="Пожалуйста, введите свой email!")

    def reg(self):
        self.e1.delete(0, END)
        self.e2.delete(0, END)
        self.controller.show_frame(Register)


"""
todo:
"""


class Register(Frame):

    def __init__(self, parent, controller):
        self.controller = controller
        Frame.__init__(self, parent)

        global canvas2
        canvas2 = Canvas(self, bg='#d9d9d9', width=1100, height=700)
        canvas2.grid()

        self.l2 = ttk.Label(self, text="Окно регистрации")
        self.l2.place(x=425, y=60)

        self.l3 = ttk.Label(self, text="Email")
        self.l3.place(x=300, y=197)

        self.email_ = StringVar()
        self.e1 = ttk.Entry(self, textvariable=self.email_)
        self.e1.place(width=200, x=400, y=200)

        self.l4 = ttk.Label(self, text="Пароль")
        self.l4.place(x=300, y=247)

        self.password1_ = StringVar()
        self.e2 = ttk.Entry(self, textvariable=self.password1_, show="*")
        self.e2.place(width=200, x=400, y=250)

        self.l4 = ttk.Label(self, text="Повторите пароль")
        self.l4.place(x=200, y=297)

        self.password2_ = StringVar()
        self.e3 = ttk.Entry(self, textvariable=self.password2_, show="*")
        self.e3.place(width=200, x=400, y=300)

        self.l4 = ttk.Label(self, text="", font=("Times", 12))
        self.l4.place(x=397, y=330)

        self.b1 = ttk.Button(self, text="Зарегистрироваться", width=20,
                             command=lambda: self.add_user(database, self.email_.get(), self.password1_.get(),
                                                           self.password2_.get()))
        self.b1.place(height=40, width=200, x=400, y=370)

        self.b2 = ttk.Button(self, text="Назад", width=20, command=lambda: self.back())
        self.b2.place(height=40, width=200, x=400, y=420)

        self.b3 = ttk.Button(self, text="Выход", width=20, command=lambda: close())
        self.b3.place(height=40, width=200, x=400, y=470)

        self.bpop = ttk.Button(self, text="Информация", width=20, command=lambda: popup(
            "На этой странице, вы можете зарегистрироваться в системе, вписав свой email и пароль в соответствующие поля."))
        self.bpop.place(height=40, width=200, x=720, y=65)

    def add_user(self, database, email, password1, password2):
        result = backend.Database_user.check(database, email, password1)
        pattern = r"([\w\.-]+)@([\w\.-]+)(\.[\w\.]+)"
        match = re.search(pattern, email)
        if self.email_ == "":
            self.l4.config(text="Пожалуйста, введите свои данные!")
        else:
            if match:
                if self.password1_.get() == "" or self.password2_.get() == "":
                    self.l4.config(text="Пожалуста, укажите свой пароль!")
                elif password1 != password2:
                    self.l4.config(text="Пароли не совпадают!")
                elif len(result) == 0:
                    b = backend.Database_user.check_email(database, email)
                    if not b:
                        self.e1.delete(0, END)
                        self.e2.delete(0, END)
                        self.e3.delete(0, END)
                        backend.Database_user.register(database, email, password1)
                        self.l4.config(text="Регистрация прошла успешно")
                    else:
                        self.l4.config(text="Пользователь с такими данными уже существует!")
                elif len(result) == 1:
                    self.l4.config(text="Пользователь с такими данными уже существует!")
            else:
                self.l4.config(text="Пожалуйста, введите email!")

    def back(self):
        self.e1.delete(0, END)
        self.e2.delete(0, END)
        self.e3.delete(0, END)
        self.l4.config(text="")
        self.controller.show_frame(Login)


"""
todo: 
"""


class Choice(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        global canvas3
        canvas3 = Canvas(self, bg='#d9d9d9', width=1100, height=700)
        canvas3.grid()

        self.result = backend.Database_user.check_all_user_points(database, current_email)

        self.l2 = ttk.Label(self, text="Выберите предмет теста")
        self.l2.place(x=440, y=60)

        self.b1 = ttk.Button(self, text="Математика", width=20, command=lambda: self.button_choice(button="mat"))
        self.b1.place(height=40, width=200, x=400, y=130)

        self.b2 = ttk.Button(self, text="Русский язык", width=20, command=lambda: self.button_choice(button="rus"))
        self.b2.place(height=40, width=200, x=400, y=180)

        self.b3 = ttk.Button(self, text="Английский язык", width=20, command=lambda: self.button_choice(button="eng"))
        self.b3.place(height=40, width=200, x=1110, y=1110)

        self.b4 = ttk.Button(self, text="Информатика", width=20, command=lambda: self.button_choice(button="inf"))
        self.b4.place(height=40, width=200, x=400, y=230)

        self.b_analysis = ttk.Button(self, text="Прогноз поступлений", command=lambda: self.analysis())
        self.b_analysis.place(height=40, width=200, x=720, y=490)

        self.b5 = ttk.Button(self, text="Сменить пользователя", width=20,
                             command=lambda: self.controller.show_frame(Login))
        self.b5.place(height=40, width=200, x=400, y=440)

        self.b6 = ttk.Button(self, text="Выход", width=20, command=lambda: close())
        self.b6.place(height=40, width=200, x=400, y=490)

        self.bpop = ttk.Button(self, text="Информация", width=20, command=lambda: popup(
            "На этой странице можно выбрать предмет, по которому вы хотите пройти тестирование (при нулевом количестве баллов, начнётся калибровочное тестирование, которое определит ваш начальный уровень), либо, при достаточном количестве баллов, узнать вашы шансы поступления в вузы России."))
        self.bpop.place(height=40, width=200, x=720, y=65)

        self.t1 = Text(self, height=1, width=3)
        self.t1.config(state="disabled")
        self.t1.place(x=610, y=140)

        self.t2 = Text(self, height=1, width=3)
        self.t2.config(state="disabled")
        self.t2.place(x=610, y=190)

        # self.t3 = Text(self, height=1, width=3)
        # self.t3.config(state="disabled")
        # self.t3.place(x=610, y=290)

        self.t4 = Text(self, height=1, width=3)
        self.t4.config(state="disabled")
        self.t4.place(x=610, y=240)

    def analysis(self):
        if int(self.t1.get('1.0', END)) <= 60 or int(self.t2.get('1.0', END)) <= 60:
            showerror("Ошибка",
                      "Чтобы получить анализ поступлений, минимум нужны результаты семи уровнией математики и русского языка")
        else:
            analys_obj = analysis.Analyser()
            analys_obj.analysis_window(self.t1.get('1.0', END), self.t2.get('1.0', END), # self.t3.get('1.0', END),
                                       self.t4.get('1.0', END), current_email)

    def update_points(self):
        self.result = backend.Database_user.check_all_user_points(database, current_email)
        self.t1.config(state="normal")
        self.t1.delete('1.0', END)
        self.t1.insert(END, self.points_mat())
        self.t1.config(state="disabled")
        self.t2.config(state="normal")
        self.t2.delete('1.0', END)
        self.t2.insert(END, self.points_rus())
        self.t2.config(state="disabled")
        # self.t3.config(state="normal")
        # self.t3.delete('1.0', END)
        # self.t3.insert(END, self.points_eng())
        # self.t3.config(state="disabled")
        self.t4.config(state="normal")
        self.t4.delete('1.0', END)
        self.t4.insert(END, self.points_inf())
        self.t4.config(state="disabled")

    def points_mat(self):
        return self.result[0][0]

    def points_rus(self):
        return self.result[0][1]

    def points_eng(self):
        return self.result[0][2]

    def points_inf(self):
        return self.result[0][3]

    def button_choice(self, button):
        self.result = backend.Database_user.check_all_user_points(database, current_email)
        global subject
        global current_level
        subject = button
        if button == 'mat':
            if self.result[0][0] == 0:
                current_level = 0
                self.controller.show_frame(Calibration)
            else:
                self.controller.show_frame(Levels)
        elif button == 'rus':
            if self.result[0][1] == 0:
                current_level = 0
                self.controller.show_frame(Calibration)
            else:
                self.controller.show_frame(Levels)
        elif button == 'eng':
            if self.result[0][2] == 0:
                current_level = 0
                self.controller.show_frame(Calibration)
            else:
                self.controller.show_frame(Levels)
        elif button == 'inf':
            if self.result[0][3] == 0:
                current_level = 0
                self.controller.show_frame(Calibration)
            else:
                self.controller.show_frame(Levels)


"""
todo:
"""


class Levels(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        global canvas4
        canvas4 = Canvas(self, bg='#d9d9d9', width=1100, height=700)
        canvas4.grid()

        self.controller = controller
        self.result = []

        self.l1 = ttk.Label(self, text="")
        self.l1.place(x=300, y=440)

        self.l2 = ttk.Label(self, text="Выбор сложности")
        self.l2.place(x=450, y=60)

        self.b1 = ttk.Button(self, text="1", width=20, command=lambda: self.test_start(1))
        self.b1.place(height=40, width=200, x=400, y=100)

        self.b2 = ttk.Button(self, text="2", width=20, command=lambda: self.test_start(2))
        self.b2.place(height=40, width=200, x=400, y=150)

        self.b3 = ttk.Button(self, text="3", width=20, command=lambda: self.test_start(3))
        self.b3.place(height=40, width=200, x=400, y=200)

        self.b4 = ttk.Button(self, text="4", width=20, command=lambda: self.test_start(4))
        self.b4.place(height=40, width=200, x=400, y=250)

        self.b5 = ttk.Button(self, text="5", width=20, command=lambda: self.test_start(5))
        self.b5.place(height=40, width=200, x=400, y=300)

        self.b6 = ttk.Button(self, text="6", width=20, command=lambda: self.test_start(6))
        self.b6.place(height=40, width=200, x=400, y=350)

        self.b7 = ttk.Button(self, text="7", width=20, command=lambda: self.test_start(7))
        self.b7.place(height=40, width=200, x=400, y=400)

        self.bpop = ttk.Button(self, text="Информация", width=20, command=lambda: popup(
            "Это страница выбора уровней. Здесь вы можете выбрать сложность тестирования по предмету, который был выбран. Новые уровни сложности открываются по достижении количества баллов, указанного рядом с кнопкой, до тех пор кнопка будет заблокирована."))
        self.bpop.place(height=40, width=200, x=720, y=65)

        self.b8 = ttk.Button(self, text="Назад", command=lambda: controller.show_frame(Choice))
        self.b8.place(height=40, width=200, x=400, y=490)

    def test_start(self, level):
        self.result = backend.Database_user.check_all_user_points(database, current_email)
        global current_level
        current_level = level
        if current_level == 1:
            self.controller.show_frame(Test_window)
            app.frames[Test_window].lstart.config(text="В этом тестировании " + str(len(database.question_pool(subject,
                                                                                                               current_level))) + " вопроса. Время решения теста будет \nзаписываться. Чтобы закончить тест, нужно пройти его до конца, \nкнопки 'назад' не будет.",
                                                  font=("Courier", 15))
        elif current_level == 2:
            if self.result[0][0] >= 10:
                self.l1.config(text="")
                self.controller.show_frame(Test_window)
                app.frames[Test_window].lstart.config(text="В этом тестировании " + str(len(
                    database.question_pool(subject,
                                           current_level))) + " вопроса. Время решения теста будет \nзаписываться. Чтобы закончить тест, нужно пройти его до конца, \nкнопки 'назад' не будет.",
                                                      font=("Courier", 15))
            else:
                self.l1.config(text="У вас недостаточно баллов, пройдите тест меньшего уровня")
        elif current_level == 3:
            if self.result[0][0] >= 20:
                self.l1.config(text="")
                self.controller.show_frame(Test_window)
                app.frames[Test_window].lstart.config(text="В этом тестировании " + str(len(
                    database.question_pool(subject,
                                           current_level))) + " вопроса. Время решения теста будет \nзаписываться. Чтобы закончить тест, нужно пройти его до конца, \nкнопки 'назад' не будет.",
                                                      font=("Courier", 15))
            else:
                self.l1.config(text="У вас недостаточно баллов, пройдите тест меньшего уровня")
        elif current_level == 4:
            if self.result[0][0] >= 30:
                self.l1.config(text="")
                self.controller.show_frame(Test_window)
                app.frames[Test_window].lstart.config(text="В этом тестировании " + str(len(
                    database.question_pool(subject,
                                           current_level))) + " вопроса. Время решения теста будет \nзаписываться. Чтобы закончить тест, нужно пройти его до конца, \nкнопки 'назад' не будет.",
                                                      font=("Courier", 15))
            else:
                self.l1.config(text="У вас недостаточно баллов, пройдите тест меньшего уровня")
        elif current_level == 5:
            if self.result[0][0] >= 40:
                self.l1.config(text="")
                self.controller.show_frame(Test_window)
                app.frames[Test_window].lstart.config(text="В этом тестировании " + str(len(
                    database.question_pool(subject,
                                           current_level))) + " вопроса. Время решения теста будет \nзаписываться. Чтобы закончить тест, нужно пройти его до конца, \nкнопки 'назад' не будет.",
                                                      font=("Courier", 15))
            else:
                self.l1.config(text="У вас недостаточно баллов, пройдите тест меньшего уровня")
        elif current_level == 6:
            if self.result[0][0] >= 50:
                self.l1.config(text="")
                self.controller.show_frame(Test_window)
                app.frames[Test_window].lstart.config(text="В этом тестировании " + str(len(
                    database.question_pool(subject,
                                           current_level))) + " вопроса. Время решения теста будет \nзаписываться. Чтобы закончить тест, нужно пройти его до конца, \nкнопки 'назад' не будет.",
                                                      font=("Courier", 15))
            else:
                self.l1.config(text="У вас недостаточно баллов, пройдите тест меньшего уровня")
        elif current_level == 7:
            if self.result[0][0] >= 60:
                self.l1.config(text="")
                self.controller.show_frame(Test_window)
                if subject == "mat":
                    app.frames[Test_window].lstart.config(
                        text="В этом тестировании 14 вопросов. Время решения теста будет \nзаписываться. Чтобы закончить тест, нужно пройти его до конца, \nкнопки 'назад' не будет.",
                        font=("Courier", 15))
                else:
                    app.frames[Test_window].lstart.config(
                        text="В этом тестировании 18 вопросов. Время решения теста будет \nзаписываться. Чтобы закончить тест, нужно пройти его до конца, \nкнопки 'назад' не будет.",
                        font=("Courier", 15))

            else:
                self.l1.config(text="У вас недостаточно баллов, пройдите тест меньшего уровня")


"""
todo:
"""


class Test_window(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        self.l2 = ttk.Label(text="", font=("Courier", 10))
        global canvas5
        canvas5 = Canvas(self, bg='#d9d9d9', width=1100, height=700)
        canvas5.grid()

        self.controller = controller

        self.lstart = ttk.Label(self)
        self.lstart.place(x=76, y=100)

        self.b1 = ttk.Button(self, text="Начать тест", command=self.test_start)
        self.b1.place(height=40, width=200, x=400, y=250)
        self.b2 = ttk.Button(self, text="Назад", command=lambda: controller.show_frame(Levels))
        self.b2.place(height=40, width=200, x=400, y=320)
        self.text = tkinter.scrolledtext.ScrolledText(self, wrap=WORD, font=("Courier", 10))
        self.end_list = Listbox(self, height=7, width=74)
        self.end_list.place(x=1000, y=1000)
        self.sb1 = Scrollbar(self)
        self.end_list.configure(yscrollcommand=self.sb1.set)

    def test_start(self):
        if current_level == 7:
            if subject == "mat":
                self.result = backend.Database_user.ege_pool_mat(database, subject)
            else:
                self.result = backend.Database_user.ege_pool(database, subject)
        else:
            self.result = backend.Database_user.question_pool(database, subject, current_level)
        self.q_count = 1
        self.q_all = str(len(self.result))
        self.q_now = 0
        self.right_answer = 0
        self.points = 0
        self.questions_list = []
        self.b1.place(x=1000, y=1000)
        self.b2.place(x=1000, y=1000)
        self.lstart.place(x=1000, y=1000)

        q_count = "Вопрос 1 из " + self.q_all

        self.b3 = ttk.Button(self, command=lambda: self.check_answer(self.b3['text']))
        self.b4 = ttk.Button(self, command=lambda: self.check_answer(self.b4['text']))
        self.b5 = ttk.Button(self, command=lambda: self.check_answer(self.b5['text']))
        self.b6 = ttk.Button(self, command=lambda: self.check_answer(self.b6['text']))
        self.b7 = ttk.Button(self, text="Ответить", command=lambda: self.check_answer(self.answer1.get()))
        self.b8 = ttk.Button(self, text="Ответить", command=lambda: self.check_answer(
            [self.answer1.get(), self.answer2.get(), self.answer3.get()]))
        self.answer1 = StringVar()
        self.answer2 = StringVar()
        self.answer3 = StringVar()
        self.answer_entry1 = ttk.Entry(self, textvariable=self.answer1)
        self.answer_entry2 = ttk.Entry(self, textvariable=self.answer2)
        self.answer_entry3 = ttk.Entry(self, textvariable=self.answer3)
        self.l1 = ttk.Label(text="", font=("Courier", 30))
        self.l1.place(x=415, y=70)
        self.l2.config(text=q_count)
        self.l2.place(x=200, y=150)

        self.text.place(height=150, width=600, x=200, y=180)
        self.text.insert("1.0", self.result[self.q_now][1])

        self.b3.place(height=50, width=275, x=200, y=380)
        self.b4.place(height=50, width=275, x=525, y=380)
        self.b5.place(height=50, width=275, x=200, y=470)
        self.b6.place(height=50, width=275, x=525, y=470)

        self.timer(0, 60)
        self.random_answer()

    def timer(self, sec1, min1):
        try:
            if min1 == 0 and sec1 == 0:
                showwarning("Предупреждение!", "Время вышло!")
                self.test_end()
            if sec1 != 0:
                sec1 -= 1
                if sec1 < 10:
                    comb = str(min1) + ":0" + str(sec1)
                else:
                    comb = str(min1) + ":" + str(sec1)
                self.l1.config(text=comb)
                self.after(1000, lambda: self.timer(sec1, min1))
            else:
                sec1 = 59
                min1 -= 1
                if sec1 < 10:
                    comb = str(min1) + ":0" + str(sec1)
                else:
                    comb = str(min1) + ":" + str(sec1)
                self.l1.config(text=comb)
                self.after(1000, lambda: self.timer(sec1, min1))
        except:
            pass

    def random_answer(self):
        self.list_ = [2, 3, 4, 5]
        self.right_answer = self.result[self.q_now][self.list_[0]]
        random.shuffle(self.list_)
        if self.result[self.q_now][3] == "None":
            self.b3.place(height=40, width=220, x=1111, y=1111)
            self.b4.place(height=40, width=220, x=1111, y=1111)
            self.b5.place(height=40, width=220, x=1111, y=1111)
            self.b6.place(height=40, width=220, x=1111, y=1111)
            self.b8.place(height=40, width=220, x=1111, y=1111)
            self.answer_entry2.place(height=20, width=220, x=1111, y=1111)
            self.answer_entry3.place(height=20, width=220, x=1111, y=1111)
            self.answer_entry1.place(height=20, width=220, x=390, y=380)
            self.b7.place(height=40, width=220, x=390, y=470)
        elif self.result[self.q_now][5] == "None":
            self.b3.place(height=40, width=220, x=1111, y=1111)
            self.b4.place(height=40, width=220, x=1111, y=1111)
            self.b5.place(height=40, width=220, x=1111, y=1111)
            self.b6.place(height=40, width=220, x=1111, y=1111)
            self.b7.place(height=40, width=220, x=1111, y=1111)
            self.answer_entry1.place(height=20, width=220, x=390, y=380)
            self.answer_entry2.place(height=20, width=220, x=390, y=410)
            self.answer_entry3.place(height=20, width=220, x=390, y=440)
            self.b8.place(height=40, width=220, x=390, y=470)
        else:
            self.answer_entry1.place(height=20, width=220, x=1111, y=1111)
            self.answer_entry2.place(height=20, width=220, x=1111, y=1111)
            self.answer_entry3.place(height=20, width=220, x=1111, y=1111)
            self.b7.place(height=40, width=220, x=1111, y=1111)
            self.b8.place(height=40, width=220, x=1111, y=1111)
            self.b3.place(height=40, width=220, x=200, y=380)
            self.b4.place(height=40, width=220, x=525, y=380)
            self.b5.place(height=40, width=220, x=200, y=470)
            self.b6.place(height=40, width=220, x=525, y=470)
            self.b3.configure(text=self.result[self.q_now][self.list_[0]])
            self.b4.configure(text=self.result[self.q_now][self.list_[1]])
            self.b5.configure(text=self.result[self.q_now][self.list_[2]])
            self.b6.configure(text=self.result[self.q_now][self.list_[3]])

    def check_answer(self, button):
        question = []
        question.append(self.q_count)
        question.append(self.result[self.q_now][1])
        question.append(self.result[self.q_now][self.list_[0]])
        question.append(self.result[self.q_now][self.list_[1]])
        question.append(self.result[self.q_now][self.list_[2]])
        question.append(self.result[self.q_now][self.list_[3]])
        question.append(self.right_answer)
        question.append(button)
        question.append(self.result[self.q_now][8])
        self.questions_list.append(question)
        self.answer_entry1.delete(0, END)
        self.answer_entry2.delete(0, END)
        self.answer_entry3.delete(0, END)
        if button == self.right_answer:
            if str(self.q_count) != self.q_all:
                self.points += int(self.result[self.q_now][6])
                self.q_now += 1
                self.q_count += 1
                self.text.delete("1.0", END)
                self.text.insert("1.0", self.result[self.q_now][1])
                q_count = "Вопрос " + str(self.q_count) + " из " + self.q_all
                self.l2.configure(text=q_count)
                self.random_answer()
            else:
                self.test_end()
        else:
            if str(self.q_count) != self.q_all:
                self.q_count += 1
                self.q_now += 1
                self.text.delete("1.0", END)
                self.text.insert("1.0", self.result[self.q_now][1])
                q_count = "Вопрос " + str(self.q_count) + " из " + self.q_all
                self.l2.configure(text=q_count)
                self.random_answer()
            else:
                self.test_end()

    def test_end(self):
        self.text.delete("1.0", END)
        self.text.place(height=120, width=400, x=530, y=160)
        self.l1.place(x=1000, y=1000)
        self.l2.place(x=1000, y=1000)
        self.b3.place(x=1000, y=1000)
        self.b4.place(x=1000, y=1000)
        self.b5.place(x=1000, y=1000)
        self.b6.place(x=1000, y=1000)
        self.b7.place(x=1000, y=1000)
        self.b8.place(x=1000, y=1000)
        self.answer_entry1.place(height=20, width=220, x=1111, y=1111)
        self.answer_entry2.place(height=20, width=220, x=1111, y=1111)
        self.answer_entry3.place(height=20, width=220, x=1111, y=1111)
        if current_level == 7:
            if subject == "mat":
                self.points = int(self.points/2.5)
                if self.points >= 60:
                    self.end_results = "Поздравляем, теперь вам открыта кнопка анализа\n возможных будущих мест поступлений!"
                    database.add_final_points(subject, current_email, self.points)
                else:
                    self.end_results = "К сожалению, набранных баллов не достаточно для определения места поступления.\nНиже указан ваш результат."
            else:
                self.points = int(self.points/3)
                if self.points >= 60:
                    self.end_results = "Поздравляем, теперь вам открыта кнопка анализа\n возможных будущих мест поступлений!"

                else:
                    self.end_results = "К сожалению, набранных баллов не достаточно для определения места поступления.\nНиже указан ваш результат."

        elif self.points >= 60:
            self.end_results = "Поздравляем, вы набрали достаточное количество баллов для перехода на следующую \nсложность! Ниже указан ваш результат."
            database.add_points(subject, current_email, current_level)
        else:
            self.end_results = "К сожалению, набранных баллов не достаточно для перехода на следующую сложность.\nНиже указан ваш результат."

        self.lend = ttk.Label(self, text=self.end_results)
        self.lend.place(x=76, y=80)

        self.end_list.place(height=120, width=400, x=100, y=160)
        self.end_list.delete(0, END)
        for item in self.questions_list:
            self.end_list.insert(END, item[0:2])
        self.end_list.bind('<<ListboxSelect>>', self.get_selected_row)

        self.e1 = Text(self, wrap=WORD)
        self.e2 = Text(self, wrap=WORD)
        self.e3 = Text(self, wrap=WORD)
        self.e4 = Text(self, wrap=WORD)
        self.e5 = Text(self, wrap=WORD)
        self.e1.place(height=40, width=160, x=530, y=300)
        self.e2.place(height=40, width=160, x=720, y=300)
        self.e3.place(height=40, width=160, x=530, y=370)
        self.e4.place(height=40, width=160, x=720, y=370)
        self.e5.place(height=120, width=400, x=100, y=300)
        self.l11 = ttk.Label(self, text="Вопрос:")
        self.l11.place(x=530, y=130)

        self.b_end = ttk.Button(self, text="К выбору предмета", command=lambda: self.to_menu())
        self.b_end.place(height=40, width=220, x=400, y=480)

    def get_selected_row(self, event=None):
        if self.end_list.curselection():
            self.e1.config(bg="white")
            self.e2.config(bg="white")
            self.e3.config(bg="white")
            self.e4.config(bg="white")

        self.e1.place(height=40, width=160, x=530, y=300)
        self.e2.place(height=40, width=160, x=720, y=300)
        self.e3.place(height=40, width=160, x=530, y=370)
        self.e4.place(height=40, width=160, x=720, y=370)

        global selected_tuple1
        if self.end_list.curselection():
            index = self.end_list.curselection()[0]
            selected_tuple1 = self.end_list.get(index)
            self.text.config(state="normal")
            self.text.delete("1.0", END)
            self.text.insert(END, selected_tuple1[1])
            self.text.config(state="disabled")
            self.e1.config(state="normal")
            self.e1.delete("1.0", END)
            self.e1.insert(END, self.questions_list[index][2])
            self.e1.config(state="disabled")
            self.e2.config(state="normal")
            self.e2.delete("1.0", END)
            self.e2.insert(END, self.questions_list[index][3])
            self.e2.config(state="disabled")
            self.e3.config(state="normal")
            self.e3.delete("1.0", END)
            self.e3.insert(END, self.questions_list[index][4])
            self.e3.config(state="disabled")
            self.e4.config(state="normal")
            self.e4.delete("1.0", END)
            self.e4.insert(END, self.questions_list[index][5])
            self.e4.config(state="disabled")
            self.e5.config(state="normal")
            self.e5.delete("1.0", END)
            self.e5.insert(END, ("Ваш ответ: " + str(self.questions_list[index][7]) + "\nПравильый ответ: " +
                                 str(self.questions_list[index][6])))
            self.e5.config(state="disabled")

            if self.e1.get(1.0, END) == "None\n" or self.e2.get(1.0, END) == "None\n" or self.e3.get(1.0,
                                                                                                     END) == "None\n" or self.e4.get(
                    1.0, END) == "None\n":
                self.e1.place(height=40, width=160, x=530, y=300)
                self.e2.place(height=40, width=160, x=530, y=300)
                self.e3.place(height=40, width=160, x=530, y=300)
                self.e4.place(height=40, width=160, x=530, y=300)
                if self.e1.get(1.0, END) == "None\n":
                    self.e1.place(x=1000, y=1000)
                if self.e2.get(1.0, END) == "None\n":
                    self.e2.place(x=1000, y=1000)
                if self.e3.get(1.0, END) == "None\n":
                    self.e3.place(x=1000, y=1000)
                if self.e4.get(1.0, END) == "None\n":
                    self.e4.place(x=1000, y=1000)

    def to_menu(self):
        self.lstart.place(x=76, y=100)
        self.b1.place(height=40, width=200, x=400, y=250)
        self.b2.place(height=40, width=200, x=400, y=320)
        self.end_list.place(x=1000, y=1000)
        self.text.place(x=1000, y=1000)
        self.text.config(state='normal')
        self.text.delete("1.0", END)
        app.frames[Choice].update_points()
        self.controller.show_frame(Choice)

        self.l1.destroy()
        self.l11.destroy()
        self.e1.destroy()
        self.e2.destroy()
        self.e3.destroy()
        self.e4.destroy()
        self.e5.destroy()
        self.b_end.destroy()
        self.lend.destroy()


"""
todo:
"""


class Calibration(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.l2 = ttk.Label(text="", font=("Courier", 10))

        global canvas6
        canvas6 = Canvas(self, bg='#d9d9d9', width=1100, height=700)
        canvas6.grid()

        self.controller = controller

        self.lstart = ttk.Label(self,
                                text="Этот тест определит ваш начальный \nуровень знаний, чем выше, тем больше уровней \nсложости будет доступно после прохождения. \nЧтобы закончить тест, нужно пройти его до \nконца, кнопки 'назад' не будет.",
                                font=("Courier", 15))
        self.lstart.place(x=76, y=100)

        self.b1 = ttk.Button(self, text="Начать тест", command=self.test_start)
        self.b1.place(height=40, width=200, x=400, y=250)
        self.b2 = ttk.Button(self, text="Назад", command=lambda: controller.show_frame(Choice))
        self.b2.place(height=40, width=200, x=400, y=320)
        self.text = tkinter.scrolledtext.ScrolledText(self, wrap=WORD, font=("Courier", 10))
        self.end_list = Listbox(self, height=7, width=74)
        self.end_list.place(x=1000, y=1000)
        self.sb1 = Scrollbar(self)
        self.end_list.configure(yscrollcommand=self.sb1.set)

    def test_start(self):
        if subject == "mat":
            self.result = backend.Database_user.ege_pool_mat(database, subject)
        else:
            self.result = backend.Database_user.ege_pool(database, subject)
        self.q_count = 1
        self.q_all = str(len(self.result))
        self.q_now = 0
        self.right_answer = 0
        self.points = 0
        self.questions_list = []
        self.b1.place(x=1000, y=1000)
        self.b2.place(x=1000, y=1000)
        self.lstart.place(x=1000, y=1000)

        q_count = "Вопрос 1 из " + self.q_all

        self.b3 = ttk.Button(self, command=lambda: self.check_answer(self.b3['text']))
        self.b4 = ttk.Button(self, command=lambda: self.check_answer(self.b3['text']))
        self.b5 = ttk.Button(self, command=lambda: self.check_answer(self.b3['text']))
        self.b6 = ttk.Button(self, command=lambda: self.check_answer(self.b3['text']))
        self.b7 = ttk.Button(self, text="Ответить", command=lambda: self.check_answer(self.answer1.get()))
        self.b8 = ttk.Button(self, text="Ответить", command=lambda: self.check_answer(
            [self.answer1.get(), self.answer2.get(), self.answer3.get()]))
        self.answer1 = StringVar()
        self.answer2 = StringVar()
        self.answer3 = StringVar()
        self.answer_entry1 = ttk.Entry(self, textvariable=self.answer1)
        self.answer_entry2 = ttk.Entry(self, textvariable=self.answer2)
        self.answer_entry3 = ttk.Entry(self, textvariable=self.answer3)
        self.l1 = ttk.Label(text="", font=("Courier", 30))
        self.l1.place(x=415, y=70)
        self.l2.config(text=q_count)
        self.l2.place(x=200, y=150)

        self.text.place(height=150, width=600, x=200, y=180)
        self.text.insert("1.0", self.result[self.q_now][1])

        self.b3.place(height=50, width=275, x=200, y=380)
        self.b4.place(height=50, width=275, x=525, y=380)
        self.b5.place(height=50, width=275, x=200, y=470)
        self.b6.place(height=50, width=275, x=525, y=470)

        self.timer(0, 60)
        self.random_answer()

    def timer(self, sec1, min1):
        try:
            if min1 == 0 and sec1 == 0:
                showwarning("Предупреждение!", "Время вышло!")
                self.test_end()
            if sec1 != 0:
                sec1 -= 1
                if sec1 < 10:
                    comb = str(min1) + ":0" + str(sec1)
                else:
                    comb = str(min1) + ":" + str(sec1)
                self.l1.config(text=comb)
                self.after(1000, lambda: self.timer(sec1, min1))
            else:
                sec1 = 59
                min1 -= 1
                if sec1 < 10:
                    comb = str(min1) + ":0" + str(sec1)
                else:
                    comb = str(min1) + ":" + str(sec1)
                self.l1.config(text=comb)
                self.after(1000, lambda: self.timer(sec1, min1))
        except:
            pass

    def random_answer(self):
        self.list_ = [2, 3, 4, 5]
        self.right_answer = self.result[self.q_now][self.list_[0]]
        random.shuffle(self.list_)
        if self.result[self.q_now][3] == "None":
            self.b3.place(height=40, width=220, x=1111, y=1111)
            self.b4.place(height=40, width=220, x=1111, y=1111)
            self.b5.place(height=40, width=220, x=1111, y=1111)
            self.b6.place(height=40, width=220, x=1111, y=1111)
            self.b8.place(height=40, width=220, x=1111, y=1111)
            self.answer_entry2.place(height=20, width=220, x=1111, y=1111)
            self.answer_entry3.place(height=20, width=220, x=1111, y=1111)
            self.answer_entry1.place(height=20, width=220, x=390, y=380)
            self.b7.place(height=40, width=220, x=390, y=470)
        elif self.result[self.q_now][5] == "None":
            self.b3.place(height=40, width=220, x=1111, y=1111)
            self.b4.place(height=40, width=220, x=1111, y=1111)
            self.b5.place(height=40, width=220, x=1111, y=1111)
            self.b6.place(height=40, width=220, x=1111, y=1111)
            self.b7.place(height=40, width=220, x=1111, y=1111)
            self.answer_entry1.place(height=20, width=220, x=390, y=380)
            self.answer_entry2.place(height=20, width=220, x=390, y=410)
            self.answer_entry3.place(height=20, width=220, x=390, y=440)
            self.b8.place(height=40, width=220, x=390, y=470)
        else:
            self.answer_entry1.place(height=20, width=220, x=1111, y=1111)
            self.answer_entry2.place(height=20, width=220, x=1111, y=1111)
            self.answer_entry3.place(height=20, width=220, x=1111, y=1111)
            self.b7.place(height=40, width=220, x=1111, y=1111)
            self.b8.place(height=40, width=220, x=1111, y=1111)
            self.b3.place(height=40, width=220, x=200, y=380)
            self.b4.place(height=40, width=220, x=525, y=380)
            self.b5.place(height=40, width=220, x=200, y=470)
            self.b6.place(height=40, width=220, x=525, y=470)
            self.b3.configure(text=self.result[self.q_now][self.list_[0]])
            self.b4.configure(text=self.result[self.q_now][self.list_[1]])
            self.b5.configure(text=self.result[self.q_now][self.list_[2]])
            self.b6.configure(text=self.result[self.q_now][self.list_[3]])

    def check_answer(self, button):
        question = []
        question.append(self.q_count)
        question.append(self.result[self.q_now][1])
        question.append(self.result[self.q_now][self.list_[0]])
        question.append(self.result[self.q_now][self.list_[1]])
        question.append(self.result[self.q_now][self.list_[2]])
        question.append(self.result[self.q_now][self.list_[3]])
        question.append(self.right_answer)
        question.append(button)
        question.append(self.result[self.q_now][8])
        self.questions_list.append(question)
        self.answer_entry1.delete(0, END)
        self.answer_entry2.delete(0, END)
        self.answer_entry3.delete(0, END)
        if button == self.right_answer:
            if str(self.q_count) != self.q_all:
                self.points += int(self.result[self.q_now][6])
                self.q_now += 1
                self.q_count += 1
                self.text.delete("1.0", END)
                self.text.insert("1.0", self.result[self.q_now][1])
                q_count = "Вопрос " + str(self.q_count) + " из " + self.q_all
                self.l2.configure(text=q_count)
                self.random_answer()
            else:
                self.test_end()
        else:
            if str(self.q_count) != self.q_all:
                self.q_count += 1
                self.q_now += 1
                self.text.delete("1.0", END)
                self.text.insert("1.0", self.result[self.q_now][1])
                q_count = "Вопрос " + str(self.q_count) + " из " + self.q_all
                self.l2.configure(text=q_count)
                self.random_answer()
            else:
                self.test_end()

    def test_end(self):
        self.text.delete("1.0", END)
        self.text.place(height=120, width=400, x=530, y=160)
        self.l1.place(x=1000, y=1000)
        self.l2.place(x=1000, y=1000)
        self.b3.place(x=1000, y=1000)
        self.b4.place(x=1000, y=1000)
        self.b5.place(x=1000, y=1000)
        self.b6.place(x=1000, y=1000)
        self.b7.place(x=1000, y=1000)
        self.b8.place(x=1000, y=1000)
        self.answer_entry1.place(height=20, width=220, x=1111, y=1111)
        self.answer_entry2.place(height=20, width=220, x=1111, y=1111)
        self.answer_entry3.place(height=20, width=220, x=1111, y=1111)
        self.b_end = ttk.Button(self, text="К выбору предмета", command=lambda: self.to_menu())
        self.e4 = Text(self)
        self.e3 = Text(self)
        self.e2 = Text(self)
        self.e1 = Text(self)
        if subject == "mat":
            self.points = int(self.points / 2.5)
        else:
            self.points = int(self.points / 3)
        if self.points >= 60:
            self.points = 60
        elif self.points >= 50:
            self.points = 50
        elif self.points >= 40:
            self.points = 40
        elif self.points >= 30:
            self.points = 30
        elif self.points >= 20:
            self.points = 20
        else:
            self.points = 10
        database.add_points(subject, current_email)
        self.end_results = "Поздравляем с прохождением квалификации. Ваш финальный балл равен " + str(
            self.points) + ". \nЭто значит, что вам будет доступны все уровни включительно до " + str(
            int((self.points / 10) + 1))
        self.lend = ttk.Label(self, text=self.end_results)
        self.lend.place(x=76, y=80)

        self.end_list.place(height=120, width=400, x=100, y=160)
        self.end_list.delete(0, END)
        for item in self.questions_list:
            self.end_list.insert(END, item[0:2])
        self.end_list.bind('<<ListboxSelect>>', self.get_selected_row)

        self.e1 = Text(self, wrap=WORD)
        self.e2 = Text(self, wrap=WORD)
        self.e3 = Text(self, wrap=WORD)
        self.e4 = Text(self, wrap=WORD)
        self.e5 = Text(self, wrap=WORD)
        self.e1.place(height=40, width=160, x=530, y=300)
        self.e2.place(height=40, width=160, x=720, y=300)
        self.e3.place(height=40, width=160, x=530, y=370)
        self.e4.place(height=40, width=160, x=720, y=370)
        self.e5.place(height=120, width=400, x=100, y=300)
        self.l11 = ttk.Label(self, text="Вопрос:")
        self.l11.place(x=530, y=130)

        self.b_end = ttk.Button(self, text="К выбору предмета", command=lambda: self.to_menu())
        self.b_end.place(height=40, width=220, x=400, y=480)

    def get_selected_row(self, event=None):
        if self.end_list.curselection():
            self.e1.config(bg="white")
            self.e2.config(bg="white")
            self.e3.config(bg="white")
            self.e4.config(bg="white")

        self.e1.place(height=40, width=160, x=530, y=300)
        self.e2.place(height=40, width=160, x=720, y=300)
        self.e3.place(height=40, width=160, x=530, y=370)
        self.e4.place(height=40, width=160, x=720, y=370)

        global selected_tuple1
        if self.end_list.curselection():
            index = self.end_list.curselection()[0]
            selected_tuple1 = self.end_list.get(index)
            self.text.config(state="normal")
            self.text.delete("1.0", END)
            self.text.insert(END, selected_tuple1[1])
            self.text.config(state="disabled")
            self.e1.config(state="normal")
            self.e1.delete("1.0", END)
            self.e1.insert(END, self.questions_list[index][2])
            self.e1.config(state="disabled")
            self.e2.config(state="normal")
            self.e2.delete("1.0", END)
            self.e2.insert(END, self.questions_list[index][3])
            self.e2.config(state="disabled")
            self.e3.config(state="normal")
            self.e3.delete("1.0", END)
            self.e3.insert(END, self.questions_list[index][4])
            self.e3.config(state="disabled")
            self.e4.config(state="normal")
            self.e4.delete("1.0", END)
            self.e4.insert(END, self.questions_list[index][5])
            self.e4.config(state="disabled")
            self.e5.config(state="normal")
            self.e5.delete("1.0", END)
            self.e5.insert(END, ("Ваш ответ: " + str(self.questions_list[index][7]) + "\nПравильый ответ: " +
                                 str(self.questions_list[index][6])))
            self.e5.config(state="disabled")

            if self.e1.get(1.0, END) == "None\n" or self.e2.get(1.0, END) == "None\n" or self.e3.get(1.0,
                                                                                                     END) == "None\n" or self.e4.get(
                1.0, END) == "None\n":
                self.e1.place(height=40, width=160, x=530, y=300)
                self.e2.place(height=40, width=160, x=530, y=300)
                self.e3.place(height=40, width=160, x=530, y=300)
                self.e4.place(height=40, width=160, x=530, y=300)
                if self.e1.get(1.0, END) == "None\n":
                    self.e1.place(x=1000, y=1000)
                if self.e2.get(1.0, END) == "None\n":
                    self.e2.place(x=1000, y=1000)
                if self.e3.get(1.0, END) == "None\n":
                    self.e3.place(x=1000, y=1000)
                if self.e4.get(1.0, END) == "None\n":
                    self.e4.place(x=1000, y=1000)

    def to_menu(self):
        self.lstart.place(x=76, y=100)
        self.b1.place(height=40, width=200, x=400, y=250)
        self.b2.place(height=40, width=200, x=400, y=320)
        self.end_list.place(x=1000, y=1000)
        self.text.place(x=1000, y=1000)
        self.text.config(state='normal')
        self.text.delete("1.0", END)
        app.frames[Choice].update_points()
        self.controller.show_frame(Choice)

        self.l1.destroy()
        self.l11.destroy()
        self.e1.destroy()
        self.e2.destroy()
        self.e3.destroy()
        self.e4.destroy()
        self.e5.destroy()
        self.b_end.destroy()
        self.lend.destroy()


"""
todo:
"""


class Administrator(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        global canvas7
        canvas7 = Canvas(self, bg='#d9d9d9', width=1100, height=700)
        canvas7.pack()

        self.l1 = ttk.Label(self, text="Окно администратора")
        self.l1.place(x=400, y=60)

        self.b1 = ttk.Button(self, text="Математика", width=20, command=lambda: self.button_choice(button="mat"))
        self.b1.place(height=40, width=200, x=400, y=160)

        self.b2 = ttk.Button(self, text="Русский язык", width=20, command=lambda: self.button_choice(button="rus"))
        self.b2.place(height=40, width=200, x=400, y=210)

        # self.b4 = ttk.Button(self, text="Английский язык", width=20, command=lambda: self.button_choice(button="eng"))
        # self.b4.place(height=40, width=200, x=400, y=310)

        self.b3 = ttk.Button(self, text="Информатика", width=20, command=lambda: self.button_choice(button="inf"))
        self.b3.place(height=40, width=200, x=400, y=260)

        self.b5 = ttk.Button(self, text="Сменить пользователя", width=20,
                             command=lambda: self.controller.show_frame(Login))
        self.b5.place(height=40, width=200, x=400, y=380)

        self.b6 = ttk.Button(self, text="Выход", width=20, command=lambda: close())
        self.b6.place(height=40, width=200, x=400, y=430)

        self.bpop = ttk.Button(self, text="Информация", width=20, command=lambda: popup(
            "Это окно администратора. Выбрав предмет, вы можете изменять содержание тестов для пользователей."))
        self.bpop.place(height=40, width=200, x=720, y=65)

        self.b2pop = ttk.Button(self, text="Информация", command=lambda: popup(
            "В этом окне можно изменить значения тестов (вопросы, ответы, баллы, уровень). При решении добавления или удаления вопросов, рекомендуется оставлять суммарное кол-вом баллов тестирования равному 100 (Стандартно: 2 вопроса по 10 баллов, 2 вопроса по 15 балла, 2 вопроса по 25 баллов, не считая квалификационный и финальный тест)."))
        self.b2pop.place(x=1000, y=1000)
        self.list1 = Listbox(self, height=7, width=74)
        self.list1.place(x=1000, y=1000)

    def button_choice(self, button):
        global admin_subject
        admin_subject = button
        self.list1.delete(0, END)
        for row in backend.Database_user.view(database, admin_subject):
            self.list1.insert(END, row)
        self.administrator_change()

    def administrator_change(self):
        self.b1.place(x=1000, y=1000)
        self.b2.place(x=1000, y=1000)
        self.b3.place(x=1000, y=1000)
        # self.b4.place(x=1000, y=1000)
        self.b5.place(x=1000, y=1000)
        self.b6.place(x=1000, y=1000)
        self.bpop.place(x=1000, y=1000)

        self.l22 = ttk.Label(self, text="Вопрос")
        self.l22.place(x=80, y=205)
        self.l23 = ttk.Label(self, text="Кол-во очков(4-6)")
        self.l23.place(x=290, y=460)
        self.l24 = ttk.Label(self, text="Ответ №1(Прав.)")
        self.l24.place(x=80, y=330)
        self.l25 = ttk.Label(self, text="Ответ №2")
        self.l25.place(x=290, y=330)
        self.l26 = ttk.Label(self, text="Ответ №3")
        self.l26.place(x=80, y=395)
        self.l27 = ttk.Label(self, text="Ответ №4")
        self.l27.place(x=290, y=395)
        self.l28 = ttk.Label(self, text="Уровень")
        self.l28.place(x=80, y=460)
        self.l29 = ttk.Label(self, text="Объяснение")
        self.l29.place(x=360, y=205)
        self.lerror = ttk.Label(self, text="")
        self.lerror.place(x=370, y=250)

        self.list1.place(x=80, y=85)
        self.list1.bind('<<ListboxSelect>>', self.get_selected_row)

        self.b22 = ttk.Button(self, text="Добавить", width=20, command=lambda: self.add_command(admin_subject))
        self.b22.place(height=40, width=200, x=650, y=240)

        self.b23 = ttk.Button(self, text="Изменить", width=20, command=lambda: self.update_command(admin_subject))
        self.b23.place(height=40, width=200, x=650, y=290)

        self.b24 = ttk.Button(self, text="Удалить", width=20, command=lambda: self.delete_command(admin_subject))
        self.b24.place(height=40, width=200, x=650, y=340)

        self.b25 = ttk.Button(self, text="Назад", width=20, command=lambda: self.user_change())
        self.b25.place(height=40, width=200, x=650, y=390)

        self.b26 = ttk.Button(self, text="Выход", width=20, command=lambda: close())
        self.b26.place(height=40, width=200, x=650, y=440)

        self.b2pop.place(height=40, width=200, x=720, y=65)

        self.answer1 = StringVar()
        self.e1 = ttk.Entry(self, textvariable=self.answer1)
        self.e1.place(height=40, width=200, x=80, y=355)

        self.answer2 = StringVar()
        self.e2 = ttk.Entry(self, textvariable=self.answer2)
        self.e2.place(height=40, width=200, x=290, y=355)

        self.answer3 = StringVar()
        self.e3 = ttk.Entry(self, textvariable=self.answer3)
        self.e3.place(height=40, width=200, x=80, y=420)

        self.answer4 = StringVar()
        self.e4 = ttk.Entry(self, textvariable=self.answer4)
        self.e4.place(height=40, width=200, x=290, y=420)

        self.level = StringVar()
        self.e5 = ttk.Entry(self, textvariable=self.level)
        self.e5.place(height=40, width=200, x=80, y=485)

        self.text = tkinter.scrolledtext.ScrolledText(self, wrap=WORD, font=("Courier", 10))
        self.text.place(height=100, width=270, x=80, y=230)

        self.explanation = tkinter.scrolledtext.ScrolledText(self, wrap=WORD, font=("Courier", 10))
        self.explanation.place(height=100, width=270, x=360, y=230)

        self.dif_points = StringVar()
        self.e7 = ttk.Entry(self, textvariable=self.dif_points)
        self.e7.place(height=40, width=200, x=290, y=485)

    def user_change(self):
        self.list1.delete(0, END)
        self.e1.destroy()
        self.e2.destroy()
        self.e3.destroy()
        self.e4.destroy()
        self.e5.destroy()
        self.text.place(x=1000, y=1000)
        self.explanation.place(x=1000, y=1000)
        self.e7.destroy()
        self.list1.place(x=1000, y=1000)
        self.b22.destroy()
        self.b23.destroy()
        self.b24.destroy()
        self.b25.destroy()
        self.b26.destroy()
        self.l22.destroy()
        self.l23.destroy()
        self.l24.destroy()
        self.l25.destroy()
        self.l26.destroy()
        self.l27.destroy()
        self.l28.destroy()
        self.l29.destroy()

        self.b1.place(height=40, width=200, x=400, y=160)
        self.b2.place(height=40, width=200, x=400, y=210)
        self.b3.place(height=40, width=200, x=400, y=260)
        # self.b4.place(height=40, width=200, x=400, y=310)
        self.b5.place(height=40, width=200, x=400, y=380)
        self.b6.place(height=40, width=200, x=400, y=430)
        self.bpop.place(height=40, width=200, x=720, y=65)
        self.b2pop.place(x=1000, y=1000)
        self.controller.show_frame(Administrator)

    def add_command(self, subject):
        questions = []
        for a in backend.Database_user.view(database, subject):
            questions.append(a[1])
        if self.text.get("1.0", END) in questions:
            self.lerror.config(text="Дааный вопрос \nуже существует")
        else:
            backend.Database_user.insert(database, subject, self.text.get(1.0, END), self.answer1.get(),
                                         self.answer2.get(), self.answer3.get(), self.answer4.get(),
                                         self.dif_points.get(), self.level.get())
        self.list1.delete(0, END)
        for row in backend.Database_user.view(database, subject):
            self.list1.insert(END, row)

    def update_command(self, subject):
        backend.Database_user.update(database, subject, str(selected_tuple[0]), self.text.get(1.0, END),
                                     self.answer1.get(), self.answer2.get(), self.answer3.get(), self.answer4.get(),
                                     self.dif_points.get(), self.level.get())
        self.list1.delete(0, END)
        for row in backend.Database_user.view(database, subject):
            self.list1.insert(END, row)

    def delete_command(self, subject):
        backend.Database_user.delete(database, subject, selected_tuple[0])
        self.list1.delete(0, END)
        for row in backend.Database_user.view(database, subject):
            self.list1.insert(END, row)

    def get_selected_row(self, event):
        global selected_tuple
        if self.list1.curselection():
            index = self.list1.curselection()[0]
            selected_tuple = self.list1.get(index)
            self.text.delete("1.0", END)
            c = len(selected_tuple[1])
            self.text.insert(END, selected_tuple[1][0:c - 1])
            self.explanation.delete("1.0", END)
            c = len(selected_tuple[8])
            self.explanation.insert(END, selected_tuple[8][0:c - 1])
            self.e1.delete(0, END)
            self.e1.insert(END, selected_tuple[2])
            self.e2.delete(0, END)
            self.e2.insert(END, selected_tuple[3])
            self.e3.delete(0, END)
            self.e3.insert(END, selected_tuple[4])
            self.e4.delete(0, END)
            self.e4.insert(END, selected_tuple[5])
            self.e7.delete(0, END)
            self.e7.insert(END, selected_tuple[6])
            self.e5.delete(0, END)
            self.e5.insert(END, selected_tuple[7])


def popup(info="Информация", x=350, y=220, **kwargs):
    window = Tk()
    window.wm_title("Информация")
    window.resizable(width=False, height=False)
    window.iconbitmap(r'D:\Projects\PythonProjects\Testing2\images\py.ico')
    window.geometry(str(x) + "x" + str(y) + "+500+260")
    text = tkinter.scrolledtext.ScrolledText(window, wrap=WORD, font=("Courier", 10), width=41, height=10)
    text.place(x=0, y=0)
    text.insert('1.0', info)
    text.config(state="disabled")
    pop = ttk.Button(window, text="Понятно", command=lambda: popup_close(window))
    pop.place(height=40, width=200, x=75, y=170)

    app.frames[Login].bpop.config(state="disabled")
    app.frames[Register].bpop.config(state="disabled")
    app.frames[Choice].bpop.config(state="disabled")
    app.frames[Levels].bpop.config(state="disabled")
    app.frames[Administrator].bpop.config(state="disabled")
    app.frames[Administrator].b2pop.config(state="disabled")
    window.mainloop()


def popup_close(window):
    window.destroy()
    app.frames[Login].bpop.config(state="normal")
    app.frames[Register].bpop.config(state="normal")
    app.frames[Choice].bpop.config(state="normal")
    app.frames[Levels].bpop.config(state="normal")
    app.frames[Administrator].bpop.config(state="normal")
    app.frames[Administrator].b2pop.config(state="normal")


def close():
    quit()


if __name__ == "__main__":
    app = A()
    s = ttk.Style()
    s.configure("TButton", background="#005c6c", font=("Times", 15))
    s.configure("TLabel", background="#d9d9d9", font=("Times", 15))
    app.geometry("1002x602+180+50")
    photoimage = PhotoImage(file="images/9.png")
    canvas1.create_image(500, 300, image=photoimage)
    canvas2.create_image(500, 300, image=photoimage)
    canvas3.create_image(500, 300, image=photoimage)
    canvas4.create_image(500, 300, image=photoimage)
    canvas5.create_image(500, 300, image=photoimage)
    canvas6.create_image(500, 300, image=photoimage)
    canvas7.create_image(500, 300, image=photoimage)
    app.mainloop()
