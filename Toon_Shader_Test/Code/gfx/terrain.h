#include "SuperMesh.h"

using namespace std;
using namespace llgl;


class Terrain
{
public:

    SuperMesh* ground = new SuperMesh("Assets/models/terrain/terrain.spec.mesh");
    //SuperMesh* water = new SuperMesh("Assets/models/terrain/water.spec.mesh");
    mat4 terrainwm = scaling(vec4(1000,100,1000,1.0)) * translation(vec4(0,-10,0,0));

    void draw(Program &p, Program& edgeProg)
    {
        p.use();
        p.setUniform("worldMatrix", terrainwm);
        ground->draw(p, edgeProg);

        //water->draw(p, edgeProg);
    }
};

class Sky
{
public:

    SuperMesh* sky = new SuperMesh("Assets/models/terrain/bluesky.spec.mesh");
    mat4 skywm = scaling(vec4(30,30,30,1.0)) * translation(vec4(0,100,0,0));

    void draw(Program &p, Program& edgeProg)
    {
        p.use();
        p.setUniform("worldMatrix", skywm);
        sky->draw(p, edgeProg);
    }
};
