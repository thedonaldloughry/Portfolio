#ifndef WP_TORP_H_
#define WP_TORP_H_

#include "AI_Main.h"
#include "math.h"
#include <vector>





static SuperMesh * torpMesh = new SuperMesh("Assets/models/weapons/Missle.spec.mesh");
class Wp_Torp: AI_Main
{
public:
    SuperMesh* mMesh;


    Wp_Torp(vec4 pos,vec4 tDir,SuperMesh * mesh,float ang,float tilt)
    {
        this->mPos = pos;
        this->angle = ang;
        this->tiltAngle = tilt;
        mMesh = mesh; // Alternative way to make torpedo with what ever mesh wanted... maybe special torps!
        mMesh->load();
        this->mSpeed = 0.05;

    }
    Wp_Torp(vec4 pos,vec4 tDir,float ang,float tilt) //tDir means temp dir..
    {
        this->mPos = pos;
        this->angle = ang;
        this->tiltAngle = tilt;
        mMesh = torpMesh;
        mMesh->load();
        this->mSpeed = 0.05;
    }


    void update(int elapsed)
    {
        //AI_Main::rotMesh();
        AI_Main::update(elapsed);
    }

    float get_distance(vec4 pPos)
    {
        float nums[6];
        nums[0] = pPos.x;
        nums[1] = pPos.y;
        nums[2] = pPos.z;

        nums[3] = mPos.x;
        nums[4] = mPos.y;
        nums[5] = mPos.z;
        int i = 0;
        while(i < 6)
        {
            if(nums[i] < 0)
                nums[i] = -nums[i];
            i++;
        }

        float dist = sqrt(((nums[0] - nums[3]) * (nums[0] - nums[3]))
                         + ((nums[1] -nums[4]) * (nums[1] -nums[4]))
                         + ((nums[2] - nums[5]) * (nums[2] - nums[5])));
        return dist;
    }

    void draw(Program& p, Program& edgeProg)
    {
        AI_Main::draw(p,edgeProg,mMesh);
    }
    vec4 get_pos()
    {
        return this->mPos;
    }
};
#endif

