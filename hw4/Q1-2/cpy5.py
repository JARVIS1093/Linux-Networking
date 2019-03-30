#!/usr/bin/python

from math import *
import subprocess
import os
#import pexpect
with open('./conn1.csv') as f:
  connectivity_mat = f.readlines()
b=[]
print(connectivity_mat)
connectivity_mat = [x.strip() for x in connectivity_mat] 
for x in connectivity_mat:

        b.append(x.split(","))
print(b)
raw_nodes=[]
print(raw_nodes)
for i in b:
        raw_nodes.append(i[0])
        raw_nodes.append(i[1])  
nodes=set(raw_nodes)
node_num = len(nodes)
open('./var_file.yaml', 'w').close() #Clear Previous data
file =open('./var_file.yaml','a')
file.write("container_names:\n")
for node_name in nodes:
  file.write("  - "+node_name+"\n")

## Reading the node names


## Getting the PIDs of nodes
pid={}

for i in b:
  d,e={} , {}  
  output = subprocess.Popen("sudo docker inspect -f '{{.State.Pid}}' "+i[0], stdout=subprocess.PIPE, shell=True)
  (out, err) = output.communicate()
  c1,c2=i[0],i[1]
  d[c1]=out.strip()
  output1 = subprocess.Popen("sudo docker inspect -f '{{.State.Pid}}' "+i[1], stdout=subprocess.PIPE, shell=True)
  (out1, err1) = output1.communicate()
  d[c2]=out1.strip()
  pid.update(d)
  pid.update(e)
print(pid)

pid1=[]
cont=["lc1","lc2","sc1","sc2"]
#print(len(cont))
for i in range(0,len(cont)):
  #d={} , 
  output2 = subprocess.Popen("sudo docker inspect -f '{{.State.Pid}}'  "+cont[i], stdout=subprocess.PIPE, shell=True)

  (out2, err) = output2.communicate()
  pid1.append(out2)  
print("pid1:",pid1)

