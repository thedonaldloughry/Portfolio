#include "player.h"
#include "AI_enSub.h"
#include <math.h>
#include <vector>
#include "../gfx/SuperMesh.h"

class Collision
{
    public:
    class Sphere
    {
    public:
      vec4 center;
      float radius;
      Sphere(vec4 temp_center, float temp_radius)
      {
        center = temp_center;
        radius = temp_radius;
      }
    };
    vector <Sphere* > c;
    void ship_ship()// Sphere-Sphere detection
    {

    	    // Assuming mPos is in the center of the mesh
    	    /*amin = mPos.x - mPos.x + mPos.y;
    	   amax = mPos.x + mPos.x + mPos.y;
    	   bmin = mPos.x - mPos.x - mPos.y;
    	   bmax = mPos.x + mPos.x - mPos.y;

    	   if(bmax < amin || bmin > amax)
    	   	   take_dam = false;
    	   else
    	   {
    	   	 take_dam = true;
    	   	 mPos -= mPos;
    	   	 pPos -= pPos;
    	   }*/
    }
//NOT WORKING STILL NEEDS DEBUGGED
    void sub_ensub(Player* player, vector<AI_Ensub*> enemySubs)
    {
        vector <Sphere* > c1;
        vector <Sphere* > c2;
        float minSpeed = 0.0;

        for (int i=0; i<1; i++)
        {
            c1.push_back(new Sphere(player->pos, 3.2f));
        }
        for(int i=0; i<enemySubs.size(); i++)
        {
            c2.push_back(new Sphere(enemySubs[i]->mPos, 3.2f));
            enemySubs[i]->mSpeed = 0.0049;
        }

        vec4 v;
        for (int i=0; i<1; i++)
        {
            for (int j=0; j<enemySubs.size(); j++)
            {
                v = c1[i]->center - c2[j]->center;
                float cDist;
                cDist = dot(v, v);
                float rSum;
                rSum = c1[i]->radius + c2[j]->radius; //c1.radius + c2.radius
                //cout << "cDist: " << cDist << endl;
                //cout << "rSum : " << rSum*rSum << endl;

                if( rSum*rSum >= cDist )
                {
                    //Collision
                    //cout << "Collision! SUB" << endl;
                    enemySubs[j]->mSpeed = 0.0;
                }
/*
                else
                {
                    //cout << "No Collision. SUB" << endl;
                    while (minSpeed <= 0.006 )
                    {
                        minSpeed += 0.000001;
                        enemySubs[j]->mSpeed = minSpeed;
                    }
                    if ( minSpeed == 0.006)
                    {
                        minSpeed = 0.006;
                        enemySubs[j]->mSpeed = minSpeed;
                    }
                }
*/
            }
        }
    }


    void ensub_ensub(vector<AI_Ensub*> enemySubs)
    {
        vector <Sphere*> c;
        float minSpeed = 0.0;

        for(int i=0; i<enemySubs.size(); i++)
        {
            c.push_back(new Sphere(enemySubs[i]->mPos, 3.2f));
            //cout << "------c.center " << c[i]->center << endl;
        }

        vec4 v;
        for (int i=0; i<enemySubs.size(); i++)
        {
            bool will_hit = false;
            for (int j=i+1; j<enemySubs.size(); j++)
            {
                v = c[i]->center - c[j]->center;
                float cDist;
                cDist = dot(v, v);
                float rSum;
                rSum = c[i]->radius + c[j]->radius;

                if( rSum*rSum >= cDist )
                {
                    //Collision
                    enemySubs[i]->mSpeed -= 0.001; //This slows the enemeySub[i] down to 0 Speed

                    enemySubs[j]->mSpeed = 0.0;

                    will_hit = true;
                    break;
                }
            }
            if (will_hit)
            {
                //Speeds the enemySub back up when not colliding
                enemySubs[i]->mSpeed += 0.001;
            }
        }

    }


};
