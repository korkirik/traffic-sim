'''
Swarm optimization with ethical behaviour constraints
Created on 20 Mar 2018

@author: Alexander Struck, Rhein-Waal University of Applied Sciences
'''
import numpy as np
from math import *
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy import stats 
#from operator import pos
import copy



"""class Vector:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
"""
#def remove_duplicates(data_array):
 #   uniques = []
  #  for arr in data_array:
   #     if not any(np.array_equal(arr, unique_arr) for unique_arr in uniques):
    #        uniques.append(arr)
    #return uniques
def remove_duplicates(victim_array):
    
    if len(victim_array)>1:
        rem=[]
        for i in range(0,len(victim_array)-1):
            for j in range(i+1,len(victim_array)):
                #print"ij",i,j,len(victim_array)
                if victim_array[i].position == victim_array[j].position:
                        if victim_array[i].rescue_status != victim_array[j].rescue_status:
                            victim_array[i].rescue_status=1
                        rem.append(j)
                        
        for index in sorted(rem, reverse=True):
            del victim_array[index]
   # return victim_array  
# --------- define agent class ---------------------------------------#
class agent:
    def __init__(self,id_idx,position,velocity,comm_range,scan_range,charge,recharge_flag,attitude,worldrange):
        self.id_idx = id_idx
        self.position = position
        self.velocity = velocity
        self.comm_range = comm_range
        self.scan_range = scan_range
        self.charge = charge
        self.recharge_flag = recharge_flag
        self.attitude = attitude
        self.worldrange=worldrange
        self.victim_map = []
        self.sector_weight = []
        self.n_of_sectors=int(floor(np.pi*self.worldrange/self.scan_range))
        for i in range(0,self.n_of_sectors):
            self.sector_weight.append(1.0)
        self.sector_angle=2*np.pi/self.n_of_sectors

        
        #self.acceleration = [None, acceleration, None]
        #self.mass = mass
    def update_victim_map(self, newmap):
        if len(newmap)>0:
            #print"L: ", len(self.victim_map), len(newmap)
            self.victim_map=self.victim_map + newmap
            # self.victim_map = remove_duplicates(self.victim_map)
            #print"LL: ", len(self.victim_map)
            remove_duplicates(self.victim_map)
            #print"LLL: ", len(self.victim_map)
    def add_victim(self,newvictim):
        self.victim_map.append(newvictim)
        #self.victim_map = remove_duplicates(self.victim_map)
        remove_duplicates(self.victim_map)
    def scan(self,victims,swarm,base):
        for victim in victims:
            distance=sqrt((victim.position[0]-self.position[0])**2+(victim.position[1]-self.position[1])**2)
            if distance <= self.scan_range:
                self.add_victim(victim)
        for agent in swarm:
            distance=sqrt((agent.position[0]-self.position[0])**2+(agent.position[1]-self.position[1])**2)
            if distance <= self.comm_range:
                self.update_victim_map(agent.victim_map)
        distance=sqrt((base.position[0]-self.position[0])**2+(base.position[1]-self.position[1])**2)
        self.distance_base=distance
        if distance <= self.comm_range:
            base.update_victim_map(self.victim_map)
            self.update_victim_map(base.victim_map)
    
    def utilization(self):
        #a_sector =self.scan_range/(2.0*self.worldrange)#2*np.pi/self.n_of_sectors 
        sw=1.0-sqrt((self.position[0])**2+(self.position[1])**2)/self.worldrange
        #sw=sqrt((self.position[0])**2+(self.position[1])**2)/self.worldrange
        agl=atan2(self.position[1],self.position[0])
        if agl<0.0:
            agl=agl+2.0*np.pi
        nr_sector=int(floor(agl/self.sector_angle))
        #print agl/np.pi, self.sector_angle, nr_sector,self.n_of_sectors
        if self.sector_weight[nr_sector] > sw  and sw > 0.0:
            self.sector_weight[nr_sector] =sw
            #print sw
# --------- define victim class --------------------------------------#
class victim:
    def __init__(self,id_idx,position,health,rescue_status):
        self.id_idx = id_idx
        self.position=position
        self.health=health
        self.rescue_status=rescue_status
        self.dist=0
    def set_dist(self,d):
        self.dist=d

