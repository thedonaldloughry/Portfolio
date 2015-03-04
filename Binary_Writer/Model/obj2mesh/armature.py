
#IMPORTANT! The mesh + armature should NOT have
#any overall translation, rotation, or scale -- else, this won't work properly.

from mmath import *

class Node:
    def __init__(self,name,parent,nodelist):
        self.idx=len(nodelist)
        nodelist.append(self)
        self.name=name
        self.ch=[]
        self.head=None   #where the bone's head is (absolute position)
        self.channels=[]
        self.endeff=None   #where the end effector is. Only defined
                        #if this bone has no children.
        self.parent=parent
        
        #index = frame number
        #values = data for each channel for that frame as a tuple
        self.framedata=[]
        
        #quaternion data
        #one Quaternion per frame
        self.qframedata=[]
        
    def parse(self,fp,nodelist):
        #assume fp is sitting just before the opening { of this
        #item's definition
        x=fp.readline()
        x=x.strip()
        assert x == "{"
        while 1:
            x=fp.readline()
            x=x.strip()
            lst=x.split()
            if lst[0] == "OFFSET":
                #this is relative to the parent, not an
                #absolute position
                self.head=Vector4( 
                    float(lst[1]),float(lst[2]),float(lst[3]),0.0)
                if self.parent != None:
                    self.head = self.head + self.parent.head
            elif lst[0] == "CHANNELS":
                self.channels = lst[2:]
            elif lst[0] == "JOINT":
                b=Node(lst[1],self,nodelist)
                b.parse(fp,nodelist)
                self.ch.append(b)
            elif lst[0] == "End" and lst[1]== "Site":
                #location of the end effector
                fp.readline()   #{
                x=fp.readline().strip()
                lst=x.split()
                assert lst[0]=="OFFSET"
                self.endeff=Vector4(float(lst[1]),
                    float(lst[2]),
                    float(lst[3]),0.0)
                fp.readline()   #}
            elif lst[0] == "}":
                return 
            else:
                print("Got",lst)
                assert 0

        assert self.end != None
        assert len(self.ch) != 0
def compute_maxdepth(n):
    if len(n.ch) == 0:
        return 1
    else:
        x=-1
        for c in n.ch:
            d = compute_maxdepth(c)
            if d > x:
                x=d
        return x+1
        
def compute_quaternions(n):
    # if we have quaternions a and b:
    # a*b = rotate first by b, then by a
    framedata = n.framedata
    for j in range(len(framedata)):
        Q=Quaternion(Vector4(0,0,0,0), 1.0)
        for i in range(len(n.channels)):
            if n.channels[i] in ["Xposition","Yposition","Zposition"]:
                continue 
            if n.channels[i] == "Xrotation":
                axis=Vector4(1,0,0,0)
            elif n.channels[i] == "Yrotation":
                axis=Vector4(0,1,0,0)
                #axis=Vector4(0,0,1,0)
            elif n.channels[i] == "Zrotation":
                axis=Vector4(0,0,1,0)
                #axis=Vector4(0,1,0,0)
            else:
                assert 0
                
            #this is in degrees
            angle = framedata[j][i]
            
            q=quat_for_rot( 
                angle/180.0 * 3.14159265358979323,
                axis)
            Q=q*Q
        n.qframedata.append(Q)
    for c in n.ch:
        compute_quaternions(c)
        
        
def read_armature_data(oc,inobj,pfx):
    #parse a biovision bvh file
    nodelist = oc.bonelist
    nodemap = oc.bonemap
    
    fname=inobj.replace(".obj",".bvh")
    try:
        fp=open(fname)
    except IOError:
        print("Cannot make armature without BVH file")
        assert 0
        
    assert fp.readline().strip() == "HIERARCHY"
    lst=fp.readline().strip().split()
    assert lst[0] == "ROOT"
    root = Node(lst[1],None,nodelist)
    root.parse(fp,nodelist)
    
    for n in nodelist:
        nodemap[n.name]=n.idx
        
    x=fp.readline().strip()
    assert x == "MOTION"
    lst=fp.readline().strip().split()
    assert lst[0] == "Frames:"
    numframes=int(lst[1])
    fp.readline()       #Frame Time
    #data follows
    #one line per frame
    for i in range(numframes):
        lst=fp.readline().strip().split()
        j=0
        for n in nodelist:
            L=[]
            for k in range(len(n.channels)):
                L.append(float(lst[j]))
                j+=1
            n.framedata.append(L)
    
    compute_quaternions(root)
    
    md = compute_maxdepth(root)
    oc.bonedepth = md

    #make sure it follows the format we expect
    assert len(nodelist[0].channels) == 6
    assert root.channels[0] == "Xposition"
    assert root.channels[1] == "Yposition"
    assert root.channels[2] == "Zposition"
    assert root.channels[3] == "Xrotation"
    assert root.channels[4] == "Yrotation"
    assert root.channels[5] == "Zrotation"
    for n in nodelist[1:]:
        assert len(n.channels) == 3
        assert n.channels[0] == "Xrotation"
        assert n.channels[1] == "Yrotation"
        assert n.channels[2] == "Zrotation"
