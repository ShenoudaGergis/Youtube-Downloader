from pafy import new , get_playlist;
from io import BytesIO
import urllib
import urllib.request
from tkinter import Tk , Label;
from PIL import Image, ImageTk

def imagedLabel(root , url) :
	with urllib.request.urlopen(url) as u:
	    raw_data = u.read()
	im = Image.open(BytesIO(raw_data))
	image = ImageTk.PhotoImage(im)
	label = Label(root,image=image)
	label.img = image; 
	return label;

#r = Tk();
#lbl = imagedLabel(r , "http://i.ytimg.com/vi/FAPK5NOWObQ/default.jpg");
#lbl.grid(row=0,column=0);
#r.mainloop()