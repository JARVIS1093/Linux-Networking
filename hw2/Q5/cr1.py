
import datetime
import sys
import time
import libvirt
conn = libvirt.open('qemu:///system')
currentDT=datetime.datetime.now()
domainIDs = conn.listDomainsID()
newlist=[]
dict={}
dictm={}
memlist=[]
intr=int(raw_input("please enter no of iterations"))
param=raw_input("please enter cpu/mem:")
#poll=int(raw_input("please enter polling interval"))
#threshold=int(raw_input("please enter threshold"))
if (param =='cpu'):
        poll=int(raw_input("please enter polling interval"))
        threshold=int(raw_input("please enter threshold"))
        for k in range(1,intr+1):
                for i in domainIDs:
                        dom=conn.lookupByID(i)
                        VM=dom.name()
                        cpu_stats=dom.getCPUStats(True)
                        dict[VM]=cpu_stats[0]['cpu_time']
                newlist.append(dict)
                d=newlist[0]
                print("result of %dth iteration \n " % (k) )
                print(d )
                print("\n")
                sorted_keys = sorted(d, key=lambda x: (d[x]))
                print(" below is the sorted list of VMs as per the CPU usage\n")
                print(sorted_keys)
                f=open("aler.csv", "a")
                #inp=input("enter threshold value")
                print("following VMs are working byond threshold value\n")
                for x in d:
                               if(int(d[x])/1000000000>threshold):
                                       a=[ x, currentDT.strftime("%H:%M;%S"), d[x]]
                                       print(a)
                                       f.write(str(a)+"\n")
                time.sleep(poll)

if (param =='mem'):
        for i in domainIDs:
                dom=conn.lookupByID(i)
                VM=dom.name()
                mem_stats=dom.memoryStats()
                #print(mem_stats)
                dictm[VM]=mem_stats
        memlist.append(dictm)
        d=memlist[0]
        print(d)
        memsorted_keys = sorted(d, key=lambda x: (d[x]['rss']))
        print(memsorted_keys)

conn.close()
exit(0)


