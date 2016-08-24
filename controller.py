import datetime
import sys
import getopt
import time
import pdb 
startT=0
endT=100
class controller :
	routList= [],
	hList= [],
	routList= [],
	houtList=[],
	rList= [],
	lanList= [],
	rcvrList=[],
	rcvrLanList = {},
	senderLanList = {},
	countMap = {}

	def println(self, output):		
	 	now = datetime.datetime.now()
		print "cont "+str(now)+" "+output
	        #System.out.println("host "+self.hostId+" "+dateFormat.format(date)+ " " + output)

	
	def checkNewMsg(self) :		
	   	for i in range(0,self.houtList[0].__len__() ):
	   		f = open(self.houtList[0][i],"a")
			f.close()
	   		count=0
	    		f = open(self.houtList[0][i])
	    		line = f.readline()
	    		countContL=self.countMap[self.houtList[0][i]]
	    		while (line) :
				
	    			if(count < countContL):
	    				count=count+1
					line=f.readline()
	    				continue
	    			else:
					self.println("from "+self.houtList[0][i]+": count:"+str(count)+",countContL:"+str(countContL)+">"+line)
			    		countContL=countContL+1
			    		count=count+1				    		
			    		fw = open("lan"+line.split(" ")[1].strip("\n")+".txt","a")
	   				fw.write(line)
	   				fw.close()					        
					line=f.readline()
	    		self.countMap[self.houtList[0][i]] = countContL
	    		f.close()
	    	
	   	for i in range(0,self.routList[0].__len__()):
	   		f = open(self.routList[0][i],"a")
			f.close()
	   		count=0
	    		f = open(self.routList[0][i])
	    		line=f.readline()
	    		countContL=self.countMap[self.routList[0][i]]				
			while (line) :
			    if(count < countContL):
	    			count=count+1
				line=f.readline()
	    			continue
	    		    else:
			    	countContL=countContL+1
			    	count=count+1			    		
			    	fw = open("lan"+line.split(" ")[1]+".txt","a")
	   			fw.write(line)
	   			fw.close()	
			    line=f.readline()
	    		self.countMap[self.routList[0][i]]=countContL
	    		f.close()
	
	   
	def start(self):
		for t in range(startT,endT):			
			self.checkNewMsg()
			time.sleep(1)
			
def main(argv):
	    argvLen=sys.argv.__len__()
	    obj = controller()
	    level=""
	    for i in range(1,argvLen):
		if(sys.argv[i].__contains__("host")):
			level="host"
		elif(sys.argv[i].__contains__("router")):
			level="router"
		elif(sys.argv[i].__contains__("lan")):
			level="lan"
		else:
			if(level.__contains__("host")):
				obj.houtList[0].append("hout"+sys.argv[i]+".txt")
				obj.hList[0].append(sys.argv[i])
				controller.countMap["hout"+sys.argv[i]+".txt"]=0					
			elif(level.__contains__("router")):
				obj.routList[0].append("rout"+sys.argv[i]+".txt")
				obj.rList[0].append(sys.argv[i])					
				controller.countMap["rout"+sys.argv[i]+".txt"]=0
			elif(level.__contains__("lan")):
				obj.lanList[0].append(sys.argv[i])
	    obj.start()

if __name__ == "__main__":
    main(sys.argv)
