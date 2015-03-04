#ifndef AI_ENSUB_H_
#define AI_ENSUB_H_
#include "wp_torp.h"
#include "AI_Main.h"
#include "math.h"
#include <vector>



/*
 * to make one of these work, Create an instance then use the update and (or) the
 * chase player to get them to follow the player. these can be put in a single function
 * later if you wish, but i thought that they might not start chasing the player till
 * they are close.
 */
 static SuperMesh * subMesh = new SuperMesh("Assets/models/player/sub/Sub.spec.mesh");
class AI_Ensub : public AI_Main
{
public:
    SuperMesh* mMesh;
    int torpDelay = 0;
    vector<Wp_Torp*> torpsShot;
    AI_Ensub(vec4 pos,SuperMesh * mesh)
    {
        this->mPos = pos;
        mMesh = mesh; // Alternative way to make sub with what ever mesh wanted..
        mMesh->load();

    }
    AI_Ensub(vec4 pos)
    {
        this->mPos = pos;
        mMesh = subMesh;
        mMesh->load();
    }


    void update(int elapsed)
    {
        AI_Main::update(elapsed); // put sub specific things here..
        //AI_Main::rotMesh();
        for(int i = 0;i < torpsShot.size(); i++)
        {
            if(get_distance(torpsShot[i]->get_pos()) > 300)
            {
                Wp_Torp* temp;
                temp = torpsShot[torpsShot.size()-1];
                torpsShot[torpsShot.size()-1] = torpsShot[i];
                torpsShot[i] = temp;
                torpsShot.pop_back();
            }
        }
        //cout << "dir.x : "<< dir.x << endl;
        //cout << "dir.y : "<< dir.y << endl;
        //cout << "dir.z : "<< dir.z << endl;

        for(int i = 0; i < torpsShot.size();i++)
        {
            torpsShot[i]->update(elapsed);
        }


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
        for(int i = 0; i < torpsShot.size();i++)
        {
            torpsShot[i]->draw(p, edgeProg);
        }
    }
    void chase_player(vec4 pPos,float elapsed)
    {
        vec4 dirT = pPos - mPos;
        vec4 nDir = normalize(dirT);
        vec4 north = vec4(0.0,0.0,1.0,0.0);
        vec3 thing = cross(vec3(north.x,north.y,north.z),vec3(dirT.x,dirT.y,dirT.z));
        //cout << thing << endl;
        float Q = atan2(-dirT.z,dirT.x);
        cout << "Q : " << Q << endl;
        float heading = atan2(-dir.z,dir.x);
        cout << "Heading : " << heading << endl;
        float delta = Q - heading;
        cout << "delta : " << delta << endl;
        if(delta > 0)
            angle += 0.0002 * elapsed;
        else
            angle -= 0.0002 * elapsed;

        if(thing.x > 0.0)
            tiltAngle += 0.0002 * elapsed;
        else
            tiltAngle -= 0.0002 * elapsed;
        if(tiltAngle > 0.1)
            tiltAngle -= 0.0002 * elapsed;

        if(tiltAngle < -0.1)
            tiltAngle += 0.0002 * elapsed;










        fireTorp(elapsed);
    }

    void fireTorp(int elapsed)
    {
        torpDelay += elapsed;
        if(torpDelay > 3000)
        {
            torpsShot.push_back(new Wp_Torp(this->mPos,this->dir,this->angle,this->tiltAngle));
            torpDelay = 0;
        }
    }
};


// below is garbage left for reference..//


/*if(nDir.x < dir.x)
        {
            angle = angle - aSpeed * elapsed * turnVar;
        }

        else if(nDir.x > dir.x)
        {
            angle = angle + aSpeed * elapsed * turnVar;
        }*/

        /*if(nDir.z < -0.1)
        {
            turnVar = -1;
        }
        else
        {
            turnVar = 1;
        }*/
#endif