# --------- define base class ----------------------------------------#
class base:
   
    def __init__(self,position):
        self.position=position
        self.victim_map = []
    
    def update_victim_map(self, newmap):
        if len(newmap) >0:
            self.victim_map=self.victim_map + newmap
            #self.victim_map = remove_duplicates(self.victim_map)
            remove_duplicates(self.victim_map)
# --------------------------------------------------------------------#
# ------------------------GLOBAL FUNCTIONS ---------------------------#
def update_utilization(map1,map2):
    res = []
    for i in range(0,len(map1)):
        res_i = min(map1[i],map2[i])
        res.append(res_i)
    return(res)
        
def update(swarm,base,victims,worldrange):
    global vcount,vmax,chargemax,distance_distribution
#check if recharge is needed
    #print "Median distance: ",stats.nanmedian(distance_distribution(swarm)),"Mean distance: ",stats.nanmean(distance_distribution(swarm))
    for agent in swarm: 
        if agent.charge > 0:
            dist_to_base=sqrt((agent.position[0]-base.position[0])**2+(agent.position[1]-base.position[1])**2)
            
            if dist_to_base >= 1.5*agent.charge:
                agent.recharge_flag=1
            else:
                agent.recharge_flag=0
            #check if base is in range
            if dist_to_base <= agent.comm_range :
                base.update_victim_map(agent.victim_map)
                agent.update_victim_map(base.victim_map)
                #print "Update vmap: Agent ", agent.id_idx
            # recharge when close to base
            if dist_to_base <= 10.0:#0.1*worldrange:
                agent.recharge_flag=0
                agent.charge = chargemax
                #print "Recharge: Agent ", agent.id_idx
            
            for victim in victims:
                #check if new victims are in range
                if victim.rescue_status ==0 :
                    dist_to_vic=sqrt((agent.position[0]-victim.position[0])**2+(agent.position[1]-victim.position[1])**2)
                    if dist_to_vic <= agent.scan_range:
                        agent.add_victim(victim)
                        remove_duplicates(agent.victim_map)
                        #print "Agent ",agent.id_idx, " found new victim!"
                    #rescue close victims
                    if (dist_to_vic <= 10.0):#0.1*worldrange
                            victim.rescue_status = 1 
                            for v in agent.victim_map:
                                if victim.id_idx == v.id_idx:
                                    v.rescue_status = 1
                                    #print "Update vmap to 1"
                            #print "Rescued victim ", victim.id_idx, " by agent ",agent.id_idx
                            vcount=vcount+1
                
            #check if other agents are in range
            for fellow in swarm:
                if agent.id_idx != fellow.id_idx:
                    dist_to_fellow=sqrt((agent.position[0]-fellow.position[0])**2+(agent.position[1]-fellow.position[1])**2)
                    if dist_to_fellow <= agent.comm_range:
                        agent.update_victim_map(fellow.victim_map)
                        agent.sector_weight = update_utilization(agent.sector_weight, fellow.sector_weight)
                        #print "Agent ",agent.id_idx, " met agent " , fellow.id_idx      
            # --------------- set up coefficients ------------------------------------------------------------------------#
            
            #cstable=exp(-agent.attitude)*(1-agent.recharge_flag)
            cstable=(1.0-agent.attitude)*(1-agent.recharge_flag)
            crnd=(1-agent.recharge_flag)*exp(-agent.attitude)
            crnd=(1.0-agent.attitude)*(1-agent.recharge_flag)
            cbase=exp(-agent.attitude)*agent.recharge_flag*exp(chargemax/(agent.charge+0.1))
            #cbase=exp(-agent.attitude)*agent.recharge_flag*exp(chargemax/(agent.charge+0.1))
            cnorm=0.0
            cnorm=cstable+crnd+cbase
            cvic=np.zeros(len(agent.victim_map),float)
            # -------------------------------------------------------------------------------------------------------------#
            # -------------------------------- setup velocities------------------------------------------------------------#
            
            vel=np.array([agent.velocity[0],agent.velocity[1]])
            pos=np.array([agent.position[0],agent.position[1]])
            bpos=np.array([base.position[0],base.position[1]])
            # stable and random velocity component
            rphi=np.random.uniform(0.0,2.0*np.pi)
            rvx=cos(rphi)*vmax
            rvy=sin(rphi)*vmax
            vrnd=np.array([rvx,rvy])
            vel=cstable*vel+crnd*vrnd
            # return to base component
            d=bpos-pos
            vel=vel+cbase*d/sqrt((d[0])**2+(d[1])**2)*vmax
            # move to victim component
            for victim in agent.victim_map:
                
                dist_to_vic=sqrt((agent.position[0]-victim.position[0])**2+(agent.position[1]-victim.position[1])**2)
                #print "VSTAT:", agent.id_idx,victim.id_idx,victim.rescue_status,dist_to_vic/worldrange
                #deploy rescue if in range
                
                        #cv=agent.attitude*worldrange/dist_to_vic*(1-victim.rescue_status)
                #cv=agent.attitude*(1.0-dist_to_vic/worldrange)*(1-victim.rescue_status)
                if dist_to_vic>10.0:#0.1*worldrange:
                    cv=exp(agent.attitude)*exp(-dist_to_vic/worldrange)*(1-victim.rescue_status)
                    #cv=agent.attitude*(1.0-dist_to_vic/worldrange)*(1-victim.rescue_status)
                    #cv=agent.attitude*worldrange/(dist_to_vic)**6*(1-victim.rescue_status)
                    #print "cv: ",cv,victim.id_idx,len(agent.victim_map),victim.rescue_status
                else:
                    cv=0.0
                vpos=np.array([victim.position[0],victim.position[1]])
                #print cv
                d=vpos-pos
                #print "d:",d,vpos,pos
                #print "vic pos:",agent.id_idx,victim.id_idx,cvic[victim.id_idx],d/sqrt((d[0])**2+(d[1])**2)
                #vel=vel+cvic[victim.id_idx]*d/dist_to_vic*vmax
                vel=vel+cv*d/dist_to_vic*vmax
                v=sqrt(vel[0]**2+vel[1]**2)
                #cvic.append(cv)       
                cnorm=cnorm+cv
             
            for fellow in swarm:
                if agent.id_idx != fellow.id_idx:
                    fpos=np.array([fellow.position[0],fellow.position[1]])
                    d=fpos-pos
                    dist_to_fellow = sqrt((d[0])**2+(d[1])**2)
                    d=d/dist_to_fellow
                    #print "d:",d,fpos,pos
                    if dist_to_fellow < 10.0:#0.1*worldrange:
                        vel=vel-d*vmax
                        cnorm=cnorm+1.0 
             
            # improve utilization of area
            agent.utilization() 
            for j in range(0,agent.n_of_sectors):
                alp=(1.0*j+0.5)*agent.sector_angle
                sector_pos=np.array(worldrange/2.0*np.cos(alp),worldrange/2.0*np.sin(alp))
                d=sector_pos-pos
                dist_to_sector = sqrt((d[0])**2+(d[1])**2)
                d=d/dist_to_sector
                vel=vel+agent.sector_weight[j]*d*vmax*0.0001
                cnorm=cnorm+agent.sector_weight[j]*0.0001
                
            if cnorm > 0.0:
                cstable=cstable/cnorm
                crnd=crnd/cnorm
                cbase=cbase/cnorm
                cvic=cvic/cnorm
            else:
                crnd=1.0
                cnorm=1.0
                vel=vrnd
                #print"Coeff:", agent.id_idx,cstable,crnd,cbase,cvic,agent.charge
        
        
            
                
            #if v != 0.0:
            vel=vel/cnorm
            agent.velocity=([vel[0],vel[1]])
            pos=pos+vel
            agent.position=([pos[0],pos[1]])
            agent.charge=agent.charge-1
            if sqrt((pos[0])**2+(pos[1])**2)>worldrange:
                vel=-vel  
                agent.velocity=([vel[0],vel[1]])
            #print"vel:", agent.id_idx,agent.velocity,sqrt((agent.velocity[0])**2+(agent.velocity[1])**2)
        
        else:
            agent.velocity=(0.0,0.0)
        # ---------------------------------------end update-------------------------------------------------------------#
        #print "Agent:",agent.id_idx,agent.charge,agent.recharge_flag,len(agent.victim_map)
    #print "########### VICTIMS FOUND:", vcount
    

