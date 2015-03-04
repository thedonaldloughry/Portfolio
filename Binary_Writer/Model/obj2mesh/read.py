#!/usr/bin/env python3


#http://research.cs.wisc.edu/graphics/Courses/cs-838-1999/Jeff/BVH.html

import sys,struct,random,math,os.path,traceback,re

from mmath import *
from warn import *

class ObjDat:
    def __init__(self,oname,oc):
        self.oname=oname
        self.outverts=[]    #vertices to output
                            #list of (vi,ti,ni,group) tuples
        self.outtris=[]     #list of (i0,i1,i2, vi0,vi1,vi2, ti0,ti1,ti2) 
                            #triples of indices:
                            #First three are indices in outverts
                            #Second three are indices in fverts
        self.facetnorms=[]  #one entry per outtris entry: Faceted normals
        self.vdict={}       #maps (vi,ti,ni,groupnum) to index in outverts
        self.nfwm={}        #maps mtl name to number of faces with that
                            #material so we know which materials are most
                            #heavily used
        self.mainmtl=None
        self.edge_normals={}    #key=set of indices from fverts
                                #value = [vertex,vertex,
                                #   normal,normal,normal,... ]
                                #Associates edge with normals of faces
                                #adjacent to that edge
                                #If entries are p0,p1,n0,...
                                #then edge p0p1 belongs to triangle with
                                #normal n0
        self.owner=oc
    
class ObjCollection:
    def __init__(self):
        self.fverts=[None]      #file vertices
        self.fnorms=[None]      #file normals
        self.ftexs=[None]       #file textures coords
        self.weights=[None]     #weights for animation. length==len(fverts)
                                #list of (weight,bonename) pairs
        self.bonelist=[]        #list of bones for skeletal animation
        self.bonemap={}         #map bone names to indices in bonelist
        self.bonedepth=-1       #max depth of the bone tree
        self.mtls={}            #key=string, value=Material (as a dictionary)
        self.tangents=[None]    #tangents. length == len(fverts)
        self.binormals=[None]   #binormals; length == len(fverts)
        self.snormals=[None]    #smoothed (averaged) normals. length==len(fverts)
        self.objs=[]            #list of ObjDat items
        
def read_obj_data(inobj,pfx,scale):
    try:
        ifp=open(inobj,"r")
    except IOError:
        if have_tk:
            showerror("Error","I can't find the file "+inobj)
            raise
            
    currmtl=None        #current material
    
    oc = ObjCollection()
    
    fverts=oc.fverts
    fnorms=oc.fnorms
    ftexs=oc.ftexs
    mtls=oc.mtls
    tangents=oc.tangents
    binormals=oc.binormals
    snormals=oc.snormals
    objdats=oc.objs
    weights=oc.weights
    
    currgroup=None  #current polygon group ('g' lines)
    
    filedat = ifp.readlines()
    for line in filedat:
        line=line.strip()
        lst=line.split()
        if len(line) == 0 or line[0] == "#":
            pass
        elif lst[0] == "o":
            tmp=lst[1]
            tmp=re.sub(r"\W","_",tmp)
            objdats.append(ObjDat(tmp,oc))
            print("------------Parsing object",tmp,"from",inobj,"----------------")
        elif lst[0] == "v":
            if len(objdats) == 0:
                objdats.append(ObjDat("_anonymous_",oc))
            lst=line.split(" ")[1:]
            fverts.append( Vector4(scale*float(lst[0]),scale*float(lst[1]),scale*float(lst[2]),1.0) )
            tangents.append(Vector4(0,0,0,0))
            binormals.append(Vector4(0,0,0,0))
            snormals.append(Vector4(0,0,0,0))
            ww=[]
            wsum=0
            for jj in range(3,len(lst),2):
                wt=lst[jj]
                bname=lst[jj+1]
                ww.append( [float(wt),bname] )
                wsum += ww[-1][0]
                if len(ww) == 4:
                    break 
            while len(ww) < 4:
                ww.append( [0,None] )
            if wsum != 0:
                for q in ww:
                    q[0] /= wsum
            else:
                #no bones influence this vertex
                #give the root bone 100% influence
                ww=[ (1,None), (0,None), (0,None), (0,None) ]
                
            #sort in decreasing order of weight
            ww.sort( key=lambda x: -x[0] )
            
            #take only the top 4 bones
            ww=ww[:4]
            
            weights.append(ww)
        elif lst[0] == "vt":
            lst=line.split(" ")[1:]
            if lst[0] == "nan" or lst[1] == "nan":
                warn("NaN texture coordinates")
                ftexs.append(Vector4(0,0,0,1))
            else:
                ftexs.append( Vector4(float(lst[0]),float(lst[1]),0.0,1.0) )
        elif lst[0] == "vn":
            lst=line.split(" ")[1:]
            fnorms.append( Vector4(float(lst[0]),float(lst[1]),float(lst[2]),0.0))
        elif lst[0] == "g":
            tmp=lst[1]
            currgroup=tmp
        elif lst[0] == "f":
            lst=lst[1:]
            vis=[]
            tis=[]
            nis=[]
            if len(lst) != 3:
                warn("Non-triangles found")
            else:
                tri=[]
                for ii in range(3):
                    l2 = lst[ii].split("/")
                    
                    vi = int(l2[0])
                    
                    vis.append(vi)
                    
                    if len(l2) < 2 or len(l2[1]) == 0:
                        warn("Missing texture coordinates")
                        ti=0
                    else:
                        ti=int(l2[1])
                    
                    tis.append(ti)
                    
                    if len(l2) < 3 or len(l2[2]) == 0:
                        warn("Missing normals")
                        ni=0
                    else:
                        ni=int(l2[2])
                    
                    nis.append(ni)
                            
                    V=(vi,ti,ni,currgroup)
                    
                    if V not in objdats[-1].vdict:
                        objdats[-1].vdict[V]=len(objdats[-1].outverts)
                        objdats[-1].outverts.append(V)
                    vidx = objdats[-1].vdict[V]    
                    tri.append(vidx)
                        
                assert len(tri) == 3

                objdats[-1].outtris.append( [tri[0],tri[1],tri[2],
                    vis[0],vis[1],vis[2], tis[0], tis[1], tis[2]] )
                
            if currmtl == None:
                warn("No material on faces")
                    
            if currmtl not in objdats[-1].nfwm:
                objdats[-1].nfwm[currmtl]=0
            objdats[-1].nfwm[currmtl]+=1
            
        elif lst[0] == "mtllib":
            lst=line.split()
            mfile=os.path.join(pfx,lst[1])
            fp2=open(mfile)
            for line in fp2:
                line=line.strip()
                lst=line.split()
                if len(lst) == 0 or line[0] == '#':
                    pass
                elif lst[0] == "newmtl":
                    if len(lst) == 1:
                        mname = None
                    else:
                        mname=lst[1]
                    mtls[mname]={}
                else:
                    if len(lst) == 2:
                        mtls[mname][lst[0]] = lst[1]
                    else:
                        mtls[mname][lst[0]] = lst[1:]
            fp2.close()
        elif lst[0] == "usemtl":
            if len(lst) == 1:
                currmtl = None
            else:
                currmtl=lst[1]
            if len(objdats) > 0 and currmtl not in objdats[-1].nfwm:
                objdats[-1].nfwm[currmtl]=0
        else:
            #ignore
            pass
        
    return oc
