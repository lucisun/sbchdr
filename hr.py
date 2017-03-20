#!/usr/bin/python

# tlucciano Mar 12 2017

import csv
import os,glob,sys,re
from datetime import datetime
import MySQLdb
import numpy as np
import matplotlib.pyplot as plt
import scipy
#from pylab import *



def cls():
    os.system(['clear','cls'][os.name == 'linux'])

def is_int(chkstring):
   try: 
        int(chkstring)
        return True
   except ValueError:
        return False

def make_date_time(intime):
    #print("time: ", intime)
    convertTS = (datetime.fromtimestamp(int(intime)).strftime('%Y-%m-%d %H:%M:%S'))
    return convertTS

def get_all_files(srchpath):
    """get names of all file in dir"""
    allfiles = []

    for root,dirs,files in os.walk(srchpath):
        for file in files:
            try:
                pathname = os.path.join(root,file)
                filesize = os.path.getsize(pathname)
                allfiles.append([file,pathname,filesize])
            except FileNotFoundError:
                pass

    return allfiles

def getIntAnswer():
    try:
        inp=raw_input("Selection: ")
        sel = int(inp)
    except ValueError:
        print "valueError - not a number! " + inp
        sys.exit(1)
    except UnboundLocalError:
        print "UnboundLocalError - not a number! " + inp
        sys.exit(1)
    return sel

def remove_file(fname):
    #print("fname: ", fname)
    try:
        os.remove(fname)
    except OSError,e:
        print("Error: %s -%s." % (e.filename,e.strerror))

#################################
#  check hdr path
#################################
def check_hdr_path(dbinfo,hdrType):
    #print("hdrType: ", hdrType)
    hdrpath=dbinfo[4]
    if hdrpath.endswith('/'):
        hdrpath=hdrpath + hdrType
    else:
        hdrpath=hdrpath + "/" + hdrType
    #hdrpath=dbinfo[4] + hdr
    if os.path.exists(hdrpath):
        #print("hdrpath: ", hdrpath)
        return hdrpath
    else:
        print("No path " , hdrpath)
        sys.exit(1)    

#####################################################
# display_system_data
###################################################
def display_system_data_over_days(dbinfo):
    dtlist = []
    cpulist = []
    memlist = []
    cpslist = []
    print("show system data")
    bdate = raw_input("Enter beginning date YYYY-MM-DD HH:MM:SS ")
    edate = raw_input("Enter ending date YYYY-MM-DD HH:MM:SS ")
    #bdate=bdate + " " + "00:00:00"
    #edate=edate + " " + "23:59:59"
    print("beg date: %s" % (bdate))
    print("end date: %s" % (edate))
    mydb = MySQLdb.connect(host=dbinfo[0],db=dbinfo[1], user=dbinfo[2],passwd=dbinfo[3])
    cur = mydb.cursor() 
    #sql = ('SELECT tstamp,datetime,cpu,memory,cps FROM system WHERE datetime < "%s"' % (bdate))
    sql = ('SELECT tstamp,datetime,cpu,memory,cps FROM system WHERE datetime > "%s" AND datetime < "%s"' % (bdate,edate))
    #sql = ("SELECT tstamp,datetime,cpu,memory,cps FROM system WHERE datetime < '2017-02-10'")
    try:
        cur.execute(sql)
        results = cur.fetchall()
        for row in results:
             ts = row[0]
             dt = row[1]
             cpu = row[2]
             mem = row[3]
             cps = row[4]
             dtlist.append(dt)
             cpulist.append(cpu)
             memlist.append(mem)
             cpslist.append(cps)
             print("ts=%s,dt=%s,cpu=%d,memory=%d,cps=%d" % (ts,dt,cpu,mem,cps))
    except:
         print("Error: unable to fetch data")
    mydb.close()

    try:
        fig = plt.figure(dpi=96,figsize=(14,8))
        plt.plot(dtlist,cpulist,c='red',linewidth=1.0)
        plt.plot(dtlist,memlist,c='orange',linewidth=2.0)
        plt.plot(dtlist,cpslist,c='green',linewidth=3.0)
        plt.title("cpu=Red mem=Orange cps=Green graph",fontsize=8)
        plt.xlabel('Time',fontsize=8)
        plt.ylabel('CPU/MEM',fontsize=10)
        fig.autofmt_xdate(rotation=80)
        fig.tight_layout()
        plt.show()
    except:
        print("No Display")


