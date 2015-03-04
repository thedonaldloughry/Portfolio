
#include "../gfx/SuperMesh.h"

#ifndef _AI_main_H_
#define _AI_main_H_ NULL
#define PI 3.1415926535897932384626433832
class AI_Main
{
public:
    float angle = 0;
    float turn = 0;
    float tiltAngle = 0;
    float mSpeed = 0.0049;
    vec4 dir = vec4(0.0,0.0,1.0,0.0);
    vec4 mPos;



    void update(int elapsed)
    {
        this->mPos = this->mPos + elapsed * this->mSpeed * this->dir;

    }
    void draw(Program& p,Program& edgeProg,SuperMesh* mMesh)
    {
        mat4 M = axisRotation(vec3(0,1,0),this->angle); // rotation on y axis
        mat4 B = axisRotation(vec3(0,0,1),this->turn); // rotation on z axis
        mat4 T = axisRotation(vec3(1,0,0),this->tiltAngle); // rotation on x axis
        mat4 tempM = axisRotation(vec3(0,1,0),this->angle); //rotation on y axis used for dir changes.
        tempM = B * T * tempM;
        vec4 tempD = vec4(0,0,1,0);
        M = B * T * M;
        dir = tempD * tempM;
        M = M * scaling(vec4(0.5,0.5,0.5,1.0))  * translation(vec4(this->mPos.x,this->mPos.y,this->mPos.z,0.0));
        p.use();
        p.setUniform("worldMatrix", M);
        mMesh->draw(p, edgeProg);

    }
    void rotMesh(char axis,float num,float elapsed)
    {
        /*** axis is the axis that is to be rotated around. num is a variable to multiply the change in angle ***/

        if(axis == 'y')
            angle = angle + 0.0001 * num * elapsed;

        if(axis == 'x')
        {
            tiltAngle = tiltAngle + 0.0001 * num * elapsed;

            if(tiltAngle > PI/4)
                tiltAngle = PI/4; // y axis limitations, may be changed later to reflect realism.
            if(tiltAngle < -PI/4)
                tiltAngle = -PI/4;
        }

    }


};
#endif
