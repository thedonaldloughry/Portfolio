#ifndef AI_MINE_H_
#define AI_MINE_H_

#include "AI_Main.h"
#include "math.h"
#include <vector>




static SuperMesh * mineMesh = new SuperMesh("Assets/models/weapons/Mine.spec.mesh");
class AI_Mine : AI_Main
{
public:
    SuperMesh* mMesh;
    float fallSpeed = 0.005;



    AI_Mine(vec4 pos)
    {
        this->mPos = pos;
        this->mMesh = mineMesh;
        this->mMesh->load();
        this->dir = vec4(0,-1,0,0.0);
    }


    void update(int elapsed)
    {
        mPos.y = mPos.y - fallSpeed * elapsed;
        //cout << "falling" << endl;
        //AI_Main::rotMesh();
        if(mPos.y < -8)
            mPos.y = -8;
        angle += 0.0 * - turn;

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

        float dist =sqrt(((nums[0] - nums[3]) * (nums[0] - nums[3]))
                         + ((nums[1] -nums[4]) * (nums[1] -nums[4]))
                         + ((nums[2] - nums[5]) * (nums[2] - nums[5])));
        return dist;
    }

    void draw(Program& p, Program& edgeProg)
    {
        AI_Main::draw(p,edgeProg,mMesh);
    }
};
#endif // AI_MINE_H_
