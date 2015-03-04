#include "Mesh.h"
#include "assert.h"
#include "llgl.h"
#include <vector>
#include <stdexcept>
#include <iostream>
#include <fstream>

using namespace std;
using namespace llgl;

Mesh::Mesh(string fname = "sphere_Sphere.binary.mesh")
{
    initialized = false;
    areLinesThere = false;
    this->fname = fname;
}

void Mesh::Load(Program& p)
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

    //vec4 dc;
    in.read((char*) &dc, sizeof(dc));
    //p.setUniform("diffuse", dc);

    //vec4 sc;
    in.read((char*) &sc, sizeof(sc));
    //p.setUniform("specular", sc);

    char tf[128];
    in.read(tf, 128);

    if(tf[0] != 0)
        tex = new Texture2D(pfx + tf);
    else
        tex = new SolidTexture(dc.x, dc.y, dc.z, dc.w);
    cellTex = new Texture2D("Code/gfx/cellShade1.png");  //COMMENT THIS LINE OUT IF NOT CELL SHADING//
    cellTex->setParameter(GL_TEXTURE_MIN_FILTER, GL_NEAREST);
    cellTex->setParameter(GL_TEXTURE_MAG_FILTER, GL_NEAREST);

    uint32_t vc;
    in.read((char*) &vc, 4);
    vector<float> vdata;
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
    vector<char> idata(ic * isize);
    in.read(&idata[0], ic * isize);

    glGenBuffers(1, &vbuff);
    glBindBuffer(GL_ARRAY_BUFFER, vbuff);
    glBufferData(GL_ARRAY_BUFFER, vdata.size() * sizeof(vdata[0]), &vdata[0],GL_STATIC_DRAW);

    glGenBuffers(1, &ibuff);
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ibuff);
    glBufferData(GL_ELEMENT_ARRAY_BUFFER,idata.size() * sizeof(idata[0]), &idata[0],GL_STATIC_DRAW);
    initialized = true;
}

void Mesh::Draw(Program& p)
{
    if(!initialized)
        Mesh::Load(p);
    glBindBuffer(GL_ARRAY_BUFFER, vbuff);
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER,ibuff);
    p.use();
    p.setUniform("tex", tex);
    p.setUniform("iramp", cellTex);  //COMMENT THIS LINE OUT IF NOT CELL SHADING//
    p.setUniform("diffuse", dc);
    p.setUniform("specular", sc);
    p.setVertexFormat("a_pos", 4, GL_FLOAT,
                              "a_texc", 4, GL_FLOAT,
                              "a_normal", 4, GL_FLOAT);
    glDrawElements(GL_TRIANGLES, ic, ise, 0);
}

void Mesh::LoadOutlines()
{
    /*
        Requires global variable[s]: linebuff
    */
    //"TesterModels/TestBox/TestBox.txt" is an example file name
    ifstream in(lineFileName.c_str(), ios::binary);
    if(!in.good())
        cerr << "Bad file: " << lineFileName << endl;

    // READ IN VERTEX DATA FROM OUR BINARY FILE //
    in.seekg(0, ios::end);
    unsigned fileSize = in.tellg();
    in.seekg(ios::beg);
    cout << "File size is: " << fileSize << endl;
    vector<float> vertData(fileSize / sizeof(float));
    in.seekg(0, ios::beg);
    in.read((char*) &vertData[0], fileSize);
    // END READ //

    // GENERATE BUFFERS //
    glGenBuffers(1, &linebuff);
    glBindBuffer(GL_ARRAY_BUFFER, linebuff);
    glBufferData(GL_ARRAY_BUFFER, vertData.size() * sizeof(vertData[0]), &vertData[0],GL_STATIC_DRAW);
    cout << "Size of this line buffer: " << vertData.size() << endl;
    // END GENERATE BUFFERS //

    areLinesThere = true;
}

void Mesh::DrawLines(Program& p) // PROGRAM* P will be a different program than the rest of the lighting, using unique FS and VS//
{
    if(!areLinesThere)
        Mesh::LoadOutlines();
    // VERTEX FORMAT SETTINGS //
    p.use();
    glBindBuffer(GL_ARRAY_BUFFER, linebuff);
    p.setVertexFormat("a", 3, GL_FLOAT,
                              "b", 3, GL_FLOAT,
                              "n1", 3, GL_FLOAT,
                              "n2", 3, GL_FLOAT,
                              "w", 1, GL_FLOAT);
    // END VERTEX FORMAT SETTINGS //

    // DRAW //
    glLineWidth(1.0);
    glDrawArrays(GL_LINES, 0, ic);
}