##########################################
# Display sip session data
##########################################
def display_sipinvite_data(dbinfo):
        
    dtlist = []
    serverlist = []
    msglist = []
    print("show sip invite data")
    bdate = raw_input("Enter beginning date YYYY-MM-DD ")
    edate = raw_input("Enter ending date YYYY-MM-DD ")
    bdate=bdate + " " + "00:00:00"
    edate=edate + " " + "23:59:59"
    print("beg date: %s" % (bdate))
    print("end date: %s" % (edate))
    mydb = MySQLdb.connect(host=dbinfo[0],db=dbinfo[1], user=dbinfo[2],passwd=dbinfo[3])
    cur = mydb.cursor() 
    sql = ('SELECT datetime,messageevent,servertotals FROM sipinvites WHERE datetime > "%s" AND datetime < "%s" AND messageevent="INVITE Requests" ' % (bdate,edate))
    try:
        cur.execute(sql)
        results = cur.fetchall()
        for row in results:
             dt = row[0]
             msgevent = row[1]
             servertotals = row[2]
             dtlist.append(dt)
             msglist.append(msgevent)
             serverlist.append(servertotals)
             print("dt=%s,msgevent=%s,invites=%d" % (dt,msgevent,servertotals))
    except:
         print("Error: unable to fetch data")
    mydb.close()

    try:
        fig = plt.figure(dpi=96,figsize=(10,6))
        plt.plot(dtlist,serverlist,c='green')
        #plt.plot(dtlist,memlist,c='orange')
        #plt.plot(dtlist,cpslist,c='green')
        plt.title("INVITES=Green graph",fontsize=8)
        plt.ylabel('INVITE REQUESTS',fontsize=10)
        plt.xlabel('Time',fontsize=8)
        fig.autofmt_xdate()
        plt.show()
    except:
        print("No Display")




#####################################################
# insert_interface_data
# read data from interface hdr and then call funct to insert into interface table
###################################################
def insert_interface_data(dbinfo,mode):
    count=0
    hdrpath = check_hdr_path(dbinfo,"interface")
    #print("interfae hdr path: ", hdrpath)
    mydb = MySQLdb.connect(host=dbinfo[0],db=dbinfo[1], user=dbinfo[2],passwd=dbinfo[3])
    cur = mydb.cursor() 
    #mydb.close()
    mydb2 = MySQLdb.connect(host=dbinfo[0],db=dbinfo[1], user=dbinfo[2],passwd=dbinfo[3])
    cur2 = mydb2.cursor()
    lineHeading=0
    allFileList=[]
    allFileList=get_all_files(hdrpath)
    if mode == "A":
        if len(allFileList) == 0:
            return 0
    if mode != "A":
        if len(allFileList) == 0:
            print("No data to insert (no files found)")
            return 0
    if mode != "A":
        print("Inserting interface data. Please wait")     
    allFileList=sorted(allFileList)
    for f in allFileList:
        #print f[1]
        filein = open(f[1])
        lineHeading=0
        for line in csv.reader(filein,skipinitialspace=True):
            #print lineHeading
            if lineHeading > 0:
                #print("line 1:", line)
                (time,indx,descr,intype,mtu,speed,phyaddr,adminstatus,operstatus,iflastchg,inoctets,inunicastpkts,innonunicastpkts,indiscards,outerr,outoctets,outunicastpkts,outnonunicastpkts,outdiscards,inerrors) = (line[0], line[1],line[2],line[3],line[4],line[5],line[6],line[7],line[8],line[9],line[10],line[11],line[12],line[13],line[14],line[15],line[16],line[17],line[18],line[19])
                convertTS = make_date_time(time)
                cmd = cur.execute("SELECT tstamp,interfaceindx FROM interface WHERE tstamp=%s AND interfaceindx=%d" % (line[0],int(indx)))
                if not cmd:
                    cmdin = cur2.execute('INSERT INTO interface(tstamp,datetime,interfaceindx,intdescr,type,mtu,speed,phyaddr,adminstate,operstate,iflastchange,inoctets,inunicastpkts,innonunicastpkts,indiscard,outerr,outoctets,outunicastpkts,outnonunicastpkts,outdiscards,inerrors) VALUES ("%s","%s","%d","%s","%s","%d","%d","%s","%s","%s","%d","%d","%d","%d","%d","%d","%d","%d","%d","%d","%d")' % (line[0],convertTS, int(line[1]),line[2],line[3],int(line[4]),int(line[5]),line[6],line[7],line[8],int(line[9]),int(line[10]),int(line[11]),int(line[12]),int(line[13]),int(line[14]),int(line[15]),int(line[16]),int(line[17]),int(line[18]),int(line[19])))
                    mydb2.commit()
                    if mode != "A":
                        if ((count % 100) == 1):
                            print(".  currently on record number %d." % (count))
                        count+=1
                else:
                    if mode != "A":
                        print cmd
                        print("Already Exists: ", line)

            lineHeading+=1

        remove_file(f[1])

####################################################
#
####################################################
def insertsipinvitesDB(ts,dt,msgevent,servertotals,clienttotals,dbinfo,mode):
    count=0
    mydb = MySQLdb.connect(host=dbinfo[0],db=dbinfo[1], user=dbinfo[2],passwd=dbinfo[3])
    cur = mydb.cursor() 
    cmd = cur.execute("SELECT tstamp,messageevent FROM sipinvites WHERE tstamp=%s AND messageevent='%s'" % (ts,msgevent))
    mydb.close()
    mydb2 = MySQLdb.connect(host=dbinfo[0],db=dbinfo[1], user=dbinfo[2],passwd=dbinfo[3])
    cur2 = mydb2.cursor()
    if is_int(servertotals):
        servertotals=int(servertotals)
    else:
        servertotals=0
    if is_int(clienttotals):
        clienttotals=int(clienttotals)
    else:
        clienttotals=0
    if not cmd:
          cmdin = cur2.execute('INSERT INTO sipinvites(tstamp,datetime,messageevent,servertotals,clienttotals) VALUES("%s","%s", "%s","%d","%d")' % (ts,dt,msgevent,servertotals,clienttotals))
          #print("cmdin: ", cmdin)
          mydb2.commit()
          if mode != "A":
              if ((count % 100) == 1):
                  print(".  currently on record number %d." % (count))
                  count+=1
    else:
          if mode != "A":
              print cmd
              print("Already Exists: ")
    mydb2.close()


