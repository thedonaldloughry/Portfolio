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
        TextureX* tex;
        vec4 dc;
        vec4 sc;
        GLenum ise;
        uint32_t ic;
        unsigned vbuff, ibuff;

        Mesh(string fname);
        void Load(Program& p);
        void Draw(Program& p);
};

