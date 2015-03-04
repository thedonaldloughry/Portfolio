#!/usr/bin/env python3

#to fix:
#change askint to askfloat
#change struct.pack 'h' to 'H'

#export from blender:
#   selection only: usually no
#   animation: no
#   Apply modifiers: yes
#   Include edges: yes
#   Include normals: yes
#   Include UVs: yes
#   Write materials: yes
#   Triangulate faces: yes
#   Write nurbs: no
#   Polygroups: yes
#   Objects as OBJ objects: yes
#   Forward: y forward
#   Up: Z up
#   Path mode: relative


#http://research.cs.wisc.edu/graphics/Courses/cs-838-1999/Jeff/BVH.html

#to export vertex bone data: Change obj export file:
"""         # Vert
            jhvk=ob.vertex_groups.keys()
            for v in me_verts:
                jh=[]
                if EXPORT_POLYGROUPS:
                    for vvv in v.groups:
                        jh.append( str(vvv.weight)+" "+str(jhvk[vvv.group])) 
                jh=" ".join(jh)
                fw('v %.6f %.6f %.6f %s\n' % (v.co[0],v.co[1],v.co[2],jh))
"""

import sys,struct,random,math,os.path,traceback,re
from mmath import *
from mainfunc import *

meshes=None
scale=None
level=None
furdensity=None
furdivs=None

do_ordinary=True
do_unindexed=True
do_linefur=True
do_edge=True
do_ascii=True

if len(sys.argv) > 1 and sys.argv[1]=='--help':
    print(sys.argv[0],"level","scale","furdensity,furdivs","meshes")
    sys.exit(0)
    
if len(sys.argv) > 1:
    level=int(sys.argv[1])
if len(sys.argv) > 2:
    scale=float(sys.argv[2])
if len(sys.argv) > 3:
    lst=sys.argv[3].split(",")
    furdensity=int(lst[0])
    furdivs=int(lst[1])
if len(sys.argv) > 4:
    meshes = sys.argv[4:]
levels=[None,"Basic","Textures","Lighting","Bounding Box",
    "Emission Maps","Bump Map","Gloss Map","Armature"]

have_tk=False
try:
    from tkinter import *
    from tkinter.filedialog import *
    from tkinter.simpledialog import *
    from tkinter.messagebox import *
    have_tk=True
    root=Tk()
    root.withdraw()
except Exception:
    pass