def read_config(cfg_file):
    #read swarm configuration from file
    global chargemax, worldrange, vmax, crange, srange,nov,noa,ethics_mean,ethics_spread
    infile=open(cfg_file,'r')
    line=infile.readline()
    line=infile.readline()
    cols=line.split()
    worldrange=float(cols[0])
    line=infile.readline()
    line=infile.readline()
    cols=line.split()
    noa=int(cols[0])
    line=infile.readline()
    line=infile.readline()
    cols=line.split()
    nov=int(cols[0])
    line=infile.readline()
    line=infile.readline()
    cols=line.split()
    chargemax=float(cols[0])
    line=infile.readline()
    line=infile.readline()
    cols=line.split()
    crange=float(cols[0])
    line=infile.readline()
    line=infile.readline()
    cols=line.split()
    srange=float(cols[0])
    line=infile.readline()
    line=infile.readline()
    cols=line.split()
    ethics_mean=float(cols[0])
    ethics_spread=float(cols[1])
    line=infile.readline()
    line=infile.readline()
    cols=line.split()
    vmax=float(cols[0])
    
    
    
    infile.close()
def print_cfg():
    print ("Worldrange: ",worldrange)
    print ("Number of agents/destinations: ",noa,nov)
    print ("Scan range: ",srange)
    print ("Comm range: ",crange)
    print ("Ethics: ",ethics_mean,ethics_spread)
    print ("Vmax: ",vmax)
