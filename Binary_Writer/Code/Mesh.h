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
        string fname;
        vector<float> vdata; // for mesh outline conversion //
        vector<char> idata;
        TextureX* tex;
        //TextureX* cellTex; //COMMENT THIS LINE OUT IF NOT CELL SHADING//
        vec4 dc;
        vec4 sc;
        GLenum ise;
        uint32_t ic;
        uint32_t vc;
        unsigned vbuff, ibuff, shitbuff;

        Mesh(string fname);
        void Load();
        void Draw();
        //void DrawLines(Program& p);
};
