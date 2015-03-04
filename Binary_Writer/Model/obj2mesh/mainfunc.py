#!/usr/bin/env python3


#http://research.cs.wisc.edu/graphics/Courses/cs-838-1999/Jeff/BVH.html

import sys,struct,random,math,os.path,traceback,re

from mmath import *
from read import *
from averages import *
from write import *
from warn import *
from armature import *

def compute_materials(oc):
    for od in oc.objs:
        lst=[]
        for k in od.nfwm:
            lst.append( (od.nfwm[k],k) )
        lst.sort()
        if len(lst) == 0:
            od.mainmtl="_FAKE_"
            oc.mtls["_FAKE_"]={
                "Ka":"0 0 0 1",
                "Kd":"1 1 1 1",
                "Ks":"1 1 1 1",
                "Ns":"32",
                "d":"1.0"
            }
        else:
            od.mainmtl = lst[-1][1]
        
def main(inobj,scale,inbvh,level,furdensity,furdivs,
             do_ascii,
             do_ordinary,do_linefur,do_edge,do_unindexed):
    
    warn_reset()
    #construct output filename: replace obj with mesh
    idx=inobj.find(".obj")
    if idx < 0:
        raise Exception("Input file must have .obj suffix")
    
    stem = inobj[:idx]
    
    if scale != 1.0:
        stem += "_"+str(scale)
        
    pfx=""
    
    idx=stem.rfind("/")
    if idx != -1:
        pfx=stem[:idx]
        #stem=stem[idx+1:]
    
    print("Reading from",inobj,"...")
    
    oc = read_obj_data(inobj,pfx,scale)
    if level == 8:
        read_armature_data(oc,inobj,pfx)
        
    compute_face_normals(oc)
    compute_edge_adjacency_info(oc)
    compute_tangents(oc)
    compute_materials(oc)
    
    fverts = oc.fverts
    fnorms = oc.fnorms
    ftexs = oc.ftexs
    mtls = oc.mtls
    tangents = oc.tangents
    binormals = oc.binormals
    snormals = oc.snormals 
    objdats = oc.objs 

    outs=[]
    for od in objdats:
        if len(od.outverts)==0:
            continue 
            
        oname=od.oname
        
        L=[]
        for q in od.nfwm:
            if od.nfwm[q]>0:
                L.append( (od.nfwm[q],q) )
        L.sort()
        if len(L) > 1:
            warn("More than one material used")
        currmtl=mtls[L[-1][1]]
        
        if do_ascii:
            an=stem+"_"+oname+".ascii.mesh"
        else:
            an=None
        bn=stem+"_"+oname+".binary.mesh"
        if do_ordinary:
            write_ordinary_mesh(level,od,an,bn)
            outs.append( ("binarymesh",bn) )

        if do_ascii:
            aen=stem+"_"+oname+".asciiedges.mesh"
        else:
            aen=None
        ben=stem+"_"+oname+".binaryedges.mesh"
        if do_edge:
            write_edge_mesh(od,aen,ben)
            outs.append( ("binaryedges",ben))
        
        if do_ascii:
            atri=stem+"_"+oname+".asciitris.mesh"
        else:
            atri=None
        btri=stem+"_"+oname+".binarytris.mesh"
        if do_unindexed:
            write_unindexed_mesh(level,od,atri,btri)
            outs.append( ("binarytris",btri) )

        if do_ascii:
            a=stem+"_"+oname+".asciilinefur.mesh"
        else:
            a=None
        b=stem+"_"+oname+".binarylinefur.mesh"
        if do_linefur:
            write_linefur_mesh(level,od,a,b,furdensity,furdivs)
            outs.append( ("binarylinefur",b) )
        
    fname=stem+".spec.mesh"
    fp=open(fname,"w")
    for ty,o in outs:
        print(ty,o[len(pfx)+1:],file=fp)
    fp.close()

    print("-----------------")
    print("Spec file:",fname)
        
