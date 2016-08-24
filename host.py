import datetime
import sys
import getopt
import time
import pdb
endT=100
class host:
    
    def println(self,output):
    		now = datetime.datetime.now()
		print str(now) +" host"+self.hostId[0]+" "+output
		#System.out.println("host "+self.hostId[0]+" "+dateFormat.format(date)+ " " + output)
		
    def __init__(self,hostId,lanId, Type, timeToStart=None,period=0):
    	self.hostId = hostId,
    	self.lanId = lanId,
    	self.type=Type,
    	self.timeToStart = timeToStart,
    	self.period=period,
    	self.hInFile="hin"+hostId+".txt",
    	self.hOutFile="hout"+hostId+".txt",
	self.countL=0
    
    
    def advertiseRcvr(self):
		fw = open(self.hOutFile[0],"a")			
		fw.write("receiver "+ self.lanId[0] +"\n")
		fw.close() 
	 
    def checkLanX(self): 
	    count=0
	    f = open("lan"+self.lanId[0]+".txt","a")	    		      
	    f.close();
    	
	    f = open("lan"+self.lanId[0]+".txt")
	    line = f.readline()
	    while (line):
		if(count < self.countL):
			count = count +1
			line=f.readline()
	    		continue
	    	else:
			count = count +1
			self.countL=self.countL+1
			if(self.type[0].__eq__("receiver") and line.__contains__("data")):
			    	fw = open(self.hInFile[0],"a")
			    	fw.write(line)
			    	fw.close()
			line=f.readline()
	    f.close()
	 

    def sendData(self):
		fw = open(self.hOutFile[0],"a")			
		self.println("sent data.")
		fw.write("data "+ self.lanId[0]+" "+self.lanId[0]+"\n")
		fw.close() 
	 
    def start(self) :
    		startT=0
		if(self.type[0].__eq__("sender")):
			startT=int(self.timeToStart[0])
			time.sleep(int(self.timeToStart[0]))
		
		
		for t in range(startT,endT):						
			if(self.type[0].__eq__("sender") and (t%int(self.period[0]) == 0)):    		    		
				self.sendData()				
    	
    			elif(self.type[0].__eq__("receiver")):
    				if(t%10 == 0):
    					self.advertiseRcvr()    				
    				self.checkLanX()    				
			time.sleep(1)
			
def main(argv):
    			if(sys.argv[3].__contains__("sender")):
    				obj = host(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5])
    			else:
    				obj = host(sys.argv[1],sys.argv[2],sys.argv[3])
			obj.start()
    
    
if __name__ == "__main__":
    main(sys.argv)
