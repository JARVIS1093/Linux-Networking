import libvirt 


conn=libvirt.open('qemu:///system')
nodeinfo=conn.getInfo()
#Host Information
print "Host Information:\n","1. Hostname - ",conn.getHostname(),"\n2. Maximum Virtual CPUs",conn.getMaxVcpus(None),"\n3. CPU Model - ",nodeinfo[0],"\n4. Memory Size - ",nodeinfo[1]," MBytes","\n5. No of Active CPU$
print "\n\n Guest Information:\n"
domainNames = conn.listDefinedDomains()
domainIDs = conn.listDomainsID()
domcpustats={} 
dommemstats={}
i=1 
for domainID in domainIDs:
  print "#",i
  print "\n1. Domain ID - ",str(domainID)
  domain=conn.lookupByID(domainID)
  domainNames.append(domain.name)
  state, maxmem, mem, cpus, cput = domain.info()
  print "\n2. Domain Name - ",domain.name()
  print "\n3. Domain State - ",state
  print "\n4. Domain Max Memory - ",maxmem
  print "\n5. Domain Memory - ",mem
  print "\n6. Domain UUID - ",str(domain.UUIDString()) 
  print "\n7. Domain OS Type - ",str(domain.OSType()),"\n\n"
  i+=1

