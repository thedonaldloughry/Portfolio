#pragma once

#include "llgl.h"
#include "assert.h"
#include <vector>
#include <stdexcept>
#include <iostream>

using namespace std;
using namespace llgl;



class Mesh
{
    public:
        bool initialized;
        bool areLinesThere;
        string fname;
        string lineFileName;
        TextureX* tex;
        TextureX* cellTex; //COMMENT THIS LINE OUT IF NOT CELL SHADING//
        vec4 dc;
        vec4 sc;
        GLenum ise;
        uint32_t ic, vc;
        unsigned vbuff, ibuff, linebuff;
        vector<float> vdata;

        Mesh(string fname);
        void Load(Program& p);
        void Draw(Program& p);
        void LoadOutlines();
        void DrawLines(Program& p);
};
