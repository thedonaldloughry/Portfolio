#ifndef GUI_H_INCLUDED
#define GUI_H_INCLUDED
#include "../gfx/SuperMesh.h"
#include <math.h>
#include <vector>


static SuperMesh * healthbar = new SuperMesh("Assests/models/Gui/health.spec.mesh");
static SuperMesh * healthbar_OL = new SuperMesh("Assests/models/Gui/health_outline.spec.mesh");

class gui{
public:

        mat4 M;
        vec4 mPos;

/*void sethealth(pos, Va, W, U, V)
{

    Va = Camera->up;
    W = Camera->eye - healthbar;
    U = cross(Va,W);
    V = cros(W, U);

}*/
    void draw(Program& prog1,Program& prog2,SuperMesh* healthbar, SuperMesh * healthbar_OL)
    {

        M = translation(vec4(this->mPos.x,this->mPos.y,this->mPos.z,0.0));
        prog1.use();
        prog1.setUniform("worldMatrix", M);
        healthbar->draw(prog1, prog2);
        healthbar_OL->draw(prog1,prog2);
    }





};
#endif // GUI_H_INCLUDED
