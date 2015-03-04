#!/usr/bin/env python3


#http://research.cs.wisc.edu/graphics/Courses/cs-838-1999/Jeff/BVH.html

import sys,struct,random,math,os.path,traceback,re

from mmath import *

def padstr(s):
    if len(s) > 127:
        print("String is too long:",s)
        assert 0
    while len(s) < 128:
        s += "\0"
    return struct.pack( "128s",s.encode() )
    

    
def has_textures(l):
    return l>=2
def has_lighting(l):
    return l >= 3
def has_bbox(l):
    return l>=4
def has_emap(l):
    return l>=5
def has_bumpmap(l):
    return l>=6
def has_glossmap(l):
    return l>=7
def has_anim(l):
    return l>=8
    
def write_ordinary_mesh_header(aofp,bofp,level,od):
        
        #level 1: header word, diffuse color, vertex count, vertices (x,y,z,1),
        #       index count, index size, indices.
        #       Note that the file is padded with zeros after indices so the file ends
        #       on a multiple of 4 bytes.
        #level 2: Textures: header, diffuse color, diffuse tex, vertex count, vertices 
        #           (x,y,z,1, s,t,0,0), index count, size, values
        #level 3: Lighting: header, diffuse, specular color, diffuse tex, vertex count, vertices 
        #           (x,y,z,1, s,t,0,0, nx,ny,nz,0)), index count, size, values
        #level 4: bounding box: hdr, diffcol, speccol, difftex, bbox (6 floats: minx/y/z, maxx/y/z),
        #       vcount, vdata as in level 3, index count, size, data
        #level 5: Emission/specular maps: header, diffcol, speccol, difftex, emitmap, specmap, bbox, 
        #       vcount, vdata as in level 4, index count, size, data
        #level 6: Bump maps: header word, diffcol, speccol, difftex, emap, smap, bmap, bbox, 
        #       vcount, vertices (x,y,z,1, s,t,0,0, nx,ny,nz,0, tx,ty,tz,0), face count, index
        #       count, size, data
        #level 7: Gloss maps: Gloss texture filename is included after bmap. Otherwise, no change.
        #level 8: Skeletal animation: Adds weight data: No change to header compared to level 7,
        #           but vertex data changes:
        #           x,y,z,1, s,t,0,0, nx,ny,nz,0, tx,ty,tz,0, weights0-3, boneindex0-3
        #       Then index data is stored in the same format as level 7.
        #       The file is padded to a 4 byte boundary.
        #       Then armature data is stored.
    
        oc = od.owner
        currmtl = oc.mtls[od.mainmtl]
        fverts = oc.fverts
        
        if aofp: aofp.write(  "ASCII %2d\n" % level)
        bofp.write(  ("BINARY%2d" % level).encode() )
        
        texf=currmtl.get("map_Kd","")
        etexf=currmtl.get("map_Ka","")
        stexf=currmtl.get("map_Ks","")
        btexf=currmtl.get("map_Bump","")
        gtexf=currmtl.get("map_Ns","")
        diffuse=currmtl.get("Kd")
        specular=currmtl.get("Ks")
        shininess=float(currmtl.get("Ns"))
        alpha=currmtl.get("d",1.0)
    

        diffuse=[float(q) for q in diffuse]
        specular=[float(q) for q in specular]
        if len(specular) >= 4:
            specular[3] = shininess
        else:
            specular.append(shininess)
            
        alpha=float(alpha)

        if aofp: aofp.write("diffuse "+" ".join([str(q) for q in diffuse])+"\n")
        bofp.write( struct.pack("<ffff" , diffuse[0],diffuse[1],diffuse[2],alpha))

        if has_lighting(level):
            if aofp: aofp.write("specular "+" ".join([str(q) for q in specular])+"\n")
            bofp.write(struct.pack("<ffff" , specular[0],specular[1],specular[2],specular[3]))
    
        if has_textures(level):
            if aofp: aofp.write("basetexture "+texf+"\n")
            bofp.write(padstr(texf))
    
        if has_emap(level):
            #emission map
            if aofp: aofp.write("emissiontexture "+etexf+"\n")
            bofp.write(padstr(etexf))
    
            #specular map
            if aofp: aofp.write("spectexture "+stexf+"\n")
            bofp.write(padstr(stexf))
    
        if has_bumpmap(level):
            if aofp: aofp.write("bumpmap:"+btexf+"\n")
            bofp.write(padstr(btexf))
        
        if has_glossmap(level):
            if aofp: aofp.write("glossmap:"+gtexf+"\n")
            bofp.write(padstr(gtexf))
            
        if has_bbox(level):
            #write bounding box
            bbox_min = Vector4(1E99,1E99,1E99,0)
            bbox_max = Vector4(-1E99,-1E99,-1E99,0)
            for v in od.outverts:
                vi=v[0]
                V=fverts[vi]
                if V.x < bbox_min.x:
                    bbox_min.x = V.x
                if V.x > bbox_max.x:
                    bbox_max.x = V.x
                if V.y < bbox_min.y:
                    bbox_min.y = V.y
                if V.y > bbox_max.y:
                    bbox_max.y = V.y
                if V.z < bbox_min.z:
                    bbox_min.z = V.z
                if V.z > bbox_max.z:
                    bbox_max.z = V.z
                
            if aofp: aofp.write("bbox %f %f %f %f %f %f\n" % (bbox_min.x,bbox_min.y,bbox_min.z,
                bbox_max.x,bbox_max.y,bbox_max.z))
            bofp.write( struct.pack("<6f",bbox_min.x,bbox_min.y,bbox_min.z,
                bbox_max.x,bbox_max.y,bbox_max.z))