def distance_distribution(swarm):
    distances = []
    for i in range(0,len(swarm)-1):
        for j in range(i+1,len(swarm)):
            d=sqrt((swarm[i].position[0]-swarm[j].position[0])**2+(swarm[i].position[1]-swarm[j].position[1])**2)
            distances.append(d)
            
    return distances
        
# --------- initialization -------------------------------------------#

nov=30 # number ov victims
noa=60 #number of agents

Lx=100 # dimension of search field
Ly=100
worldrange=100.0
chargemax= 200 # maximum charge
vmax=10.0
swarm   = []
swarm_orig = []
victims = []
victims_orig = []
base_x =0.0
base_y=0.0
base=base([base_x,base_y])
crange=0.2*worldrange # comm range
srange=2*worldrange # scan range
ethics_mean=0.5
ethics_spread=0.1
read_config('swarm.config')
print_cfg()
# --- set up victims ----------------------------------------#
for i in range(0,nov):
    rphi=np.random.uniform(0.0,2.0*np.pi)
    rr=np.random.uniform(0.2*worldrange,0.9*worldrange)
    rx=cos(rphi)*rr
    ry=sin(rphi)*rr
    rh = 100#np.random.randint(20,100)
    victims.append(victim(i,[rx,ry],rh,0))
    
#victims_orig=copy.deepcopy(victims)
# -----------------------------------------------------------#
#set up swarm
for i in range(0,noa):
    rphi=np.random.uniform(0.0,2.0*np.pi)
    rx=cos(rphi)*12.0#0.12*worldrange
    ry=sin(rphi)*12.0#0.12*worldrange
    rphi=np.random.uniform(0.0,2.0*np.pi)
    rvx=cos(rphi)*vmax
    rvy=sin(rphi)*vmax
    
    if ethics_spread >0.0 :
        rattitude = np.random.normal(ethics_mean,ethics_spread) # attitude 1: altruistic,0:egoistic
    else:
        rattitude = ethics_mean
    
    swarm.append(agent(i,[rx,ry],[rvx,rvy],crange,srange,chargemax,0,rattitude,worldrange))
    
swarm_orig=copy.deepcopy(swarm)



# -------end initialization ------------------------------------------# 


# ------- main program -----------------------------------------------#