#####################################################
# insert_sip_invite_data
# read data from sip-invite hdr and then call funct to insert into interface table
###################################################
def insert_sipinvite_data(dbinfo,mode):
    recordCount=0
    hdrpath = check_hdr_path(dbinfo,"sip-invites")
    #print("interfae hdr path: ", hdrpath)
    lineHeading=0
    allFileList=[]
    allFileList=get_all_files(hdrpath)
    if mode != "A":
        if len(allFileList) == 0:
            print("No data to insert (no files found)")
            return 0
    if mode != "A":
        print("Inserting sip-invite data. Please wait.")     
    allFileList=sorted(allFileList)
    for f in allFileList:
        #print f[1]
        filein = open(f[1])
        lineHeading=0
        for line in csv.reader(filein,skipinitialspace=True):
            #print lineHeading
            if lineHeading > 0:
                #print("line 1:", line)
                (time,msgevent,servertotals,clienttotals) = (line[0], line[1],line[2],line[3])
                ConvertTS = make_date_time(time)
                #print ConvertTS
                insertsipinvitesDB(time,ConvertTS,msgevent,servertotals,clienttotals,dbinfo,mode)
                recordCount+=1
                #if mode != "A":
                #    print("Record: %d" % (recordCount))

            lineHeading+=1
        remove_file(f[1])

##########################################
# Read in the data from cfgFile hdr.cfg
##########################################
def readDBconfig(cfgFile):
    flist=[]
    #f=open(cfgFile,'r')    

    with open(cfgFile) as f:
        flist=f.readlines()
    flist = [x.strip() for x in flist]
    myhost=flist[0].split('=') 
    myhost=myhost[1]
    mydb=flist[1].split('=')
    mydb=mydb[1]

    myuser=flist[2].split('=') 
    myuser=myuser[1]
    mypwd=flist[3].split('=')
    mypwd=mypwd[1]
    mypath=flist[4].split('=')
    mypath=mypath[1]
    return (myhost,mydb,myuser,mypwd,mypath) 

#####################################################
# insert_system_data NEW    
# read data from system hdr and then call funct to insert into system table
###################################################
def insert_system_data(dbinfo,mode):
    count=0
    hdrpath = check_hdr_path(dbinfo,"system")
    #print "hdrpath: ", hdrpath
    mydb = MySQLdb.connect(host=dbinfo[0],db=dbinfo[1], user=dbinfo[2],passwd=dbinfo[3])
    cur = mydb.cursor() 
    mydb2 = MySQLdb.connect(host=dbinfo[0],db=dbinfo[1], user=dbinfo[2],passwd=dbinfo[3])
    cur2 = mydb2.cursor()
    lineHeading=0
    allFileList=[]
    allFileList=get_all_files(hdrpath)
    if mode == "A":
        if len(allFileList) == 0:
            return 0
    if mode != "A":
        if len(allFileList) == 0:
            print("No data to insert (no files found)")
            return 0
    if mode != "A":
        print("Inserting system data. Please wait")     
    allFileList=sorted(allFileList)
    for f in allFileList:
        #print f[1]
        filein = open(f[1])
        lineHeading=0
        for line in csv.reader(filein,skipinitialspace=True):
            if lineHeading > 0:
                #print("line 1:", line)
                (TimeStamp,cpu,memory,healthscore,redundancystate,signalsessions,cps,camutilnat,camutilarp,i2cbuststate,liccapacity,currentcachedsiplocalcontactreg,currmgcppublendptgwreg,currh323numofreg,applloadrate,currdenyentriesallocated) = (line[0], line[1],line[2],line[3],line[4],line[5],line[6],line[7],line[8],line[9],line[10],line[11],line[12],line[13],line[14],line[15])
                #print("line 9: ", line[9]) 
                ConvertTS = make_date_time(TimeStamp)
                #print("ConvertTS: ",ConvertTS)
                cmd = cur.execute("SELECT tstamp FROM system WHERE tstamp=%s" % (TimeStamp))
                if not cmd:
                    cmdin = cur2.execute('INSERT INTO system(tstamp,datetime,cpu,memory,healthscore,redundancystate,signalsess,cps,camutilnat,camutilarp,i2cbuststate,liccapacity,currentcachedsiplocalcontactreg,currmgcppublendptgwreg,currh323numofreg,applloadrate,currdenyentriesallocated) VALUES("%s","%s", "%f","%f","%f","%s","%f","%f","%f","%f","%s","%f","%d","%d","%d","%f","%d")' % (TimeStamp,ConvertTS,float(line[1]),float(line[2]),float(line[3]),line[4],float(line[5]),float(line[6]),float(line[7]),float(line[8]),line[9],float(line[10]),int(line[11]),int(line[12]),int(line[13]),float(line[14]),int(line[15])  ))
                    #print("cmdin: ", cmdin)
                    mydb2.commit()
                    if mode != "A":
                        if ((count % 100) == 1):
                            print(".  currently on record number %d." % (count))
                        count+=1
                else:
                    if mode != "A":
                        print cmd
                        print("Already Exists: ", line)

            lineHeading+=1

        remove_file(f[1])

