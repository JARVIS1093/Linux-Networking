import sys
from ruamel.yaml import YAML
import yaml

vmno=int(raw_input("please enter the no of VMs\n"))
inp={}
for i in range(0,vmno):
        inp[i]=list(raw_input(("please enter the networks you want to attach VM" + str( vmno) + " with\n")).split(" "))
bfinal={}
final=[]
print(inp)
for i in inp:
        print(final)
        bl={}
        bl['name']=i
        b=[]
        for j in (range(0,len(inp[i]))):
                a={}
                if (inp[i][j]=='internet'):
                        a['net']=inp[i][j]
                        a['slot']="0x03"

                if(inp[i][j]=='L2'):
                        a['net']=inp[i][j]
                        a['slot']="0x09"
                if(inp[i][j]=='L3'):
                        a['net']=inp[i][j]
                        a['slot']="0x10"
                if(inp[i][j]=='other'):
                        a['net']=inp[i][j]
                        a['slot']="0x11"
                b.append(a)
        bl['network']=b
        print(bl)
        final.append(bl)
        print(final)
bfinal['created']=final
print(bfinal)

with open('yamal.yml', 'w') as outfile:
   yaml.dump(bfinal, outfile, default_flow_style=False)




