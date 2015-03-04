#!/usr/bin/env python3

#matrix/vector math

import sys,struct,random,math,os.path,traceback,re

# a 4d vector: xyzw
class Vector4(object):
    def __init__(self,x,y,z,w):
        self.x=x
        self.y=y
        self.z=z
        self.w=w
    def __add__(self,o):
        return Vector4(self.x+o.x,self.y+o.y,self.z+o.z,self.w+o.w)
    def __rmul__(self,o):
        return Vector4(o*self.x,o*self.y,o*self.z,o*self.w)
    def __sub__(self,o):
        return Vector4(self.x-o.x,self.y-o.y,self.z-o.z,self.w-o.w)
    def __repr__(self):
        return "[ %f , %f , %f , %f ]" % (self.x,self.y,self.z,self.w) 
    def __getitem__(self,idx):
        if idx ==0:
            return self.x
        elif idx == 1:
            return self.y
        elif idx == 2:
            return self.z
        elif idx == 3:
            return self.w
        else:
            assert 0
def length(v):
    return dot(v,v)**0.5

def dot(v,w):
    assert v.w == 0.0 and w.w == 0.0
    return v.x*w.x+v.y*w.y+v.z*w.z+v.w*w.w

def cross(v,w):
    assert v.w == 0.0 and w.w == 0.0
    return Vector4( v.y*w.z-v.z*w.y, w.x*v.z-v.x*w.z, v.x*w.y-v.y*w.x, 0 )
    
def normalize(v):
    return  1.0/length(v) * v
 
class Quaternion(object):
    def __init__(self,v,a):
        self.a=a
        self.x=v.x
        self.y=v.y
        self.z=v.z
    def __mul__(self,o):
        if type(o) == Quaternion:
            v1=Vector4(self.x,self.y,self.z,0)
            v2=Vector4(o.x,o.y,o.z,0)
            a=self.a*o.a-dot(v1,v2)
            v3=self.a*v2 + o.a*v1 + cross(v1,v2)
            return Quaternion(v3,a)
        else:
            assert 0
    def conj(self):
        return Quaternion(-1.0*self.v,self.a)

def quat_for_rot(radians,axis):
    c=math.cos(radians/2.0)
    s=math.sin(radians/2.0)
    return Quaternion( s*axis , c )
    
#4x4 matrix
class Matrix4(object):
    def __init__(self,v=None):
        self.M=[ [1,0,0,0] , [0,1,0,0] , [0,0,1,0], [0,0,0,1] ]
        if v != None:
            c=0
            for i in range(4):
                for j in range(4):
                    self.M[i][j] = v[c]
                    c+=1
                    
    def __mul__(self,o):
        R=Matrix4( [0,0,0,0,  0,0,0,0,  0,0,0,0,  0,0,0,0 ] )
        if type(o) == Matrix4:
            for i in range(4):
                for j in range(4):
                    s=0
                    for k in range(4):
                        s += self.M[i][k] * o.M[k][j]
                    R[i][j]=s
            return R
        elif type(o) == Vector4:
            R=[0,0,0,0]
            v=[o.x,o.y,o.z,o.w]
            for i in range(4):
                for j in range(4):
                    R[i] += self.M[i][j] * v[j]
            return Vector4(R[0],R[1],R[2],R[3])
        else:
            assert 0
    
    def transpose(self):
        R=Matrix4()
        for i in range(4):
            for j in range(4):
                R[i][j]=self.M[j][i]
        return R
        
    def __rmul__(self,o):
        v=[o.x,o.y,o.z,o.w]
        R=[0,0,0,0]
        for i in range(4):
            for j in range(4):
                   R[i] += v[j]*self.M[j][i] 

#simulate matrix multiply on two lists of lists
def matrix_multiply(M,N):
    R=[]
    nrm = len(M)
    ncm = len(M[0])
    nrn = len(N)
    ncn = len(N[0])
    assert ncm == nrn
    
    for i in range(nrm):
        R.append([])
        for j in range(ncn):
            summ=0
            for k in range(ncm):
                summ += M[i][k] * N[k][j]
            R[-1].append(summ)

    assert len(R) == nrm
    assert len(R[0]) == ncn
    return R
    
