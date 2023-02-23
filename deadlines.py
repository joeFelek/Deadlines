import PySimpleGUI as sg
from datetime import datetime
import webbrowser

links, deadlines, classes, time_left = [],[],[],[]

f = open("info.txt", "r")


for x in f:
	item = x.split()
	
	classes.append(item[0])

	if(item[1] == "N/A"): 
		deadlines.append(None)
		links.append(None)
		time_left.append(None)
		continue

	links.append(item[3])

	date_time_str = item[1]+"/2021" + " " + item[2]
	date_time_obj = datetime.strptime(date_time_str, '%d/%m/%Y %H:%M')
	deadlines.append(date_time_obj)

	time_left.append(date_time_obj - datetime.now())

for i in range(len(deadlines)):
	x = deadlines[i]
	if(not x == None):
		deadlines[i] = x.strftime('%m/%d %I:%M%p').lstrip("0").replace(" 0", " ")

for i in range(len(time_left)):
	x = time_left[i]
	if(not x == None):
		time_left[i] = ("{} days, {} hours".format(x.days, x.seconds//3600))

info = []
for x in range(len(classes)):
	if(deadlines[x] == None):
		info.append("{}\t{}".format(classes[x], deadlines[x]))
	else:
		info.append("{}\t{}\t{}".format(classes[x], deadlines[x], time_left[x]))

for x in info:
	print(x)

layout = [[]]
keys = {}
for x in range(len(info)):
	if(links[x] is not None):
		keys["Link"+str(x)] = links[x] 
		layout.append([sg.Text(info[x]), sg.Text(text = "Link", enable_events = True, key = "Link"+str(x))])
	else:
		layout.append([sg.Text(info[x])])

window = sg.Window('Deadlines', layout, finalize=True, icon='doge.ico')

for x in keys:
	window[x].set_cursor(cursor='hand2')

while True:
    event, values = window.read()
    if event in (None, 'Cancel'):
        break
    if event in keys:
    	webbrowser.open_new(keys[event])
    	print(keys[event])	

window.close()


f.close()