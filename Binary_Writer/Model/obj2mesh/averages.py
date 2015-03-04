#!/usr/bin/env python3

from mmath import *
from warn import *

def compute_face_normals(oc):
    #compute faceted and smooth face normals for the object collection
    fverts = oc.fverts 
    assert len(oc.snormals) == len(oc.fverts)
    
    for o in oc.objs:
        for t in o.outtris:
            #compute faceted normals
            tri=t[3:6]      #indices in fverts
            v0 = fverts[tri[0]]
            v1 = fverts[tri[1]]
            v2 = fverts[tri[2]]
            vv1 = v1-v0
            vv2 = v2-v0
            fn = cross(vv1,vv2)
            if length(fn) == 0:
                warn("Degenerate triangle")
                fn=Vector4(0,1,0,0)
                        
            fn=normalize(fn)
            o.facetnorms.append(fn)
            oc.snormals[tri[0]] += fn
            oc.snormals[tri[1]] += fn
            oc.snormals[tri[2]] += fn
    for i in range(1,len(oc.snormals)):
        le = length(oc.snormals[i])
        if le == 0:
            warn("Smooth normal is zero")
            oc.snormals[i] = Vector4(0,1,0,0)
        else:
            oc.snormals[i] = 1.0/le * oc.snormals[i]

def compute_edge_adjacency_info(oc):
    fverts = oc.fverts
    snormals = oc.snormals
    assert len(fverts) == len(snormals)
    
    for o in oc.objs:
        assert len(o.outtris) == len(o.facetnorms)
        for i in range(len(o.outtris)):
            t=o.outtris[i]
            fn=o.facetnorms[i]
            ilist = t[3:6]
            for kk in range(3):
                vvi0 = ilist[kk]
                vvi1 = ilist[(kk+1)%3]
                vv0 = fverts[vvi0]
                vv1 = fverts[vvi1]
                key=frozenset([vvi0,vvi1])
                if key not in o.edge_normals: 
                    o.edge_normals[key]=[vv0,vv1]
                o.edge_normals[key].append(fn)
                
#compute tangent and bitangent vectors
#Assume that normals have been computed already.
def compute_tangents(oc):
    ftexs = oc.ftexs
    fverts = oc.fverts
    tangents = oc.tangents
    binormals = oc.binormals
    snormals = oc.snormals

    assert len(snormals) == len(fverts)
    assert len(tangents) == len(snormals)
    assert len(binormals) == len(snormals)
    
    #for i in range(len(snormals)):
    #    tangents.append(None)
    #    binormals.append(None)
    
    for o in oc.objs:
        for t in o.outtris:
            vi0=t[3]
            vi1=t[4]
            vi2=t[5]
            ti0=t[6]
            ti1=t[7]
            ti2=t[8]
            
            if not (ti0>0 and ti1>0 and ti2>0):
                warn("Cannot compute tangents: Missing texcoords")
                t0=Vector4(0,0,0,1)
                t1=Vector4(1,0,0,1)
                t2=Vector4(0,1,0,1)
            else:
                t0 = ftexs[ti0]
                t1 = ftexs[ti1]
                t2 = ftexs[ti2]
            
            v0 = fverts[vi0]
            v1 = fverts[vi1]
            v2 = fverts[vi2]
                   
            #make all vertex coords be relative to vertex 0
            q0=Vector4(0,0,0,0)
            q1 = v1-v0
            q2 = v2-v0
                    
            #make texture coordinates be relative to tc 0
            r0 = Vector4(0,0,0,0)
            r1=t1-t0
            r2=t2-t0
                
            #FIXME: do we need to account for wrapping?
                
            #We know that:
            #  [ r1x  r1y ] [ Tx Ty Tz ] = [ q1x q1y q1z ]
            #  [ r2x  r2y ] [ Bx By Bz ]   [ q2x q2y q2z ]
                    
            #compute inverse of r1  matrix above. Call it R_1
            R_1=[
                [ r2.y, -r1.y],
                [-r2.x, r1.x ]
            ]
            tmp = (r1.x*r2.y-r2.x*r1.y)
            if tmp == 0.0:
                #bad texture coordinates; punt
                warn("Bad texture coordinate: Degenerate triangle")
                T=Vector4(1,0,0,0)
                B=Vector4(0,1,0,0)
            else:
                tmp = 1.0/tmp
                R_1[0][0] *= tmp
                R_1[0][1] *= tmp
                R_1[1][0] *= tmp
                R_1[1][1] *= tmp
                
                Q=[
                    [q1.x, q1.y, q1.z ],
                    [q2.x, q2.y, q2.z ] 
                ]

                TB = matrix_multiply(R_1,Q)
                
                T=Vector4(TB[0][0],TB[0][1],TB[0][2],0)
                B=Vector4(TB[1][0],TB[1][1],TB[1][2],0)
                    
            if length(T) == 0 or length(B) == 0 :
                warn("Zro length tangent or binormal")
                T=Vector4(1,0,0,0)
                B=Vector4(0,1,0,0)
                    
            T=normalize(T)
            B=normalize(B)
                
            for vvi in [vi0,vi1,vi2]:
                tangents[vvi] = tangents[vvi] + T
                binormals[vvi] = binormals[vvi] + B
                
    #fix lengths and also orthonormalize
    for i in range(1,len(tangents)):
        T=tangents[i]
        B=binormals[i]
        N=snormals[i]
        
        if length(N) == 0:
            warn("Zero length normals")
            N=Vector4(0,0,1,0)
                
        if length(T) == 0 or length(B) == 0:
            warn("Zero length tangents after averaging")
            T=Vector4(1,0,0,0)
            B=Vector4(0,1,0,0)
            if length( cross(T,N) ) == 0:
                T=Vector4(0,1,0,0)
                B=Vector4(0,0,1,0)

        T = normalize(T)
        B = normalize(B)
        N = normalize(N)
        T=T-dot(T,N)*N
        if length(T) == 0:
            warn("Zero length tangents")
            T=Vector4(1,0,0,0)
            
        T=normalize(T)
        B=cross(T,N)
        if length(B) == 0:
            warn("Tangent and binormal are parallel")
            T=Vector4(0,1,0,0)
            if length(cross(T,N)) == 0 :
                T=Vector4(0,0,1,0)
        B=cross(T,N)
            
        B=normalize(B)
        
        tangents[i]=T
        binormals[i]=B
        snormals[i]=N

