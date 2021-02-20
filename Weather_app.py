import tkinter as tk
from tkinter import *
from tkinter import messagebox
import requests
import pyttsx3
import speech_recognition as sr
import pyaudio




HEIGHT = 520
WIDTH = 600

#Creating tkinter intercate
root = tk.Tk()
root.title("Weather APP")

# Initialising Speaker
speaker = pyttsx3.init()
speaker.setProperty('rate', 100 )

# Speach recognition Code function
def messs():
    speaker.say("OK, Tell Me the city name")
    speaker.runAndWait()
    
    #INitializing Speach recognition to take user input
    me = sr.Recognizer()
    with sr.Microphone() as micvar:
        print("I am listening...")
        audio = me.listen(micvar)

    try:
        print("Wait..")
        text = me.recognize_google(audio)
        print("You said : ",text)
        get_weather(text)

    except Exception as Error:
        print("Cant Recognize City/State - Say that again !")

#Speaker tell you the result
def tell(nTemp, nConditions, name):
    speaker.say("The temperature in "+name+" is "+ nTemp +" and "+ nConditions)
    speaker.runAndWait()

#Speaker tell if city is not found
def Errortell(msg):
    speaker.say(msg)
    speaker.runAndWait()

#Used in MY Place feature to get user's location(city)
def my_place():
    Find_location_link = "https://geolocation-db.com/json/"
    api_responsee = requests.get(Find_location_link)
    api_data_city = api_responsee.json()
    place = api_data_city['city']
    print(place)
    # Reture the value(city/state) to the get weather function
    get_weather(place)


# Save the data in the variables
def format_response(weather):
       
    degrees = u"\N{DEGREE SIGN}"
    try:
        name = weather['name']
        conditions = weather['weather'][0]['description'].capitalize()
        temp = '{}{}'.format(weather['main']['temp'], degrees)
        feels = '{}{}'.format(weather['main']['feels_like'], degrees)
        tell(temp, conditions, name)
        return 'City :- {}\nConditions :- {}\nTemp :- {}\nFeels like {}'.format(name, conditions, temp, feels)
    
    except:
        Errortell("Not found")
        return 'City or Location Not Found!!!'
    


# Fetching the WEATHER data of given (city/state) by API 
def get_weather(city):
    if city=="":
        Errortell("Enter the city")
        return messagebox.showinfo('Error','Enter the City Name')

    else:
        api_key = '8e8940d777f4245501bcab9be4153fba'
        url = 'https://api.openweathermap.org/data/2.5/weather'
        params = {'appid' : api_key, 'q' : city, 'units' : 'metric'}
        response = requests.get(url, params = params)
        weather = response.json()
        
        #Display the final weather report
        info = format_response(weather)
        det_label['text'] = info



#  TKINTER  Design Code

canvas=tk.Canvas(root, height = HEIGHT, width = WIDTH)
canvas.pack()

bg_img = tk.PhotoImage(file = 'icon.png')
bg_label = tk.Label(root, image=bg_img)
bg_label.place(relheight=1, relwidth=1)

frame = tk.Frame(root , bg='#80c1ff', bd=5)
frame.place(anchor = 'n', relx = 0.5, rely=0.1, relwidth = 0.75, relheight = 0.1)

# Input box in design
entry = tk.Entry(frame,font=('Courier', 15))
entry.place(relwidth=0.65, relheight=1)

# Button of get weather in design
button  = tk.Button(frame, text='Get Weather',font=('Courier', 12,'bold'), command = lambda : get_weather(entry.get()))
button.place(relx = 0.7, relheight=1, relwidth=0.3)


low_frame = tk.Frame(root, bg = '#80c1ff', bd=10)
low_frame.place(anchor = 'n', relx = 0.5, rely = 0.25, relwidth=0.75, relheight=0.6)

det_label = tk.Label(low_frame, font=('Courier', 19), anchor = 'nw', justify = 'left', bd = 5)
det_label.place(relwidth=1, relheight=1)

frame8 = tk.Frame(root , bg='#000000')
frame8.place(anchor = 'n', relx = 0.81, rely=0.87, relwidth = 0.13, relheight = 0.1)
button3 = tk.Button(frame8,bg = '#80c1ff', text="MY Place", font=('System',10), command=my_place)
button3.place(relx=0, relheight=1, relwidth=1)

# Speach recognition BUTTON
photo = PhotoImage(file = "microphone-icon.png") 
btnAUTO = tk.Button(root,bg = '#FFFFFF', text="Assistant",image = photo, font=40, command=messs)
btnAUTO.place(relx = 0.55, rely=0.87, relwidth = 0.13, relheight = 0.1)

# APP name Lable (main)
App_name = tk.Label(root, text = 'Weather APP',bg = '#FFFFFF' , font =(  'Comic Sans MS', 19,'bold'))
App_name.place(relx = 0.32, relwidth = 0.42, relheight = 0.1,) 


#menu code
def About_menu():
    messagebox.showinfo('ABOUT','WEATHER APP : Developed by Lalit Singhal')

def credit_menu():
    messagebox.showinfo('CREDIT','We user (Openweather & Geolocation API)')
    


# Creating Menubar 
menubar = Menu(root) 
  
# Adding File Menu and commands 
menubar.add_command(label ='About', command = About_menu)
menubar.add_command(label ='Credit', command = credit_menu) 
menubar.add_command(label ='Exit', command = quit) 

# display Menu 
root.config(menu = menubar) 





root.mainloop()