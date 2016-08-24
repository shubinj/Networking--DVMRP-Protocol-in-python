import datetime
import sys
import getopt
import time
import pdb

endT=100
initialNMRDelay=120
class router :
	lanConnTotal=0,
	lanConn=[],
	routerId=0,
	countRouterMap={}
	hopMap={}
	parentMap={}

      	def println(self,output):		
		now = datetime.datetime.now()
		print str(now)+" router"+self.routerId+" "+output
		#DateFormat dateFormat = new SimpleDateFormat("HH:mm:ss.SSS")
		#System.out.println("router "+self.routerId+" "+dateFormat.format(date)+ " " + output)
    
	def __init__(self, routerId,argsLen):
		self.routerId=routerId
		self.lanConnTotal=argsLen
		self.nextHopList=[]
		self.hopCountList=[]
		self.lastMsgSeenT={}
		#self.lastMsgSeenT=0
		self.nextHopLanList=[]
		self.lastDVMRPSeenT=0
		self.nmrHash={}
	
		
        def checkRoutLanX(self,t) :
	    	for i in range(0,self.lanConn[0].__len__()):
	    		count=0
	    		f = open("lan"+self.lanConn[0][i]+".txt","a")
			f.close()
	    		f = open("lan"+self.lanConn[0][i]+".txt")
		    	line=f.readline()
		    	countRoutL=self.countRouterMap[self.lanConn[0][i]]
		    	while(line) :				
		    		if(count < countRoutL):
		    			count=count+1
					line=f.readline()
		    			continue
		    		else:
				    countRoutL=countRoutL+1
				    count=count+1
				    rcvrLan=0
				    fw = open("rout"+ self.routerId+".txt","a")
				    if(line.__contains__("data")):				    					    
				    	tmpL = line.split(" ")
					minhopC=10
					tmpR=""
					if not (self.parentMap.has_key(tmpL[2].strip("\n"))):
						self.parentMap[tmpL[2].strip("\n")]=self.lanConn[0][i]
					else:
						if not(self.lanConn[0][i].__contains__(self.parentMap[tmpL[2].strip("\n")])):
							fw.close()
							line=f.readline()
							continue	

					
					tParent="10"
					tHop=10
					if not(self.lanConn[0][i].__contains__(tmpL[2].strip("\n"))):
					   for k1,v1 in self.hopMap.items():
						for k, v in v1.items():
							tmpI=int(tmpL[2].strip("\n"))
							if (v["hCount"][int(tmpI)] < tHop):
								tHop=v["hCount"][tmpI]
								tmpR = k
								tLan=k1
					   if not tLan.__contains__(self.lanConn[0][i]):
					   	line=f.readline()
						fw.close()
						continue
					for j in range (0,self.lanConn[0].__len__()):
					    if self.lanConn[0][j].__contains__(tmpL[1]) or self.lanConn[0][j].__contains__(tmpL[2].strip("\n")):
						continue
					    if (self.nmrHash.has_key(self.lanConn[0][j]) and t-self.nmrHash[self.lanConn[0][j]]<20):
					    	print "cannot forward"
					    	continue

					    if self.hopMap.has_key(self.lanConn[0][j]):
						    minhopC=10
						    tmpR=""

					            for k,v in self.hopMap[self.lanConn[0][j]].items():
							tmpI=int(tmpL[2].strip("\n"))
						 	if (v["hCount"][int(tmpI)] < minhopC):
								minhopC=v["hCount"][tmpI]
								tmpR = k
							elif(v["hCount"][int(tmpI)] == minhopC):
								if(int(k) < int(tmpR)):
									minhopC=v["hCount"][tmpI]
									tmpR=k

					    else:
						    tmpR = self.routerId
					    if(tmpR.__contains__(self.routerId)):
							tmpL[1]=self.lanConn[0][j]
							line = tmpL[0]+" "+tmpL[1]+" "+tmpL[2]							
							fw.write(line)

					    else:
						initialNMRDelay=t
						amParent=0
						minhopC=10
						tmpR=""
						if not(self.lastMsgSeenT.has_key(self.lanConn[0][j])):
							self.lastMsgSeenT[self.lanConn[0][j]]=0
						if not(t-self.lastMsgSeenT[self.lanConn[0][j]]<20):
							tmpI=int(tmpL[2].strip("\n"))
							for k,v in self.hopMap.items():
								for k1,v1 in v.items():
									if(v1["hCount"][tmpI]<minhopC):
										tmpR=k1
										minhopC=v1["hCount"][tmpI]
									elif(v1["hCount"][tmpI]==minhopC):
										tmpR=str(min(int(k1),int(tmpR)))
							if tmpR.__contains__(self.routerId):
								amParent=1
				
							elif not(self.nmrHash.has_key(self.nextHopLanList[tmpI]) and (t-self.nmrHash[self.nextHopLanList[tmpI]] < 20)):
								if(self.hopCountList[tmpI]>0):
									if amParent == 0:
										tmpline="NMR "+self.nextHopLanList[tmpI]+" "+self.routerId+" "+ self.lanConn[0][j]
										fw.write(tmpline+"\n")
										self.nmrHash[self.nextHopLanList[tmpI]] = t


				    elif (line.__contains__("NMR")):
					tmpL = line.strip("\n").split(" ")
				    	self.nmrHash[tmpL[1]]=t
					amParent=0
					maxT=0
					for k,v in self.lastMsgSeenT.items():
						if v > maxT:
							maxT=v


					


					#if not(t-maxT<20):
					for k,v in self.parentMap.items():
							
							minhopC=10
							tmpR=""		
							amParent=0

							tmpI=int(k.strip("\n"))
							for k1,v1 in self.hopMap.items():
								for k2,v2 in v1.items():
									if(v2["hCount"][tmpI]<minhopC):
										minhopC = v2["hCount"][tmpI]
										tmpR=k2
									elif(v2["hCount"][tmpI]==minhopC):
										tmpR=str(min(int(k2),int(tmpR)))
								if tmpR.__contains__(self.routerId):
									amParent=1


						   	if amParent==0:
								if not(self.nmrHash.has_key(self.parentMap[k]) and (t-self.nmrHash[self.parentMap[k]] < 10)):
									tmpline="NMR "+self.parentMap[k]+" "+self.routerId+" "+ tmpL[1]
									fw.write(tmpline+"\n")
									self.nmrHash[self.parentMap[k]] = t

				    elif (line.__contains__("receiver")):
				    	tmpL = line.strip("\n").split(" ")
					#self.lastMsgSeenT[self.lanConn[0][i]]=t
					if self.hopMap.has_key(tmpL[1]):
						minhopC=10
						tmpR=""
						for k,v in self.hopMap[tmpL[1]].items():
							tmpI=int(tmpL[1])
							if (v["hCount"][int(tmpI)] < minhopC):
								minhopC=v["hCount"][tmpI]
								tmpR = k
							elif(v["hCount"][int(tmpI)] == minhopC):
								if(int(k) < int(tmpR)):
									minhopC=v["hCount"][tmpI]
									tmpR=k

					else:
						tmpR=self.routerId

					if tmpR.__contains__(self.routerId):
						self.lastMsgSeenT[self.lanConn[0][i]]=t
						if (self.nmrHash.has_key(self.lanConn[0][i])):
							del self.nmrHash[self.lanConn[0][i]]

				    elif(line.__contains__("DV")):
				    	tmpL=line.strip("\n").split(" ")

					if not(tmpL[2].__contains__(self.routerId)):
						self.lastDVMRPSeenT=t
					if not(self.hopMap.has_key(tmpL[1])):						
						self.hopMap[tmpL[1]]={}
					if not(self.hopMap[tmpL[1]].has_key(tmpL[2])):
						self.hopMap[tmpL[1]][tmpL[2]]={}
						self.hopMap[tmpL[1]][tmpL[2]]["rMap"]={}
						self.hopMap[tmpL[1]][tmpL[2]]["hCount"]={}
					for j in range(3,tmpL.__len__()):
					     if(j%2==1):
					     	if (int(tmpL[j]) < 10):
					    		newI = int(tmpL[j])+1
						else:
							newI = int(tmpL[j])
					     else:
					     	tmpI=(j-3)/2
						if not(self.hopMap[tmpL[1]][tmpL[2]]["hCount"].has_key(tmpI) and self.hopMap[tmpL[1]][tmpL[2]]["hCount"][tmpI] < newI):
					     		self.hopMap[tmpL[1]][tmpL[2]]["hCount"][tmpI]= newI
							self.hopMap[tmpL[1]][tmpL[2]]["rMap"][tmpI]=tmpL[j]
				
							
				    fw.close()
				    line=f.readline()
		    	f.close()
		    	self.countRouterMap[self.lanConn[0][i]]=countRoutL	

	def sendNmr(self,t):
		for i in range (0,self.lanConn[0].__len__()):					
			if not(self.lastMsgSeenT.has_key(self.lanConn[0][i])):
				self.lastMsgSeenT[self.lanConn[0][i]]=0
			if not(t-self.lastMsgSeenT[self.lanConn[0][i]]<20):
				if not((self.nmrHash.has_key(self.lanConn[0][i]) and (t-self.nmrHash[self.lanConn[0][i]] < 10))):
					tmpline="NMR "+self.lanConn[0][i]+" "+self.routerId+" "+ self.lanConn[0][i]
					f=open("rout"+self.routerId+".txt","a")
					f.write(tmpline+"\n")
					f.close()
					self.nmrHash[self.lanConn[0][i]] = t
	 
	def sendDVMRP(self,t) :
		line=""

		for k,v in self.hopMap.items():
		  if not(v.has_key("rcvr")):
		    for key,value in v.items():
			for i in range(0,9):
				if (value.has_key("hCount") and value["hCount"].has_key(i) and value["hCount"][i] < self.hopCountList[i]):
					self.hopCountList[i]=value["hCount"][i]
					#self.nextHopList[i]=value["rMap"][i]
					self.nextHopList[i]=key
					self.nextHopLanList[i]=k
				else:
					if(value.has_key("hCount") and value["hCount"].has_key(i) and value["hCount"][i] == self.hopCountList[i]):
						tmpP=self.nextHopList[i]
						if (int(key) < int(tmpP)):
							self.nextHopList[i]=key
							self.nextHopLanList[i]=k

		for j in range(0,9):
			line=line+" "+str(self.hopCountList[j])+ " "+self.nextHopList[j]
			 
		for i in range(0,self.lanConn[0].__len__()):
			tmpline="DV "+self.lanConn[0][i]+" "+self.routerId+line
			f=open("rout"+self.routerId+".txt","a")
			f.write(tmpline+"\n")
			f.close()


	
	def start(self):    
		for i in  range(0,9):
	            if str(i) in self.lanConn[0]:
		          self.nextHopList.append(self.routerId)
		          self.hopCountList.append(0)
			  self.nextHopLanList.append("-")
		    else:
		          self.nextHopList.append("10")
		          self.hopCountList.append(10)
			  self.nextHopLanList.append("-")


		for t in range(0,endT):			
			self.checkRoutLanX(t)			
			if(t%5==0):
				self.sendDVMRP(t)				
			if(t%10==0 and t>initialNMRDelay):
				self.sendNmr(t)
			time.sleep(1)
	
def main(argv):
		argsLen=sys.argv.__len__()		
		obj = router(sys.argv[1],argsLen)
		#obj.lanConn =
		for i in range(2,argsLen):				
			obj.lanConn[0].append(sys.argv[i])
			obj.countRouterMap[obj.lanConn[0][i-2]]= 0
		obj.start()

if __name__ == "__main__":
    main(sys.argv)
