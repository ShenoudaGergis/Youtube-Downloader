from pathlib import Path;
from os import chmod , path , getcwd , makedirs;
from pickle import dump , load;
from datetime import datetime;
from tkinter import Toplevel , Tk , Scrollbar , Listbox , END
import logging
import logging.handlers as handlers

class History :
	def __init__(self) :
		self.fileName = "jesus.bin";
		self.createFileIfNotExists();

	def createFileIfNotExists(self) :
		try :
			file = Path(path.join(getcwd() , "history" , self.fileName));
			if not (file.exists() and file.is_file()) :
				print("file not found");
				directory = Path(path.join(getcwd() , "history"));
				if not (directory.exists() and directory.is_dir()) :
					print("directory not found")
					chmod(getcwd() , 0o777);
					makedirs(path.join(getcwd() , "history"));
				chmod(path.join(getcwd() , "history"),0o777);
				open(path.join(getcwd() , "history" , self.fileName),"w").close();
				chmod(path.join(getcwd() , "history" , self.fileName),0o777);
			else :
				print(path.join(getcwd(),"history",self.fileName))
		except : return;

	def write(self , state , text) :
		self.createFileIfNotExists();
		file = open(path.join(getcwd() , "history" , self.fileName) , "ab");
		if state == "s" : formatted = str(datetime.now()) + " <success> " + text
		elif state == "e" : formatted = str(datetime.now()) + " <error> " + text
		elif state == "n" : formatted = str(datetime.now()) + " <not completed> " + text
		dump(formatted , file);
		file.close();

	def read(self) :
		self.createFileIfNotExists();
		data = [];
		try :
			file = open(path.join(getcwd() , "history" , self.fileName) , "rb");
			while True : data.append(load(file))
		except :
			pass;
		return data;


