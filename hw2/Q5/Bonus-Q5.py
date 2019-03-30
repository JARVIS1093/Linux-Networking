  GNU nano 2.5.3                                                                                                                                   File: Q5-3.py                                                                                                                                                                                                                                                                            

import sched, time
import libvirt 
import threading 

global cpu,fcpu
cpu=[]
fcpu=[]

global util, util1, util2, util3, u1, u2, u3, count, uavg
util1=[]
util2=[]
util3=[]
util=[]
uavg=[]
u1=0
u2=0
u3=0
count=1

def funcperf():
 conn=libvirt.open('qemu:///system')


 nodeinfo=conn.getInfo()

 domainNames = conn.listDefinedDomains()
 domainIDs = conn.listDomainsID()

 domcpustats={} 
 dommemstats={}
 count=0
 for domainID in domainIDs:
#  print "#",count
#  print "\n1. Domain ID - ",str(domainID)
  domain=conn.lookupByID(domainID)
  domainNames.append(domain.name)
  state, maxmem, mem, cpus, cput = domain.info()
#  print "\n2. Domain Name - ",domain.name()
#  print "\n4. Domain Max Memory - ",maxmem
#  print "\n5. Domain Memory - ",mem
#  print "\n6. Domain UUID - ",str(domain.UUIDString()) 
#  print "\n7. Domain OS Type - ",str(domain.OSType()),"\n\n"
  cpustat=domain.getCPUStats(True)
  memstat=domain.memoryStats()
  domcpustats[domainID]=cpustat
  dommemstats[domainID]=memstat
  cpu=(domcpustats[domainID])[0]['cpu_time']
  fcpu.append(cpu)
  count+=1
 
#  print domcpustats,"\n\n",dommemstats,"\n\n"
#  print fcpu 


 
for a in range(0,5):
 funcperf() 
#0.02 seconds is the polling interval
 time.sleep(0.02)


#For each iteration
#for k in range(0,i)
for j in range(0,10):
   util1.append((fcpu[j+3]-fcpu[j])*50)
   util2.append((fcpu[j+4]-fcpu[j+1])*50)
   util3.append((fcpu[j+5]-fcpu[j+2])*50)

for k in range(0,4): 
   u1+=util1[k]
   u2+=util2[k]
   u3+=util3[k]

u1=float(u1)
u2=float(u2)
u3=float(u3)


print "\n",(u1/5000000000),"\t",(u2/5000000000),"\t", (u3/5000000000)
print "\n",fcpu

