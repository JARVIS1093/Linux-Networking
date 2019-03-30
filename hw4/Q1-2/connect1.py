#!/usr/bin/python
from math import *
import subprocess
import os

with open('./conn1.csv') as f:
  connectivity_mat = f.readlines()
b=[]
connectivity_mat = [x.strip() for x in connectivity_mat] 
for x in connectivity_mat:

        b.append(x.split(","))
#print(b)
raw_nodes=[]
for i in b:
        raw_nodes.append(i[0])
        raw_nodes.append(i[1])
#print(raw_nodes)       
nodes=set(raw_nodes)
#print(list(nodes))

node_num = len(nodes)
open('./var_file.yml', 'w').close() #Clear Previous data
file =open('./var_file.yml','a')
file.write("container_names:\n")
for node_name in nodes:
  file.write("  - "+node_name+"\n")


