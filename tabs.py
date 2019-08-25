from tkinter import Tk , LabelFrame , messagebox , Label , StringVar , Frame , Entry , Button , Text , Listbox , Scrollbar , END , MULTIPLE , font
from tkinter.filedialog import askdirectory , askopenfile
from tkinter.ttk import OptionMenu , Combobox;
from os import getcwd , mkdir , path , chmod;
from convertion import changeFormat
from threading import Thread


def createDefaultDirIfNotExists() :
	r = getcwd() + r"\temp_download";
	print(r);
	if not (path.exists(r) and path.isdir(r)) :
		chmod(getcwd() , 0o777);
		mkdir(r);

try :
	import downloadDir
except : 
	createDefaultDirIfNotExists();
	DDIR = getcwd() + r"\temp_download";
else : DDIR = downloadDir.DDIR



class convertTab :
	def __init__(self , root) :
		self.root = root;
		self.conversioning = False;
		self._upperFrame();
		self._lowerFrame()


	def _upperFrame(self) :
		frame = LabelFrame(self.root , text="Paths");
		frame.grid(row=0,column=0,sticky="snew",padx=(5,5),pady=(5,5),ipady=10,ipadx=10);
		frame.columnconfigure(1,weight=5)
		frame.columnconfigure(2,weight=1)
		self.targetLabel = Label(frame,text="Save to",fg="blue", cursor="hand2")
		self.targetLabel.grid(row=0,column=0,sticky="w",padx=(10,10),pady=(15,6));
		self.targetLabel.bind("<Button-1>" , lambda event : self._dirBrowse());
		f = font.Font(self.targetLabel, self.targetLabel.cget("font"))
		f.configure(underline=True)
		self.targetLabel.configure(font=f)
		self.pathLabel = Label(frame , text=DDIR , fg="grey" , anchor="w");
		self.pathLabel.grid(row=0,column=1,sticky="we",padx=(10,10),pady=(15,6),columnspan=2);
		
		Label(frame,text="Files").grid(row=1,column=0,sticky="wn",padx=(10,10),pady=(15,6))
		def addListBox() :
			textFrame = Frame(frame);
			textFrame.grid(row=1,column=1,sticky="ew",padx=(10,10),pady=(15,6),rowspan=3)
			textFrame.columnconfigure(0 , weight=1);
			self.lst = Listbox(textFrame , selectmode = MULTIPLE);
			self.lst.grid(row=0,column=0,sticky="snew");
			scrllx = Scrollbar(textFrame , orient="horizontal" , command=self.lst.xview)
			scrlly = Scrollbar(textFrame , orient="vertical" , command=self.lst.yview);
			self.lst["xscrollcommand"] = scrllx.set;
			self.lst["yscrollcommand"] = scrlly.set;
			scrllx.grid(row=1,column=0 , sticky="snew")
			scrlly.grid(row=0,column=1 , sticky="snew")

		addListBox()
		self.addBtn = Button(frame , text="add" , relief="groove" , command=self._addToListBox)
		self.removeBtn = Button(frame , text="remove" , relief="groove" , command=self._removeFromList)
		self.clearBtn = Button(frame , text="clear" , relief="groove" , command=self._clearList);
		self.addBtn.grid(row=1,column=2,sticky="ews",padx=(5,10),pady=(15,6))
		self.removeBtn.grid(row=2,column=2,sticky="ew",padx=(5,10),pady=(15,6))
		self.clearBtn.grid(row=3,column=2,sticky="ewn",padx=(5,10),pady=(15,6))

	def _fileBrowse(self) :
		get = askopenfile()
		if get != None : 
			if not path.splitext(path.basename(get.name))[1][1:] in ["mp3" , "mp4" , "3gp" ,"wav" ,"m4a" ,"flac" ,"wma" ,"acc" ,"ogg" ,"mp2" ,"amr" , "webm" , "gif"] : 
				messagebox.showerror("media error" , "the type of the file is not allowed");
			else : self.lst.insert(0,get.name);


	def _dirBrowse(self) :
		get = askdirectory();
		if get != "" : self.pathLabel.config(text=get);


	def _clearList(self) :
		for i in range(self.lst.size()) :
			self.lst.delete(i , END);

	def _removeFromList(self) :
		items = self.lst.curselection()
		pos = 0
		for i in items :
			idx = int(i) - pos
			self.lst.delete( idx,idx )
			pos = pos + 1
		self._colorListBox()

	def _addToListBox(self) :
		self._fileBrowse();
		self._colorListBox()

	def _colorListBox(self) :
		for i in range(self.lst.size()) :
			if i % 2 == 1 :
				self.lst.itemconfig(i,{"bg":"#e8dada"})
			else : 
				self.lst.itemconfig(i,{"bg":"#FFF"})

	
	#mp3 wav m4a flac wma acc ogg mp2 amr
	def _lowerFrame(self) :
		frame = LabelFrame(self.root,text="Conversion");
		frame.grid(row=1,column=0,sticky="snew",padx=(5,5),pady=(5,5),ipady=10,ipadx=10);
		#frame.columnconfigure(0,weight=1)
		frame.columnconfigure(1,weight=1)
		frame.rowconfigure(2,weight=1)
		text = "You can change the type of media files, by giving their path at the previous step,\nthen choose the new format of them, we have design it to be very easy for novice users it's just one click to go";
		lbl = Label(frame,text=text,justify="center")
		lbl.grid(row=0,column=0,sticky="we",padx=(10,10),pady=(15,20),columnspan=2)
		Label(frame,text="choose profile ").grid(row=1,column=0,padx=(10,10),sticky="w")
		def addOptionMenu(row , col) :
			self.format = StringVar(frame);
			options = ["mp3" , "mp4" ,"wav" ,"m4a" ,"flac" ,"wma" ,"acc" , "3gp" ,"ogg" ,"mp2" ,"amr" , "webm" , "gif"];
			self.format.set(options[0]);
			optionMenu = Combobox(frame , textvariable=self.format  , state="readonly" , values=options);
			optionMenu.grid(row=row,column=col,sticky="we",ipady=1,padx=(10,10));

		addOptionMenu(1 , 1);
		self.convertBtn = Button(frame,text="Convert",relief="groove",command=lambda : self._startNewThread(self._conversion,()))
		self.convertBtn.grid(row=2,column=1,sticky="se",columnspan=2,padx=(10,10),pady=(10,5),ipady=2,ipadx=3);
		self.convertInfo = Label(frame,text="");
		self.convertInfo.grid(row=2,column=0,sticky="sw",padx=(10,10),pady=(10,5),ipady=2,ipadx=3)

	def _startNewThread(self , func , args) :
		thrd = Thread(target=func ,args=args)
		thrd.setDaemon(True);
		thrd.start();

	def _conversion(self) :
		total = self.lst.size();
		self.convertBtn.configure(state="disabled");
		if total == 0 : return;
		success = 0;
		failed  = 0;
		files = [];
		f = self.format.get();
		for index in range(total) :
			files.append(self.lst.get(index));
		
		for index in range(len(files)) :
			self.convertInfo.configure(text="please wait "+ str((index+1)) + " of " + str(total) + " ...")
			result = changeFormat(files[index] , self.pathLabel.cget("text") , f);
			if result == False : failed += 1;
			elif result == True : success += 1;
		
		self.convertInfo.configure(text="total: "+str(total) + " success: " + str(success) + " failed: " + str(failed));
		self.convertBtn.configure(state="active");
		



