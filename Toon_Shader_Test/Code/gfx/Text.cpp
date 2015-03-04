#include "Text.h"
#include "llgl.h"
#include <iostream>
#include "Mesh.h"
#include <vector>
#include <stdexcept>
#include <fstream>

using namespace std;
using namespace llgl;

Text::Text(string ff, string mf)
{
    fontFile = ff;
    metricsFile = mf;
    vbuff = 0;
    eb = 0;

}
void Text::setText(string s,int x,int y)
/// S is the string to display,x and y is cords to place them///
{

    txt=s;
    this->x=x;
    this->y=y;
    needsInit=true;
    cout << "text setting.." << endl;
}

void Text::draw()
{
    if(txt.size() < 1)
        return;
    if(needsInit)
        initBuffer();

    glBindBuffer(GL_ARRAY_BUFFER,vbuff);

    unsigned short I[]= {0,2,1, 2,3,1};
    unsigned eb;
    glGenBuffers(1,&eb);
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER,eb);
    glBufferData(GL_ELEMENT_ARRAY_BUFFER,sizeof(I),I,GL_STATIC_DRAW);

    tProg->use();
    tProg->setVertexFormat("a_position", 4, GL_FLOAT);
    tProg->setUniform("tex",texs[fontFile]);
    tProg->setUniform("color",vec4(1,1,0,1));
    //cout <<"numverts: " << numverts << endl;
    glDrawElements( GL_TRIANGLES, numverts, GL_UNSIGNED_INT,0);
}

void Text::setup()
{
     if(isSetup)
        return;
    isSetup=true;
    if( texs.find(fontFile) == texs.end() )
        {
        Texture2D* tex = new Texture2D(fontFile);
        //next line loads texture so we
        //can get its width and height
        tex->bindToUnit(0);
        texs[fontFile] = tex;
        texs[fontFile]->setParameter(GL_TEXTURE_MIN_FILTER,GL_NEAREST);
        texs[fontFile]->setParameter(GL_TEXTURE_MAG_FILTER,GL_NEAREST);
        if( metrics.find(metricsFile) == metrics.end())
            {
                metrics[metricsFile].resize(256);
                ifstream in(metricsFile.c_str());
                while(1)
                {
                    string s;
                    getline(in,s);
                    if(!in)
                        break;
                    istringstream iss(s);
                    int ascii;
                    Metrics m;
                    iss >> ascii >> m.x >> m.y >> m.w >> m.h;
                    metrics[metricsFile][ascii]=m;
                }
            }
        }
        tProg = new Program("Code/gfx/vs.txt","Code/gfx/fs.txt");
}

void Text::setCanvasSize(int w, int h)
{
    cvsw = w;
    cvsh = h;
}

vec2 Text::pixelToViewport(int x, int y)
{
    return vec2(-1.0 + x * 2.0 / cvsw ,       //If p=(0,0) Returns -1,1 (upper left corner)
                1.0 - y * 2.0 / cvsh);        //If p=(w-1,h-1) Returns around 1,-1
                                                //As p.y goes up, returned y goes down
}

vec4 Text::getTexcoords(char c)
{
    Metrics m = metrics[metricsFile][c];
    vec4 t;
    t.x = m.x * 1.0/256;                //Returns lower left corner s,t in x,y slots
    t.y = 1.0 - (m.y + m.h) * 1.0/128; //Returns upper right corner s,t in z,w slots
    t.z = t.x + m.w * 1.0 / 256;
    t.w = t.y + m.h * 1.0 / 128;
    return t;
}

void Text::initBuffer()
{
    vector<float> vdata;
    if( !isSetup )
        setup();
    if( !needsInit)
        return;
    int x = this->x;
    int y = this->y;
    for(int c = 0;c < txt.size();c++)
    {

        if(txt[c] == '\n')
        {
            x = this->x;
            y += metrics[metricsFile]['A'].h;
        }
        else
        {
            //compute aa,bb,cc,dd
            float pw = metrics[metricsFile][txt[c]].w;
            float ph = metrics[metricsFile][txt[c]].h;
            vec2 a = this->pixelToViewport(x,y);
            vec2 d = pixelToViewport(x+pw,y-ph);
            vec4 t = getTexcoords(txt[c]);
            vec4 aa = vec4(a.x,a.y,t.x,t.y);
            vec4 bb = vec4(a.x,d.y,t.x,t.w);
            vec4 cc = vec4(d.x,a.y,t.z,t.y);
            vec4 dd = vec4(d.x,d.y,t.z,t.w);
            //add to vdata: aa,cc,bb
            vdata.push_back(aa.x);
            vdata.push_back(aa.y);
            vdata.push_back(aa.z);
            vdata.push_back(aa.w);
            vdata.push_back(cc.x);
            vdata.push_back(cc.y);
            vdata.push_back(cc.z);
            vdata.push_back(cc.w);
            vdata.push_back(bb.x);
            vdata.push_back(bb.y);
            vdata.push_back(bb.z);
            vdata.push_back(bb.w);
            //add to vdata: cc,dd,bb
            vdata.push_back(cc.x);
            vdata.push_back(cc.y);
            vdata.push_back(cc.z);
            vdata.push_back(cc.w);
            vdata.push_back(dd.x);
            vdata.push_back(dd.y);
            vdata.push_back(dd.z);
            vdata.push_back(dd.w);
            vdata.push_back(bb.x);
            vdata.push_back(bb.y);
            vdata.push_back(bb.z);
            vdata.push_back(bb.w);
            x += metrics[metricsFile][txt[c]].w;
        }
    }
    needsInit=false;
    if(vbuff==0)
        glGenBuffers(1,&vbuff);
    glBindBuffer(GL_ARRAY_BUFFER,vbuff);
    glBufferData(GL_ARRAY_BUFFER,vdata.size()*sizeof(vdata[0]),
                                    &vdata[0],GL_STATIC_DRAW);
    numverts = vdata.size();
}