#ordinary mesh = header, then vertex count (as 32 bit int),
#then vertex data, then face count as 32 bit int,
#then face indices
def write_ordinary_mesh(level,od,an,bn):
        warned={}
        
        if an: aofp=open(an,'w')
        else: aofp=None
        
        bofp=open(bn,'wb')
        
        write_ordinary_mesh_header(aofp,bofp,level,od)
        
        oc=od.owner
        fverts=oc.fverts
        fnorms=oc.fnorms
        ftexs=oc.ftexs
        tangents=oc.tangents
        binormals=oc.binormals
        snormals=oc.snormals
        weights=oc.weights
        bones = oc.bonelist
        #write the number of vertices
        if len(od.outverts) > 0xffff:
            warn("Too many vertices")

        #print("   ",len(od.outverts),"vertices",end=" ")
        if aofp: aofp.write(str(len(od.outverts))+"\n")
        bofp.write( struct.pack( "<i",len(od.outverts) ) )
        
        for v in od.outverts:
            vi=v[0]
            ti=v[1]
            ni=v[2]
            gname=v[3]     #group name
        
            V=fverts[vi]
            
            WW=weights[vi]
            
            if ti == 0:
                T=Vector4(0,0,0,1)
            else:
                T=ftexs[ti]
            if ni == 0:
                N=Vector4(0,0,1,0)
            else:
                N=fnorms[ni]

            if has_bumpmap(level):
                #make sure we use the normal which is
                #orthogonal to tangent and binormal
                pass
                #N=snormals[vi]
                
            TT=tangents[vi]
            B=binormals[vi]
            
            if aofp: aofp.write("pos= % .5f % .5f % .5f % .1f" % (V.x,V.y,V.z,V.w))
            bofp.write( struct.pack("<4f",V.x,V.y,V.z,V.w))
        
            if has_textures(level):
                if aofp: aofp.write(" tex= % .5f % .5f % .5f % .1f" % (T.x,T.y,T.z,T.w))
                bofp.write(struct.pack("<4f",T.x,T.y,T.z,T.w))
        
            if has_lighting(level):
                if aofp: aofp.write(" norm= % .5f % .5f % .5f % .1f" % (N.x,N.y,N.z,N.w))
                bofp.write(struct.pack("<4f",N.x,N.y,N.z,N.w))
            
            if has_bumpmap(level):
                if aofp: aofp.write(" tan= % .5f % .5f % .5f % .1f" % (TT.x,TT.y,TT.z,TT.w))
                bofp.write(struct.pack("<4f",TT.x,TT.y,TT.z,TT.w))
                #if aofp: aofp.write(" bin= % .5f % .5f % .5f % .1f" % (B.x,B.y,B.z,B.w))
                #bofp.write(struct.pack("<4f",B.x,B.y,B.z,B.w))
            
            if has_anim(level):
                assert len(WW) == 4
                if aofp: aofp.write(" weights="+str(WW) )
                for wt,bonename in WW:
                    bofp.write(struct.pack("<f",wt))
                for wt,bonename in WW:
                    if bonename == None:
                        b=0
                    else:
                        b = oc.bonemap[bonename]
                    bofp.write(struct.pack("<f",b))

            if aofp: aofp.write("\n")
        #end for in od.outverts
        
        if aofp: aofp.write(str(len(od.outtris*3))+"\n")
        bofp.write( struct.pack("<i",len(od.outtris*3)))

        if len(od.outverts) < 256:
            isize=1
            ifmt="<3B"
        elif len(od.outverts) < 65536:
            isize=2
            ifmt="<3H"
        else:
            isize=4
            ifmt="<4I"

        if aofp: aofp.write("index size "+str(isize)+"\n")
        bofp.write(struct.pack("<i",isize))
                   
        #triangles, as indices
        for q in od.outtris:
            if aofp: aofp.write("%d %d %d\n" % (q[0],q[1],q[2]))
            bofp.write( struct.pack( ifmt,q[0],q[1],q[2]) )
            #for zz in range(3):
            #    i1 = q[zz]
            #    i2 = q[(zz+1)%3]
            
        while bofp.tell() % 4:
            bofp.write(b'0')
        
        def d2r(deg):
            return deg/180.0 * 3.14159265358979323  
        
        def roundup(x):
            if x == 0:
                return 1
            #trick from tdl: x&(x-1)==0 -> power of 2
            if x & (x-1) == 0:
                return x 
            y = x << 1     #now it's greater than the value we want
            mask=1
            while y & (y-1) != 0:
                y &= ~mask
                mask <<= 1
            return y
                
            
            
        #write the bone hierarchy.
        #Note that data is padded out to a multiple of two
        #numbones as an integer
        #padbones: numbones rounded up to nearest power of 2
        #Then padbones data items:
        #	starting x,y,z + parent index (or -1 if none)
        #numframes as an integer
        #padframes: numframes rounded up to nearest power of 2
        #Then padframes items of data, one for each frame:
        #   padbones items of data, one for each bone:
        #       Quaternion x,y,z,a   
        #xxxx-Rotation x/y/z, then a 0
        #Then again, for padframe items:
        #   overall translation x/y/z, then a zero
        if has_anim(level):
            pnumbones=roundup(len(bones))
            if aofp: print("numbones",len(bones),file=aofp)
            bofp.write(struct.pack("<i",len(bones)))
            if aofp: print("pnumbones",pnumbones,file=aofp)
            bofp.write(struct.pack("<i",pnumbones))
            
            for i in range(pnumbones):
                if i >= len(bones):
                    pi=-1
                    name="<pad>"
                    head=Vector4(0,0,0,0)
                elif bones[i].parent == None:
                    pi=-1
                    name=bones[i].name
                    head=bones[i].head
                else:
                    pi=bones[i].parent.idx
                    name=bones[i].name
                    head=bones[i].head 
                if aofp: print("bone",i,"(",name,"): head=",head,"parent=",pi,file=aofp)
                bofp.write( struct.pack("<4f",head.x,head.y,head.z,pi))
				
            numframes = len(bones[0].framedata)
            pnumframes = roundup(numframes)
            if aofp: aofp.write( "numframes %d\n" % numframes)
            bofp.write(struct.pack("<i",numframes))
            if aofp: print("pnumframes",pnumframes,file=aofp)
            bofp.write(struct.pack("<i",pnumframes))

            for frame in range(pnumframes):
                if aofp: print("---Frame",frame,"rotations---",file=aofp)
                for bi in range(pnumbones):
                    if bi >= len(bones) or frame >= numframes:
                        #this is a pad area
                        name="<pad>"
                        tmp=[1,0,0,0]   #identity quaternion
                    else:
                        bone=bones[bi]
                        qframedata = bone.qframedata
                        name=bone.name
                        tmp=[qframedata[frame].x,qframedata[frame].y,
                            qframedata[frame].z, qframedata[frame].a]
                        
                        #fd=bone.framedata[frame]
                        ##root's first 3 will be overall x,y,z translation.
                        #Then everyone has rotation x,y,z
                        #if len(fd) == 3:
                        #   #non-root: Rotation xyz as radians
                        #    tmp=[d2r(fd[0]),d2r(fd[1]),d2r(fd[2]),0.0]
                        #elif len(fd) == 6:
                        #    #Root: position xyz, then rotation xyz
                        #    assert bone.parent == None
                        #    tmp=[d2r(fd[3]),d2r(fd[4]),d2r(fd[5]),0.0 ]
                        #else:
                        #    assert 0
                    if aofp: aofp.write("bone "+str(bi)+" ("+name+"): "+str(tmp)+"\n")
                    bofp.write(struct.pack("<4f",tmp[0],tmp[1],tmp[2],tmp[3]))

            bone=bones[0]
            for frame in range(pnumframes):
                if aofp: print("---Frame",frame,"translations---",file=aofp)
                if frame >= numframes:
                    tmp=[0,0,0]
                else:
                    fd=bone.framedata[frame]
                    tmp=fd[0:3]
                    assert len(fd) == 6
                if aofp: print(tmp,file=aofp)
                bofp.write(struct.pack("<4f",tmp[0],tmp[1],tmp[2],0))
        
        print("Wrote",bn,":",len(od.outverts),"vertices,",
            len(od.outtris*3),"indices (",len(od.outtris),"triangles)" )                               
                        