bridge2ip=1
l3ip=1
bridge1ip=1
vip=5
greip=1
l2ip=1
l3aip=1
l3bip=1
## Creating and Sending the veth links
for x in b:
        if x[2]=="bridge" :

                bridge_name="br"+x[0]+x[1]
                print('Device '+ '"'+bridge_name +'"'+' does not exist.')
                if(os.system("sudo ip link show " + bridge_name)!='Device '+ '"'+bridge_name +'"'+' does not exist.'):
                        print("Inside")
                        os.system("sudo brctl addbr " +  bridge_name)
                        print("1")
                        os.system("sudo ip link set " + bridge_name + " up ")
                        print("2")
                        #os.system("sudo brctl show bridge" + x[0]+x[1])
                        print(" sudo ip link add "+  bridge_name+"lc2 " + " type veth peer name " + " lc2"+bridge_name)

                        os.system(" sudo ip link add "+  bridge_name+"lc2 " + " type veth peer name " + " lc2"+bridge_name)
                        print("3")
                        os.system("sudo  brctl addif " + bridge_name + " " + bridge_name+"lc2")
                        print("4")
                        print("sudo ip link " + bridge_name+"lc2" + " up ")
                        os.system("sudo ip link set " + bridge_name+"lc2" + " up ")
                        print("5")
                        #lc2pid=os.system("sudo docker inspect -f '{{.State.Pid}}' lc2" )
                        #print(lc2pid)
                        #print("6")
                        os.system("sudo ip link set dev lc2"+bridge_name + " netns " + pid1[1] )
                        print("6")
                        os.system("sudo docker exec lc2 ip link set lc2" +bridge_name + " up ") 
                        print("7")
                        os.system("sudo docker exec lc2 ip addr add 30.0.0."+str(l2ip)+"/24 dev "+ "lc2"+bridge_name)
                        print("8")
                        print("inside bridge")
                        #print(i[0])
                        #print(i[1])
                        port1="eth"+x[0]
                        port2=bridge_name+x[0]
                        print("yea")
                        os.system("sudo ip link add "+ port1 + " type veth peer name " + port2)
                        print("yes")
                        #port1_ip = "30.0.0.2/24"+str(bridge2ip)+"/24"
                        #print(pid)
                        #print(pid[i[0]])
                        os.system("sudo ip link set dev "+ port1 + " netns "+pid[x[0]]+" name "+port1+" up")
                        print('9') 
                        os.system("sudo brctl addif " + bridge_name + " " + port2 )
                        print('10')
                        os.system("sudo ifconfig " + port2 + " up " )
                        port3="eth"+x[1]
                        port4=bridge_name+x[1]

                        os.system("sudo ip link add " + port3 + " type veth peer name " + port4)
                        print('11')
                        os.system("sudo docker exec "+x[0]+" ip addr add 30.0.0."+str(l2ip+1)+"/24 dev "+ port1)
                        print('12')

                        #port3_ip = "30.0.0."+str(bridge2ip+1)+"/24"
                        os.system("sudo ip link set dev "+ port3 + " netns "+pid[x[1]]+" name "+port3+" up")
                        print('13')
                        os.system("sudo brctl addif " + bridge_name + " " + port4 )
                        print('14')
                        os.system("sudo ifconfig " + port4 + " up " )
                        print('15')
                        os.system("sudo docker exec "+x[1]+" ip addr add 30.0.0."+str(l2ip+2)+"/24 dev "+port3)
                        print('16')
                        l2ip=l2ip+3
                else:
                        print(" a bridge with same name and same IP subnet already exists. PLease delete the bridge and start  again")
        if x[2]=="L3":
                port1=x[0]+"l1"
                port2="l1"+x[0]
                port3=x[1]+"l2"
                port4="l2"+x[1]
                os.system("sudo ip link add " + port1 + " type veth peer name " + port2)
                print("1")
                os.system("sudo ip link add " + port3 + " type veth peer name " + port4)
                print("2")
                os.system("sudo ip link set " + port1 + " netns "+pid[x[0]])
                print("3")

                os.system("sudo ip link set " + port3 + " netns "+pid[x[1]])
                print("4")
                os.system("sudo ip link set " + port2 + " netns "+pid1[0])
                print("5")
                os.system("sudo ip link set " + port4 + " netns "+pid1[1])
                print("6")
                os.system("sudo docker exec " + x[0]+" ip link set " + port1 + " up ")
                os.system("sudo docker exec " + x[1]+" ip link set " + port3 + " up ")
                os.system("sudo docker exec lc1 ip link set " + port2 + " up ")
                os.system("sudo docker exec lc2 ip link set " + port4 + " up ")
                os.system("sudo docker exec "+x[0]+" ip addr add 32.0.0."+str(l3aip)+"/24 dev " + port1)
                os.system("sudo docker exec "+x[1]+" ip addr add 33.0.0."+str(l3bip)+"/24 dev " + port3)
                os.system("sudo docker exec lc1 ip addr add 32.0.0."+str(l3aip+1)+"/24 dev " + port2)
                os.system("sudo docker exec lc2 ip addr add 33.0.0."+str(l3bip+1)+"/24 dev " + port4)
                os.system("sudo docker exec "+x[0]+" ip route add 33.0.0."+str(l3bip)+" via 32.0.0."+str(l3aip+1)+" dev " + port1)
                os.system("sudo docker exec "+x[1]+" ip route add 32.0.0."+str(l3aip)+" via 33.0.0."+str(l3bip+1)+" dev " + port3)
                os.system("sudo docker exec lc1 ip route add 33.0.0."+str(l3bip)+" via 47.0.0.2 ")
                os.system("sudo docker exec lc2 ip route add 32.0.0."+str(l3aip)+" via 48.0.0.2 ")
                os.system("sudo docker exec sc2 ip route add 33.0.0."+str(l3bip)+" via 48.0.0.1 ")
                os.system("sudo docker exec sc2 ip route add 32.0.0."+str(l3aip)+" via 47.0.0.1 ")
                l3aip=l3aip+2
                l3bip=l3bip+2

        if x[2]=="vxlan":
                os.system("sudo ip netns add n1")
                os.system("sudo ip netns add n2")
                bridge1name="br1n1"
                bridge2name="br1n2"
                os.system("sudo ip netns exec n1 brctl addbr " + bridge1name)
                print("1")
                os.system("sudo ip netns exec n2 brctl addbr "+ bridge2name)
                os.system("sudo ip netns exec n1 ip link set " + bridge1name + " up")
                print("2")
                os.system("sudo ip netns exec n2 ip link set " + bridge2name + " up")
                print("11")
                os.system("sudo ip link add  l1 type veth peer name n1l1")
                print("12")
                os.system("sudo ip link add  l2 type veth peer name n2l2")
                print("13")
                os.system("sudo ip link set l1 netns  " + pid1[0] )
                print("14")
                os.system("sudo ip link set n1l1 netns n1 ")
                print("15")
                os.system("sudo docker exec lc1 ip link set l1 up ")
                print("16")
                os.system("sudo ip netns exec  n1 ip link set n1l1 up")
                print("17")
                os.system("sudo ip link set l2 netns  " + pid1[1] )
                print("18")
                os.system("sudo ip link set n2l2 netns n2 ")
                print("19")
                os.system("sudo docker exec lc2 ip link set l2 up ")
                print("20")
                os.system("sudo ip netns exec n2 ip link set n2l2 up")
                print("21")
                os.system("sudo ip netns exec n1 ip addr add  42.0.0.1/24 dev n1l1 ")
                print("22")
                os.system("sudo ip netns exec n2 ip addr add  42.0.0.3/24 dev n2l2 ")
                print("23")     
                os.system("sudo docker exec lc1 ip addr add  42.0.0.2/24 dev l1 ")
                print("24")
                os.system("sudo docker exec lc2 ip addr add  42.0.0.4/24 dev l2 ")
                #os.system("sudo ip link add " + x[0]+"n1 type veth peer name n1" + x[0])
                #os.system("sudo ip link add " + x[1]+"n2 type veth peer name n2" + x[1])
                #os.system("sudo ip link set " + x[0] +"n1 netns "+ pid[x[0]])
                #os.system
                print("25")
                os.system("sudo docker exec lc1 ip route add 42.0.0.3 dev gretun0")
                print("26")
                os.system("sudo docker exec lc2 ip route add 42.0.0.1 dev gretun1")

                print("inside vxlan")
                print(x[0],x[1])
                port1="eth"+x[0]
                port2="br4"+x[0]
                print("yes")
                os.system("sudo ip link add "+ port1 + " type veth peer name " + port2)
                print("yep")
                port1_ip = "40.0.0."+str(vip)+"/24"
                os.system("sudo ip link set dev "+ port1 + " netns "+pid[x[0]]+" name "+port1+" up")
                print("here")
                os.system("sudo ip link set dev " + port2 + " netns n1  up" )
                port3="eth"+x[1]
                port4="br4"+x[1]
                os.system("sudo ip link add " + port3 + " type veth peer name " + port4)
                print("here2")
                os.system("sudo docker exec "+x[0]+" ip addr add "+port1_ip+" dev "+ port1)
                port3_ip = "40.0.0."+str(vip+1)+"/24"
                os.system("sudo ip link set dev "+ port3 + " netns "+pid[x[1]]+" name "+port3+" up")
                os.system("sudo ip link set dev " +  port4 + " netns n2  up ")
                os.system("sudo docker exec "+x[1]+" ip addr add "+port3_ip+" dev "+port3)
                print("4")
                os.system("sudo ip netns  exec n1 brctl addif br1n1 "+ port2)
                print("5")
                os.system("sudo ip netns  exec n2 brctl addif br1n2 " + port4)
                print("6")
                #os.system("sudo docker exec lc1 ip route add "+ port1_ip + " via 42.0.0.1 dev l1")
        if x[2]=="vxlan":
                os.system("sudo ip netns add n1")
                os.system("sudo ip netns add n2")
                bridge1name="br1n1"
                bridge2name="br1n2"
                os.system("sudo ip netns exec n1 brctl addbr " + bridge1name)
                print("1")
                os.system("sudo ip netns exec n2 brctl addbr "+ bridge2name)
                os.system("sudo ip netns exec n1 ip link set " + bridge1name + " up")
                print("2")
                os.system("sudo ip netns exec n2 ip link set " + bridge2name + " up")
                print("11")
                os.system("sudo ip link add  l1 type veth peer name n1l1")
                print("12")
                os.system("sudo ip link add  l2 type veth peer name n2l2")
                print("13")
                os.system("sudo ip link set l1 netns  " + pid1[0] )
                print("14")
                os.system("sudo ip link set n1l1 netns n1 ")
                print("15")
                os.system("sudo docker exec lc1 ip link set l1 up ")
                print("16")
                os.system("sudo ip netns exec  n1 ip link set n1l1 up")
                print("17")
                os.system("sudo ip link set l2 netns  " + pid1[1] )
                print("18")
                os.system("sudo ip link set n2l2 netns n2 ")
                print("19")
                os.system("sudo docker exec lc2 ip link set l2 up ")
                print("20")
                os.system("sudo ip netns exec n2 ip link set n2l2 up")
                print("21")
                os.system("sudo ip netns exec n1 ip addr add  42.0.0.1/24 dev n1l1 ")
                print("22")
                os.system("sudo ip netns exec n2 ip addr add  42.0.0.3/24 dev n2l2 ")
                print("23")     
                os.system("sudo docker exec lc1 ip addr add  42.0.0.2/24 dev l1 ")
                print("24")
                os.system("sudo docker exec lc2 ip addr add  42.0.0.4/24 dev l2 ")
                #os.system("sudo ip link add " + x[0]+"n1 type veth peer name n1" + x[0])
                #os.system("sudo ip link add " + x[1]+"n2 type veth peer name n2" + x[1])
                #os.system("sudo ip link set " + x[0] +"n1 netns "+ pid[x[0]])
                #os.system
                print("25")
                os.system("sudo docker exec lc1 ip route add 42.0.0.3 dev gretun0")
                print("26")
                os.system("sudo docker exec lc2 ip route add 42.0.0.1 dev gretun1")

                print("inside vxlan")
                print(x[0],x[1])
                port1="eth"+x[0]
                port2="br4"+x[0]
                print("yes")
                os.system("sudo ip link add "+ port1 + " type veth peer name " + port2)
                print("yep")
                port1_ip = "40.0.0."+str(vip)+"/24"
                os.system("sudo ip link set dev "+ port1 + " netns "+pid[x[0]]+" name "+port1+" up")
                print("here")
                os.system("sudo ip link set dev " + port2 + " netns n1  up" )
                port3="eth"+x[1]
                port4="br4"+x[1]
                os.system("sudo ip link add " + port3 + " type veth peer name " + port4)
                print("here2")
                os.system("sudo docker exec "+x[0]+" ip addr add "+port1_ip+" dev "+ port1)
                port3_ip = "40.0.0."+str(vip+1)+"/24"
                os.system("sudo ip link set dev "+ port3 + " netns "+pid[x[1]]+" name "+port3+" up")
                os.system("sudo ip link set dev " +  port4 + " netns n2  up ")
                os.system("sudo docker exec "+x[1]+" ip addr add "+port3_ip+" dev "+port3)
                print("4")
                os.system("sudo ip netns  exec n1 brctl addif br1n1 "+ port2)
                print("5")
                os.system("sudo ip netns  exec n2 brctl addif br1n2 " + port4)
                print("6")
                #os.system("sudo docker exec lc1 ip route add "+ port1_ip + " via 42.0.0.1 dev l1")

                print("7")
                #os.system("sudo docker exec lc2 ip route add "+ port3_ip + " via 42.0.0.1 dev l2")
                #creating vxlan
                print("8")
                os.system("sudo ip netns  exec n1 ip link add name vxlan0 type vxlan id 42 dev n1l1 remote 42.0.0.3 dstport 4789")
                print("9")
                os.system("sudo ip netns  exec n2 ip link add name vxlan1 type vxlan id 42 dev n2l2 remote 42.0.0.1 dstport 4789")
                print("10")             
                os.system("sudo ip netns exec n1 ip link set dev vxlan0 up")
                print("11")
                os.system("sudo ip netns exec n2 ip link set dev vxlan1 up")
                print("12")
                os.system("sudo ip netns exec n1 brctl addif br1n1 vxlan0")
                print("13")
                print("6")
                os.system("sudo ip netns exec n2 brctl addif br1n2 vxlan1")
                os.system("sudo ip netns exec n1 ip route add 42.0.0.3 via 42.0.0.2 dev n1l1")
                print("3")
                os.system("sudo ip netns exec n2 ip route add 42.0.0.1 via 42.0.0.4 dev n2l2")
                vip=vip+2
        if x[2]=="gre":

                os.system("sudo ip netns add n1")
                os.system("sudo ip netns add n2")
                bridge1name="br1n1"
                bridge2name="br1n2"
                os.system("sudo ip netns exec n1 brctl addbr " + bridge1name)
                print("1")
                os.system("sudo ip netns exec n2 brctl addbr "+ bridge2name)
                os.system("sudo ip netns exec n1 ip link set " + bridge1name + " up")
                print("2")
                os.system("sudo ip netns exec n2 ip link set " + bridge2name + " up")
                print("11")
                os.system("sudo ip link add  l1 type veth peer name n1l1")
                print("12")
                os.system("sudo ip link add  l2 type veth peer name n2l2")
                print("13")
                os.system("sudo ip link set l1 netns  " + pid1[0] )
                print("14")
                os.system("sudo ip link set n1l1 netns n1 ")
                print("15")
                os.system("sudo docker exec lc1 ip link set l1 up ")
                print("16")
                os.system("sudo ip netns exec  n1 ip link set n1l1 up")
                print("17")
                os.system("sudo ip link set l2 netns  " + pid1[1] )
                print("18")
                os.system("sudo ip link set n2l2 netns n2 ")
                print("19")
                os.system("sudo docker exec lc2 ip link set l2 up ")
                print("20")
                os.system("sudo ip netns exec n2 ip link set n2l2 up")
                print("21")
                os.system("sudo ip netns exec n1 ip addr add  42.0.0.1/24 dev n1l1 ")
                print("22")
                os.system("sudo ip netns exec n2 ip addr add  42.0.0.3/24 dev n2l2 ")
                print("23")     
                os.system("sudo docker exec lc1 ip addr add  42.0.0.2/24 dev l1 ")
                print("24")
                os.system("sudo docker exec lc2 ip addr add  42.0.0.4/24 dev l2 ")
                os.system("sudo ip netns exec n1 ip addr add 40.0.0.60/24 dev br1n1 ")
                

                print("inside gre")
                os.system("sudo brctl addbr brgre1 ")
                print("1")
                os.system("sudo ip link set brgre1 up")
                print("2")
                os.system("sudo ip link add brg1 type veth peer name brg1lc2")
                print("3")
                os.system("sudo ip link set brg1 up")
                print("4")
                os.system("sudo brctl addif brgre1 brg1") 
                os.system("sudo ip link set brg1lc2 netns " + pid1[1])
                print("5")
                os.system("sudo docker  exec lc2 ip link set brg1lc2 up")
                print("6")
                port5="eth"+x[0]
                print("7")
                port6="br4"+x[0]
                
                os.system("sudo ip link add "+ port5 + " type veth peer name " + port6)
                print("8")
                port5_ip = "40.0.0."+str(vip+2)+"/24"

                os.system("sudo ip link set dev "+ port5 + " netns "+pid[x[0]]+" name "+port5+" up")
                print("9")
                os.system("sudo ip link set dev " + port6 + " netns n1  up" )
                print("10")
                os.system("sudo ip netns exec n1 brctl addif br1n1 " + port6)
                print("11")
                os.system("sudo docker exec "+x[0]+" ip addr add "+port5_ip+" dev "+ port5)
                print("12")
                port7="eth"+x[1]
                port8="br4"+x[1]
                os.system("sudo ip link add " + port7 + " type veth peer name " + port8)
                #os.system("sudo docker exec "+x[0]+" ip addr add "+port5_ip+" dev "+ port5)
                print("13")
                port7_ip = "44.0.0."+str(greip)+"/24"
                os.system("sudo ip link set dev "+ port7 + " netns "+pid[x[1]]+" name "+port7+" up")
                print("14")
                os.system("sudo docker exec lc2 ip addr add 44.0.0.2/24 dev brg1lc2")
                print("15")
                os.system("sudo docker exec lc1 ip  tunnel add gretun2 mode gre local 45.0.0.1 remote 46.0.0.1")
                print("16")
                os.system("sudo docker exec lc2 ip tunnel add gretun3 mode gre local 46.0.0.1 remote 45.0.0.1")
                print("17")
                os.system("sudo docker exec lc1 ip link set gretun2 up ")
                print("18")
                os.system("sudo docker exec lc2 ip link set gretun3 up ")
                print("19")
                os.system("sudo ip netns exec n1 ip route add 44.0.0.0/24 via 42.0.0.2 dev n1l1")
                print("20")
                #os.system("sudo ip netns exec n2 ip route add 44.0.0.0/24 via 42.0.0.2 dev n2l2")
                print("21")
                os.system("sudo brctl addif brgre1 " + port8)
                print("22")
                os.system("sudo docker exec "+x[1]+" ip addr add "+port7_ip+" dev "+port7)
                print("23")
                os.system("sudo ifconfig  " + port8  + " up " )
                print("24")
                os.system("sudo docker exec "+ x[1] + " ip route add 40.0.0.0/24 via 44.0.0.2 ")
                print("25")
                os.system("sudo docker exec " + x[0] + " ip route add 44.0.0.0/24 via 40.0.0.60 ")
                print("26")
                os.system("sudo docker exec lc1  ip route add " +  "40.0.0."+str(vip+2) + " via 42.0.0.1 dev l1")
                print("27")
                os.system("sudo docker exec lc1  ip route add " +  "44.0.0."+str(greip) + " dev gretun2")
                print("28")
                os.system("sudo docker exec lc2 ip route add "+  "40.0.0."+str(vip+2) + " dev gretun3 ")
                os.system("sudo docker exec " + x[0] + " ip route add 44.0.0.0/24 via 40.0.0.60 dev ethct1 ")

                #os.system("sudo docker attach lc2 ip route add 44.0.0.0/24  
                vip=vip+3

















