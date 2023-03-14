
from tkinter import *
from tkinter import filedialog as fileD
from tkinter import ttk

from customtkinter import *
import os


root = Tk();

# set up app icon and dimensions 
noteIcon = PhotoImage(file="./Notes.png")
root.iconphoto(True, noteIcon)
root.geometry("512x512")
root.title("NotepadTkinter")



# method to load any text and html files within the same directory
def loadFiles():
	for filename in os.listdir():
		if filename.endswith(".txt") or filename.endswith(".html"):
			with open(filename, "r") as file:
				content = file.read()
				addNote(filename.split('.')[0], content)
				# print(f"Contents of {filename.split('.')[0]}:")
				# print(content)


# method to save a file immediately as a text file
def SaveFile():
	cur = notebook.select()
	val	= tab_dict[cur].get("1.0", "end")
	filename = notebook.tab(cur, "text") + ".txt"
	with open(filename, "w") as file:
		file.write(val)
	file.close()


# method to save a file as per the user preference (.txt and .html prepared)
def SaveAsFile():
	file = fileD.asksaveasfile(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("HTML Files", "*.html"), ("All Files", "*.*")])
	cur = notebook.select()
	val	= tab_dict[cur].get("1.0", "end")
	file.write(val)
	file.close()


# method to open and load any text file onto the app
def OpenFile():
	print("Open File")
	filePath = fileD.askopenfilename(initialdir= "C:\\", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")] )
	if filePath == '':
		return
	file = open(filePath, "r")
	print(file.read())




menuBar = Menu(root)
# root.config(menu=menuBar)
fileMenu = Menu(root, tearoff=0)
menuBar.add_cascade(label="File", menu=fileMenu)
fileMenu.add_command(label="Save", command=SaveFile)
fileMenu.add_command(label="Open", command=OpenFile)
fileMenu.add_separator()
fileMenu.add_command(label="Exit", command=quit)



## Methods ## 

# initialize dictionary to record the current notebook tabs details
tab_dict = {}

# inisialize the notebook tab colours
unselected = "#1f6aa5"
selected = "#144870"

# set up the styling to be applied on the notebook tabs
style = ttk.Style()
style.theme_create( "tab_style", parent="alt", settings={
		"TNotebook": {"configure": {"tabmargins": [0, 0, 0, 0] } },
		"TNotebook.Tab": {
			"configure": {"padding": [10, 5], "background": unselected, "foreground": "white", "width": 15, "anchor": "center"},
			"map":		{"background": [("selected", selected)],
						"expand": [("selected", [1, 1, 1, 0])] } } } )
style.theme_use("tab_style")


# add a "note" or a new notebook tab with a text area in the app
#	name: the name of the note, if not generating a new one
#	content: the content to add in the text area, if any
def addNote(name=None, content=None):
	num = notebook.index(END) + 1

	tab = ttk.Frame(notebook)
	if name == None:
		notebook.add(tab,text="note" + str(num))
	else:
		notebook.add(tab,text=name)

	tabFrame = Frame(tab)
	tabFrame.pack(fill="both", expand=True)

	textArea = CTkTextbox(tabFrame, font=("Calibri", 20), corner_radius=0, fg_color=("white"), text_color="black")
	textArea.grid(row=0, column=0, sticky="nsew")

	if content != None:
		textArea.insert("0.0", content)


	tab_dict[str(tab)] = textArea
	tabFrame.grid_rowconfigure(0, weight=1)
	tabFrame.grid_columnconfigure(0, weight=1)


# display the entry box and button to allow renaming the currently selected notebook tab
def renameEnable():
	renameEnableBtn.pack_forget()
	renameEntry.pack(side="left", padx=(10, 0))
	renameSubmitBtn.pack(side="left", padx=0)

	# automatically populate the entry box with the current note name
	cur = notebook.select()
	val = notebook.tab(cur, "text")
	renameEntry.delete(0, "end")
	renameEntry.insert(0, val)

# rename the currently selected notebook tab based on the entry box
def renameTab():
	renameEnableBtn.pack(side="left", padx=10)
	renameEntry.pack_forget()
	renameSubmitBtn.pack_forget()

	cur = notebook.select()
	old = notebook.tab(cur, "text")
	val = renameEntry.get()
	notebook.tab(cur, text=val)

	# rename the note in the directory as well, if it exists there
	try:
		file = open(old, "w")
		file.close()
		os.rename(old+".txt", val + ".txt")
		os.remove(old)

	except Exception as e:
		os.remove(old)
		print(e)
		return

## -x-x-x- ## 


## Buttons ##

# create a frame for all the 'action' buttons
actionBar = Frame(root)
actionBar.pack()

addNoteBtn = CTkButton(actionBar, text="+ New Note", command=addNote)
addNoteBtn.pack(side="left", padx=10)

SaveBtn = CTkButton(actionBar, text="Save Note", command=SaveFile)
SaveBtn.pack(side="left", padx=10)

renameEnableBtn = CTkButton(actionBar, text="Rename", command=renameEnable)
renameEnableBtn.pack(side="left", padx=10)

renameEntry = Entry(actionBar, text="")
renameEntry.pack_forget()

renameSubmitBtn = CTkButton(actionBar, text="Submit", command=renameTab)
renameSubmitBtn.pack_forget()

## -x-x-x- ## 


## Notebook ##

# method to reset the main option buttons if the notebook tab is changed
def resetScene (event):
	renameEnableBtn.pack(side="left")
	renameEntry.pack_forget()
	renameSubmitBtn.pack_forget()

# specific styling for vertically aligned notebook tabs
style = ttk.Style(root)
style.configure('lefttab.TNotebook', tabposition='wn', background="grey", padding=(0, 0, 0, 0))

# setup the notebook
notebook = ttk.Notebook(root, style='lefttab.TNotebook')
notebook.bind("<<NotebookTabChanged>>", resetScene)
notebook.pack(fill="both", expand=True)

## -x-x-x- ## 


loadFiles();

root.mainloop();