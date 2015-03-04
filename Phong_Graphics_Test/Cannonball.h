#include "llgl.h"
#include "Mesh.h"
#include <vector>
#include <stdexcept>
#include <iostream>

using namespace std;
using namespace llgl;

class Cannonball
{
    public:

        vec4 pos;
        vec4 vel;
        float lifeLeft = 1000.0;
        Mesh m = Mesh("sphere_Sphere.binary.mesh"); // sphere_Sphere.binary.mesh

        Cannonball(vec4 position, vec4 velocity); // REFER TO NOTES IF THIS DOESN'T WORK.
        void draw(Program& p);
        void update(int elapsed);
};