#header, vertex count, vertex data (every three vertices
#make up a triangle), index count, index size,
#index data. (indices will always be 0,1,2,3,4,5,6,7,8,9,...)
#Vertex data is different from ordinary mesh:
#it holds x,y,z,1, s,t,0,0, nx,ny,nz,0, pu,pv,u,v
#where the u,v values are useful for shell-based fur
# (pu,pv = scaled texture coordinates of vertex 0 of the triangle;
#  u,v = scaled texture coordinates of this vertex)
def write_unindexed_mesh(level,od,atri,btri):
        
        warned={}
        oc = od.owner
        fverts=oc.fverts
        ftexs=oc.ftexs
        fnorms=oc.fnorms
        
        if atri:atofp=open(atri,"w")
        else: atofp=None
        btofp=open(btri,"wb")
        
        write_ordinary_mesh_header(atofp,btofp,level,od)
        
        if atofp: print(len(od.outtris)*3,file=atofp)
        btofp.write(struct.pack("<i",len(od.outtris)*3))
        #triangle data, with info for fur
        for kk in range(len(od.outtris)):
            T=od.outtris[kk]        #three indices in outverts
            
            vtx1 = od.outverts[T[0]]    #vi,ti,ni triple: indices in fverts, ftexs, fnorms
            vtx2 = od.outverts[T[1]]
            vtx3 = od.outverts[T[2]]
            
            #get xyz coordinates of vertices
            p=fverts[vtx1[0]]
            q=fverts[vtx2[0]]
            r=fverts[vtx3[0]]
            
            #and texture/normals
            ptex=ftexs[vtx1[1]]
            qtex=ftexs[vtx2[1]]
            rtex=ftexs[vtx3[1]]
            pnorm=fnorms[vtx1[2]]
            qnorm=fnorms[vtx2[2]]
            rnorm=fnorms[vtx3[2]]
            
            if ptex==None:
                ptex=Vector4(0,0,0,0)
            if qtex==None:
                qtex=Vector4(0,1,0,0)
            if rtex == None:
                rtex=Vector4(1,0,0,0)
                
            #make a new per-triangle basis
            u=q-p
            v_=r-p
            w=cross(u,v_)
            v=cross(w,u)
            try:
                u=normalize(u)
                v=normalize(v)
            except ZeroDivisionError:
                u=Vector4(1,0,0,0)
                v=Vector4(0,1,0,0)
            
            #project q into new basis
            qu=dot(q-p,u)
            qv=dot(q-p,v)
            
            #project r into new basis
            ru=dot(r-p,u)
            rv=dot(r-p,v)
            
            #put p at random spot in new basis
            pu=random.random()
            pv=random.random()
            #qu = pu + scale*qu
            #qv = pv + scale*qv
            
            #pos, tex, norm, stex
            V=[ (p,ptex,pnorm,(pu,pv,0,0)), 
                (q,qtex,qnorm,(pu,pv,qu,qv)), 
                (r,rtex,rnorm,(pu,pv,ru,rv)) ]
            for vtx in V:
                if atofp: print("v=",vtx[0],"t=",vtx[1],"n=",vtx[2],"stex=",vtx[3],file=atofp)
                btofp.write(
                    struct.pack( "<16f",
                        vtx[0][0],vtx[0][1],vtx[0][2],1.0,  #pos
                        vtx[1][0],vtx[1][1],0.0,0.0,        #tex
                        vtx[2][0],vtx[2][1],vtx[2][2],0.0,  #norm
                        vtx[3][0],vtx[3][1],vtx[3][2],vtx[3][3] )       #scaled tex
                    )
        
        ni = 3*len(od.outtris)
        if ni <256:
            ifmt="<3B"
            isize=1
        elif ni < 65536:
            ifmt="<3H"
            isize=2
        else:
            ifmt="<3I"
            isize=4

        btofp.write(struct.pack("<i",3*len(od.outtris)))
        btofp.write(struct.pack("<i",isize))
                    
        for kk in range(0,3*len(od.outtris),3):
            btofp.write(struct.pack(ifmt,kk,kk+1,kk+2))


