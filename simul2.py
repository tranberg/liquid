import numpy as np
from random import *
from scipy.stats import norm

#parameters
pop = 50
runs = 10

#vars
avg_finalnode_pk = 0

#delegation function
def dele(pk):
    x = 1-norm.cdf(pk)
    y = random()
    if x > y:
        return 1    # delegate
    else:
        return 0    # not delegate

#which nodes links to this node, function
def linksto(node):
    return np.where(list[2]==node)[0]

#structure parsing function
def counter(pot,level,dels):
    #print "we're now at level =",level
    for i in pot:
        dels[0].append(i)
        dels[1].append(level)
        #print "i=",i
        a = linksto(i)
        #print 'a=',a
        for b in a:
            b = [b]
            counter(b,level+1,dels)
    level -= 1
    #print "we're back to level =",level
    return dels

for p in range(runs):

    #set up initial array
    list = np.zeros((5,pop))
    # 1: final voting power (FVP)
    # 2: political knowledge
    # 3: delegate to who?
    # 4: will you delegate? yes/no: 1/0
    # 5: Voting power before delegation (if any)

    #put in PK values
    list[0,:] = 1
    for i in range(pop):
        list[1,i] = gauss(0,1)

    #sort after PK value
    list = np.sort(list,1)  # sorting after voting power

    #fill in delegations
    for i in range(pop):
        list[3,i] = dele(list[1,i])

    #list=np.array([[0,0,0,0,0,0,0,7,0,3,1],[0,0,0,0,0,0,0,0,0,0,0],[5,5,6,8,5,6,7,0,9,0,0],[1,1,1,1,1,1,1,0,1,0,0],[1,1,1,1,1,4,6,7,2,3,1]])

    #decide if it actually delegates
    x=1
    while x>0:
        x=0
        for i in range(pop-1):
            if list[0,i]>0:
                list[4,i] = list[0,i]
                if list[3,i]==1:
                    startrange = 0
                    for m,k in enumerate(list[1]):
                        if k>list[1,i]+.5:
                            startrange = m
#                            print "startrange: ",startrange,"; i: ",i,"; list[1,i]: ",list[1,i],"; +0.5: ",(list[1,i]+.5),"; k: ",k
                            break
                    if startrange == 0:
                        list[3,i] = 0
                        list[2,i] = -1
                    else:
#                        print startrange

                        p = randint(startrange,pop-1)
                        list[0,p] += list[0,i]
                        list[2,i] = p
                        list[0,i] = 0
                    x+=1
        list[4,pop-1] = list[0,pop-1]
    #find top nodes
    top = np.where((list[0]-list[4])==0)[0] # list of highest rank nodes
#    print top

    #replace DT=0 with -1 (to prevent infinite loops with counter function
    for n, i in enumerate(list[2]):
        if i==0:
            list[2,n] = -1

    #call the counter function
    dels = [[],[]]
    level = 0
    d = counter(top,0,dels)
#    print list
#    print d
#    print len(d[0]),len(d[1])

    #average FNP of all final nodes
    sum = 0
    for i in top:
        sum += list[1,i]*list[0,i]
    avg_finalnode_pk += sum/pop

    print "at run ",p

#divide by number of runs
avg_finalnode_pk = avg_finalnode_pk/runs

#print "avg. node PK of ",runs," is ",avg_node_pk
print "avg. finalnode PK of ",runs," is ",avg_finalnode_pk