#include "llgl.h"
#include <iostream>
#include "Mesh.h"



class Text
{
public:
    struct Metrics
    {
        int x,y,w,h;
    };

    ///Variable declarations below///
    string fontFile, metricsFile;
    string txt;
    map<string,Texture2D*> texs;
    map<string,vector<Metrics> > metrics;
    int cvsw;
    int cvsh;
    Program * tProg;
    int x,y,numverts;
    unsigned vbuff;
    unsigned eb;
    vector<float> vdata;
    bool isSetup = false;
    bool needsInit = true;

    ///Method declarations below///
    Text(string ff, string mf);
    void setText(string S,int x,int y);
    void draw();
    void setup();
    void setCanvasSize(int w, int h);
    void initBuffer();
    vec4 getTexcoords(char c);
    vec2 pixelToViewport(int x,int y);


};
