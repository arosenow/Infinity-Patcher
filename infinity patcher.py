from tkinter import filedialog
import tkinter as tk
import re
import math
import os

root = tk.Tk()
root.title("Mod patcher")
root.geometry("300x150")

name_var=tk.StringVar()

# Create Frame widget
#frameL1 = tk.Frame(root, width=100, height=140)
#frameL1.pack(padx=10, pady=5,side='left')

#frameR1 = tk.Frame(root, width=100, height=140)
#frameR1.pack(padx=10, pady=5,side='right')



# Add a button
def on_button_click():
	file_path = tk.filedialog.askdirectory()

	modules = []
	module_end = []
	labels = []
	label_found = []
	save_lines = []
	modname = (file_path.split('/'))[-1] 
	inifound = 0
	modexists = 0

	for file in os.listdir(file_path): 
		if file == modname+".tp2": 
			modexists = 1
			modtp2 = modname+".tp2"
		if file == 'setup-' + modname+".tp2": 
			modexists = 2
			modtp2 = 'setup-' + modname+".tp2"
		if file == modname+".ini": inifound = 1
		

	if modexists > 0:
		with open(file_path+'/'+ modtp2) as f:
			lines = f.readlines()
			for i0 in range(len(lines)): 
				i = lines[i0]
				i = re.sub("\\s+", " ", i)
				i = i.lstrip()

				if i[:1] == '/': continue

				i_n = (lines[min(len(lines)-1,i0+1)]).lstrip()

				check_b = ('BEGIN ~' in i or 'BEGIN @' in i )
                
				check_nb = ('BEGIN ~%' in i or 
                    'BEGIN ~' in i and i_n[:1] == '%' )

				check_begin = check_b and not check_nb

				check_l = ('LABEL ~' in i or 
			   		re.search(r" LABEL \w", ' ' + i) 
					)

				if check_begin: modules.append(i0)
				if check_l: labels.append(i0)

			module_end.extend(modules)
			module_end.append(len(lines)+1)
			module_end.pop(0)

			notmatched = 0
			for i1 in range(len(modules)):
				matched = 0
				for i2 in labels:
					if i2 >= modules[i1] and i2 < module_end[i1]: matched = 1
				if matched == 0: notmatched = notmatched + 1
				label_found.append(matched)
			
			for i3 in range(len(modules)):
				if label_found[i3] == 0:
					lines[modules[i3]] = lines[modules[i3]] + '\tLABEL ~' + modname + 'mc' + str(i3+ 1) + '~\n'

			save_lines.extend(lines)
			
			with open(file_path+'/'+modtp2,'w') as f:
				for line in save_lines:
					f.write(line)

			newini = [
			"""""",
			"""[Metadata]""",
			"""Name = TEMPMODNAME""",
			"""Author = Guy Incognito""",
			"""Description = Substitute ini where it's missing, this mod was not compatible with Project Infinity, but we've tried to fix it""",
			"""Homepage = www.google.com""",
			"""Forum = www.google.com""",
			"""Download = www.google.com""",
			"""LabelType = GloballyUnique""",
			"""Type = """,
			"""Before = """,
			"""After = """, ]

			newini[2] = newini[2].replace("TEMPMODNAME",modname) 

			if inifound == 0:
				with open(file_path+'/'+modname +'.ini','w') as f:
					for line in newini:
						line = line.lstrip()
						line = line + '\n'
						f.write(line)

			if inifound == 1:
				foundlabels = 0
				foundname = 0
				wronglabel = 0
				metadata = 0
				editedini = []
				with open(file_path+'/'+modname +'.ini') as f:
					lines = f.readlines()
					editedini.extend(lines)            
					for i4 in range(len(lines)): 
						i = lines[i4]
						i = re.sub("\\s+", " ", i)
						i = i.lstrip()
						if i[:1] == '#': continue
						if "LABELTYPE = GLOBALLYUNIQUE" in i.upper(): foundlabels = i4 + 1
						if ("LABELTYPE =" in i.upper()) & (foundlabels==0): wronglabel = i4 + 1
						if "NAME =" in i.upper(): foundname = i4 + 1
						if "[METADATA]" in i.upper(): metadata = i4 + 1
					if foundlabels == 0: 
						if metadata == 0: editedini.extend(newini)
						if metadata > 0: editedini[metadata-1] = editedini[metadata-1] + 'LabelType = GloballyUnique\n'
						if wronglabel > 0: editedini[wronglabel-1] = '#' + editedini[wronglabel-1]
					if foundlabels > 0: 
						if metadata == 0: 
							if foundname == 0: editedini[foundlabels-1] = '[Metadata]\n'  + editedini[foundlabels-1]
							if foundname > 0: editedini[foundname-1] = '[Metadata]\n'  + editedini[foundname-1]

				with open(file_path+'/'+modname +'.ini','w') as f:
					for line in editedini:
						line = line.lstrip()
						if line != ' ': line + '\n'
						f.write(line)

			my_label.config(text="Mod Patched\n"+ file_path,wraplength=139)
			my_label.pack(pady=5) # Add some padding

		if modexists == 0:
			my_label.config(text="Mod Not Found",wraplength=139)
			my_label.pack(pady=5) # Add some padding

#Add a text entry gfield
#entry = tk.Entry(frameL1,text='Hi',textvariable = name_var)
#entry.pack()

my_button = tk.Button(root, text="Select Mod Path", command=on_button_click)
my_button.pack(pady=15)

my_label = tk.Label(root, text="Select the directory of your weidu mod files, where the tp2 is located",wraplength=139)
my_label.pack(pady=5)

# Start the event loop
root.mainloop()