plot_flag = 1
if plot_flag == 1:
    # ------- PLOTTER ----------------------------------------------------#
    # ---- set up plotting area ---- #
     #set up figure and axes
    fig, ax = plt.subplots(figsize=(8,8))
    #set axes limits (in advance, stops dynamic rescaling of the axes
    ax.set(xlim=(-worldrange,worldrange),ylim=(-worldrange,worldrange))
    xa=np.zeros(noa,float)
    ya=np.zeros(noa,float)
    
    for i in range(0,noa):
        xa[i]=swarm[i].position[0]
        ya[i]=swarm[i].position[1]
    xv=np.zeros(nov,float)
    yv=np.zeros(nov,float)
    for i in range(0,nov):
        xv[i]=victims[i].position[0]
        yv[i]=victims[i].position[1]
    #for i in range(0,nov):   
    #print i,"Plot: ",xv[i],yv[i]
    scat_swarm = ax.scatter(xa,ya,color="blue")
    scat_vic = ax.scatter(xv,yv,color="red",s=100)
    circle = plt.Circle((0, 0), radius=worldrange, fc='none')
    circle_base = plt.Circle((0, 0), radius=0.02*worldrange, fc='pink')
    plt.gca().add_patch(circle)
    plt.gca().add_patch(circle_base)
    
    #for agent in swarm:
    #    print"vel0:", agent.id_idx,agent.velocity,sqrt((agent.velocity[0])**2+(agent.velocity[1])**2)
        
    
    #update(swarm,base,victims,worldrange)
    vcount=0
    def animate(i):
        #line.set_ydata(F[i, :])
        #line.set_ydata(np.cos(i*x)*np.sin(i*y))
        #scatter
        update(swarm,base,victims,worldrange)
        for i in range(0,noa):
            xa[i]=swarm[i].position[0]
            ya[i]=swarm[i].position[1]
            
        for i in range(0,nov):
            xv[i]=victims[i].position[0]
            yv[i]=victims[i].position[1]
        
         # ::3 instead of : reduces number of points
        #scat.set_offsets(np.c_[x[::3], y_i])
        scat_swarm.set_offsets(np.c_[xa,ya])
        scat_vic.set_offsets(np.c_[xv,yv])
        #scat2.set_offsets(np.c_[x, 0.5*y_i])
        for victim in victims:
            if victim.rescue_status == 1:
                circle_resc = plt.Circle((victim.position[0], victim.position[1]), radius=0.025*worldrange, fc='green')
                plt.gca().add_patch(circle_resc)
    # the function needs 1 argument; only the y data are changed
    
    # call FuncAnimation and display
    
    anim = FuncAnimation(fig, animate)
    
    
    plt.draw()
    plt.show()    
    # ------- END PLOTTER ------------------------------------------------#
run_flag = 0
if run_flag == 1:
    
    # ------- RUNNER -----------------------------------------------------#
    nr_of_configs = 10  #number of different victim configurations 
    nr_of_ethics = 11   #number of different ethics configurations 
    for j in range(0,nr_of_configs):  
        flname2="r"+str(j)+".dat"
        print (flname2)
        f2=open(flname2,"w")
        # --- set up victims ----------------------------------------#
        for i in range(0,nov):
            rphi=np.random.uniform(0.0,2.0*np.pi)
            rr=np.random.uniform(0.2*worldrange,0.9*worldrange)
            rx=cos(rphi)*rr
            ry=sin(rphi)*rr
            rh = 100#np.random.randint(20,100)
            victims.append(victim(i,[rx,ry],rh,0))
            
        victims_orig=copy.deepcopy(victims)
# -----------------------------------------------------------#
        for u in range(0,nr_of_ethics):
            
            swarm=copy.deepcopy(swarm_orig)
            victims=copy.deepcopy(victims_orig)
            
            
            for i in range(0,noa):
                if u == 0 :
                    rattitude =0.0
                    ethics_mean=0.0
                    ethics_spread=0.0
                 # attitude 1: altruistic,0:egoistic
                if u >0 and u<nr_of_ethics-1:
                    ethics_mean=u*1.0/(nr_of_ethics-1)
                    ethics_spread=0.1
                    rattitude = np.random.normal(ethics_mean,ethics_spread)
                if u == nr_of_ethics-1:
                    rattitude = 1.0
                    ethics_mean =1.0
                    ethics_spread=0.0
                
                swarm[i].attitude = rattitude
            print ("Ethics: ", u,ethics_mean, ethics_spread)
            flname="t"+str(j)+"-"+str(u)+".dat"
            print (flname)
            
            f1=open(flname,"w")
            vcount=0
            for t in range(100):
                tau=t*1.0
                vc=vcount*1.0
                #for j in range(0,len(swarm[0].victim_map)):
                    #print u,t,vcount,swarm[0].victim_map[j].position
                update(swarm, base, victims, worldrange)
                #print "Median distance: ",stats.nanmedian(distance_distribution(swarm)),"Mean distance: ",stats.nanmean(distance_distribution(swarm))
                f1.write('%8.4f %8.4f %8.4f %8.4f' %(tau,vc,stats.nanmedian(distance_distribution(swarm)),ethics_mean))
                f1.write('\n')
                f1.flush()
            f1.close()
            print( u,t,vcount)
            f2.write('%8.4f %8.4f' %(ethics_mean,vc))
            f2.write('\n')
            f2.flush()
        
        del(victims[:])
        f2.close()
    print( "Done.")
    # ------- END RUNNER -------------------------------------------------#
# ---------- end main-------------------------------------------------#