#####################################################
# insert_session_agent_data
# read data from interface hdr and then call funct to insert into interface table
###################################################
def insert_sa_data(dbinfo,mode):
    count=0
    hdrpath = check_hdr_path(dbinfo,"session-agent")
    mydb = MySQLdb.connect(host=dbinfo[0],db=dbinfo[1], user=dbinfo[2],passwd=dbinfo[3])
    cur = mydb.cursor() 
    mydb2 = MySQLdb.connect(host=dbinfo[0],db=dbinfo[1], user=dbinfo[2],passwd=dbinfo[3])
    cur2 = mydb2.cursor()
    lineHeading=0
    allFileList=[]
    allFileList=get_all_files(hdrpath)
    if mode != "A":
        if len(allFileList) == 0:
            print("No data to insert (no files found)")
            return 0
    if mode != "A":
        print("Inserting session-agent data. Please wait")     
    allFileList=sorted(allFileList)
    for f in allFileList:
        #print f[1]
        filein = open(f[1])
        lineHeading=0
        for line in csv.reader(filein,skipinitialspace=True):
            if lineHeading > 0:
                #print("line 1:", line)
                (TimeStamp,Hostname,SystemType,Status,InboundActiveSessions,InboundSessionRate,OutboundActiveSessions,OutboundSessionRate,InboundSessionsAdmitted,InboundSessionsNotAdmitted,InboundConcurrentSessionsHigh,InboundAverageSessionRate,OutboundSessionsAdmitted,OutboundSessionsNotAdmitted,OutboundConcurrentSessionsHigh,OutboundAverageSessionsRate,MaxBurstRate,TotalSeizures,TotalAnsweredSessions,AnswerSeizureRatio,AverageOneWaySignalingLatency,MaximumOneWaySignalingLatency) = (line[0], line[1],line[2],line[3],line[4],line[5],line[6],line[7],line[8],line[9],line[10],line[11],line[12],line[13],line[14],line[15],line[16],line[17],line[18],line[19],line[20],line[21])
                
                ConvertTS = make_date_time(TimeStamp)
                cmd = cur.execute("SELECT tstamp,Hostname FROM sessionagent WHERE tstamp=%s AND Hostname='%s'" % (TimeStamp,Hostname))
                if not cmd:
                    cmdin = cur2.execute('INSERT INTO sessionagent(tstamp,datetime,Hostname,SystemType,Status,InboundActiveSessions,InboundSessionRate,OutboundActiveSessions,OutboundSessionRate,InboundSessionsAdmitted,InboundSessionsNotAdmitted,InboundConcurrentSessionsHigh,InboundAverageSessionRate,OutboundSessionsAdmitted,OutboundSessionsNotAdmitted,OutboundConcurrentSessionsHigh,OutboundAverageSessionsRate,MaxBurstRate,TotalSeizures,TotalAnsweredSessions,AnswerSeizureRatio,AverageOneWaySignalingLatency,MaximumOneWaySignalingLatency) VALUES("%s","%s", "%s","%s","%s","%d","%d","%d","%d","%d","%d","%d","%f","%d","%d","%d","%f","%f","%f","%d","%f","%f","%f")' % (TimeStamp,ConvertTS,Hostname,SystemType,Status,int(InboundActiveSessions),int(InboundSessionRate),int(OutboundActiveSessions),int(OutboundSessionRate),int(InboundSessionsAdmitted),int(InboundSessionsNotAdmitted),int(InboundConcurrentSessionsHigh),float(InboundAverageSessionRate),int(OutboundSessionsAdmitted),int(OutboundSessionsNotAdmitted),int(OutboundConcurrentSessionsHigh),float(OutboundAverageSessionsRate),float(MaxBurstRate),float(TotalSeizures),int(TotalAnsweredSessions),float(AnswerSeizureRatio),float(AverageOneWaySignalingLatency),float(MaximumOneWaySignalingLatency) ))
                    #print("cmdin: ", cmdin)
                    mydb2.commit()
                    if mode != "A":
                        if ((count % 100) == 1):
                            print(".  currently on record number %d." % (count))
                        count+=1
                else:
                    if mode != "A":
                        print cmd
                        print("Already Exists: ", line)

            lineHeading+=1

        remove_file(f[1])

