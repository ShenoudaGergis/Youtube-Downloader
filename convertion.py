import ffmpy3;
from os import path;

def extractNewFileName(inputs , format_) :
	fileName = path.basename(inputs);
	absName = path.splitext(fileName)[0];
	return absName+"."+format_;


def changeFormat(inputs , outputsDir , format_) :
	try :
		ff = ffmpy3.FFmpeg(
				inputs={inputs:None},
				outputs={outputsDir+"/"+extractNewFileName(inputs,format_):None}
			)
		ff.run()
		return True;
	except : 
		return False;


#print(changeFormat("F:/from youtube/أبونا فلتاؤس السريانى - بيعمل القهوة للاباء فى القلاية بنفسه.webm" , "F:" , "mp4"))