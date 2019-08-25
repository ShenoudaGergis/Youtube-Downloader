from pafy import new;

class video :
	def setLink(self , url) :
		self.link = new(url);


	def getMetaData(self) :
		return {
			"author": self.link.author,
			"title": self.link.title,
			"category": self.link.category,
			"duration": self.link.duration,
			"likes": self.link.likes,
			"dislikes": self.link.dislikes,
			"published": self.link.published.split()[0],
			"rating": str(self.link.rating)[:3],
			"viewcount": self.link.viewcount
		}

		
	def getThumbURL(self) :
		return self.link.thumb;

	"""
	def _getStreams(self) :
		streams = {
			"audio"  :[],
			"video"  :[],
			"normal" :[]
		};
		for s in self.link.allstreams :
			if str(s).split(":")[0] == "audio" : 
				streams["audio"].append(s);
			if str(s).split(":")[0] == "video" : 
				streams["video"].append(s);				
			if str(s).split(":")[0] == "normal" : 
				streams["normal"].append(s);
		return streams;


	def getOnlyStreams(self) :
		st = [];
		for type_ in ["audio" , "video" , "normal"] :
			for audio in self._getStreams()[type_] :
				s = str(audio).split(":")[1].split("@")
				st.append([s[0],s[1],audio]);
		return st


	"""
	@staticmethod
	def download(self , downloadPath , stream , callback) :
		self.downloadBtn.config(state="disabled");
		stream.download(filepath=downloadPath,quiet=False,callback=callback);
		self.downloadBtn.config(state="active");
	

	def getStreams(self) :
		return self.link.allstreams;

"""
v = video();
v.setLink("https://www.youtube.com/watch?v=_VzQyxrhgao")
print(v.getStreams())
"""