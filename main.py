from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from fake_useragent import UserAgent

import json
import os
import re
import requests


window = Tk()
window.title('Get_Weather')
window.geometry('800x600')
window.resizable(width=False, height=False)
window.config(bg='#f2e8c9')


frame = Frame(window)
frame.pack(pady=20)

lbl = Label(text='Введите ваш город', fg='black', bg='#f2e8c9', font='Times 20')
lbl.pack()
my_entry = Entry(
    window,
    font=('Times', 20)
)
my_entry.pack(pady=20)

btn_frame = Frame(window)
btn_frame.pack()

weather = dict()

def get_weather(name):
    global weather
    name = name.lower()
    page = requests.get('http://api.openweathermap.org/data/2.5/weather?q=' + name + '&appid=d4f204ce8fd704e6a465d49949543a67&lang=ru', headers={'User-Agent': UserAgent().chrome})
    weather = json.loads(page.content)

def parse(text):
    cnt = 0
    for i in re.findall(r'<img.*?>', text):
        if (cnt == 3):
            break
        j = i
        k = re.search(r'src="(.*?)"', i)
        if (k is not None):
            if (k.group(1) != ''):
                with open(str(cnt) + '.png', 'wb') as f:
                    temp = requests.get('http:' + k.group(1), headers={'User-Agent': UserAgent().chrome})
                    f.write(temp.content)
                cnt += 1

def get_image(name):
    name = name.lower()
    page = requests.get('https://yandex.ru/images/search?&text=' + name, headers={'User-Agent': UserAgent().chrome})
    parse(page.text)

frames = list()
frame_for_images = Frame(window, bg='#f2e8c9')
frame_for_images.pack()

def display_images():
    global frames
    if (len(frames) != 0):
        for i in frames:
            i.destroy()
    frames = [Frame(frame_for_images) for _ in range(3)]
    for i in range(3):
        frames[i].configure(bg='#f2e8c9')
        frames[i].grid(row=1, column=i)

    for i in range(3):
        img = Image.open(str(i) + '.png')
        lbl = Label(frames[i], bg='#f2e8c9')
        lbl.img = ImageTk.PhotoImage(img)
        lbl['image'] = lbl.img
        lbl.pack()

frame_for_weather = Frame(window, bg='#f2e8c9')
frame_for_weather.pack()

def get_temperature():
    global weather
    temp = format(weather['main']['temp'] - 273, '.2f')
    return (lambda temp: '+' if (temp >= 0) else '-')(float(temp)) + temp

def display_favicons_and_description():
    global weather
    favic = weather['weather'][0]['icon'][:-1] + 'd'
    favic = requests.get('http://openweathermap.org/img/wn/{}@2x.png'.format(favic), headers={'User-Agent': UserAgent().chrome}).content
    with open('favic.png', 'wb') as f:
        f.write(favic)
    img = Image.open('favic.png')
    lbl = Label(frame_for_weather, bg='#f2e8c9')
    lbl.img = ImageTk.PhotoImage(img)
    lbl['image'] = lbl.img
    lbl.grid(row=1, column=0)
    lbl_description = Label(frame_for_weather, text=weather['weather'][0]['description'] + '   ' + get_temperature(), font=('Times 20'), bg='#f2e8c9')
    lbl_description.grid(row=1, column=1, pady=10)

def click():
    global frame_for_weather
    global frames
    text = my_entry.get()
    if (text != ''):
        for i in range(3):
            if (os.path.isfile(str(i) + '.png')):
                os.remove(str(i) + '.png')
        if (os.path.isfile('favic.png')):
            os.remove('favic.png')
        my_entry.delete(0, 'end')
        get_weather(text)
        get_image(text)
        frame_for_weather.destroy()
        frame_for_weather = Frame(window, bg='#f2e8c9')
        frame_for_weather.pack()
        display_images()
        display_favicons_and_description()
    else:
        messagebox.showwarning('Ошибка', 'Пожалуйста, ввведите название города')

find_btn = Button(
    btn_frame,
    text='Узнать погоду в городе',
    font='Times 20',
    command=click
)
find_btn.pack()

window.mainloop()