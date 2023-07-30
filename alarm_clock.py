import PySimpleGUI as sg
import time
import random
import pygame
import pytz
from pygame import mixer
from datetime import datetime
sg.theme("GreenMono")

pygame.init()

# ORIGINAL ALARM LOAD
# try:
# 	mixer.music.load('sounds/alarm_tone.mp3')
# except:
# 	mixer.musice,load('sounds/alarm_tone.wav')


list_of_alarms = []
list_of_sounds = ['sounds/alarm_tone.mp3', 'sounds/Angelipad.mp3', 'sounds/SoftPiano.mp3', 'sounds/TrapLoop.mp3']

sound_loaded = False

def get_time():
	global list_of_alarms
	now = time.strftime("%H:%M:%S")
	green = datetime.now(pytz.timezone('Etc/GMT-2')).strftime('%H:%M:%S')
	ny = datetime.now(pytz.timezone('Etc/GMT-4')).strftime('%H:%M:%S')
	cal = datetime.now(pytz.timezone('Etc/GMT-7')).strftime("%H:%M:%S")
	eng =datetime.now(pytz.timezone('Etc/GMT+1')).strftime('%H:%M:%S')
	mos = datetime.now(pytz.timezone('Etc/GMT+3')).strftime('%H:%M:%S')
	india = datetime.now(pytz.timezone('Etc/GMT+5')).strftime('%H:%M:%S')
	viet = datetime.now(pytz.timezone('Etc/GMT+7')).strftime('%H:%M:%S')
	china = datetime.now(pytz.timezone('Etc/GMT+8')).strftime('%H:%M:%S')
	nz = datetime.now(pytz.timezone('Etc/GMT+12')).strftime('%H:%M:%S')
	
	window["-TIME-"].update(now)
	window["-GREEN-"].update(green)
	window["-NY-"].update(ny)
	window["-CAL-"].update(cal)
	window["-ENG-"].update(eng)
	window["-MOS-"].update(mos)
	window["-IND-"].update(india)
	window["-VIET-"].update(viet)
	window["-CHI-"].update(china)
	window['-NZ-'].update(nz)

	if list_of_alarms:
		for index, alarm in enumerate(list_of_alarms):
			if now == alarm:
				mixer.music.play(10)
				window["Stop"].update(disabled = False)
				list_of_alarms = list_of_alarms[index:]
				update()


def confirm_alarm():
	hour_val = values["-HR-"]
	minute_val = values["-MIN-"]
	
	if hour_val and minute_val:
		list_of_alarms.append(f"{hour_val}:{minute_val}:00")
		update()


def stop_alarm():
	mixer.music.stop()
	window['Stop'].update(disabled = True)
	list_of_alarms.pop(0)
	update()


def update():
	window['-LST-'].update("")
	for alarm in list_of_alarms:
		window['-LST-'].update(window['-LST-'].get() + alarm + '\t')


def time_as_int():
	return int(round(time.time()*100))


clock_layout = [
	[sg.Text("", key = '-TIME-', font = ('ds-digital', 100), background_color = 'black', text_color = 'lawn green')]
]


alarm_layout = [
	[sg.Text("Hour", size = (20, 1)), sg.Text('Minute', size = (20, 1))],
	[sg.Input(key = '-HR-', size =(20,3)), sg.Input(key = '-MIN-',size = (20,1)), sg.Button("Alarm Tone", size = (10,3)), sg.Button('Angelipad', size=(10,3))],
	[sg.Text("", size=(37,5), key = '-LST-'), sg.Button("Soft Piano", size = (10,3)), sg.Button('Trap Loop', size=(10,3))],
	[sg.Text(size = (37,1)), sg.Text(key = '-ALARM-', size = (23,1), background_color = 'black', text_color = 'white')],
	[sg.Button("Confirm", size = (17,2), button_color = ('white', 'black')), sg.Button("Stop", size = (17,2), disabled = True, button_color = ('white', 'black')), sg.Button('Random Alarm', size = (23,3))],
]


