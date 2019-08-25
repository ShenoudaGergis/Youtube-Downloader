from tkinter import Tk , Toplevel , Frame , LabelFrame , Menu , Entry , Label , Button , Scrollbar , Listbox , PhotoImage , END
from tkinter import messagebox as msg;
from tabs import convertTab;
from imgLabel import imagedLabel;
from download import video;
from threading import Thread
from time import sleep
from urllib.request import HTTPError , URLError
from tkinter.filedialog import askdirectory;
from tkinter import ttk as k;
from PIL import ImageTk
from entryWithPlaceholder import add_placeholder_to;
#from os.path import dirname , realpath , isdir , exists
from os import getcwd , mkdir , path , chmod;
from history import History;
from playsound import playsound

def createDefaultDirIfNotExists() :
	r = getcwd() + r"\temp_download";
	print(r);
	if not (path.exists(r) and path.isdir(r)) :
		mkdir(r);

try :
	import downloadDir
except : 
	createDefaultDirIfNotExists();
	DDIR = getcwd() + r"\temp_download";
else : DDIR = downloadDir.DDIR

class MainWin(Tk) :

	downloadVideo = video();
	
	def __init__(self, title , *args , **kwargs) :
		Tk.__init__(self,*args,**kwargs);
		self.minsize(500,600)
		self.last = History();
		self.downloadDir = DDIR;
		self.title(title + " - " + self.downloadDir);
		self.downloading = False;
		self.protocol("WM_DELETE_WINDOW", self._onClose)
		try : self.iconbitmap("icons/ytb.ico")
		except : pass;		
		self._mainmenu()
		self._tabs()
		self.columnconfigure(0, weight=1)
		self.rowconfigure(0, weight=1)
		self._upperEntries();
		self._defaultFrames();
		self._downloadingFrame()
		self._metaDataFrame()
		convertTab(self.converter)


	def _onClose(self) :
		if self.downloading == True :
			ans = msg.askyesno("quit" , "your downloading hasn't finished yet are your sure to quit ?");
			if ans == True : self.last.write("n" , self.url);self.destroy();
			else : return;
		else : self.destroy()


	def popupmsg(self):
		msg = "jesus christ"
		popup = Tk()
		popup.geometry("600x200")
		popup.wm_title("jesus christ")
		def listBox() :
			scrollbar = Scrollbar(popup)
			scrollbar.grid(row=0,column=1,sticky="ns")
			listbox = Listbox(popup)
			listbox.grid(row=0,column=0,sticky="snew")
			listbox.config(yscrollcommand=scrollbar.set)
			scrollbar.config(command=listbox.yview)
			self.columnconfigure(0,weight=1)
			self.rowconfigure(0,weight=1)
			def addLogsToListBox() :
				i = 0;
				for log in self.last.read() :
					listbox.insert(END, log.replace("\n",""));
					if i % 2 == 1 :
						listbox.itemconfig(i,{"bg":"#e8dada"})
					i += 1;
			addLogsToListBox();
		listBox()
		popup.columnconfigure(0,weight=1)
		popup.rowconfigure(0,weight=1)


		popup.mainloop()


	def _startNewThread(self , func , args) :
		thrd = Thread(target=func ,args=args)
		thrd.setDaemon(True);
		thrd.start();


	def _mainmenu(self) :
		mainM = Menu(self);
		self.config(menu=mainM);
		sub1 = Menu(mainM , tearoff=False);
		mainM.add_cascade(label="  File  " , menu=sub1);
		sub1.add_command(label="Change Download Path  ",command=self._changeDownloadPath);
		sub1.add_command(label="History            ",command=self.popupmsg);
		sub1.add_command(label="Exit                  ",command=self.destroy);
		self._sub1 = sub1;
		sub2 = Menu(mainM , tearoff=False);
		mainM.add_cascade(label="  Help  " , menu=sub2);
		#add list of command here for <Help>
		sub2.add_command(label="About us               " , command=None);
		sub2.add_command(label="Application manual               " , command=None);
		self._mainM = mainM;


	def _tabs(self) :
		note = k.Notebook(self);
		note.grid(row=0 , column=0 , sticky="snew");
		note.columnconfigure(0,weight=1);
		self.videof = Frame(self);
		self.plist  = Frame(self);
		self.converter = Frame(self);
		note.add(self.videof , text="Video");
		note.add(self.plist  , text="Playlist");
		note.add(self.converter , text="Convert");
		self.videof.columnconfigure(0,weight=1)
		self.plist.columnconfigure(0,weight=1)
		self.converter.columnconfigure(0,weight=1)
		self.converter.rowconfigure(1,weight=1)

	def _changeDownloadPath(self) :
		folder = askdirectory(initialdir=self.downloadDir);
		if folder == "" : pass;
		else : 
			self.downloadDir = folder
			self.title("jesus - " + self.downloadDir)
			self.pathEntry.delete(0,END);
			self.pathEntry.insert(0,self.downloadDir)
			
	def _upperEntries(self) :
		frame = LabelFrame(self.videof,text="Paths");
		frame.grid(row=0,column=0,sticky="we",ipady=10,pady=(5,5),padx=(5,5),ipadx=10);
		frame.columnconfigure(1,weight=1);

		self.urlEntry = Entry(frame,font=("Consolas",10));
		self.urlEntry.grid(row=0,column=0,ipady=2,sticky="we",padx=(10,10),pady=(15,6),columnspan=2);
		Label(frame,text="Save to").grid(row=1,column=0,padx=(10,0))
		self.pathEntry = Entry(frame,font=("Consolas",10));
		self.pathEntry.grid(row=1,column=1,ipady=2,sticky="we",padx=(10,10),pady=6);
		self.pathEntry.insert(0,self.downloadDir)
		add_placeholder_to(self.urlEntry , "add youtube video url...")

		self.checkBtn = Button(frame,text="attach",relief="groove",command=self._checkEntries)
		self.checkBtn.grid(row=0,column=2,sticky="we",pady=(15,6),padx=(0,10),ipadx=15,ipady=1);

		chngdir = Button(frame,relief="flat",command=self._changeDownloadPath)
		chngdir.grid(row=1,column=2,padx=(0,10),sticky="w")
		try :
			image = PhotoImage(file="icons/dir.png");
			chngdir.image = image;
			chngdir.configure(image=image);
		except :
			chngdir.configure(text="...",relief="groove")


	def _checkEntries(self) :
		data = self.urlEntry.get();
		if data.replace(" ","") == "" : return;
		data = data.replace(" ","");
		allSols = [
			"https://www.youtube.com/watch?v=",
			"http://www.youtube.com/watch?v=",
			"www.youtube.com/watch?v=",
			"youtube.com/watch?v="
		];
		flag = False;
		for sol in allSols :
			if data.startswith(sol) :
				flag = True;
		if flag == False : msg.showerror("URL Error","please enter valid URL youtube video");
		else : 
			save = self.pathEntry.get();
			if save.replace(" ","") == "" : return;
			if not (path.exists(save) and path.isdir(save)) : msg.showerror("Directory Error","the directory specified not found"); 
			else :
				try :
					self.checkBtn.config(text="wait..",state="disabled");
					MainWin.downloadVideo.setLink(data);
				except HTTPError : 
					msg.showerror("Network Error" , "No network available at this time or path not resolved")
				except URLError : 
					msg.showerror("Network Error" , "No network available at this time or path not resolved")
				except Exception as e:
					msg.showerror("URL Error","No network available at this time or path not resolved " + str(e));
				else :
					self.url  = data;
					self.path = save;
					self._viewMetadata()
					streams = [];
					for s in MainWin.downloadVideo.getStreams() :
						stream = str(s);
						sol = "";
						sol = stream.split(":")[0] + " " + stream.split(":")[1].split("@")[0] + " " + stream.split(":")[1].split("@")[1];
						streams.append(sol)
					self.combo.config(state="readonly" , values=streams)
					self.combo.set(streams[0])
					if self.downloading == False : 
						self._startNewThread(lambda : playsound("notification/canDownload.mp3"),());
						self.downloadBtn.config(state="active")
					print(self.url , " " , self.path);
				finally : self.checkBtn.config(text="attach",state="active");

	def _viewMetadata(self) :
		def formateTitle(title) :
			formatted = "";
			for index in range(len(title)) :
				if index % 34 == 0 and index != 0 : 
					if title[index] != " " : formatted += "-"
					formatted += "\n"+title[index]
				else : formatted += title[index];
			return formatted;

		metadata = MainWin.downloadVideo.getMetaData();
		self.metaLabels[0].config(text=metadata["author"])
		self.metaLabels[1].config(text=metadata["duration"])
		self.metaLabels[2].config(text=metadata["category"])
		self.metaLabels[3].config(text=metadata["published"])
		self.metaLabels[4].config(text=metadata["likes"])
		self.metaLabels[5].config(text=metadata["dislikes"])
		self.metaLabels[6].config(text=metadata["rating"])
		self.metaLabels[7].config(text=metadata["viewcount"])
		self.metaLabels[8].config(text=formateTitle(metadata["title"]))
		self.metaLabels[-1].destroy();
		self.metaLabels.pop();
		self.metaLabels.append(imagedLabel(self.mFrame , MainWin.downloadVideo.getThumbURL()));
		self.metaLabels[-1].grid(row=0,column=0,pady=(15,0),padx=(10,10))


	def startDownload(self) :
		choice = self.combo.get();
		choice = choice.split();
		#choice now is ["normal" , "mp4" , "480x360"];

		for s in MainWin.downloadVideo.getStreams() :
			if s.mediatype == choice[0] and s.extension == choice[1] and s.quality == choice[2] :  
				print("downloading : " , s.mediatype , s.extension , s.quality)
				try :
					self.downloading = True;
					MainWin.downloadVideo.download(self , self.path , s , self.progressBarCallback);
					self.last.write("s" , self.url);
				except HTTPError : 
					msg.showerror("Network Error" , "No network available at this time or path not resolved")
					self.last.write("e" , self.url);
				except URLError : 
					msg.showerror("Network Error" , "No network available at this time or path not resolved")
					self.last.write("e" , self.url);
				except PermissionError :
					msg.showerror("Saving Error" , "Cant't download your file in the given path , permission denied")
					self.last.write("e" , self.url);
				except MemoryError :
					msg.showerror("Memory Error" , "Not enough memory");
					self.last.write("e" , self.url);
				except FileExistsError : 
					msg.showerror("Error" , "the files name is already found in the given path")
					self.last.write("e" , self.url);
				except : 
					msg.showerror("Error" , "An error accurred")
					self.last.write("e" , self.url);
				finally :
					self.downloadBtn.config(state="active")
					self.progress["value"] = 0;
					self.downloading = False;
				break;


	def progressBarCallback(self,total, recvd, ratio, rate, eta) :
		self.downloaded.config(text="Downloaded " + " :  " + str(recvd / 1024 / 1024)[:4] + " MB" + "  Of  " + str(total / 1024 / 1024)[:4] + "  ETA: " + str(eta / 60)[:4] + " Min");
		self.netRate.config(text="[ " + str(rate)[:4] + " kbps ]");
		self.progRate.config(text="[ " + str(ratio*100).split(".")[0] +" % ]");
		self.progress["value"] = float(str(ratio*100).split(".")[0])


	def threadedDownloading(self) :
		self._startNewThread(self.startDownload , ())


	def _defaultFrames(self) :
		frame = LabelFrame(self.videof,text="Video metadata")
		frame.grid(row=2,column=0,sticky="we",padx=(5,5),pady=(5,5),ipady=10,ipadx=10);
		self.mFrame = frame;
		frame = LabelFrame(self.videof , text="Downloading");
		frame.grid(row=3,column=0,sticky="snew",padx=(5,5),pady=(5,5),ipady=10,ipadx=10)
		self.videof.rowconfigure(3,weight=1)
		self.dFrame = frame;


	def _downloadingFrame(self) :
		self.progress=k.Progressbar(self.dFrame,orient="horizontal",mode='determinate')
		self.progress["value"] = 0;
		#self.dFrame.rowconfigure(1,weight=1)
		#self.dFrame.rowconfigure(0,weight=1)
		self.dFrame.rowconfigure(2,weight=1)
		#self.dFrame.columnconfigure(0,weight=1)
		self.dFrame.columnconfigure(1,weight=1)
		Label(self.dFrame,text="Options").grid(row=0,column=0,sticky="w",padx=(10,0))
		self.combo = k.Combobox(self.dFrame , values=["jesus","christ","mariam","karas"],state='disabled');
		self.combo.grid(row=0,column=1,sticky="e",columnspan=2,padx=(0,10),pady=(5,15))
		self.combo.set("Select : ")

		self.progress.grid(row=2,column=0,sticky="wen",padx=(10,10),pady=(5,5),columnspan=3);
		self.netRate = Label(self.dFrame,text="[ -- ]")
		self.netRate.grid(row=1,column=1,sticky="es");
		self.progRate = Label(self.dFrame,text="[ -- ]")
		self.progRate.grid(row=1,column=2,sticky="es",padx=(0,10));
		self.downloaded = Label(self.dFrame,text="Downloaded :  --  Of  --  ETA :  --")
		self.downloaded.grid(row=1,column=0,sticky="ws",padx=(10,10));
		self.downloadBtn = Button(self.dFrame,command=self.threadedDownloading,text="Download",state="disabled",relief="groove")
		self.downloadBtn.grid(row=3,column=1,sticky="se",columnspan=2,padx=(10,10),pady=(10,5),ipady=2,ipadx=3)
		#self.cancelBtn = Button(self.dFrame,text="Cancel",state="disabled",relief="groove")
		#self.cancelBtn.grid(row=3,column=0,sticky="se",columnspan=2,padx=(10,50),pady=(10,5),ipady=2,ipadx=10)


	def _metaDataFrame(self) :
		def label(root,text) :
			return Label(root,text=text,font=("Consolas","10","italic"));
		#http://i.ytimg.com/vi/j2Obuh4Sv9A/default.jpg
		#imgLbl = imagedLabel(self.mFrame, "https://dummyimage.com/160x110/875d87/000000.png&text=++No+Video");
		imgLbl = Label(self.mFrame);
		imgLbl.grid(row=0,column=0,pady=(15,0),padx=(15,15))
		try :
			img = PhotoImage(file="icons/novideo.png")
			imgLbl.image = img;
			imgLbl.configure(image=img)
		except : 
			imgLbl.grid(row=0,column=0,ipadx=70,ipady=40);
			imgLbl.configure(bg="#875d87")
		
		title = label(self.mFrame,"no title")
		title.grid(row=1,column=0,padx=(10,10))

		frame = Frame(self.mFrame)
		frame.grid(row=0,column=1,sticky="snew",rowspan=2,padx=(0,10),pady=(15,0));
		
		lbls = [];
		lblsTxts = [
			"author","duration","category","published","--","--","--","--",
			"likes","dislikes","rating","viewcount","--","--","--","--"
		]
		for i in range(16) :
			lbls.append(label(frame , lblsTxts[i]));
			if i >= 0 and i <= 3 : lbls[-1].grid(row=i,column=0,pady=(8,8));lbls.pop();
			if i >= 4 and i <= 7 : lbls[-1].grid(row=i-4,column=1,pady=(8,8),sticky="w");lbls[-1].config(font=("Consolas",10,"bold italic"))
			if i >= 8 and i <= 11 : lbls[-1].grid(row=i-8,column=2,pady=(8,8));lbls.pop();
			if i >= 12 and i <= 15 : lbls[-1].grid(row=i-12,column=3,pady=(8,8),sticky="w");lbls[-1].config(font=("Consolas",10,"bold italic"))
		self.metaLabels = lbls;
		self.metaLabels.append(title)
		self.metaLabels.append(imgLbl)
	
		self.mFrame.columnconfigure(1,weight=1)
		frame.columnconfigure(0,weight=1)
		frame.columnconfigure(1,weight=1)
		frame.columnconfigure(2,weight=1)
		frame.columnconfigure(3,weight=1)

	def run(self) :
		self.mainloop();

#try :
MainWin("jesus").run()
#except HTTPError : 
	#msg.showerror("Network Error" , "No network available at this time")
#except URLError : 
	#msg.showerror("Network Error" , "No network available at this time")
#except OSError :
	#msg.showerror("Network Error" , "No network available at this time")
#except IOError :
	#msg.showerror("Network Error" , "No network available at this time")
#except Exception as e:
	#msg.showerror("Error" , "sorry, there is an error accurred\n")