"""
def _upperFrame(self) :
		frame = LabelFrame(self.root , text="Paths");
		frame.grid(row=0,column=0,sticky="snew",padx=(5,5),pady=(5,5),ipady=10,ipadx=10);
		frame.columnconfigure(1,weight=1);	
		Label(frame,text="Add new file name ").grid(row=0,column=0,sticky="we",padx=(10,10),pady=(15,6));
		self.newNameEntry = Entry(frame,font=("Consolas",10));
		self.newNameEntry.grid(row=0,column=1,ipady=2,sticky="we",padx=(10,10),pady=(15,6),columnspan=2)
		Label(frame,text="File path* ").grid(row=1,column=0,sticky="we",padx=(10,10),pady=(15,6));
		self.filePathEntry = Entry(frame,font=("Consolas",10));
		self.filePathEntry.grid(row=1,column=1,ipady=2,sticky="we",padx=(10,10),pady=(15,6))
		Label(frame,text="Save to* ").grid(row=2,column=0,sticky="we",padx=(10,10),pady=(15,6));
		self.dirPathEntry = Entry(frame,font=("Consolas",10));
		self.dirPathEntry.insert(0 , DDIR)
		self.dirPathEntry.grid(row=2,column=1,ipady=2,sticky="we",padx=(10,10),pady=(15,6))
		self.changeFileBtn = Button(frame,text="Browse",relief="groove",command=self._fileBrowse)
		self.changeFileBtn.grid(row=1,column=2,sticky="we",pady=(15,6),padx=(0,10),ipadx=15);
		self.changeDirBtn = Button(frame,text="Browse",relief="groove",command=self._dirBrowse)
		self.changeDirBtn.grid(row=2,column=2,sticky="we",pady=(15,6),padx=(0,10),ipadx=15);

		#self.saveBtn = Button(frame , text="attach" , relief="groove")
		#self.saveBtn.grid(row=3,column=0,sticky="we",pady=(15,6),padx=(0,10),ipadx=15)

"""
"""
root = Tk();
text = Text(root , wrap="none");
text.grid(row=0,column=0);

scrlly = Scrollbar(root , command=text.yview);
scrllx = Scrollbar(root , orient="horizontal" , command=text.xview);

text["xscrollcommand"] = scrllx.set
text["yscrollcommand"] = scrlly.set

scrllx.grid(row=1,column=0,sticky="snew");
scrlly.grid(row=0,column=1,sticky="snwe");

root.mainloop()
"""

"""
root = Tk();

v = ["asdasdasdasdasdasddfsdfwerqweqwe","asd","asd","asd","asd","asd","asd","asd","asd","asd"]

lst = Listbox(root);

for i in range(10) :
	lst.insert(i , v[i]);

lst.grid(row=0,column=0);


scrllx = Scrollbar(root , orient="horizontal" , command=lst.xview)
scrlly = Scrollbar(root , orient="vertical" , command=lst.yview);

lst["xscrollcommand"] = scrllx.set;
lst["yscrollcommand"] = scrlly.set;
scrllx.grid(row=1,column=0 , sticky="snew")
scrlly.grid(row=0,column=1 , sticky="snew")

root.mainloop();
"""