class OptionDialog:
    def __init__(self):
        self.cancelled=True
        
        win=Tk()
        self.win=win
        
        fr=Frame(win)
        fr.pack(side=TOP,expand=NO,fill=X)
        ys=Scrollbar(fr,orient=VERTICAL)
        xs=Scrollbar(fr,orient=HORIZONTAL)
        ys.grid(row=0,column=1,sticky=NS)
        xs.grid(row=1,column=0,sticky=EW)
        lbox=Listbox(fr,xscrollcommand=xs.set,yscrollcommand=ys.set)
        lbox.grid(row=0,column=0,sticky=NSEW)
        xs["command"]=lbox.xview
        ys["command"]=lbox.yview
        for x in levels:
            lbox.insert(END,x)
        lbox.bind('<Double-ButtonRelease-1>',lambda x: self.go() )
        self.lbox=lbox   

        fr=Frame(win)
        fr.pack(side=TOP,expand=YES,fill=X)
        tmp=Label(fr)
        tmp["text"]="Scale"
        tmp.pack(side=LEFT)

        self.scale=Entry(fr)
        self.scale.pack(side=LEFT)
        self.scale.insert(0,"1.0")

        fr=Frame(win)
        fr.pack(side=TOP,expand=YES,fill=X)
        Label(fr,text="Fur divs").pack(side=LEFT)
        self.furdivs = Entry(fr)
        self.furdivs.pack(side=LEFT)
        self.furdivs.insert(0,"0")

        fr=Frame(win)
        fr.pack(side=TOP,expand=YES,fill=X)
        Label(fr,text="Fur density").pack(side=LEFT)
        self.furdensity=Entry(fr)
        self.furdensity.pack(side=LEFT)
        self.furdensity.insert(0,"0")

        def cbox(var,txt):
            fr=Frame(win)
            fr.pack(side=TOP,expand=YES,fill=X)
            cb = Checkbutton(fr,
                    text="Write "+txt,
                    command=lambda: self.toggle(var))           
            cb.pack(side=LEFT)
            if var[0]:
                cb.select()
            else:
                cb.deselect()

        self.ordinary=[True]
        cbox(self.ordinary,"ordinary mesh")
        self.edge=[False]
        cbox(self.edge,"edge mesh")
        self.unindexed=[False]
        cbox(self.unindexed,"unindexed mesh")
        self.linefur=[False]
        cbox(self.linefur,"line fur mesh")

        self.ascii=[False]
        cbox(self.ascii,"ASCII files")
        
        fr=Frame(win)
        fr.pack(side=TOP,expand=YES,fill=X)
        cancel=Button(fr)
        cancel["text"]="Cancel"
        cancel["command"]=self.cancel
        cancel.pack(side=LEFT)
        ok=Button(fr)
        ok["text"]="OK"
        ok["command"]=self.go
        ok.pack(side=RIGHT)
        win.wait_window()

    def toggle(self,x):
        x[0] = not x[0]
        
    def go(self):
        global scale
        global furdensity
        global furdivs
        global level
        global do_ordinary,do_linefur,do_unindexed,do_edge,do_ascii

        try:
            scale = float(self.scale.get())
            furdensity = int(self.furdensity.get())
            furdivs = int(self.furdivs.get())
            idx=self.lbox.curselection()
            idx = int(idx[0])
            do_ordinary = self.ordinary[0]
            do_linefur = self.linefur[0]
            do_unindexed = self.unindexed[0]
            do_edge = self.edge[0]
            do_ascii=self.ascii[0]
        except ValueError:
            showerror("Error","Cannot parse value")
            return
        except IndexError:
            showerror("Error","Choose a level")
            return
        
        level=idx+1
        self.win.destroy()
        print("scale=",scale,"fur=",furdensity,furdivs,"level=",level,
              "do_ordinary",do_ordinary,do_linefur,do_unindexed,do_edge)
        self.cancelled=False
    def cancel(self):
        self.win.destroy()
        sys.exit(0)


#OptionDialog()
#sys.exit(0)

try:
    if meshes == None:
        if have_tk:
            tmplist=askopenfilename(filetypes=[("OBJ files","*.obj"),("Any","*")],multiple=True)
            print(tmplist)
            if not tmplist:
                sys.exit(0)
            
            if type(tmplist) == str:
                tmplist=tmplist.replace("{","")
                tmplist=tmplist.replace("}","")
                meshes = [tmplist] 
            else:
                meshes=[]
                for q in tmplist:
                    meshes.append(q.replace("{","").replace("}",""))
                
            for q in meshes:
                print(q)
            
            if not meshes[0]:
                sys.exit(0)
        else:
            meshes=[input("Mesh file? ")]


    if scale == None or furdensity == None or level == None:
        if have_tk:
            o=OptionDialog()
            if o.cancelled:
                sys.exit(0)
        else:
            scale = askfloat("Scale","Scale factor?")
            furdensity=float(input("Fur density? "))
            furdivs=float(input("Fur divisions? "))    
            for i in range(1,len(levels)):
                print(i,":",levels[i])
            level=int(input("Level? "))

    for meshfile in meshes:
        main(meshfile,scale,None,level,furdensity,furdivs,
             do_ascii,
            do_ordinary,do_linefur,do_edge,do_unindexed)
            
    if have_tk:
        showinfo("Note","Conversion completed successfully")
        
except Exception as e:
    if have_tk:
        t,v,tb= sys.exc_info()
        v=str(v)
        showerror("Error",
            "Something went wrong.\n"+
            v)
        print(traceback.format_exc())
    else:
        print(traceback.format_exc())
        input("What do? ")
        