#####################################################
# insert_session_realm_data
# read data from session-realm hdr
###################################################
def insert_sessionrealm_data(dbinfo,mode):
    count=0
    hdrpath = check_hdr_path(dbinfo,"session-realm")
    mydb = MySQLdb.connect(host=dbinfo[0],db=dbinfo[1], user=dbinfo[2],passwd=dbinfo[3])
    cur = mydb.cursor() 
    mydb2 = MySQLdb.connect(host=dbinfo[0],db=dbinfo[1], user=dbinfo[2],passwd=dbinfo[3])
    cur2 = mydb2.cursor()
    lineHeading=0
    allFileList=[]
    allFileList=get_all_files(hdrpath)
    if mode != "A":
        if len(allFileList) == 0:
            print("No data to insert (no files found)")
            return 0
    if mode != "A":
        print("Inserting session-realm data. Please wait")     
    allFileList=sorted(allFileList)
    for f in allFileList:
        #print f[1]
        filein = open(f[1])
        lineHeading=0
        for line in csv.reader(filein,skipinitialspace=True):
            if lineHeading > 0:
                #print("line 1:", line)
                (TimeStamp,RealmName,InboundActiveSessions,InboundSessionRate,OutboundActiveSessions,OutboundSessionRate,InboundSessionsAdmitted,InboundSessionsNotAdmitted,InboundConcurrentSessionsHigh,InboundAverageSessionRate,OutboundSessionsAdmitted,OutboundSessionsNotAdmitted,OutboundConcurrentSessionsHigh,OutboundAverageSessionsRate,MaxBurstRate,TotalSeizures,TotalAnsweredSessions,AnswerSeizureRatio,AverageOneWaySignalingLatency,MaximumOneWaySignalingLatency,AverageQoSRFactor,MaximumQoSRFactor,CurrentQoSMajorExceeded,TotalQoSMajorExceeded,CurrentQoSCriticalExceeded,TotalQoSCriticalExceeded, EarlySession, SuccessfulSessions, ActiveSubscriptions, SubscriptionsPerMax, SubscriptionsHigh, TotalSubscriptions, ActiveLocalContacts) = (line[0],line[1],line[2],line[3],line[4],line[5],line[6],line[7],line[8],line[9],line[10],line[11],line[12],line[13],line[14],line[15],line[16],line[17],line[18],line[19],line[20],line[21],line[22],line[23],line[24],line[25],line[26],line[27],line[28],line[29],line[30],line[31],line[32])
                ConvertTS = make_date_time(TimeStamp)
                cmd = cur.execute("SELECT tstamp,RealmName FROM sessionrealm WHERE tstamp=%s AND RealmName='%s'" % (TimeStamp,RealmName))
                if not cmd:
                    cmdin = cur2.execute('INSERT INTO sessionrealm(tstamp,datetime,RealmName,InboundActiveSessions,InboundSessionRate,OutboundActiveSessions,OutboundSessionRate,InboundSessionsAdmitted,InboundSessionsNotAdmitted,InboundConcurrentSessionsHigh,InboundAverageSessionRate,OutboundSessionsAdmitted,OutboundSessionsNotAdmitted,OutboundConcurrentSessionsHigh,OutboundAverageSessionsRate,MaxBurstRate,TotalSeizures,TotalAnsweredSessions,AnswerSeizureRatio,AverageOneWaySignalingLatency,MaximumOneWaySignalingLatency,AverageQoSRFactor,MaximumQoSRFactor,CurrentQoSMajorExceeded,TotalQoSMajorExceeded,CurrentQoSCriticalExceeded,TotalQoSCriticalExceeded, EarlySession, SuccessfulSessions, ActiveSubscriptions, SubscriptionsPerMax, SubscriptionsHigh, TotalSubscriptions, ActiveLocalContacts) VALUES("%s","%s","%s","%d","%d","%d","%f","%d","%d","%d","%f","%d","%d","%d","%f","%f","%f","%d","%f","%f","%f","%f","%f","%f","%f","%f","%f","%d","%d","%d","%d","%d","%d","%d")' % (TimeStamp,ConvertTS,RealmName,int(InboundActiveSessions),int(InboundSessionRate),int(OutboundActiveSessions),float(OutboundSessionRate),int(InboundSessionsAdmitted),int(InboundSessionsNotAdmitted),int(InboundConcurrentSessionsHigh),float(InboundAverageSessionRate),int(OutboundSessionsAdmitted),int(OutboundSessionsNotAdmitted),int(OutboundConcurrentSessionsHigh),float(OutboundAverageSessionsRate),float(MaxBurstRate),float(TotalSeizures),int(TotalAnsweredSessions),float(AnswerSeizureRatio),float(AverageOneWaySignalingLatency),float(MaximumOneWaySignalingLatency),float(AverageQoSRFactor),float(MaximumQoSRFactor),float(CurrentQoSMajorExceeded),float(TotalQoSMajorExceeded),float(CurrentQoSCriticalExceeded),float(TotalQoSCriticalExceeded), int(EarlySession), int(SuccessfulSessions), int(ActiveSubscriptions), int(SubscriptionsPerMax), int(SubscriptionsHigh), int(TotalSubscriptions), int(ActiveLocalContacts)))
                    mydb2.commit()
                    if mode != "A":
                        if ((count % 100) == 1):
                            print(".  currently on record number %d." % (count))
                        count+=1
                else:
                    if mode != "A":
                        print cmd
                        print("Already Exists: ", line)

            lineHeading+=1

        remove_file(f[1])