world_layout = [
	[sg.Text('Greenland', size = (20,1)), sg.Text('England', size = (20,1)), sg.Text('Vietnam', size = (20,1))],
	[sg.Text("", key='-GREEN-', font = ('ds-digital', 10), background_color = 'Black', text_color = 'lawn green'), sg.Text(size = (12,1)), sg.Text("", key='-ENG-', font = ('ds-digital', 10), background_color = 'Black', text_color = 'lawn green'), sg.Text(size = (12,1)), sg.Text("", key='-VIET-', font = ('ds-digital', 10), background_color = 'Black', text_color = 'lawn green')],
	[sg.Text('New York', size = (20,1)), sg.Text('Moscow', size = (20,1)), sg.Text('China', size = (20,1))],
	[sg.Text("", key='-NY-', font = ('ds-digital', 10), background_color = 'Black', text_color = 'lawn green'), sg.Text(size = (12,1)), sg.Text("", key='-MOS-', font = ('ds-digital', 10), background_color = 'Black', text_color = 'lawn green'),  sg.Text(size = (12,1)), sg.Text("", key='-CHI-', font = ('ds-digital', 10), background_color = 'Black', text_color = 'lawn green')],
	[sg.Text('California', size = (20,1)), sg.Text('India', size = (20,1)), sg.Text('New Zealand', size = (20,1))],
	[sg.Text("", key='-CAL-', font = ('ds-digital', 10), background_color = 'Black', text_color = 'lawn green'), sg.Text(size = (12,1)), sg.Text("", key='-IND-', font = ('ds-digital', 10), background_color = 'Black', text_color = 'lawn green'), sg.Text(size = (12,1)), sg.Text("", key='-NZ-', font = ('ds-digital', 10), background_color = 'Black', text_color = 'lawn green')],
]


timer_layout = [
	[sg.Text("0:00", key = '-TIMER-',font = ('ds-digital', 100), background_color = 'black', text_color = 'lawn green')], 
	[sg.Button('Pause',size = (10,2)), sg.Button('Reset', size = (10,2))]
]

layout = [
	[sg.TabGroup([[sg.Tab("Clock", clock_layout), sg.Tab("Alarm", alarm_layout), sg.Tab("World", world_layout), sg.Tab('Timer', timer_layout)]])]
]


window = sg.Window("Clock", layout)    

current_time, paused_time, paused = 0, 0, False
start_time = time_as_int() 

while True:
	
	event, values = window.read(timeout = 10)
	if not paused:
		window.read(timeout = 0)
		current_time = time_as_int() - start_time
	
	if event == sg.WIN_CLOSED:
		break
	if event == 'Confirm':
		confirm_alarm()
	if event == "Stop":
		stop_alarm()

	if event == 'Random Alarm':
		random_alarm = random.choice(list_of_sounds)
		mixer.music.load(random_alarm)
		if random_alarm == "sounds/alarm_tone.mp3":
			window["-ALARM-"].update('Current Alarm: Alarm Tone')
		elif random_alarm == "sounds/Angelipad.mp3":
			window["-ALARM-"].update('Current Alarm: Angelipad')
		elif random_alarm == "sounds/SoftPiano.mp3":
			window["-ALARM-"].update('Current Alarm: Soft Piano')
		elif random_alarm == "sounds/TrapLoop.mp3":
			window["-ALARM-"].update('Current Alarm: Trap Loop')

	if event == 'Alarm Tone':
		mixer.music.load('sounds/alarm_tone.mp3')
		window["-ALARM-"].update('Current Alarm: Alarm Tone')
	
	if event == 'Angelipad':
		mixer.music.load('sounds/Angelipad.mp3')
		window["-ALARM-"].update('Current Alarm: Angelipad')
	
	if event == 'Soft Piano':
		mixer.music.load('sounds/SoftPiano.mp3')
		window["-ALARM-"].update('Current Alarm: Soft Piano')
	
	if event == 'Trap Loop':
		mixer.music.load('sounds/TrapLoop.mp3')
		window["-ALARM-"].update('Current Alarm: Trap Loop')
	
	#TIMER LOGIC
	if event == 'Reset':
		paused_time = start_time = time_as_int()
		current_time = 0
	if event == 'Pause':
		paused = not paused
		if paused:
			paused_time = time_as_int()
		else:
			start_time = start_time + time_as_int() - paused_time
		
		window["Pause"].update('Start' if paused else 'Pause')
	get_time()
	window['-TIMER-'].update('{:02d}:{:02d}:{:02d}'.format((current_time // 100) // 60,(current_time//100) % 60, current_time % 100))

window.close()