#data for line fur 
#header, vertex count, vertices, index count=0, no indices written                
def write_linefur_mesh(level,od,afname,bfname,furdensity,furdivs):
    if furdensity == 0 and furdivs == 0:
        return
    
    if afname: afp=open(afname,"w")
    else: afp=None
    
    bfp=open(bfname,"wb")
    write_ordinary_mesh_header(afp,bfp,level,od)
    
    oc=od.owner
    fverts=oc.fverts
    fnorms=oc.fnorms
    ftexs=oc.ftexs
    
    
    #create line data
    V=[]
    for kk in range(len(od.outtris)):
        T=od.outtris[kk]    #three indices in outverts
        
        vtx1=od.outverts[T[0]]  #vi,ti,ni
        vtx2=od.outverts[T[1]]
        vtx3=od.outverts[T[2]]
        
        p=fverts[vtx1[0]]
        q=fverts[vtx2[0]]
        r=fverts[vtx3[0]]
        
        ptex=ftexs[vtx1[1]]
        qtex=ftexs[vtx2[1]]
        rtex=ftexs[vtx3[1]]
        
        pnorm=fnorms[vtx1[2]]
        qnorm=fnorms[vtx2[2]]
        rnorm=fnorms[vtx3[2]]
        
        u=q-p
        v=r-p
        w=cross(u,v)
        wlen=length(w)
        #number of shafts in this triangle is proportional
        #to triangle area (wlen/2) and furdensity.
        #Add 0.5 to round up when taking int().
        numshafts = int(0.5+ furdensity * wlen/2.0)
        for k in range(numshafts):
            w0=random.random()
            w1=random.random()
            w2=random.random()
            sm=w0+w1+w2
            w0/=sm
            w1/=sm
            w2/=sm
            start=w0*p+w1*q+w2*r
            n=w0*pnorm+w1*qnorm+w2*rnorm
            t=w0*ptex+w1*qtex+w2*rtex
            for mm in range(furdivs):
                ffa=(mm  )*1.0/(furdivs)
                ffb=(mm+1)*1.0/(furdivs)
                V.append( (Vector4(start.x,start.y,start.z,ffa),t,n) )
                V.append( (Vector4(start.x,start.y,start.z,ffb),t,n) )
    
    print(len(V),"vertices in fur line mesh")        
    if afp: print("numv=",len(V),file=afp)
    bfp.write(struct.pack("<i",len(V)))
    for v in V:
        if afp:  print(v,file=afp)
        bfp.write(struct.pack("<16f",
            v[0].x,v[0].y,v[0].z,v[0].w,
            v[1].x,v[1].y,v[1].z,v[1].w,
            v[2].x,v[2].y,v[2].z,v[2].w,
            0,0,0,1))
    if afp: print("numtris=0 (not written)",file=afp)
    bfp.write(struct.pack("<i",0))
    
    
                    

