from tkinter import *
import serial
import time
import pyfirmata

mode=' '
turn_off = False
root = Tk()
frame = Frame(root)
board = pyfirmata.Arduino('COM3')
LED = board.digital[11]
reading = board.analog[0]
LED.mode = pyfirmata.PWM
reading.enable_reporting()

def timer_check(final_time):
    t = 0
    while t < final_time and not turn_off:
        time.sleep(0.1)
        t+=0.1
        frame.update()

#==========================================================#
#Arduino command functions
#==========================================================#
def arduino_timer(time_val):
    t=0
    initial_power = int(powerLevel.get())
    initial_slider = int(w2.get())
    LED.write(initial_power/100)
    board.digital[13].write(1)
    while not turn_off and t < time_val:
        newSlider = int(w2.get())
        try:
            newPower = int(powerLevel.get())
        except:
            newPower = 0
        time.sleep(0.1)
        t += 0.1
        if newPower != initial_power:
            LED.write(newPower/100)
            initial_power = newPower
            w2.set(newPower)
            initial_slider = int(newPower)
        elif newSlider != initial_slider:
            LED.write(newSlider/100)
            initial_slider = newSlider
            initial_power = newSlider
            newPower = newSlider
            powerLevel.delete(0, 'end')
            powerLevel.insert(0, str(newSlider))
        opLabel.config(text='Spray running at %s%% power' %(powerLevel.get()))
        frame.update()
    LED.write(0)
    board.digital[13].write(0)

def arduino_oscillate(runTime, restTime, oscillations):
    i = 0
    while i < oscillations:
        board.digital[11].write(1)
        board.digital[13].write(1)
        timer_check(runTime)
        board.digital[11].write(0)
        board.digital[13].write(0)
        timer_check(restTime)
        i += 1

def arduino_constant():
    initial_power = int(powerLevel.get())
    initial_slider = int(w2.get())
    LED.write(initial_power/100)
    board.digital[13].write(1)
    while not turn_off:
        newSlider = int(w2.get())
        try:
            newPower = int(powerLevel.get())
        except:
            newPower = 0
        time.sleep(0.1)
        if newPower != initial_power:
            LED.write(newPower/100)
            initial_power = newPower
            w2.set(newPower)
            initial_slider = int(newPower)
        elif newSlider != initial_slider:
            LED.write(newSlider/100)
            initial_slider = newSlider
            initial_power = newSlider
            newPower = newSlider
            powerLevel.delete(0, 'end')
            powerLevel.insert(0, str(newSlider))
        opLabel.config(text='Spray running at %s%% power' %(powerLevel.get()))
        frame.update()
    LED.write(0)
    board.digital[13].write(0)

#==========================================================#

def forget():
   for widgets in frame.winfo_children():
      widgets.grid_forget()
      if widgets.winfo_class() == 'Entry':
        widgets.delete(0, 'end')

def shut_off(mode):
    global turn_off
    turn_off = True
    topLabel.config(text='Spray Shutoff')
    shutoff.grid_forget()
    opLabel.grid_forget()
    if mode == 'timer':
        home_button.grid(row=3, column=0)
    elif mode == 'oscillate':
        home_button.grid(row=4, column=0)
    else:
        home_button.grid(row=2, column = 0)
    
def start_screen():
    forget()
    global turn_off
    turn_off = False
    #shutoff.deselect()
    start_label.grid(row=0, column=0)
    timer_button.grid(row=1, column=0, padx=50)
    oscillate_button.grid(row=2, column=0, padx=50)
    const_button.grid(row=3, column=0, padx=50)
    topLabel.grid_forget()
    time_int=-1
    power_int=-1
    rest_int=-1

#==========================================================#
#Operating Buttons
#==========================================================#
def timer():
    global mode
    global turn_off
    turn_off = False
    #shutoff.deselect()
    mode='timer'
    opLabel.grid(row=4, column=1)
    timerLabel.grid(row=5, column=1)
    topLabel.config(text='Timer Mode')
    time_s = runTime.get()
    powerVal = powerLevel.get()
    time_int = int(time_s)
    power_int = int(powerVal) / 100
    if time_int > 0 and power_int > 0 and power_int <= 100:
        opLabel.config(text='Spray running at %s%% power for %s seconds' %(powerVal, time_s))
        timer_run_button.grid(row=3, column=1)
        home_button.grid_forget()
        shutoff.grid(row=3, column=0)
        w2.set(int(powerVal))
        w2.grid(row=5, column=0)
        frame.update()
        arduino_timer(time_int)
        opLabel.config(text='Done')
        #timer_check(time_int)

