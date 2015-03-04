#include "Mesh.h"
#include "assert.h"
#include "llgl.h"
#include <vector>
#include <stdexcept>
#include <iostream>
#include <fstream>

using namespace std;
using namespace llgl;

Mesh::Mesh(string fname) // worth noting that this line said 'Mesh::Mesh(string fname = "sphere_Sphere.binary.mesh")' originally
{
    initialized = false;
    this->fname = fname;
}

void Mesh::Load()
{
    if(initialized) return;

    string pfx;
    string::size_type si = fname.rfind("/");
    if(si != string::npos)
        pfx = fname.substr(0, si + 1);

    ifstream in(fname.c_str(), ios::binary);
    if(!in.good())
        cerr << "Bad file: "<< fname <<  endl;

    char c[9];
    in.read(c, 8);
    c[8] = 0;
    if(strcmp(c, "BINARY 3") != 0)
    {
        cout << "Bad file: "<< fname <<  endl;
        assert(0);
    }

    in.read((char*) &dc, sizeof(dc));

    in.read((char*) &sc, sizeof(sc));

    char tf[128];
    in.read(tf, 128);

    if(tf[0] != 0)
        tex = new Texture2D(pfx + tf);
    else
        tex = new SolidTexture(dc.x, dc.y, dc.z, dc.w);
    //cellTex = new Texture2D("cellShade1.png");  //COMMENT THIS LINE OUT IF NOT CELL SHADING//


    in.read((char*) &vc, 4);
    vdata.resize(vc * 12);
    in.read((char*) &vdata[0], vc*12*4);

    uint32_t isize;
    in.read((char*) &ic, 4);
    in.read((char*) &isize, 4);

    if(isize == 1)
        ise = GL_UNSIGNED_BYTE;
    else if(isize == 2)
        ise = GL_UNSIGNED_SHORT;
    else
        ise = GL_UNSIGNED_INT;
    //vector<char> idata(ic * isize);
    idata.resize(ic*isize);
    in.read(&idata[0], ic * isize);

    initialized = true;
}

void Mesh::Draw() // YES, I KNOW THAT THIS IS TECHNICALLY WRONG. I'LL FIX THIS ON MY OWN TIME.
{
    if(!initialized)
        Mesh::Load(); // FOR OUR PURPOSES, DRAW IS JUST GOING TO LOAD UP THE MESH IF IT HAS NOT ALREADY BEEN LOADED.
    /*glBindBuffer(GL_ARRAY_BUFFER, vbuff);
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER,ibuff);
    p.setUniform("tex", tex);
    //p.setUniform("iramp", cellTex);  //COMMENT THIS LINE OUT IF NOT CELL SHADING//
    p.setUniform("diffuse", dc);
    p.setUniform("specular", sc);
    p.setVertexFormat("a_pos", 4, GL_FLOAT,
                              "a_texc", 4, GL_FLOAT,
                              "a_normal", 4, GL_FLOAT);*/
    //glDrawElements(GL_TRIANGLES, ic, ise, 0);
}

/*void Mesh::DrawLines(Program& p)
{
    if(!initialized)
        Mesh::Load();
    p.setUniform("tex", tex);
    p.setUniform("iramp", cellTex);  //COMMENT THIS LINE OUT IF NOT CELL SHADING//

}*/
