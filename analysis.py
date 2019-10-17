from tkinter import *
from tkinter import ttk
from tkinter import scrolledtext
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from time import sleep
import pandas as pd
from email.mime.text import MIMEText
import smtplib
from tkinter.messagebox import showerror


class Analyser:
    def analysis_window(self, points_mat=0, points_rus=0, points_inf=0, email=""):
        self.email = email
        self.points_mat = points_mat
        self.points_rus = points_rus
        self.points_inf = points_inf
        self.window = Tk()
        self.window.geometry("800x600+270+50")
        self.window.resizable(width=False, height=False)
        self.window.wm_title("Анализ поступлений")
        canvas1 = Canvas(self.window, bg='#d9d9d9', width=1000, height=600)
        canvas1.grid()
        self.s = ttk.Style(self.window)
        self.s.configure("TButton", background="#005c6c", font=("Times", 15))
        self.s.configure("TLabel", background="#d9d9d9", font=("Times", 15))
        self.l1 = ttk.Label(self.window, text="Анализ занимает некоторое время!")
        self.l1.place(x=250, y=200)
        self.b1 = ttk.Button(self.window, text="Результат", command=lambda: self.analysis())
        self.b1.place(height=40, width=200, x=300, y=300)
        self.b2 = ttk.Button(self.window, text="Создать таблицу в csv", command=lambda: self.to_csv())
        self.b4 = ttk.Button(self.window, text="Послать на почту", command=lambda: self.to_email())
        self.b5 = ttk.Button(self.window, text="Закрыть", command=lambda: self.window.destroy())
        self.list = Listbox(self.window)
        self.fakultet = scrolledtext.ScrolledText(self.window, wrap=WORD)
        self.univer = scrolledtext.ScrolledText(self.window, wrap=WORD)
        self.napravlen = scrolledtext.ScrolledText(self.window, wrap=WORD)
        self.addons = scrolledtext.ScrolledText(self.window, wrap=WORD)

        self.window.mainloop()

    def analysis(self):
        try:
            options = Options()
            options.add_argument("--headless")
            options.add_argument("--window-size=650,700")
            options.binary_location = "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
            driver = webdriver.Chrome(chrome_options=options)
            driver.get("http://tabiturient.ru/calculator/")
            if self.points_rus != 0:
                driver.find_element_by_name("ege0").send_keys(self.points_rus)
            if self.points_mat != 0:
                driver.find_element_by_id("plus10").click()
                driver.find_element_by_name("ege10").send_keys(self.points_mat)
            if self.points_inf != 0:
                #driver.find_element_by_id("plus3").click()
                element = driver.find_element_by_id("plus3")
                driver.execute_script("arguments[0].click();", element)
                driver.find_element_by_name("ege3").send_keys(self.points_inf)

            sleep(3)
            soup = BeautifulSoup(driver.page_source, "html.parser")
            self.results = soup.find_all("tr", {"class": "trprox"})
            self.all_info = list()
            for item in self.results:
                d = dict()
                university = item.find_all("td", {"class": "trdod2"})
                d['Университет'] = university[0].text.replace("\n", "")
                d['Факультет'] = item.find("span", {"class": "yesmobile2"}).text.replace("\n", "")
                d['Направление'] = item.find("b", {"class": "yesmobilebable centermobile"}).text.replace("\n", "")
                parts = item.find_all("span", {"class": "yesmobile3"})
                d['Подробности'] = parts[0].text.replace("\n", "") + ", " + parts[1].text.replace("\n", "") + ", " + parts[2].text.replace("\n", "")

                self.all_info.append(d)
            driver.close()
            self.b1.destroy()
            self.b2.place(height=40, width=220, x=500, y=440)
            self.b4.place(height=40, width=220, x=500, y=490)
            self.b5.place(height=40, width=220, x=500, y=540)
            self.l1.destroy()
            self.list.place(height=140, width=600, x=100, y=70)
            i = 1
            for item in self.all_info:
                self.list.insert(END, str(i)+") "+item['Университет']+", "+item['Направление'])
                i += 1

            self.univer.place(height=100, width=200, x=80, y=240)
            self.fakultet.place(height=100, width=200, x=300, y=240)
            self.napravlen.place(height=100, width=200, x=520, y=240)
            self.addons.place(height=100, width=300, x=80, y=400)

            self.list.bind('<<ListboxSelect>>', self.get_selected_row)
            print(self.all_info)
        except Exception as e:
            showerror("Ошибка", "Проверьте соединение с интернетом!")

    def get_selected_row(self, event):
        global selected_tuple
        if self.list.curselection():
            index = self.list.curselection()[0]
            selected_tuple = self.list.get(index)
            self.univer.config(state="normal")
            self.univer.delete(1.0, END)
            self.univer.insert(END, self.all_info[index]['Университет'])
            self.univer.config(state="disabled")
            self.napravlen.config(state="normal")
            self.napravlen.delete(1.0, END)
            self.napravlen.insert(END, self.all_info[index]['Направление'])
            self.napravlen.config(state="disabled")
            self.fakultet.config(state="normal")
            self.fakultet.delete(1.0, END)
            self.fakultet.insert(END, self.all_info[index]['Факультет'])
            self.fakultet.config(state="disabled")
            self.addons.config(state="normal")
            self.addons.delete(1.0, END)
            self.addons.insert(END, self.all_info[index]['Подробности'])
            self.addons.config(state="disabled")

    def to_csv(self):
        pd.set_option('display.max_colwidth', -1)
        df = pd.DataFrame(self.all_info)
        df.to_csv("Info.csv", index_label="Номер", encoding="windows-1251", sep=",")

    def to_email(self):
        from_email = "kursovayarabota2018@gmail.com"
        from_password = "hn7dop45xh12"
        to_email = self.email
        subject = "Результаты анализа"

        pd.set_option('display.max_colwidth', -1)
        info = pd.DataFrame(self.all_info)
        message = info.to_html()

        msg = MIMEText(message, 'html')
        msg['Subject'] = subject
        msg['To'] = to_email
        msg['From'] = from_email

        gmail = smtplib.SMTP('smtp.gmail.com', 587)
        gmail.ehlo()
        gmail.starttls()
        gmail.login(from_email, from_password)
        gmail.send_message(msg)