def cont():
    global mode
    global turn_off
    turn_off = False
    #shutoff.deselect()
    opLabel.grid(row=3, column=1)
    mode='const'
    topLabel.config(text='Constant Mode')
    powerVal = powerLevel.get()
    opLabel.config(text='Spray running at %s%% power ' %(powerVal))
    home_button.grid_forget()
    const_run_button.grid(row=2, column=1)
    shutoff.grid(row=2, column=0)
    w2.set(int(powerVal))
    w2.grid(row=6, column=0)
    frame.update()
    arduino_constant()


def oscillate():
    global mode
    global turn_off
    turn_off = False
    #shutoff.deselect()
    opLabel.grid(row=5, column=1)
    mode='oscillate'
    topLabel.config(text='Osiclattion Mode')
    time_on = runTime.get()
    time_off = restTime.get()
    time_int = int(time_on)
    rest_int = int(time_off)
    oscillations_string = oscillation_number.get()
    oscillations = int(oscillations_string)
    if time_int > 0 and rest_int > 0:
        opLabel.config(text='Spray pulsing for %ss on and %ss off %s iterations' %(time_on, time_off, oscillations))
        time.sleep(0.5)
        oscillate_run_button.grid(row=4, column=1)
        home_button.grid_forget()
        shutoff.grid(row=4, column=0)
        frame.update()
        arduino_oscillate(time_int, rest_int, oscillations)
        opLabel.config(text='Done')
    

#==========================================================#
#Home Screen Buttons
#==========================================================#
def timer_function():
    forget()
    opLabel.config(text = ' ')
    topLabel.config(text='Timer Mode')
    topLabel.grid(row=0, column=0)
    runTime.grid(row=1, column=0)
    powerLevel.grid(row = 2, column=0)
    timeLabel.grid(row=1, column=1)
    powerLabel.grid(row=2, column=1)
    timer_run_button.grid(row=3, column=0, padx=50)


def oscillate_function():
    forget()
    opLabel.config(text = ' ')
    topLabel.config(text='Osiclattion Mode')
    topLabel.grid(row=0, column=0)
    runTime.grid(row=1, column=0)
    restTime.grid(row = 2, column=0)
    timeLabel.grid(row=1, column=1)
    restTimeLabel.grid(row=2, column=1)
    oscillation_number.grid(row=3, column=0)
    oscillation_number_label.grid(row=3, column=1)
    oscillate_run_button.grid(row=4, column=0)
    

def const_function():
    forget()
    opLabel.config(text = ' ')
    topLabel.config(text='Constant Mode')
    topLabel.grid(row=0, column=0)
    powerLevel.grid(row = 1, column=0)
    powerLabel.grid(row=1, column=1)
    const_run_button.grid(row=2, column=0, padx=50)
    


#==========================================================#
#All widgets
#==========================================================#
root.geometry('600x200')
topLabel = Label(frame, text=' ')
opLabel = Label(frame, text=' ')
timerLabel = Label(frame, text=' ')
runTime = Entry(frame)
powerLevel = Entry(frame)
timeLabel = Label(frame, text='Run Time in seconds')
powerLabel = Label(frame, text='Power level in %')
#shutoff = Button(frame, text='Shutoff', padx=50, command=lambda: shut_off(mode), width=10, height=1)
restTime = Entry(frame)
shutoff = Button(frame, text='Shutoff', padx=50, command=lambda: shut_off(mode), width=10, height=1)
restTimeLabel = Label(frame, text='Rest Time in Seconds')
timer_button = Button(frame, text='Timer Mode', command=timer_function, width=20, height=1)
timer_run_button = Button(frame, text='Run', command=timer, width=10, height=1)
oscillate_button = Button(frame, text='Oscillation Mode', command=oscillate_function, width=20, height=1)
oscillate_run_button = Button(frame, text='Run', command=oscillate, width=10, height=1)
const_button = Button(frame, text='Constant Operation Mode', command=const_function, width=20, height=1)
const_run_button = Button(frame, text='Run', command=cont,width=10, height=1)
start_label = Label(frame, text='Select Mode')
home_button = Button(frame, text='Return to Home Screen', command=start_screen, width=20, height=1)
oscillation_number = Entry(frame)
oscillation_number_label = Label(frame, text='Number of Oscillations')
w2 = Scale(frame, from_=0, to=100, length = 200, tickinterval=10, orient=HORIZONTAL)
#==========================================================#
frame.pack()
start_screen()
root.mainloop()