def write_edge_mesh(od,aen,ben):
        warned={}
        
        if aen:
            aeofp =open(aen,"w")
        else:
            aeofp=None
            
        beofp=open(ben,"wb")
        
        if aeofp: print("EDGE0006",file=aeofp)
        beofp.write("EDGE0006".encode())
        
        en = od.edge_normals
        ilist=[]    #index list
        vcount=0
        if aeofp: aeofp.write("nv="+str(len(en)*4)+"\n")
        beofp.write(struct.pack("<i",len(en)*4))
        
        debug1=0
        debug2=0
        for k in en:
            v1 = en[k][0]
            v2 = en[k][1]
            n1 = en[k][2]
            if len(en[k]) == 3:
                #only one incident triangle;
                #force it to be considered a silhouette
                n2 = -1.0*n1
                debug1+=1
            elif len(en[k]) >= 4:
                #locally manifold
                n2 = en[k][3]
                debug2+=1
            
            if len(en[k]) > 4 and "nonmanifold" not in warned:
                warned["nonmanifold"]=True
                print("Warning: Nonmanifold edges")
                
            
            #write the "vertex" four times, but with
            #different w values on the n1,n2 values
            #so the vertex shader knows which one it's processing
            #Note: Edge n1 belongs to the face which had vertices v1v2
            #in the order v1v2 (and so the face with normal n2
            #had the vertices in the order v2v1, assuming constant CCW winding order)
            for iii in range(2):
                for jjj in range(2):
                    if aeofp: aeofp.write("%f %f %f %f   %f %f %f %f   %f %f %f %f   %f %f %f %f" %
                        (v1.x,v1.y,v1.z,1.0,
                        v2.x,v2.y,v2.z,1.0,
                        n1.x,n1.y,n1.z,iii,
                        n2.x,n2.y,n2.z,jjj))
                    if len(en[k]) == 3:
                        if aeofp: aeofp.write(" *")
                    if aeofp: aeofp.write("\n")
                        
                    tmp=struct.pack("<16f",
                            v1.x,v1.y,v1.z,1.0,
                            v2.x,v2.y,v2.z,1.0,
                            n1.x,n1.y,n1.z,iii,
                            n2.x,n2.y,n2.z,jjj)
                    beofp.write(tmp)

            #connect in two triangles to make a quad
            #Use n2.w to determine whether we are at the v1 end
            #or the v2 end of the edge; use n1.w to determine
            #which direction to go from the end we are at
            ilist += [vcount,vcount+2,vcount+1]
            ilist += [vcount+1,vcount+2,vcount+3]
            vcount += 4


        if vcount < 256:
            ifmt="<1B"
            isize=1
        elif vcount < 65536:
            ifmt="<1H"
            isize=2
        else:
            ifmt="<1I"
            isize=4
        
        if aeofp: aeofp.write("icount,size="+str(len(ilist))+" "+str(isize)+"\n")
        beofp.write( struct.pack("<i",len(ilist)))
        beofp.write( struct.pack("<i",isize))
        
        for idx in range(len(ilist)):
            if idx != 0 and idx%3 == 0:
                if aeofp: aeofp.write("\n")
            if aeofp: aeofp.write(str(ilist[idx])+" ")
            beofp.write(struct.pack(ifmt,ilist[idx]))
                    