#####################################################
# insert_sip_session_data
# read data from sip-sessions hdr
###################################################
def insert_sipsessions_data(dbinfo,mode):
    count=0
    hdrpath = check_hdr_path(dbinfo,"sip-sessions")
    mydb = MySQLdb.connect(host=dbinfo[0],db=dbinfo[1], user=dbinfo[2],passwd=dbinfo[3])
    cur = mydb.cursor() 
    mydb2 = MySQLdb.connect(host=dbinfo[0],db=dbinfo[1], user=dbinfo[2],passwd=dbinfo[3])
    cur2 = mydb2.cursor()
    lineHeading=0
    allFileList=[]
    allFileList=get_all_files(hdrpath)
    if mode != "A":
        if len(allFileList) == 0:
            print("No data to insert (no files found)")
            return 0
    if mode != "A":
        print("Inserting sip sessions data. Please wait")     
    allFileList=sorted(allFileList)
    for f in allFileList:
        #print f[1]
        filein = open(f[1])
        lineHeading=0
        for line in csv.reader(filein,skipinitialspace=True):
            if lineHeading > 0:
                #print("line 1:", line)
                (TimeStamp,Sessions,SessionsInitial,SessionsEarly,SessionsEstablished,SessionsTerminated,Dialogs,DialogsEarly,DialogsConfirmed,DialogsTerminated) = (line[0],line[1],line[2],line[3],line[4],line[5],line[6],line[7],line[8],line[9])
                ConvertTS = make_date_time(TimeStamp)
                cmd = cur.execute("SELECT tstamp FROM sipsessions  WHERE tstamp=%s" % (TimeStamp))
                if not cmd:
                    cmdin = cur2.execute('INSERT INTO sipsessions(tstamp,datetime,sessions,sessionsInitial,sessionsEarly,sessionsEstablished,sessionsTerminated,dialogs,dialogsEarly,dialogsConfirmed,dialogsTerminated ) VALUES("%s","%s", "%d","%d","%d","%d","%d","%d","%d","%d","%d")' % (TimeStamp,ConvertTS, int(Sessions),int(SessionsInitial),int(SessionsEarly),int(SessionsEstablished),int(SessionsTerminated),int(Dialogs),int(DialogsEarly),int(DialogsConfirmed),int(DialogsTerminated ) ))
                    #print("cmdin: ", cmdin)
                    mydb2.commit()
                    if mode != "A":
                        if ((count % 100) == 1):
                            print(".  currently on record number %d." % (count))
                        count+=1
                else:
                    if mode != "A":
                        print cmd
                        print("Already Exists: ", line)

            lineHeading+=1

        remove_file(f[1])

#####################################################
# insert_voltage_data
# read data from voltage hdr
###################################################
def insert_voltage_data(dbinfo,mode):
    count=0
    hdrpath = check_hdr_path(dbinfo,"voltage")
    mydb = MySQLdb.connect(host=dbinfo[0],db=dbinfo[1], user=dbinfo[2],passwd=dbinfo[3])
    cur = mydb.cursor() 
    mydb2 = MySQLdb.connect(host=dbinfo[0],db=dbinfo[1], user=dbinfo[2],passwd=dbinfo[3])
    cur2 = mydb2.cursor()
    lineHeading=0
    allFileList=[]
    allFileList=get_all_files(hdrpath)
    if mode == "A":
        if len(allFileList) == 0:
            return 0
    if mode != "A":
        if len(allFileList) == 0:
            print("No data to insert (no files found)")
            return 0
    if mode != "A":
        print("Inserting voltage data. Please wait")     
    allFileList=sorted(allFileList)
    for f in allFileList:
        #print f[1]
        filein = open(f[1])
        lineHeading=0
        for line in csv.reader(filein,skipinitialspace=True):
            if lineHeading > 0:
                #print("line 1:", line)
                (TimeStamp,vtype_in,desc,voltage) = (line[0],line[1],line[2],line[3])
                ConvertTS = make_date_time(TimeStamp)
                cmd = cur.execute("SELECT tstamp,vtype,description FROM voltage  WHERE tstamp=%s AND vtype='%s' AND description='%s'" % (TimeStamp,vtype_in,desc))
                if not cmd:
                    cmdin = cur2.execute('INSERT INTO voltage(tstamp,datetime,vtype,description,voltage ) VALUES("%s","%s", "%s","%s","%f")' % (TimeStamp,ConvertTS, vtype_in,desc,float(voltage) ))
                    #print("cmdin: ", cmdin)
                    mydb2.commit()
                    if mode != "A":
                        if ((count % 100) == 1):
                            print(".  currently on record number %d." % (count))
                        count+=1
                else:
                    if mode != "A":
                        print cmd
                        print("Already Exists: ", line)

            lineHeading+=1

        remove_file(f[1])

