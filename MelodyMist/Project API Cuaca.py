from tkinter import *
from tkinter.messagebox import showinfo
from PIL import ImageTk, Image
from customtkinter import *
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
from datetime import datetime
from functools import partial
from collections import deque
import requests
import pytz
import locale
import os
import pygame
import random
import threading
import time


class project:
    pygame.init()
    pygame.mixer.init()
    
    def __init__ (self, window):
        self.play_image1 = ImageTk.PhotoImage(file="C:/Project UAS TERBARU/Button Play.png")
        self.play_image2 = ImageTk.PhotoImage(file="C:/Project UAS TERBARU/Play.png")
        self.pause_image1 = ImageTk.PhotoImage(file="C:/Project UAS TERBARU/Button Pause.png")
        self.pause_image2 = ImageTk.PhotoImage(file="C:/Project UAS TERBARU/Pause.png")
        self.peringatancuaca = False
        self.running = True 
        self.current_playlist = []
        self.playlist=[]
        self.last_played_songs = []
        self.history = []
        self.all_songs = []
        self.location = []
        self.current_index = 0
        self.event_thread = threading.Thread(target=self.check_music_event)
        self.event_thread.daemon = True
        self.event_thread.start()
        
        self.window = window 
        window.title("MelodyMist")
        window.configure(bg="white")
        window.state("zoomed")
        self.ukw = self.window.winfo_screenwidth
        self.ukh = self.window.winfo_screenheight
        self.mainframe=Frame(self.window,bg="#132a46")
        self.mainframe.place(x=0, y= 0)
        self.imgawal = Image.open("C:/Project UAS TERBARU/Halaman Utama.png")
        self.resize = self.imgawal.resize((self.window.winfo_screenwidth(), self.window.winfo_screenheight()), Image.LANCZOS)
        self.halaman_awal = ImageTk.PhotoImage(self.resize)
        self.label_main_page = Label(self.window, image=self.halaman_awal)
        self.label_main_page.place(x=0, y=0, relwidth=1, relheight=1)
        window.iconbitmap("C:/Project UAS TERBARU/Icon.ico")

        self.imgyes = ImageTk.PhotoImage(Image.open("C:/Project UAS TERBARU/Yes.png"))
        self.buttonyes = Button(self.label_main_page,image=self.imgyes, command=self.login, bg="white", border=0, activebackground="white")
        self.buttonyes.place(relwidth=0.075, relheight=0.15, relx = 0.645, rely=0.755)

        self.imgno = ImageTk.PhotoImage(Image.open("C:/Project UAS TERBARU/No.png"))
        self.buttonno = Button(self.label_main_page,image=self.imgno, command=self.register, bg="white", border=0, activebackground="white")
        self.buttonno.place(relwidth=0.075, relheight=0.15, relx = 0.78, rely=0.755)


    def register(self):
        def cek():
            def cek2():
                a = self.registeremail.get()
                akun_loginpassword = data_akun_text.split('\n')
                for akun in akun_loginpassword:
                        if akun == '':
                            continue
                        ap = akun.split(',')
                        if ap[0] == a:
                            showinfo(title="Info", message="Email is used")
                            return False
                return True

            global a
            a = self.registeremail.get()
            x = self.registerpass.get()
            if a != "" and a != "Email (..@gmail.com)" and x != "Make Password":
                if a[-1:-11:-1][::-1] != '@gmail.com' and len(x)<6:
                    showinfo(title="Info", message="Wrong Email Or Password")
                    return False
                else : 
                    c = cek2()   
            else: 
                showinfo(title="Info", message="Please insert your Email and Password")
                return False

            self.data_akun.write(f"{a},{x}\n")
            self.data_akun.close()
            self.label_main_page.destroy() 
            self.login()
    
        self.label_main_page.destroy()
        self.mainframe=Frame(self.window,bg="#132a46")
        self.mainframe.place(x=0, y= 0)
        self.main_page_first = Image.open("C:/Project UAS TERBARU/Halaman Register.png")
        self.resize = self.main_page_first.resize((self.window.winfo_screenwidth(), self.window.winfo_screenheight()), Image.LANCZOS)
        self.main_page_first_read = ImageTk.PhotoImage(self.resize)
        self.label_main_page = Label(self.window, image=self.main_page_first_read)
        self.label_main_page.place(x=0, y=0, relwidth=1, relheight=1)
        
        self.data_akun = open("C:/Project UAS TERBARU/data_akun.txt",'a+')
        self.data_akun_r = open("C:/Project UAS TERBARU/data_akun.txt", 'r')
        data_akun_text = self.data_akun_r.read()

        self.registeremail = StringVar()
        self.entry1 = Entry(self.label_main_page, border=0, text=self.registeremail, bg="white", fg="grey", font=("Poppins",25, 'bold'), justify=LEFT)
        self.entry1.place(relwidth=0.365, relheight=0.125, relx=0.315, rely=0.2975)
        self.entry1.insert(0, "Email (..@gmail.com)")
        self.entry1.bind("<FocusIn>", lambda e: self.entry1.delete(0,"end"))

        self.registerpass = StringVar()
        self.entry2 = Entry(self.label_main_page, border=0, text=self.registerpass, bg="white", fg="grey", font=("Poppins",25, 'bold'), justify=LEFT)
        self.entry2.place(relwidth=0.365, relheight=0.125, relx=0.315, rely=0.4975)
        self.entry2.insert(0, "Make Password")
        self.entry2.bind("<FocusIn>", lambda e: self.entry2.delete(0,"end"))

        self.registerbutton = Button(self.label_main_page, text="REGISTER",bg="#dadad9", border=0, fg="#545454", command=cek, font=("Poppins",25, 'bold'), activebackground="#dadad9").place(relwidth=0.4, relheight=0.125, relx=0.3, rely=0.7)
        self.imgb = ImageTk.PhotoImage(Image.open("C:/Project UAS TERBARU/Arrow Left.png"))
        Button(self.label_main_page, image=self.imgb, command=self.backtologin, bg="#38b6ff", border=0, fg="white", font=("Poppins",20, 'bold'), activebackground="#38b6ff").place(relwidth=0.05, relheight=0.067, relx=0.035, rely=0.05)


    def backtologin(self):
         self.label_main_page.destroy()
         self.login()


    def login(self):
        def masuk():
            def checkin(email, password):
                def getweather():
                    self.cuacakota = {'Clear': 'Cerah','Clouds': 'Berawan','Rain': 'Hujan','Drizzle': 'Gerimis','Thunderstorm': 'Badai Petir',
                                        'Snow': 'Salju','Mist': 'Kabut','Smoke': 'Asap','Haze': 'Kabut','Fog': 'Kabut','Ash': 'Abu','Squall': 'Angin Kencang'}
                    nama_kota = self.entry5.get()
                    geolocator = Nominatim(user_agent="geoapiExercises")
                    location = geolocator.geocode(nama_kota)
                    if location:
                        obj = TimezoneFinder()
                        result = obj.timezone_at(lng=location.longitude, lat=location.latitude)
                        
                        now = datetime.now()
                        hari = now.strftime("%A")
                        tanggal = now.day
                        bulan = now.strftime("%B")
                        tahun = now.year
                        self.tanggal = f"{hari}, {tanggal} {bulan} {tahun}"

                        home = pytz.timezone(result)
                        local_time = datetime.now(home)
                        current_time = local_time.strftime("%I:%M %p")
                        self.waktu = current_time

                        api_key = "f8edab22d9f7156f121d820aa31e94bf"
                        api = f"https://api.openweathermap.org/data/2.5/weather?q={nama_kota}&appid={api_key}"
                        json_data = requests.get(api).json()
                        if 'weather' in json_data and 'main' in json_data:
                            cuaca = json_data['weather'][0]['main']
                            if cuaca in self.cuacakota:
                                cuaca = self.cuacakota[cuaca]
                            temp = int(json_data['main']['temp'] - 273.15)
                            temp_bulat = round(temp)
                            self.temp = f"{temp_bulat}°C"
                            global cc
                            cc = cuaca
                            self.set_lokasi()
                            self.home()
                        else:
                            showinfo(title="Info", message="Kota tidak ditemukan. Silakan coba lagi")
                            return False
                    else:
                        showinfo(title="Info", message="Kota tidak ditemukan. Silakan coba lagi")

                data_akun = open("C:/Project UAS TERBARU/data_akun.txt", 'r').read().split('\n')
                a = 0
                if email != "" and email != "Email" and password != "" and password != "Password":
                    for akun in data_akun:
                        if akun == '':
                            continue
                        acloginpassword = akun.split(',')
                        ac = acloginpassword[0]
                        loginpasswordd = acloginpassword[1]
                        if (email == ac and password == loginpasswordd):
                            a += 1
                            b = getweather()
                            break
                        else:
                            pass
                    if a == 0:
                        showinfo(title="Info", message="Wrong Username Or Password")
                        return False
                else:
                    showinfo(title="Info", message="Please insert your Email and Password")

            self.masuk = masuk
            email = self.entry3.get()
            password = self.entry4.get()
            checkin(email, password)
        
        self.label_main_page.destroy()
        self.music_playing = False
        self.songs_loaded = False
        self.mainframe = Frame(self.window, bg="#132a46")
        self.mainframe.place(x=0, y=0)
        self.main_page_first = Image.open("C:/Project UAS TERBARU/Halaman Login.png")
        self.resize = self.main_page_first.resize((self.window.winfo_screenwidth(), self.window.winfo_screenheight()), Image.LANCZOS)
        self.main_page_first_read = ImageTk.PhotoImage(self.resize)
        self.label_main_page = Label(self.window, image=self.main_page_first_read)
        self.label_main_page.place(x=0, y=0, relwidth=1, relheight=1)

        self.loginemail = StringVar()
        self.entry3 = Entry(self.label_main_page, justify=LEFT, text=self.loginemail, border=0, bg="white", font=("Poppins", 25, 'bold'), fg="grey")        
        self.entry3.place(relwidth=0.365, relheight=0.125, relx=0.315, rely=0.2)
        self.entry3.insert(0, "Email")
        self.entry3.bind("<FocusIn>", lambda e: self.entry3.delete(0, "end"))

        self.loginpassword = StringVar()
        self.entry4 = Entry(self.label_main_page, justify=LEFT, text=self.loginpassword, border=0, bg="white", font=("Poppins", 25, 'bold'), fg="grey")
        self.entry4.place(relwidth=0.33, relheight=0.125, relx=0.315, rely=0.4)
        self.entry4.insert(0, "Password")
        self.entry4.bind("<FocusIn>", lambda e: self.entry4.delete(0, "end"))

        self.lokasi = StringVar()
        self.entry5 = Entry(self.label_main_page, justify=LEFT, text=self.lokasi, border=0, bg="white", font=("Poppins", 25, 'bold'), fg="grey")
        self.entry5.place(relwidth=0.365, relheight=0.125, relx=0.315, rely=0.59)
        self.entry5.insert(0, "Lokasi")
        self.entry5.bind("<FocusIn>", lambda e: self.entry5.delete(0, "end"))

        self.loginbutton = Button(self.label_main_page, text="LOGIN", bg="#dadad9", border=0, fg="#545454", command=masuk, font=("Poppins", 25, 'bold'), activebackground="#dadad9").place(relwidth=0.4, relheight=0.125, relx=0.3, rely=0.785)

        self.registerbutton = Button(self.label_main_page, text="Make new account", command=self.register, border=0, bg="white", fg="black", font=("Poppins", 15), activebackground="white")
        self.registerbutton.place(relwidth=0.17, relheight=0.07, relx=0.79, rely=0.895)

        def button_show():
            if self.entry4['show'] == '*':
                self.entry4['show'] = ''
                toggle_btn.config(image=self.imgshow)
            else:
                self.entry4['show'] = '*'
                toggle_btn.config(image=self.imghide)

        self.imgshow = ImageTk.PhotoImage(Image.open("C:/Project UAS TERBARU/show.png"))
        self.imghide = ImageTk.PhotoImage(Image.open("C:/Project UAS TERBARU/hide.png"))
        toggle_btn = Button(self.label_main_page, command=button_show, bg="white", border=0, fg="black", font=("Poppins", 22, 'bold'), activebackground="white")
        toggle_btn.config(image=self.imghide)
        toggle_btn.place(relwidth=0.07, relheight=0.08, relx=0.63, rely=0.425)

    
    def set_lokasi(self):
        input_cuaca = self.entry5.get().capitalize()
        self.location.append(input_cuaca)
        lokasi = self.location[0]
        self.lokasinow = lokasi


    def home(self):
        self.mainframe.destroy()
        self.mainframe = Frame(self.window, bg="#132a46")
        self.mainframe.place(relheight=1, relwidth=1)
        self.main_page_first = Image.open("C:/Project UAS TERBARU/Halaman.png")
        self.resize = self.main_page_first.resize((self.window.winfo_screenwidth(), self.window.winfo_screenheight()), Image.LANCZOS)
        self.main_page_first_read = ImageTk.PhotoImage(self.resize)
        self.label_main_page = Label(self.mainframe, image=self.main_page_first_read)
        self.label_main_page.place(x=0, y=0, relwidth=1, relheight=1)

        self.frame_button = Frame(self.label_main_page, bg="#132a46")
        self.frame_button.place(relwidth=0.11, relheight=0.45, relx=0.018, rely=0.04)
        self.frame_playmusic = Frame(self.label_main_page, bg="white")
        self.frame_playmusic.place(relwidth=0.09, relheight=0.425, relx=0.0295, rely=0.505)
        self.frame = Frame(self.label_main_page, bg="#2f5389")
        self.frame.place(relwidth=0.88, relheight=0.985, relx=0.138, rely=0.01)

        # Frame
        self.imglabelhalaman = ImageTk.PhotoImage(file="C:\Project UAS TERBARU\Label Halaman.png")
        self.labelhalaman = Label(self.frame, image=self.imglabelhalaman, bg="#2f5389")
        self.labelhalaman.place(relwidth=0.975, relheight=1, relx=0, rely=0)

        self.label_isi =  Label(self.frame, bg="#132a46")
        self.label_isi.place(relwidth=0.95, relheight=0.955, relx=0.011, rely=0.02)

        # Label_isi
        self.username = Label(self.label_isi, text=f"Hello, {self.entry3.get()[:-10].capitalize()}!", bg="#132a46", fg="white", font=("Poppins", 40, 'bold'), anchor='w')
        self.username.place(relwidth=0.4, relheight=0.12, relx=0.029, rely=0.035)

        self.imgnamaapp = ImageTk.PhotoImage(file="C:\Project UAS TERBARU\MelodyMist.png")
        self.melodymist = Label(self.label_isi, image=self.imgnamaapp, bg="#132a46")
        self.melodymist.place(relwidth=0.3, relheight=0.15, relx=0.6975, rely=0.015)
        
        self.imglabelcuaca = ImageTk.PhotoImage(file="C:\Project UAS TERBARU\Label Cuaca.png")
        self.labelcuaca = Label(self.label_isi, image=self.imglabelcuaca, bg="#132a46")
        self.labelcuaca.place(relwidth=0.75, relheight=0.35, relx=0.009, rely=0.14)

        self.frame_cuaca = Frame(self.label_isi, bg="#fcffe0")
        self.frame_cuaca.place(relwidth=0.68, relheight=0.25, relx=0.033, rely=0.185)

        self.frame_gambarcuaca = Frame(self.label_isi, bg="#132a46")
        self.frame_gambarcuaca.place(relwidth=0.2, relheight=0.28, relx=0.8, rely=0.175)
        self.show_image()

        self.frame_weatherplaylist = Frame(self.label_isi, bg="#132a46")
        self.frame_weatherplaylist.place(relwidth=0.5, relheight=0.51, relx=0.01, rely=0.4825)
        self.frame_playlistforyou = Frame(self.label_isi, bg="#132a46")
        self.frame_playlistforyou.place(relwidth=0.5, relheight=0.51, relx=0.5, rely=0.4825)

        # Frame_button
        self.imghome = ImageTk.PhotoImage(file="C:/Project UAS TERBARU/Button Home.png")
        self.button_home = Button(self.frame_button, image=self.imghome, bg="#132a46", border=0, command=self.home, activebackground="#132a46")
        self.button_home.place(relwidth=0.7, relheight=0.3, relx=0.15, rely=0.02)
        self.imgsearch = ImageTk.PhotoImage(file="C:/Project UAS TERBARU/Button Search.png")
        self.button_search = Button(self.frame_button, image=self.imgsearch, bg="#132a46", border=0, command=self.search, activebackground="#132a46")
        self.button_search.place(relwidth=0.7, relheight=0.3, relx=0.15, rely=0.32)
        self.imgprofil = ImageTk.PhotoImage(file="C:/Project UAS TERBARU/Button Profil.png")
        self.button_profil = Button(self.frame_button, image=self.imgprofil, bg="#132a46", border=0, command=self.profil, activebackground="#132a46")
        self.button_profil.place(relwidth=0.7, relheight=0.3, relx=0.15, rely=0.62)

        # Frame_cuaca
        self.lokasi = Label(self.frame_cuaca, text=f"{self.lokasinow}", bg="#fcffe0", fg="black", font=("Poppins", 50), anchor="w")
        self.lokasi.place(relwidth=0.5, relheight=0.52, relx=0.02, rely=0)
        self.texttanggal = Label(self.frame_cuaca, text=self.tanggal, bg="#fcffe0", fg="black", font=("Open Sans", 15), anchor="w")
        self.texttanggal.place(relwidth=0.5, relheight=0.2, relx=0.03, rely=0.58)
        self.textwaktu = Label(self.frame_cuaca, text=self.waktu, bg="#fcffe0", fg="black", font=("Open Sans", 15), anchor="w")
        self.textwaktu.place(relwidth=0.15, relheight=0.2, relx=0.03, rely=0.78)
        self.texttemp = Label(self.frame_cuaca, text=self.temp, bg="#fcffe0", fg="black", font=("Open Sans", 80, "bold"), anchor="w")
        self.texttemp.place(relwidth=0.4, relheight=0.6, relx=0.525, rely=0.2)
        self.textcuaca = Label(self.frame_cuaca, text=cc, bg="#fcffe0", fg="black", font=("Open Sans", 15), anchor="w")
        self.textcuaca.place(relwidth=0.15, relheight=0.25, relx=0.85, rely=0.6)

        # Frame_weatherplaylist
        self.imgweatherplaylist = ImageTk.PhotoImage(file="C:/Project UAS TERBARU/Button WeatherPlaylist.png")
        self.button_weatherplaylist = Button(self.frame_weatherplaylist, image=self.imgweatherplaylist, bg="#132a46", border=0, command=self.weatherplaylist, activebackground="#132a46")
        self.button_weatherplaylist.place(relwidth=1, relheight=0.8, relx=0, rely=0)
        self.textweatherplaylist = Button(self.frame_weatherplaylist, text="#WeatherPlaylist", bg="#132a46", border=0, fg="white", command=self.weatherplaylist, font=("Poppins", 25, 'bold'), activebackground="#132a46")
        self.textweatherplaylist.place(relwidth=0.6, relheight=0.125, relx=0.225, rely=0.81)

        # Frame_genremusik
        self.imgplaylistforyou = ImageTk.PhotoImage(file="C:/Project UAS TERBARU/Button Playlistforyou.png")
        self.button_playlistforyou = Button(self.frame_playlistforyou, image=self.imgplaylistforyou, bg="#132a46", border=0, command=self.playlistforyou, activebackground="#132a46")
        self.button_playlistforyou.place(relwidth=1, relheight=0.8, relx=0., rely=0)
        self.textplaylistforyou = Button(self.frame_playlistforyou, text="#Playlistforyou", bg="#132a46", border=0, fg="white", command=self.playlistforyou, font=("Poppins", 25, 'bold'), activebackground="#132a46")
        self.textplaylistforyou.place(relwidth=0.6, relheight=0.125, relx=0.225, rely=0.81)

        self.update_frame_playmusic()

        # Peringatan Cuaca
        if not self.peringatancuaca:
            weather_condition = cc
            if weather_condition in ['Berawan', 'Gerimis']:
                showinfo(title="Peringatan Cuaca", message=f"Cuaca buruk terdeteksi: {weather_condition}.\nHarap sedia payung sebelum Hujan!")
            elif weather_condition == 'Hujan':
                showinfo(title="Peringatan Cuaca", message=f"Cuaca buruk terdeteksi: {weather_condition}.\nLagi Hujan nih, jangan lupa pakai jas hujan atau payung!")
            elif weather_condition in ['Badai Petir', 'Angin Kencang']:
                showinfo(title="Peringatan Cuaca", message=f"Cuaca buruk terdeteksi: {weather_condition}.\nHati-hati cuaca ekstrim!")
            elif weather_condition in ['Kabut', 'Asap', 'Abu']:
                showinfo(title="Peringatan Cuaca", message=f"Cuaca buruk terdeteksi: {weather_condition}.\nHati-hati jalan berkabut!")
            elif weather_condition == 'Salju':
                showinfo(title="Peringatan Cuaca", message=f"Cuaca terdeteksi: {weather_condition}.\nNikmati salju, tetapi hati-hati jalan licin!")
            self.peringatancuaca = True


    def get_weather_image(self):
        image_path = ""

        if cc in ['Hujan', 'Gerimis', 'Angin Kencang']:
            image_path = "C:/Project UAS TERBARU/Cuaca Hujan.png"
        elif cc == 'Cerah':
            image_path = "C:/Project UAS TERBARU/Cuaca Cerah.png"
        elif cc == 'Berawan':
            image_path = "C:/Project UAS TERBARU/Cuaca Berawan.png"
        elif cc == 'Salju':
            image_path = "C:/Project UAS TERBARU/Cuaca Snow.png"
        elif cc in ['Asap', 'Kabut', 'Abu']:
            image_path = "C:/Project UAS TERBARU/Cuaca Berkabut.png"
        elif cc == 'Badai Petir':
            image_path = "C:/Project UAS TERBARU/Cuaca Petir.png"
        else:
            image_path = "C:/Project UAS TERBARU/Cuaca Lain.png"

        weather_image = Image.open(image_path)
        weather_photo = ImageTk.PhotoImage(weather_image)

        return weather_photo
        

    def show_image(self):
        self.frame_gambarcuaca.destroy()
        self.frame_imgcuaca = Frame(self.label_isi, bg="#132a46")
        self.frame_imgcuaca.place(relwidth=0.263, relheight=0.28, relx=0.745, rely=0.165)
        
        weather_image = self.get_weather_image()
        label_weather = Label(self.frame_imgcuaca, image=weather_image, bg="#132a46")
        label_weather.place(relwidth=1, relheight=1, relx=0, rely=0)
        label_weather.image = weather_image
        label_weather.pack()


    def profil(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

        self.imglabelhalaman = ImageTk.PhotoImage(file="C:\Project UAS TERBARU\Label Halaman.png")
        self.labelhalaman = Label(self.frame, image=self.imglabelhalaman, bg="#2f5389")
        self.labelhalaman.place(relwidth=0.975, relheight=1, relx=0, rely=0)

        self.label_isi =  Label(self.frame, bg="#132a46")
        self.label_isi.place(relwidth=0.95, relheight=0.955, relx=0.011, rely=0.02)

        # Label_isi
        self.imgtemplateprofil = ImageTk.PhotoImage(file="C:\Project UAS TERBARU\Profil.png")
        self.labelprofil = Label(self.label_isi, image=self.imgtemplateprofil, bg="#132a46")
        self.labelprofil.place(relwidth=1, relheight=1, relx=0, rely=0)

        self.username = Label(self.label_isi, text=f"Hello\n{self.entry3.get()[:-10].capitalize()}!", bg="white", fg="black", font=("Poppins", 37, 'bold'))
        self.username.place(relwidth=0.225, relheight=0.223, relx=0.635, rely=0.22)
        self.datausername = Label(self.label_isi, text=f"{self.entry3.get()[:-10].capitalize()}", bg="white", fg="grey", font=("Open Sans", 22),anchor="w")
        self.datausername.place(relwidth=0.23, relheight=0.1, relx=0.26, rely=0.21)
        self.dataemail = Label(self.label_isi, text=f"{self.entry3.get()}", bg="white", fg="grey", font=("Open Sans", 22),anchor="w")
        self.dataemail.place(relwidth=0.23, relheight=0.1, relx=0.26, rely=0.36)
        self.datapassword = Label(self.label_isi, text=f"{self.entry4.get()}", bg="white", fg="grey", font=("Open Sans", 22),anchor="w")
        self.datapassword.place(relwidth=0.23, relheight=0.1, relx=0.26, rely=0.51)
        self.entry_lokasi = self.entry5.get()
        self.datalokasi = Label(self.label_isi, text=f"{self.lokasinow}", bg="white", fg="grey", font=("Open Sans", 22),anchor="w")
        self.datalokasi.place(relwidth=0.23, relheight=0.1, relx=0.26, rely=0.66)

        self.logout = Button(self.label_isi, text="Logout",bg="#a6a6a6", border=0, fg="white", command=self.exit, font=("Poppins",25, 'bold'), activebackground="#a6a6a6")
        self.logout.place(relwidth=0.3, relheight=0.1, relx=0.165, rely=0.835)


    def weatherplaylist(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

        self.imglabelhalaman = ImageTk.PhotoImage(file="C:/Project UAS TERBARU/Label Halaman.png")
        self.labelhalaman = Label(self.frame, image=self.imglabelhalaman, bg="#2f5389")
        self.labelhalaman.place(relwidth=0.975, relheight=1, relx=0, rely=0)

        self.label_isi = Label(self.frame, bg="#132a46")
        self.label_isi.place(relwidth=0.95, relheight=0.955, relx=0.011, rely=0.02)

        cuaca = cc
        if cuaca in ['Hujan', 'Gerimis', 'Angin Kencang', 'Kabut', 'Asap', 'Berawan', 'Abu', 'Badai Petir', 'Angin Kencang']:
            image_path = "C:/Project UAS TERBARU/WeatherPlaylist Galau.png"
            jenis_playlist = "galau"
        else:
            image_path = "C:/Project UAS TERBARU/WeatherPlaylist Ceria.png"
            jenis_playlist = "ceria"

        img_weather = Image.open(image_path)
        self.imgweather = ImageTk.PhotoImage(img_weather)
        self.label_weather = Label(self.label_isi, image=self.imgweather, bg="#132a46")
        self.label_weather.place(relwidth=1, relheight=0.2, relx=0, rely=0)

        self.frame_daftarmusic = Frame(self.label_isi, bg="#132a46")
        self.frame_daftarmusic.place(relwidth=1, relheight=0.8, relx=0.001, rely=0.21)

        self.load_cover("C:/Project UAS TERBARU/path_lagu - Copy.txt", jenis_playlist)


    def load_cover(self, filename, jenis_playlist):
        if not self.songs_loaded:
            self.selected_songs = {"galau": [], "ceria": []}
            with open(filename, 'r', encoding='utf-8') as file:
                lines = file.readlines()[1:]
                songs = [line.strip().split(',') for line in lines]
                for song in songs:
                    if song[3] == "galau":
                        self.selected_songs["galau"].append(song)
                    elif song[3] == "ceria":
                        self.selected_songs["ceria"].append(song)
            self.songs_loaded = True
            self.now_playlist = random.sample(self.selected_songs[jenis_playlist], 10)
        self.current_playlist = self.now_playlist
        self.playlist_music()

        for i, data in enumerate(self.current_playlist):
            cover_image = Image.open(data[2])
            ukuran_baru = (200, 200)
            resized_image = cover_image.resize(ukuran_baru, Image.BILINEAR)
            imgcover = ImageTk.PhotoImage(resized_image)
            button_cover = Button(self.frame_daftarmusic, image=imgcover, bg="#132a46", border=0, command=lambda idx=i: self.load_lagu(idx), activebackground="#132a46")
            button_cover.image = imgcover
            button_cover.place(relwidth=0.2, relheight=0.4, relx=(i % 5) * 0.2, rely=(i // 5) * 0.5)

            judul = Button(self.frame_daftarmusic, text=data[1], bg="#132a46", fg="white", font=("Poppins", 8, 'bold'), border=0, command=lambda idx=i: self.load_lagu(idx), activebackground="#132a46")
            judul.place(relwidth=0.2, relheight=0.05, relx=(i % 5) * 0.2, rely=(i // 5) * 0.5 + 0.4)

            artis = Button(self.frame_daftarmusic, text=data[0], bg="#132a46", fg="white", font=("Poppins", 8), border=0, command=lambda idx=i: self.load_lagu(idx), activebackground="#132a46")
            artis.place(relwidth=0.2, relheight=0.05, relx=(i % 5) * 0.2, rely=(i // 5) * 0.5 + 0.438)


    def load_lagu(self, index):
        data = self.current_playlist[index]
        artis = data[0]
        judul = data[1]
        song_path = data[2]
        self.current_index = index

        lagu_title = os.path.basename(song_path).split(".")[0]
        selected_lagu= os.path.join("C:/Project UAS TERBARU/Lagu", lagu_title + ".mp3")
        selected_song = selected_lagu
        
        if os.path.exists(selected_song):
            self.play_music(selected_song)


    def halamanplaymusic(self, selected_song):
        for widget in self.frame.winfo_children():
            widget.destroy()

        self.imglabelhalaman = ImageTk.PhotoImage(file="C:\Project UAS TERBARU\Label Halaman.png")
        self.labelhalaman = Label(self.frame, image=self.imglabelhalaman, bg="#2f5389")
        self.labelhalaman.place(relwidth=0.975, relheight=1, relx=0, rely=0)

        self.label_isi =  Label(self.frame, bg="#132a46")
        self.label_isi.place(relwidth=0.95, relheight=0.955, relx=0.011, rely=0.02)

        self.frame_updatemusic = Frame(self.label_isi, bg="#132a46")
        self.frame_updatemusic.place(relwidth=1, relheight=1, relx=0, rely=0)

        self.selected_song = selected_song
        self.update_frame_playmusic()
        
        # Frame_playmusic
        if self.music_playing and self.running:
            nama_lagu = os.path.splitext(os.path.basename(selected_song))[0]
            nama_lagu_png = nama_lagu + ".png"
            cover_lagu = os.path.join("C:/Project UAS TERBARU/Gambar Lagu/", nama_lagu_png)
            ukuran_baru = (100, 100)
            
            if os.path.exists(cover_lagu):
                imgcover_lagu = Image.open(cover_lagu)
                resized_image = imgcover_lagu.resize(ukuran_baru, Image.BILINEAR)
                imgcover = ImageTk.PhotoImage(resized_image)
                self.lagu = Button(self.frame_playmusic, command=lambda: self.halamanplaymusic(selected_song), image=imgcover, bg="white", border=0)
                self.lagu.image = imgcover
                self.lagu.place(relwidth=1, relheight=0.4, relx=0, rely=0.03)

                penyanyi_lagu = nama_lagu.split(' - ')[0].strip()
                self.textartis = Label(self.frame_playmusic, text=penyanyi_lagu, bg="white", border=0, fg="black", font=("Poppins", 7), anchor="center")
                self.textartis.place(relwidth=1, relheight=0.1, relx=0, rely=0.5)

                judul_lagu = nama_lagu.split(' - ')[1].strip()
                self.textjudul = Label(self.frame_playmusic, text=judul_lagu, bg="white", border=0, fg="black", font=("Poppins", 8, "bold"), anchor="center")
                self.textjudul.place(relwidth=1, relheight=0.1, relx=0, rely=0.43)

                self.togglebutton1 = Button(self.frame_playmusic, command=self.toggle_play_pause2, bg="white", border=0, fg="black", font=("Poppins", 22, 'bold'), activebackground="white")
                self.togglebutton1.config(image=self.play_image1 if self.music_playing else self.pause_image1)
                self.togglebutton1.place(relwidth=0.62, relheight=0.3, relx=0.2, rely=0.6)
            else:
                self.textmusic = Label(self.frame_playmusic, text="No Song\nPlay", border=0, fg="grey", font=("Poppins", 10), bg="white")
                self.textmusic.place(relwidth=0.5, relheight=0.15, relx=0.235, rely=0.45)
        else:
            self.textmusic = Label(self.frame_playmusic, text="No Song\nPlay", border=0, fg="grey", font=("Poppins", 10), bg="white")
            self.textmusic.place(relwidth=0.5, relheight=0.15, relx=0.235, rely=0.45)

        # Frame_updatemusic
        if self.music_playing and self.running:
            nama_file = os.path.splitext(os.path.basename(selected_song))[0]
            nama_file_png = nama_file + ".png"
            path_cover_lagu = os.path.join("C:/Project UAS TERBARU/Gambar Lagu/", nama_file_png)
            if os.path.exists(path_cover_lagu):
                cover_lagu = Image.open(path_cover_lagu)
                imgcover = ImageTk.PhotoImage(cover_lagu)
                self.lagu = Label(self.frame_updatemusic, image=imgcover, bg="#132a46", border=0)
                self.lagu.image = imgcover
                self.lagu.place(relwidth=0.48, relheight=0.8, relx=0.03, rely=0.1)

            judul_lagu = nama_file.split(' - ')[1].strip()
            penyanyi_lagu = nama_file.split(' - ')[0].strip()
            if len(judul_lagu) >= 21 and len(judul_lagu) <= 35 :
                self.textjudul = Text(self.frame_updatemusic, bg="#132a46", border=0, fg="white", font=("Poppins", 30, "bold"), wrap="word", height=2)
                self.textjudul.insert("1.0", judul_lagu)
                self.textjudul.config(state="disabled")
                self.textjudul.place(relwidth=0.4, relheight=0.2, relx=0.565, rely=0.1)

                self.textartis = Label(self.frame_updatemusic, text=penyanyi_lagu, bg="#132a46", border=0, fg="white", font=("Poppins", 20), anchor="w")
                self.textartis.place(relwidth=0.4, relheight=0.05, relx=0.57, rely=0.265)
            elif len(judul_lagu) >= 30 :
                self.textjudul = Text(self.frame_updatemusic, bg="#132a46", border=0, fg="white", font=("Poppins", 30, "bold"), wrap="word", height=2)
                self.textjudul.insert("1.0", judul_lagu)
                self.textjudul.config(state="disabled")
                self.textjudul.place(relwidth=0.4, relheight=0.25, relx=0.565, rely=0.1)

                self.textartis = Label(self.frame_updatemusic, text=penyanyi_lagu, bg="#132a46", border=0, fg="white", font=("Poppins", 20), anchor="w")
                self.textartis.place(relwidth=0.4, relheight=0.05, relx=0.57, rely=0.335)
            elif len(penyanyi_lagu) >= 30 :
                self.textjudul = Label(self.frame_updatemusic, text=judul_lagu, bg="#132a46", border=0, fg="white", font=("Poppins", 30, "bold"), anchor="w")
                self.textjudul.place(relwidth=0.4, relheight=0.1, relx=0.57, rely=0.1)

                self.textartis = Text(self.frame_updatemusic, bg="#132a46", border=0, fg="white", font=("Poppins", 20), wrap="word", height=1)
                self.textartis.insert("1.0", penyanyi_lagu)
                self.textartis.config(state="disabled")
                self.textartis.place(relwidth=0.4, relheight=0.2, relx=0.57, rely=0.2)
            else :
                self.textjudul = Label(self.frame_updatemusic, text=judul_lagu, bg="#132a46", border=0, fg="white", font=("Poppins", 30, "bold"), anchor="w")
                self.textjudul.place(relwidth=0.4, relheight=0.1, relx=0.57, rely=0.1)
                
                self.textartis = Label(self.frame_updatemusic, text=penyanyi_lagu, bg="#132a46", border=0, fg="white", font=("Poppins", 20), anchor="w")
                self.textartis.place(relwidth=0.4, relheight=0.05, relx=0.57, rely=0.2)

            self.imgprevious = PhotoImage(file="C:/Project UAS TERBARU/Previous.png")
            self.button_previous = Button(self.frame_updatemusic, image=self.imgprevious, bg="#132a46", border=0, command=self.previous_music, activebackground="#132a46")
            self.button_previous.place(relwidth=0.1, relheight=0.12, relx=0.57, rely=0.75)

            self.togglebutton2 = Button(self.frame_updatemusic, command=self.toggle_play_pause2, image=self.play_image2, bg="#132a46", border=0, activebackground="#132a46")
            self.togglebutton2.config(image=self.play_image2 if self.music_playing else self.pause_image2)
            self.togglebutton2.place(relwidth=0.15, relheight=0.2, relx=0.7, rely=0.7)

            self.imgnext = PhotoImage(file="C:/Project UAS TERBARU/Next.png")
            self.button_next = Button(self.frame_updatemusic, image=self.imgnext, bg="#132a46", border=0, command=self.next_music, activebackground="#132a46")
            self.button_next.place(relwidth=0.1, relheight=0.12, relx=0.87, rely=0.75)
        else:
            showinfo(title="Info", message="Tidak ada lagu yang bisa diputar")


    def playlist_music(self):
        self.playlist = [os.path.join("C:/Project UAS TERBARU/Lagu", os.path.basename(data[2]).split(".")[0] + ".mp3") for data in self.current_playlist]
        return self.playlist


    def play_music(self, selected_song):
        if selected_song not in self.last_played_songs:
            self.last_played_songs.append(selected_song)
            if len(self.last_played_songs) > 10:
                self.last_played_songs.pop(0)
        self.play_mode = None
        pygame.mixer.music.load(selected_song)
        pygame.mixer.music.play()
        self.music_playing = True
        self.running = True
        pygame.mixer.music.set_endevent(pygame.USEREVENT)
        pygame.event.set_allowed(pygame.USEREVENT)
        print(f"Playing: {selected_song}")
        self.halamanplaymusic(selected_song)
        self.save_to_history(selected_song) 


    def next_music(self):
        self.current_index = (self.current_index + 1) % len(self.current_playlist)
        next_song = self.playlist[self.current_index]
        self.play_music(next_song)


    def previous_music(self):
        self.current_index = (self.current_index - 1) % len(self.current_playlist)
        prev_song = self.playlist[self.current_index]
        self.play_music(prev_song)

    def load_all_songs(self):
        self.all_songs = []
        if len(self.history) >= 10:
            return self.history
        else:
            with open('C:/Project UAS TERBARU/path_lagu - Copy.txt', 'r', encoding='utf-8') as file:
                lines = file.readlines()[1:]
                for line in lines:
                    artis, judul, path_cover, jenis_playlist = line.strip().split(',')
                    base_name = os.path.splitext(os.path.basename(path_cover))[0]
                    path_mp3 = f"C:/Project UAS TERBARU/Lagu/{base_name}.mp3"
                    song_info = {
                        "artis": artis,
                        "judul": judul,
                        "path_cover": path_cover,
                        "path_mp3": path_mp3}
                    self.all_songs.append(song_info)
            return self.all_songs


    def recent_or_random_playlist(self):
        songs = self.load_all_songs()
        if len(self.history) < 10:
            remaining_count = 10 - len(self.history)
            random_songs = random.sample(songs, remaining_count)
            for song in random_songs:
                self.save_to_history(song["path_mp3"])

        self.current_playlist = self.history[:10]


    def save_to_history(self, selected_song):
        nama_lagu = os.path.splitext(os.path.basename(selected_song))[0]
        nama_lagu_png = nama_lagu + ".png"
        nama_lagu_mp3 = nama_lagu + ".mp3"
        nama_artis = nama_lagu.split(' - ')[0]
        judul_lagu = nama_lagu.split(' - ')[1]
        cover_lagu = os.path.join("C:/Project UAS TERBARU/Gambar Lagu/", nama_lagu_png)
        path_lagu = os.path.join("C:/Project UAS TERBARU/Lagu/", nama_lagu_mp3)
        
        song_info = {
            "artis": nama_artis,
            "judul": judul_lagu, 
            "path_cover": cover_lagu,
            "path_mp3": path_lagu}

        if song_info in self.history:
            self.history.remove(song_info)
        
        self.history.insert(0, song_info)
        
        if len(self.history) > 10:
            self.history = self.history[:10]


    def playlistforyou(self):
        self.recent_or_random_playlist()

        songs = self.current_playlist

        for widget in self.frame.winfo_children():
            widget.destroy()

        self.imglabelhalaman = ImageTk.PhotoImage(file="C:/Project UAS TERBARU/Label Halaman.png")
        self.labelhalaman = Label(self.frame, image=self.imglabelhalaman, bg="#2f5389")
        self.labelhalaman.place(relwidth=0.975, relheight=1, relx=0, rely=0)

        self.label_isi = Label(self.frame, bg="#132a46")
        self.label_isi.place(relwidth=0.95, relheight=0.955, relx=0.011, rely=0.02)

        self.imgplaylistforyou = ImageTk.PhotoImage(file="C:/Project UAS TERBARU/Playlistforyou.png")
        self.label_playlistforyou = Label(self.label_isi, image=self.imgplaylistforyou, bg="#132a46")
        self.label_playlistforyou.place(relwidth=1, relheight=0.2, relx=0.015, rely=0.01)

        self.frame_daftarmusic = Frame(self.label_isi, bg="#132a46")
        self.frame_daftarmusic.place(relwidth=1, relheight=0.8, relx=0.001, rely=0.21)

        for i, data in enumerate(songs):
            cover_image = Image.open(data["path_cover"])
            ukuran_baru = (200, 200)
            resized_image = cover_image.resize(ukuran_baru, Image.BILINEAR)
            imgcover = ImageTk.PhotoImage(resized_image)
            button_cover = Button(self.frame_daftarmusic, image=imgcover, bg="#132a46", border=0, command=lambda idx=i: self.load_lagu_recently(idx), activebackground="#132a46")
            button_cover.image = imgcover
            button_cover.place(relwidth=0.2, relheight=0.4, relx=(i % 5) * 0.2, rely=(i // 5) * 0.5)

            judul = Button(self.frame_daftarmusic, text=data["judul"], bg="#132a46", fg="white", font=("Poppins", 8, 'bold'), border=0, command=lambda idx=i: self.load_lagu_recently(idx), activebackground="#132a46")
            judul.place(relwidth=0.2, relheight=0.05, relx=(i % 5) * 0.2, rely=(i // 5) * 0.5 + 0.4)

            artis = Button(self.frame_daftarmusic, text=data["artis"], bg="#132a46", fg="white", font=("Poppins", 8), border=0, command=lambda idx=i: self.load_lagu_recently(idx), activebackground="#132a46")
            artis.place(relwidth=0.2, relheight=0.05, relx=(i % 5) * 0.2, rely=(i // 5) * 0.5 + 0.435)
            

    def load_lagu_recently(self, idx):
        selected_song = self.history[idx]["path_mp3"]
        self.play_music2(selected_song)


    def halamanplaymusic2(self, selected_song):
        for widget in self.frame.winfo_children():
            widget.destroy()
        
        # Frame
        self.imglabelhalaman = ImageTk.PhotoImage(file="C:\Project UAS TERBARU\Label Halaman.png")
        self.labelhalaman = Label(self.frame, image=self.imglabelhalaman, bg="#2f5389")
        self.labelhalaman.place(relwidth=0.975, relheight=1, relx=0, rely=0)

        self.label_isi =  Label(self.frame, bg="#132a46")
        self.label_isi.place(relwidth=0.95, relheight=0.955, relx=0.011, rely=0.02)

        self.frame_updatemusic = Frame(self.label_isi, bg="#132a46")
        self.frame_updatemusic.place(relwidth=1, relheight=1, relx=0, rely=0)

        self.selected_song = selected_song
        self.update_frame_playmusic()   
        
        # Frame_playmusic
        if self.music_playing and self.running:
            nama_lagu = os.path.splitext(os.path.basename(selected_song))[0]
            nama_lagu_png = nama_lagu + ".png"
            cover_lagu = os.path.join("C:/Project UAS TERBARU/Gambar Lagu/", nama_lagu_png)
            ukuran_baru = (100, 100)
            
            if os.path.exists(cover_lagu):
                imgcover_lagu = Image.open(cover_lagu)
                resized_image = imgcover_lagu.resize(ukuran_baru, Image.BILINEAR)
                imgcover = ImageTk.PhotoImage(resized_image)
                self.lagu = Button(self.frame_playmusic, command=lambda: self.halamanplaymusic_sort(selected_song), image=imgcover, bg="white", border=0)
                self.lagu.image = imgcover
                self.lagu.place(relwidth=1, relheight=0.4, relx=0, rely=0.03)

                penyanyi_lagu = nama_lagu.split(' - ')[0].strip()
                self.textartis = Label(self.frame_playmusic, text=penyanyi_lagu, bg="white", border=0, fg="black", font=("Poppins", 7), anchor="center")
                self.textartis.place(relwidth=1, relheight=0.1, relx=0, rely=0.5)

                judul_lagu = nama_lagu.split(' - ')[1].strip()
                self.textjudul = Label(self.frame_playmusic, text=judul_lagu, bg="white", border=0, fg="black", font=("Poppins", 8, "bold"), anchor="center")
                self.textjudul.place(relwidth=1, relheight=0.1, relx=0, rely=0.43)

                self.togglebutton1 = Button(self.frame_playmusic, command=self.toggle_play_pause2, bg="white", border=0, fg="black", font=("Poppins", 22, 'bold'), activebackground="white")
                self.togglebutton1.config(image=self.play_image1 if self.music_playing else self.pause_image1)
                self.togglebutton1.place(relwidth=0.62, relheight=0.3, relx=0.2, rely=0.6)

            else:
                self.textmusic = Label(self.frame_playmusic, text="No Song\nPlay", border=0, fg="grey", font=("Poppins", 10), bg="white")
                self.textmusic.place(relwidth=0.5, relheight=0.15, relx=0.235, rely=0.45)
        else:
            self.textmusic = Label(self.frame_playmusic, text="No Song\nPlay", border=0, fg="grey", font=("Poppins", 10), bg="white")
            self.textmusic.place(relwidth=0.5, relheight=0.15, relx=0.235, rely=0.45)

        # Frame_updatemusic
        if self.music_playing and self.running:
            nama_file = os.path.splitext(os.path.basename(selected_song))[0]
            nama_file_png = nama_file + ".png"
            path_cover_lagu = os.path.join("C:/Project UAS TERBARU/Gambar Lagu/", nama_file_png)
            if os.path.exists(path_cover_lagu):
                cover_lagu = Image.open(path_cover_lagu)
                imgcover = ImageTk.PhotoImage(cover_lagu)
                self.lagu = Label(self.frame_updatemusic, image=imgcover, bg="#132a46", border=0)
                self.lagu.image = imgcover
                self.lagu.place(relwidth=0.48, relheight=0.8, relx=0.03, rely=0.1)

            judul_lagu = nama_file.split(' - ')[1].strip()
            penyanyi_lagu = nama_file.split(' - ')[0].strip()
            if len(judul_lagu) >= 21 and len(judul_lagu) <= 35 :
                self.textjudul = Text(self.frame_updatemusic, bg="#132a46", border=0, fg="white", font=("Poppins", 30, "bold"), wrap="word", height=2)
                self.textjudul.insert("1.0", judul_lagu)
                self.textjudul.config(state="disabled")
                self.textjudul.place(relwidth=0.4, relheight=0.2, relx=0.565, rely=0.1)

                self.textartis = Label(self.frame_updatemusic, text=penyanyi_lagu, bg="#132a46", border=0, fg="white", font=("Poppins", 20), anchor="w")
                self.textartis.place(relwidth=0.4, relheight=0.05, relx=0.57, rely=0.265)
            elif len(judul_lagu) >= 30 :
                self.textjudul = Text(self.frame_updatemusic, bg="#132a46", border=0, fg="white", font=("Poppins", 30, "bold"), wrap="word", height=2)
                self.textjudul.insert("1.0", judul_lagu)
                self.textjudul.config(state="disabled")
                self.textjudul.place(relwidth=0.4, relheight=0.25, relx=0.565, rely=0.1)

                self.textartis = Label(self.frame_updatemusic, text=penyanyi_lagu, bg="#132a46", border=0, fg="white", font=("Poppins", 20), anchor="w")
                self.textartis.place(relwidth=0.4, relheight=0.05, relx=0.57, rely=0.335)
            elif len(penyanyi_lagu) >= 30 :
                self.textjudul = Label(self.frame_updatemusic, text=judul_lagu, bg="#132a46", border=0, fg="white", font=("Poppins", 30, "bold"), anchor="w")
                self.textjudul.place(relwidth=0.4, relheight=0.1, relx=0.57, rely=0.1)

                self.textartis = Text(self.frame_updatemusic, bg="#132a46", border=0, fg="white", font=("Poppins", 20), wrap="word", height=1)
                self.textartis.insert("1.0", penyanyi_lagu)
                self.textartis.config(state="disabled")
                self.textartis.place(relwidth=0.4, relheight=0.2, relx=0.57, rely=0.2)
            else :
                self.textjudul = Label(self.frame_updatemusic, text=judul_lagu, bg="#132a46", border=0, fg="white", font=("Poppins", 30, "bold"), anchor="w")
                self.textjudul.place(relwidth=0.4, relheight=0.1, relx=0.57, rely=0.1)
                
                self.textartis = Label(self.frame_updatemusic, text=penyanyi_lagu, bg="#132a46", border=0, fg="white", font=("Poppins", 20), anchor="w")
                self.textartis.place(relwidth=0.4, relheight=0.05, relx=0.57, rely=0.2)

            self.imgprevious = PhotoImage(file="C:/Project UAS TERBARU/Previous.png")
            self.button_previous = Button(self.frame_updatemusic, image=self.imgprevious, bg="#132a46", border=0, command=self.previous_music2, activebackground="#132a46")
            self.button_previous.place(relwidth=0.1, relheight=0.12, relx=0.57, rely=0.75)

            self.togglebutton2 = Button(self.frame_updatemusic, command=self.toggle_play_pause2, image=self.play_image2, bg="#132a46", border=0, activebackground="#132a46")
            self.togglebutton2.config(image=self.play_image2 if self.music_playing else self.pause_image2)
            self.togglebutton2.place(relwidth=0.15, relheight=0.2, relx=0.7, rely=0.7)

            self.imgnext = PhotoImage(file="C:/Project UAS TERBARU/Next.png")
            self.button_next = Button(self.frame_updatemusic, image=self.imgnext, bg="#132a46", border=0, command=self.next_music2, activebackground="#132a46")
            self.button_next.place(relwidth=0.1, relheight=0.12, relx=0.87, rely=0.75)
        else:
            showinfo(title="Info", message="Tidak ada lagu yang bisa diputar")
    

    def play_music2(self, selected_song):
        pygame.mixer.music.load(selected_song)
        pygame.mixer.music.play()
        self.music_playing = True
        self.running = True
        self.halamanplaymusic2(selected_song)
        self.save_to_history(selected_song)


    def next_music2(self):
        self.current_index += 1
        if self.current_index >= len(self.current_playlist):
            self.current_index = 0
        next_song = self.current_playlist[self.current_index]["path_mp3"]
        self.play_music2(next_song)


    def previous_music2(self):
        self.current_index -= 1
        if self.current_index < 0:
            self.current_index = len(self.current_playlist) - 1
        prev_song = self.current_playlist[self.current_index]["path_mp3"]
        self.play_music2(prev_song)


    def search(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

        self.imglabelhalaman = ImageTk.PhotoImage(file="C:/Project UAS TERBARU/Label Halaman.png")
        self.labelhalaman = Label(self.frame, image=self.imglabelhalaman, bg="#2f5389")
        self.labelhalaman.place(relwidth=0.975, relheight=1, relx=0, rely=0)

        self.label_isi = Label(self.frame, bg="#132a46")
        self.label_isi.place(relwidth=0.95, relheight=0.955, relx=0.011, rely=0.02)

        self.frame_hasil = Frame(self.label_isi, bg="#132a46")
        self.frame_hasil.place(relwidth=1, relheight=0.775, relx=0, rely=0.175)

        # Label_isi
        self.imglabelsearch = ImageTk.PhotoImage(file="C:/Project UAS TERBARU/Search Label.png")
        self.labelsearch = Label(self.label_isi, image=self.imglabelsearch, bg="#132a46")
        self.labelsearch.place(relwidth=0.62, relheight=0.15, relx=0.01, rely=0.0175)

        self.searchtext = StringVar()
        self.entry6 = Entry(self.label_isi, border=0, textvariable=self.searchtext, bg="white", fg="grey", font=("Poppins", 18), justify=LEFT)
        self.entry6.place(relwidth=0.4, relheight=0.07, relx=0.05, rely=0.058)
        self.entry6.insert(0, "Mau denger lagu apa nih?")
        self.entry6.bind("<FocusIn>", lambda e: self.entry6.delete(0, "end"))

        self.logosearch = ImageTk.PhotoImage(file="C:/Project UAS TERBARU/Search.png")
        self.button_search_action = Button(self.label_isi, image=self.logosearch, bg="white", border=0, command=self.ternary_search_and_show, activebackground="white")
        self.button_search_action.place(relwidth=0.05, relheight=0.06, relx=0.56, rely=0.06)

        self.imgsort = ImageTk.PhotoImage(file="C:/Project UAS TERBARU/Sort.png")
        self.button_sort = Button(self.label_isi, image=self.imgsort, bg="#132a46", border=0, command=self.sort, activebackground="#132a46")
        self.button_sort.place(relwidth=0.06, relheight=0.135, relx=0.6325, rely=0.025)

        self.imgnamaapp = ImageTk.PhotoImage(file="C:/Project UAS TERBARU/MelodyMist.png")
        self.buttonnamaapp = Button(self.label_isi, image=self.imgnamaapp, bg="#132a46", border=0, activebackground="#132a46")
        self.buttonnamaapp.place(relwidth=0.3, relheight=0.13, relx=0.69, rely=0.03)

        # Frame_hasil
        self.canvas = Canvas(self.frame_hasil, bg="#132a46", borderwidth=0, highlightthickness=0)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar = Scrollbar(self.frame_hasil, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.frame_hasil_search = Frame(self.canvas, bg="#132a46")
        self.canvas.create_window((0, 0), window=self.frame_hasil_search, anchor='nw')

        self.update_frame_hasil_search("C:/Project UAS TERBARU/path_lagu - Copy.txt")

        self.frame_hasil_search.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))
        

    def update_frame_hasil_search(self, filename=None, search_results=None):
        if filename:
            with open(filename, 'r', encoding='utf-8') as file:
                lines = file.readlines()[1:]
                self.songs = [line.strip().split(',') for line in lines]

        songs_to_display = search_results if search_results is not None else self.songs
        self.new_playlist = songs_to_display
        self.playlist_music_search()

        self.frame_hasil_search.destroy()
        self.frame_hasil_search = Frame(self.canvas, bg="#132a46")

        num_columns = 5
        num_rows = (len(songs_to_display) + num_columns - 1) // num_columns

        frame_height = num_rows * 200
        self.frame_hasil_search.config(height=frame_height)
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

        self.current_playlist = [data[2] for data in songs_to_display]
        self.current_index = 0

        for i in range(len(songs_to_display)):
            data = songs_to_display[i]
            
            original_image = Image.open(data[2])
            ukuran_baru = (200, 200)
            resized_image = original_image.resize(ukuran_baru, Image.BILINEAR)
            imgcover = ImageTk.PhotoImage(resized_image)
            button_cover = Button(self.frame_hasil_search, image=imgcover, bg="#132a46", border=0, command=lambda idx=i: self.load_musik(idx), activebackground="#132a46")
            button_cover.image = imgcover
            button_cover.grid(row=i // num_columns * 3, column=i % num_columns, padx=5, pady=5, sticky='n')

            judul = Label(self.frame_hasil_search, text=data[1], bg="#132a46", fg="white", font=("Poppins", 8, 'bold'), wraplength=150)
            judul.grid(row=i // num_columns * 3 + 1, column=i % num_columns, padx=5, pady=2, sticky='n')

            artis = Label(self.frame_hasil_search, text=data[0], bg="#132a46", fg="white", font=("Poppins", 8), wraplength=150)
            artis.grid(row=i // num_columns * 3 + 2, column=i % num_columns, padx=5, pady=2, sticky='n')

        self.frame_hasil_search.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))
        self.canvas.create_window((0, 0), window=self.frame_hasil_search, anchor='nw')


    def ternary_search(self, search_keyword):
        search_keyword = search_keyword.lower()
        l = 0
        r = len(self.songs) - 1

        while r >= l:
            mid1 = l + (r - l) // 3
            mid2 = r - (r - l) // 3

            if self.songs[mid1][1].lower() == search_keyword or self.songs[mid1][0].lower() == search_keyword:
                return mid1
            if self.songs[mid2][1].lower() == search_keyword or self.songs[mid2][0].lower() == search_keyword:
                return mid2

            if search_keyword < self.songs[mid1][1].lower():
                r = mid1 - 1
            elif search_keyword > self.songs[mid2][1].lower():
                l = mid2 + 1
            else:
                l = mid1 + 1
                r = mid2 - 1

        return -1

    
    def ternary_search_and_show(self):
        search_keyword = self.entry6.get().lower()
        search_results = [song for song in self.songs if search_keyword in song[1].lower() or search_keyword in song[0].lower()]
        self.update_frame_hasil_search(search_results=search_results)


    def halamanplaymusic_search(self, selected_song):
        for widget in self.frame.winfo_children():
            widget.destroy()

        # Frame
        self.imglabelhalaman = ImageTk.PhotoImage(file="C:\Project UAS TERBARU\Label Halaman.png")
        self.labelhalaman = Label(self.frame, image=self.imglabelhalaman, bg="#2f5389")
        self.labelhalaman.place(relwidth=0.975, relheight=1, relx=0, rely=0)

        self.label_isi =  Label(self.frame, bg="#132a46")
        self.label_isi.place(relwidth=0.95, relheight=0.955, relx=0.011, rely=0.02)

        self.frame_updatemusic = Frame(self.label_isi, bg="#132a46")
        self.frame_updatemusic.place(relwidth=1, relheight=1, relx=0, rely=0)

        self.selected_song = selected_song
        self.update_frame_playmusic()
        
        # Frame_playmusic
        if self.music_playing and self.running:
            nama_lagu = os.path.splitext(os.path.basename(selected_song))[0]
            nama_lagu_png = nama_lagu + ".png"
            cover_lagu = os.path.join("C:/Project UAS TERBARU/Gambar Lagu/", nama_lagu_png)
            ukuran_baru = (100, 100)
            
            if os.path.exists(cover_lagu):
                imgcover_lagu = Image.open(cover_lagu)
                resized_image = imgcover_lagu.resize(ukuran_baru, Image.BILINEAR)
                imgcover = ImageTk.PhotoImage(resized_image)
                self.lagu = Button(self.frame_playmusic, command=lambda: self.halamanplaymusic(selected_song), image=imgcover, bg="white", border=0)
                self.lagu.image = imgcover
                self.lagu.place(relwidth=1, relheight=0.4, relx=0, rely=0.03)

                penyanyi_lagu = nama_lagu.split(' - ')[0].strip()
                self.textartis = Label(self.frame_playmusic, text=penyanyi_lagu, bg="white", border=0, fg="black", font=("Poppins", 7), anchor="center")
                self.textartis.place(relwidth=1, relheight=0.1, relx=0, rely=0.5)

                judul_lagu = nama_lagu.split(' - ')[1].strip()
                self.textjudul = Label(self.frame_playmusic, text=judul_lagu, bg="white", border=0, fg="black", font=("Poppins", 8, "bold"), anchor="center")
                self.textjudul.place(relwidth=1, relheight=0.1, relx=0, rely=0.43)

                self.togglebutton1 = Button(self.frame_playmusic, command=self.toggle_play_pause2, bg="white", border=0, fg="black", font=("Poppins", 22, 'bold'), activebackground="white")
                self.togglebutton1.config(image=self.play_image1 if self.music_playing else self.pause_image1)
                self.togglebutton1.place(relwidth=0.62, relheight=0.3, relx=0.2, rely=0.6)

            else:
                self.textmusic = Label(self.frame_playmusic, text="No Song\nPlay", border=0, fg="grey", font=("Poppins", 10), bg="white")
                self.textmusic.place(relwidth=0.5, relheight=0.15, relx=0.235, rely=0.45)
        else:
            self.textmusic = Label(self.frame_playmusic, text="No Song\nPlay", border=0, fg="grey", font=("Poppins", 10), bg="white")
            self.textmusic.place(relwidth=0.5, relheight=0.15, relx=0.235, rely=0.45)

        # Frame_updatemusic
        if self.music_playing and self.running:
            nama_file = os.path.splitext(os.path.basename(selected_song))[0]
            nama_file_png = nama_file + ".png"
            path_cover_lagu = os.path.join("C:/Project UAS TERBARU/Gambar Lagu/", nama_file_png)
            if os.path.exists(path_cover_lagu):
                cover_lagu = Image.open(path_cover_lagu)
                imgcover = ImageTk.PhotoImage(cover_lagu)
                self.lagu = Label(self.frame_updatemusic, image=imgcover, bg="#132a46", border=0)
                self.lagu.image = imgcover
                self.lagu.place(relwidth=0.48, relheight=0.8, relx=0.03, rely=0.1)

            judul_lagu = nama_file.split(' - ')[1].strip()
            penyanyi_lagu = nama_file.split(' - ')[0].strip()
            if len(judul_lagu) >= 21 and len(judul_lagu) <= 35 :
                self.textjudul = Text(self.frame_updatemusic, bg="#132a46", border=0, fg="white", font=("Poppins", 30, "bold"), wrap="word", height=2)
                self.textjudul.insert("1.0", judul_lagu)
                self.textjudul.config(state="disabled")
                self.textjudul.place(relwidth=0.4, relheight=0.2, relx=0.565, rely=0.1)
                self.textartis = Label(self.frame_updatemusic, text=penyanyi_lagu, bg="#132a46", border=0, fg="white", font=("Poppins", 20), anchor="w")
                self.textartis.place(relwidth=0.4, relheight=0.05, relx=0.57, rely=0.265)

            elif len(judul_lagu) >= 30 :
                self.textjudul = Text(self.frame_updatemusic, bg="#132a46", border=0, fg="white", font=("Poppins", 30, "bold"), wrap="word", height=2)
                self.textjudul.insert("1.0", judul_lagu)
                self.textjudul.config(state="disabled")
                self.textjudul.place(relwidth=0.4, relheight=0.25, relx=0.565, rely=0.1)
                self.textartis = Label(self.frame_updatemusic, text=penyanyi_lagu, bg="#132a46", border=0, fg="white", font=("Poppins", 20), anchor="w")
                self.textartis.place(relwidth=0.4, relheight=0.05, relx=0.57, rely=0.335)

            elif len(penyanyi_lagu) >= 30 :
                self.textjudul = Label(self.frame_updatemusic, text=judul_lagu, bg="#132a46", border=0, fg="white", font=("Poppins", 30, "bold"), anchor="w")
                self.textjudul.place(relwidth=0.4, relheight=0.1, relx=0.57, rely=0.1)
                self.textartis = Text(self.frame_updatemusic, bg="#132a46", border=0, fg="white", font=("Poppins", 20), wrap="word", height=1)
                self.textartis.insert("1.0", penyanyi_lagu)
                self.textartis.config(state="disabled")
                self.textartis.place(relwidth=0.4, relheight=0.2, relx=0.57, rely=0.2)

            else :
                self.textjudul = Label(self.frame_updatemusic, text=judul_lagu, bg="#132a46", border=0, fg="white", font=("Poppins", 30, "bold"), anchor="w")
                self.textjudul.place(relwidth=0.4, relheight=0.1, relx=0.57, rely=0.1)
                self.textartis = Label(self.frame_updatemusic, text=penyanyi_lagu, bg="#132a46", border=0, fg="white", font=("Poppins", 20), anchor="w")
                self.textartis.place(relwidth=0.4, relheight=0.05, relx=0.57, rely=0.2)

            self.imgprevious = PhotoImage(file="C:/Project UAS TERBARU/Previous.png")
            self.button_previous = Button(self.frame_updatemusic, image=self.imgprevious, bg="#132a46", border=0, command=self.previous_music_search, activebackground="#132a46")
            self.button_previous.place(relwidth=0.1, relheight=0.12, relx=0.57, rely=0.75)

            self.togglebutton2 = Button(self.frame_updatemusic, command=self.toggle_play_pause2, image=self.play_image2, bg="#132a46", border=0, activebackground="#132a46")
            self.togglebutton2.config(image=self.play_image2 if self.music_playing else self.pause_image2)
            self.togglebutton2.place(relwidth=0.15, relheight=0.2, relx=0.7, rely=0.7)

            self.imgnext = PhotoImage(file="C:/Project UAS TERBARU/Next.png")
            self.button_next = Button(self.frame_updatemusic, image=self.imgnext, bg="#132a46", border=0, command=self.next_music_search, activebackground="#132a46")
            self.button_next.place(relwidth=0.1, relheight=0.12, relx=0.87, rely=0.75)
        else:
            showinfo(title="Info", message="Tidak ada lagu yang bisa diputar")


    def playlist_music_search(self):
        self.playlist = [os.path.join("C:/Project UAS TERBARU/Lagu", os.path.basename(data[2]).split(".")[0] + ".mp3") for data in self.new_playlist]
        return self.playlist
    

    def load_musik(self, index):
        data = self.new_playlist[index]
        artis = data[0]
        judul = data[1]
        song_path = data[2]
        self.current_index = index

        lagu_title = os.path.basename(song_path).split(".")[0]
        selected_lagu= os.path.join("C:/Project UAS TERBARU/Lagu", lagu_title + ".mp3")
        selected_song = selected_lagu

        if os.path.exists(selected_song):
            self.play_music_search(selected_song)
        

    def play_music_search(self, selected_song):
        if selected_song not in self.last_played_songs:
            self.last_played_songs.append(selected_song)
            if len(self.last_played_songs) > 10:
                self.last_played_songs.pop(0)
        self.play_mode = 'search'
        pygame.mixer.music.load(selected_song)
        pygame.mixer.music.play()
        self.music_playing = True
        self.running = True
        pygame.mixer.music.set_endevent(pygame.USEREVENT)
        pygame.event.set_allowed(pygame.USEREVENT)
        print(f"Playing: {selected_song}")
        self.halamanplaymusic_search(selected_song)
        self.save_to_history(selected_song)

    
    def next_music_search(self):
        if self.current_playlist:
            self.current_index = (self.current_index + 1) % len(self.current_playlist)
            next_song = self.playlist[self.current_index]
            self.play_music(next_song)
   

    def previous_music_search(self):
        if self.current_playlist:
            self.current_index = (self.current_index - 1) % len(self.current_playlist)
            prev_song = self.playlist[self.current_index]
            self.play_music(prev_song)


    def sort(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

        # Frame
        self.imglabelhalaman = ImageTk.PhotoImage(file="C:\Project UAS TERBARU\Label Sort.png")
        self.labelhalaman = Label(self.frame, image=self.imglabelhalaman, bg="#2f5389")
        self.labelhalaman.place(relwidth=0.975, relheight=1, relx=0, rely=0)

        self.frame_hasil = Frame(self.frame, bg="#cfcdee")
        self.frame_hasil.place(relwidth=0.63, relheight=0.95, relx=0.025, rely=0.025)

        # Frame_hasil
        self.canvas = Canvas(self.frame_hasil, bg="#cfcdee", borderwidth=0, highlightthickness=0)
        self.canvas.pack(side=LEFT, fill=BOTH, expand=True)
        self.scrollbar = Scrollbar(self.frame_hasil, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side=RIGHT, fill=Y)

        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind("<Configure>", self.on_canvas_configure)

        self.music_list_frame = Frame(self.canvas, bg="#cfcdee")
        self.canvas.create_window((0, 0), window=self.music_list_frame, anchor="nw")

        self.music_list_frame.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

        self.frame_hasil.bind("<Configure>", self.on_frame_hasil_configure)
        self.on_frame_hasil_configure(None)

        self.show_music_list()


    def on_canvas_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))


    def on_frame_hasil_configure(self, event):
        self.canvas.config(scrollregion=self.canvas.bbox("all"))


    def show_music_list(self):
        with open("C:\Project UAS TERBARU\music_data.txt", "r", encoding="utf-8") as file:
            lines = file.readlines()[1:]

        self.music_names = []
        self.music_artist = []
        self.music_paths = []
        self.music_covers = []
        self.music_genres = []

        for line in lines:
            parts = line.strip().split(",")
            self.music_names.append(parts[0])
            self.music_artist.append(parts[1])
            self.music_paths.append(parts[2])
            self.music_covers.append(parts[3])
            self.music_genres.append(parts[4])

        self.original_music_names = self.music_names[:]
        self.original_music_artist = self.music_artist[:]
        self.original_music_paths = self.music_paths[:]
        self.original_music_covers = self.music_covers[:]
        self.original_music_genres = self.music_genres[:]

        self.name_to_cover = {name: cover for name, cover in zip(self.music_names, self.music_covers)}
        self.artist_to_cover = {artist: cover for artist, cover in zip(self.music_artist, self.music_covers)}

        self.sortnama = Button(self.frame, text="Music Name", command=self.sort_music_name, bg="white", border=0, fg="black", font=("Poppins", 25, 'bold'), activebackground="white")
        self.sortnama.place(relwidth=0.2, relheight=0.1, relx=0.72, rely=0.06)

        self.sortartis = Button(self.frame, text="Artist", command=self.sort_music_artist, bg="white", border=0, fg="black", font=("Poppins", 25, 'bold'), activebackground="white")
        self.sortartis.place(relwidth=0.2, relheight=0.1, relx=0.72, rely=0.235)

        self.sortgenre = Button(self.frame, text="Genre", command=self.show_genre_options, bg="white", border=0, fg="black", font=("Poppins", 25, 'bold'), activebackground="white")
        self.sortgenre.place(relwidth=0.2, relheight=0.1, relx=0.72, rely=0.41)

        self.update_music_list(self.music_covers, self.music_names)


    def update_music_list(self, cover_paths, names, display_artist_first=False):
        for widget in self.music_list_frame.winfo_children():
            widget.destroy()

        num_columns = 5
        num_rows = (len(names) + num_columns - 1) // num_columns

        frame_height = num_rows * 130
        self.music_list_frame.config(height=frame_height)
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

        self.current_playlist = []

        for i in range(len(names)):
            if display_artist_first:
                artist_name = names[i]
                index_sort = self.music_artist.index(artist_name)
                music_name = self.music_names[index_sort].split(' - ', 1)[1].strip()
                music_label_text = f"{artist_name}"
            else:
                music_display = names[i]
                index_sort = self.music_names.index(music_display)
                music_label_text = names[i]

            self.current_playlist.append(self.music_paths[index_sort])  # Append the path to the current playlist

            cover_path = cover_paths[i]
            cover_image = Image.open(cover_path)
            cover_image = cover_image.resize((125, 125), Image.LANCZOS)
            cover_photo = ImageTk.PhotoImage(cover_image)

            cover_button = Button(self.music_list_frame, image=cover_photo, borderwidth=0, highlightthickness=0, command=lambda idx=index_sort: self.music_sort(idx))
            cover_button.image = cover_photo
            cover_button.grid(row=i // num_columns * 2, column=i % num_columns, padx=5, pady=2)

            music_label = Label(self.music_list_frame, text=music_label_text, bg="#cfcdee", wraplength=125)
            music_label.grid(row=i // num_columns * 2 + 1, column=i % num_columns, padx=5, pady=2)

        self.music_list_frame.update_idletasks()
        self.on_frame_hasil_configure(None)


    def combsort(self, data):
        gap = len(data)
        shrink_factor = 1.3
        sorted = False

        while not sorted:
            gap = int(gap / shrink_factor)
            if gap > 1:
                sorted = False
            else:
                gap = 1
                sorted = True

            i = 0
            while i + gap < len(data):
                if data[i] > data[i + gap]:
                    data[i], data[i + gap] = data[i + gap], data[i]
                    sorted = False
                i += 1


    def sort_music_name(self):
        original_pairs = list(zip(self.music_names, self.music_paths, self.music_covers))
        self.combsort(self.music_names)
        sorted_pairs = sorted(original_pairs, key=lambda x: x[0])
        self.sorted_cover_paths_name = [pair[2] for pair in sorted_pairs]
        self.music_paths = [pair[1] for pair in sorted_pairs]

        self.current_playlist = self.music_paths
        self.update_music_list(self.sorted_cover_paths_name, self.music_names)


    def sort_music_artist(self):
        original_pairs = list(zip(self.music_artist, self.music_names, self.music_paths, self.music_covers))
        sorted_pairs = sorted(original_pairs, key=lambda x: x[0])
        sorted_artists, sorted_names, sorted_paths, sorted_covers = zip(*sorted_pairs)
        
        self.music_artist = list(sorted_artists)
        self.music_names = list(sorted_names)
        self.music_paths = list(sorted_paths)
        self.music_covers = list(sorted_covers)
        
        self.sorted_cover_paths_artist = list(sorted_covers)
        self.update_music_list(self.sorted_cover_paths_artist, self.music_artist, display_artist_first=True)


    def show_genre_options(self):
        self.genre_window = Toplevel(self.window)
        self.genre_window.title("Select Genre")
        self.genre_window.configure(bg="pink")
        self.genre_window.state("normal")
        self.genre_window.iconbitmap("C:/Project UAS TERBARU/Icon.ico")

        genres = list(set(self.original_music_genres))
        genres.sort()

        self.entrygenre = IntVar()

        for idx, genre in enumerate(genres):
            if genre.strip():
                Radiobutton(self.genre_window, bg="pink", text=genre, variable=self.entrygenre, value=idx).pack(anchor=W)

        confirm_button = Button(self.genre_window, text="Ok", command=self.sort_music_genre)
        confirm_button.pack(anchor="center")


    def sort_music_genre(self):
        selected_genre_index = self.entrygenre.get()
        genres = list(set(self.original_music_genres))
        genres.sort()
        selected_genre = genres[selected_genre_index]

        original_pairs = list(zip(self.original_music_genres, self.original_music_names, self.original_music_paths, self.original_music_covers))
        filtered_pairs = [pair for pair in original_pairs if pair[0] == selected_genre]

        if filtered_pairs:
            _, filtered_names, filtered_paths, filtered_covers = zip(*filtered_pairs)
        else:
            filtered_names, filtered_paths, filtered_covers = [], [], []

        self.music_names = list(filtered_names)
        self.music_paths = list(filtered_paths)
        self.music_covers = list(filtered_covers)

        self.update_music_list(self.music_covers, self.music_names)


    def halamanplaymusic_sort(self, selected_song):
        for widget in self.frame.winfo_children():
            widget.destroy()
        
        # Frame
        self.imglabelhalaman = ImageTk.PhotoImage(file="C:\Project UAS TERBARU\Label Halaman.png")
        self.labelhalaman = Label(self.frame, image=self.imglabelhalaman, bg="#2f5389")
        self.labelhalaman.place(relwidth=0.975, relheight=1, relx=0, rely=0)

        self.label_isi =  Label(self.frame, bg="#132a46")
        self.label_isi.place(relwidth=0.95, relheight=0.955, relx=0.011, rely=0.02)

        self.frame_updatemusic = Frame(self.label_isi, bg="#132a46")
        self.frame_updatemusic.place(relwidth=1, relheight=1, relx=0, rely=0)

        self.selected_song = selected_song
        self.update_frame_playmusic()   
        
        # Frame_playmusic
        if self.music_playing and self.running:
            nama_lagu = os.path.splitext(os.path.basename(selected_song))[0]
            nama_lagu_png = nama_lagu + ".png"
            cover_lagu = os.path.join("C:/Project UAS TERBARU/Gambar Lagu/", nama_lagu_png)
            ukuran_baru = (100, 100)
            
            if os.path.exists(cover_lagu):
                imgcover_lagu = Image.open(cover_lagu)
                resized_image = imgcover_lagu.resize(ukuran_baru, Image.BILINEAR)
                imgcover = ImageTk.PhotoImage(resized_image)
                self.lagu = Button(self.frame_playmusic, command=lambda: self.halamanplaymusic_sort(selected_song), image=imgcover, bg="white", border=0)
                self.lagu.image = imgcover
                self.lagu.place(relwidth=1, relheight=0.4, relx=0, rely=0.03)

                penyanyi_lagu = nama_lagu.split(' - ')[0].strip()
                self.textartis = Label(self.frame_playmusic, text=penyanyi_lagu, bg="white", border=0, fg="black", font=("Poppins", 7), anchor="center")
                self.textartis.place(relwidth=1, relheight=0.1, relx=0, rely=0.5)

                judul_lagu = nama_lagu.split(' - ')[1].strip()
                self.textjudul = Label(self.frame_playmusic, text=judul_lagu, bg="white", border=0, fg="black", font=("Poppins", 8, "bold"), anchor="center")
                self.textjudul.place(relwidth=1, relheight=0.1, relx=0, rely=0.43)

                self.togglebutton1 = Button(self.frame_playmusic, command=self.toggle_play_pause2, bg="white", border=0, fg="black", font=("Poppins", 22, 'bold'), activebackground="white")
                self.togglebutton1.config(image=self.play_image1 if self.music_playing else self.pause_image1)
                self.togglebutton1.place(relwidth=0.62, relheight=0.3, relx=0.2, rely=0.6)

            else:
                self.textmusic = Label(self.frame_playmusic, text="No Song\nPlay", border=0, fg="grey", font=("Poppins", 10), bg="white")
                self.textmusic.place(relwidth=0.5, relheight=0.15, relx=0.235, rely=0.45)
        else:
            self.textmusic = Label(self.frame_playmusic, text="No Song\nPlay", border=0, fg="grey", font=("Poppins", 10), bg="white")
            self.textmusic.place(relwidth=0.5, relheight=0.15, relx=0.235, rely=0.45)

        # Frame_updatemusic
        if self.music_playing and self.running:
            nama_file = os.path.splitext(os.path.basename(selected_song))[0]
            nama_file_png = nama_file + ".png"
            path_cover_lagu = os.path.join("C:/Project UAS TERBARU/Gambar Lagu/", nama_file_png)
            if os.path.exists(path_cover_lagu):
                cover_lagu = Image.open(path_cover_lagu)
                imgcover = ImageTk.PhotoImage(cover_lagu)
                self.lagu = Label(self.frame_updatemusic, image=imgcover, bg="#132a46", border=0)
                self.lagu.image = imgcover
                self.lagu.place(relwidth=0.48, relheight=0.8, relx=0.03, rely=0.1)

            judul_lagu = nama_file.split(' - ')[1].strip()
            penyanyi_lagu = nama_file.split(' - ')[0].strip()
            if len(judul_lagu) >= 21 and len(judul_lagu) <= 35 :
                self.textjudul = Text(self.frame_updatemusic, bg="#132a46", border=0, fg="white", font=("Poppins", 30, "bold"), wrap="word", height=2)
                self.textjudul.insert("1.0", judul_lagu)
                self.textjudul.config(state="disabled")
                self.textjudul.place(relwidth=0.4, relheight=0.2, relx=0.565, rely=0.1)

                self.textartis = Label(self.frame_updatemusic, text=penyanyi_lagu, bg="#132a46", border=0, fg="white", font=("Poppins", 20), anchor="w")
                self.textartis.place(relwidth=0.4, relheight=0.05, relx=0.57, rely=0.265)
            elif len(judul_lagu) >= 30 :
                self.textjudul = Text(self.frame_updatemusic, bg="#132a46", border=0, fg="white", font=("Poppins", 30, "bold"), wrap="word", height=2)
                self.textjudul.insert("1.0", judul_lagu)
                self.textjudul.config(state="disabled")
                self.textjudul.place(relwidth=0.4, relheight=0.25, relx=0.565, rely=0.1)

                self.textartis = Label(self.frame_updatemusic, text=penyanyi_lagu, bg="#132a46", border=0, fg="white", font=("Poppins", 20), anchor="w")
                self.textartis.place(relwidth=0.4, relheight=0.05, relx=0.57, rely=0.335)
            elif len(penyanyi_lagu) >= 30 :
                self.textjudul = Label(self.frame_updatemusic, text=judul_lagu, bg="#132a46", border=0, fg="white", font=("Poppins", 30, "bold"), anchor="w")
                self.textjudul.place(relwidth=0.4, relheight=0.1, relx=0.57, rely=0.1)

                self.textartis = Text(self.frame_updatemusic, bg="#132a46", border=0, fg="white", font=("Poppins", 20), wrap="word", height=1)
                self.textartis.insert("1.0", penyanyi_lagu)
                self.textartis.config(state="disabled")
                self.textartis.place(relwidth=0.4, relheight=0.2, relx=0.57, rely=0.2)
            else :
                self.textjudul = Label(self.frame_updatemusic, text=judul_lagu, bg="#132a46", border=0, fg="white", font=("Poppins", 30, "bold"), anchor="w")
                self.textjudul.place(relwidth=0.4, relheight=0.1, relx=0.57, rely=0.1)
                
                self.textartis = Label(self.frame_updatemusic, text=penyanyi_lagu, bg="#132a46", border=0, fg="white", font=("Poppins", 20), anchor="w")
                self.textartis.place(relwidth=0.4, relheight=0.05, relx=0.57, rely=0.2)

            self.imgprevious = PhotoImage(file="C:/Project UAS TERBARU/Previous.png")
            self.button_previous = Button(self.frame_updatemusic, image=self.imgprevious, bg="#132a46", border=0, command=self.previous_music_sort, activebackground="#132a46")
            self.button_previous.place(relwidth=0.1, relheight=0.12, relx=0.57, rely=0.75)

            self.togglebutton2 = Button(self.frame_updatemusic, command=self.toggle_play_pause2, image=self.play_image2, bg="#132a46", border=0, activebackground="#132a46")
            self.togglebutton2.config(image=self.play_image2 if self.music_playing else self.pause_image2)
            self.togglebutton2.place(relwidth=0.15, relheight=0.2, relx=0.7, rely=0.7)

            self.imgnext = PhotoImage(file="C:/Project UAS TERBARU/Next.png")
            self.button_next = Button(self.frame_updatemusic, image=self.imgnext, bg="#132a46", border=0, command=self.next_music_sort, activebackground="#132a46")
            self.button_next.place(relwidth=0.1, relheight=0.12, relx=0.87, rely=0.75)
        else:
            showinfo(title="Info", message="Tidak ada lagu yang bisa diputar")


    def play_music_sort(self, selected_song):
        if selected_song not in self.last_played_songs:
            self.last_played_songs.append(selected_song)
            if len(self.last_played_songs) > 10:
                self.last_played_songs.pop(0)
        self.play_mode = 'sort'
        pygame.mixer.music.load(selected_song)
        pygame.mixer.music.play()
        self.music_playing = True
        self.running = True
        pygame.mixer.music.set_endevent(pygame.USEREVENT)
        pygame.event.set_allowed(pygame.USEREVENT)
        print(f"Playing: {selected_song}")
        self.halamanplaymusic_sort(selected_song)
        self.save_to_history(selected_song)


    def create_playlist(self, songs):
        self.current_playlist_sort = songs
        self.current_index_sort = 0


    def music_sort(self, idx):
        selected_song = self.current_playlist[idx]
        self.current_index = idx
        self.play_music_sort(selected_song)


    def playlist_music_sort(self):
        self.create_playlist(self.current_playlist_sort)


    def next_music_sort(self):
        if self.current_playlist:
            self.current_index = (self.current_index + 1) % len(self.current_playlist)
            selected_song = self.current_playlist[self.current_index]
            self.play_music_sort(selected_song)


    def previous_music_sort(self):
        if self.current_playlist:
            self.current_index = (self.current_index - 1) % len(self.current_playlist)
            selected_song = self.current_playlist[self.current_index]
            self.play_music_sort(selected_song)

    
    def update_frame_playmusic(self):
        for widget in self.frame_playmusic.winfo_children():
            widget.destroy()

        if self.music_playing and self.running:
            song_path = self.selected_song
            nama_lagu = os.path.splitext(os.path.basename(song_path))[0]
            nama_lagu_png = nama_lagu + ".png"
            nama_lagu_mp3 = nama_lagu + ".mp3"
            cover_lagu = os.path.join("C:/Project UAS TERBARU/Gambar Lagu/", nama_lagu_png)
            path_lagu = os.path.join("C:/Project UAS TERBARU/Gambar Lagu/", nama_lagu_mp3)
            ukuran_baru = (100, 100)
            selected_song = path_lagu

            if os.path.exists(cover_lagu):
                imgcover_lagu = Image.open(cover_lagu)
                resized_image = imgcover_lagu.resize(ukuran_baru, Image.BILINEAR)
                imgcover = ImageTk.PhotoImage(resized_image)
                self.lagu = Button(self.frame_playmusic, command=lambda: self.halamanplaymusic(selected_song), image=imgcover, bg="white", border=0)
                self.lagu.image = imgcover
                self.lagu.place(relwidth=1, relheight=0.4, relx=0, rely=0.03)

                penyanyi_lagu = nama_lagu.split(' - ')[0].strip()
                self.textartis = Label(self.frame_playmusic, text=penyanyi_lagu, bg="white", border=0, fg="black", font=("Poppins", 7), anchor="center")
                self.textartis.place(relwidth=1, relheight=0.1, relx=0, rely=0.5)

                judul_lagu = nama_lagu.split(' - ')[1].strip()
                self.textjudul = Label(self.frame_playmusic, text=judul_lagu, bg="white", border=0, fg="black", font=("Poppins", 8, "bold"), anchor="center")
                self.textjudul.place(relwidth=1, relheight=0.1, relx=0, rely=0.43)

                self.togglebutton1 = Button(self.frame_playmusic, command=self.toggle_play_pause, bg="white", border=0, fg="black", font=("Poppins", 22, 'bold'), activebackground="white")
                self.togglebutton1.config(image=self.play_image1 if self.music_playing else self.pause_image1)
                self.togglebutton1.place(relwidth=0.62, relheight=0.3, relx=0.2, rely=0.6)
            else:
                self.textmusic = Label(self.frame_playmusic, text="No Song\nPlay", border=0, fg="grey", font=("Poppins", 10), bg="white")
                self.textmusic.place(relwidth=0.5, relheight=0.15, relx=0.235, rely=0.45)
        else:
            self.textmusic = Label(self.frame_playmusic, text="No Song\nPlay", border=0, fg="grey", font=("Poppins", 10), bg="white")
            self.textmusic.place(relwidth=0.5, relheight=0.15, relx=0.235, rely=0.45)


    def toggle_play_pause(self):
        if self.music_playing:
            self.togglebutton1.config(image=self.pause_image1)
            self.pause_music()
            self.music_playing = False
        else:
            self.togglebutton1.config(image=self.play_image1)
            self.resume_music()
            self.music_playing = True
    
    
    def toggle_play_pause2(self):
        if self.music_playing:
            self.togglebutton1.config(image=self.pause_image1)
            self.togglebutton2.config(image=self.pause_image2)
            self.pause_music()
            self.music_playing = False
        else:
            self.togglebutton1.config(image=self.play_image1)
            self.togglebutton2.config(image=self.play_image2)
            self.resume_music()
            self.music_playing = True


    def check_music_event(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.USEREVENT:
                    if self.play_mode == 'sort':
                        self.next_music_sort()
                    elif self.play_mode == 'search':
                        self.next_music_search()
                    else:
                        self.next_music()
            time.sleep(0.1)

    
    def pause_music(self):
        if self.music_playing:
            pygame.mixer.music.pause()
            self.music_playing = False


    def resume_music(self):
        if not self.music_playing:
            pygame.mixer.music.unpause()
            self.music_playing = True


    def exit(self):
        self.running = False
        self.songs_loaded = False
        self.label_main_page.destroy()
        pygame.mixer.music.stop()
        self.login()


window = Tk()
print(window.winfo_screenwidth())
print(window.winfo_screenheight())
project(window)
window.mainloop()