#####################################################
# insert_fan_data
# read data from fan hdr
###################################################
def insert_fan_data(dbinfo,mode):
    count=0
    hdrpath = check_hdr_path(dbinfo,"fan")
    mydb = MySQLdb.connect(host=dbinfo[0],db=dbinfo[1], user=dbinfo[2],passwd=dbinfo[3])
    cur = mydb.cursor() 
    mydb2 = MySQLdb.connect(host=dbinfo[0],db=dbinfo[1], user=dbinfo[2],passwd=dbinfo[3])
    cur2 = mydb2.cursor()
    lineHeading=0
    allFileList=[]
    allFileList=get_all_files(hdrpath)
    if mode == "A":
        if len(allFileList) == 0:
            return 0
    if mode != "A":
        if len(allFileList) == 0:
            print("No data to insert (no files found)")
            return 0
    if mode != "A":
        print("Inserting fan data. Please wait")     
    allFileList=sorted(allFileList)
    for f in allFileList:
        #print f[1]
        filein = open(f[1])
        lineHeading=0
        for line in csv.reader(filein,skipinitialspace=True):
            if lineHeading > 0:
                #print("line 1:", line)
                (TimeStamp,loc,desc,speed_in) = (line[0],line[1],line[2],line[3])
                ConvertTS = make_date_time(TimeStamp)
                cmd = cur.execute("SELECT tstamp,location,description FROM fan  WHERE tstamp=%s AND location='%s' AND description='%s'" % (TimeStamp,loc,desc))
                if not cmd:
                    cmdin = cur2.execute('INSERT INTO fan(tstamp,datetime,location,description,speed ) VALUES("%s","%s", "%s","%s","%f")' % (TimeStamp,ConvertTS, loc,desc,float(speed_in) ))
                    #print("cmdin: ", cmdin)
                    mydb2.commit()
                    if mode != "A":
                        if ((count % 100) == 1):
                            print(".  currently on record number %d." % (count))
                        count+=1
                else:
                    if mode != "A":
                        print cmd
                        print("Already Exists: ", line)

            lineHeading+=1

        remove_file(f[1])

#####################################################
# insert_temperature_data
# read data from temperature hdr
###################################################
def insert_temperature_data(dbinfo,mode):
    count=0
    hdrpath = check_hdr_path(dbinfo,"temperature")
    mydb = MySQLdb.connect(host=dbinfo[0],db=dbinfo[1], user=dbinfo[2],passwd=dbinfo[3])
    cur = mydb.cursor() 
    mydb2 = MySQLdb.connect(host=dbinfo[0],db=dbinfo[1], user=dbinfo[2],passwd=dbinfo[3])
    cur2 = mydb2.cursor()
    lineHeading=0
    allFileList=[]
    allFileList=get_all_files(hdrpath)
    #print("len of allFileList: ", len(allFileList))
    if mode != "A":
        if len(allFileList) == 0:
            print("No data to insert (no files found)")
            return 0
    #if len(allFileList) != 0:
    if mode != "A":
        print("Inserting temperature data. Please wait")     
    allFileList=sorted(allFileList)
    for f in allFileList:
        #print f[1]
        filein = open(f[1])
        lineHeading=0
        for line in csv.reader(filein,skipinitialspace=True):
            if lineHeading > 0:
                #print("line 1:", line)
                (TimeStamp,vtype_in,desc,temp_in) = (line[0],line[1],line[2],line[3])
                ConvertTS = make_date_time(TimeStamp)
                cmd = cur.execute("SELECT tstamp,vtype,description FROM temperature  WHERE tstamp=%s AND vtype='%s' AND description='%s'" % (TimeStamp,vtype_in,desc))
                if not cmd:
                    cmdin = cur2.execute('INSERT INTO temperature(tstamp,datetime,vtype,description,temperature) VALUES("%s","%s", "%s","%s","%f")' % (TimeStamp,ConvertTS, vtype_in,desc,float(temp_in) ))
                    #print("cmdin: ", cmdin)
                    mydb2.commit()
                    if ((count % 100) == 1):
                        print(".  currently on record number %d." % (count))
                    count+=1
                else:
                    if mode != "A":
                        print cmd
                        print("Already Exists: ", line)

            lineHeading+=1

        remove_file(f[1])


#####################################################
# insert_space_data
# read data from space hdr
###################################################
def insert_space_data(dbinfo,mode):
    count=0
    hdrpath = check_hdr_path(dbinfo,"space")
    mydb = MySQLdb.connect(host=dbinfo[0],db=dbinfo[1], user=dbinfo[2],passwd=dbinfo[3])
    cur = mydb.cursor() 
    mydb2 = MySQLdb.connect(host=dbinfo[0],db=dbinfo[1], user=dbinfo[2],passwd=dbinfo[3])
    cur2 = mydb2.cursor()
    lineHeading=0
    allFileList=[]
    allFileList=get_all_files(hdrpath)
    if mode != "A":
        if len(allFileList) == 0:
          print("No data to insert (no files found)")
          return 0
    if mode != "A":
        print("Inserting space data. Please wait")     
    allFileList=sorted(allFileList)
    for f in allFileList:
        #print f[1]
        filein = open(f[1])
        lineHeading=0
        for line in csv.reader(filein,skipinitialspace=True):
            if lineHeading > 0:
                #print("line 1:", line)
                (TimeStamp,volname_in,spaceuse,spaceavail) = (line[0],line[1],line[2],line[3])
                ConvertTS = make_date_time(TimeStamp)
                cmd = cur.execute("SELECT tstamp FROM space WHERE tstamp=%s" % (TimeStamp))
                if not cmd:
                    cmdin = cur2.execute('INSERT INTO space(tstamp,datetime,volumename,spaceused,spaceavailable) VALUES("%s","%s", "%s","%d","%d")' % (TimeStamp,ConvertTS, volname_in,int(spaceuse),int(spaceavail) ))
                    #print("cmdin: ", cmdin)
                    mydb2.commit()
                    if ((count % 100) == 1):
                        print(".  currently on record number %d." % (count))
                    count+=1
                else:
                    if mode != "A":
                        print cmd
                        print("Already Exists: ", line)

            lineHeading+=1

        remove_file(f[1])

#####################################################
# insert_networkutil_data
# read data from network-util hdr
###################################################
def insert_networkutil_data(dbinfo,mode):
    count=0
    hdrpath = check_hdr_path(dbinfo,"network-util")
    mydb = MySQLdb.connect(host=dbinfo[0],db=dbinfo[1], user=dbinfo[2],passwd=dbinfo[3])
    cur = mydb.cursor() 
    mydb2 = MySQLdb.connect(host=dbinfo[0],db=dbinfo[1], user=dbinfo[2],passwd=dbinfo[3])
    cur2 = mydb2.cursor()
    lineHeading=0
    allFileList=[]
    allFileList=get_all_files(hdrpath)
    if mode != "A":
        if len(allFileList) == 0:
            print("No data to insert (no files found)")
            return 0
    if mode != "A":
        print("Inserting network utilization data. Please wait")     
    allFileList=sorted(allFileList)
    for f in allFileList:
        #print f[1]
        filein = open(f[1])
        lineHeading=0
        for line in csv.reader(filein,skipinitialspace=True):
            if lineHeading > 0:
                #print("line 1:", line)
                (TimeStamp,nuindx,rxuse,txuse) = (line[0],line[1],line[2],line[3])
                rxuse=rxuse[:-1]
                txuse=txuse[:-1]
                ConvertTS = make_date_time(TimeStamp)
                cmd = cur.execute("SELECT tstamp,nuindex FROM networkutil WHERE tstamp=%s" % (TimeStamp))
                if not cmd:
                    cmdin = cur2.execute('INSERT INTO networkutil(tstamp,datetime,nuindex,rxutil,txutil) VALUES("%s","%s", "%d","%f","%f")' % (TimeStamp,ConvertTS, int(nuindx),float(rxuse),float(txuse) ))
                    #print("cmdin: ", cmdin)
                    mydb2.commit()
                    if ((count % 100) == 1):
                        print(".  currently on record number %d." % (count))
                    count+=1
                else:
                    if mode != "A":
                        print cmd
                        print("Already Exists: ", line)

            lineHeading+=1

        remove_file(f[1])

def display_menu_1():
    print("1. get system data and graph if display"),
    print("\t11. insert temperature data")
    print("2. get sip invite data and graph if display"),
    print("\t12. insert space data")
    print("3. insert system data"),
    print("\t\t\t\t13. insert network-util")
    print("4. insert interface data")
    print("5. insert sip-invites data")
    print("6. insert session-agent data")
    print("7. insert session-realm data")
    print("8. insert sip-sessions data")
    print("9. insert voltage data")
    print("10.insert fan data")
    print("0. exit")

###############################################
#MENU
###############################################
def menu(cfgFile):
    # M = manual mode A = auto mode
    dbinfo=[]
    dbinfo=readDBconfig(cfgFile) 
    myAns=0
    #print dbinfo
    #display_menu_1()
    while myAns < 9:
        display_menu_1()
        myAns = getIntAnswer()

        if (myAns == 1):
            display_system_data_over_days(dbinfo)
        elif(myAns == 2):
            display_sipinvite_data(dbinfo) 
        elif(myAns == 3):
            res = insert_system_data(dbinfo,"M")
        elif(myAns == 4):
            res = insert_interface_data(dbinfo,"M")
        elif(myAns == 5):
            res = insert_sipinvite_data(dbinfo,"M")
        elif(myAns == 6):
            res = insert_sa_data(dbinfo,"M")
        elif(myAns == 7):
            res = insert_sessionrealm_data(dbinfo,"M")
        elif(myAns == 8):
            res = insert_sipsessions_data(dbinfo,"M")
        elif(myAns == 9):
            res = insert_voltage_data(dbinfo,"M")
        elif(myAns == 10):
            res = insert_fan_data(dbinfo,"M")
        elif(myAns == 11):
            res = insert_temperature_data(dbinfo,"M")
        elif(myAns == 12):
            res = insert_space_data(dbinfo,"M")
        elif(myAns == 13):
            res = insert_networkutil_data(dbinfo,"M")
        else:
            sys.exit(1)    

############################################################
def main():
    cls()
    cfgFile="/home/tluck/HDR/hdr.cfg"
    dbinfo=[]
    dbinfo=readDBconfig(cfgFile) 
    try:
        if sys.argv[1] == "auto":
            #print("Run auto")
            insert_system_data(dbinfo,"A")
            insert_interface_data(dbinfo,"A")
            insert_fan_data(dbinfo,"A")
            insert_voltage_data(dbinfo,"A")
            insert_sipinvite_data(dbinfo,"A")
            insert_sa_data(dbinfo,"A")
            insert_sessionrealm_data(dbinfo,"A")
            insert_sipsessions_data(dbinfo,"A")
            insert_temperature_data(dbinfo,"A")
            insert_space_data(dbinfo,"A")
            insert_networkutil_data(dbinfo,"A")
    except:
        menu(cfgFile)


if __name__=='__main__':
    main()


