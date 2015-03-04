/*
include all the player headers that need to be shared here
*/
#ifndef _player_H_
#define _player_H_ NULL
//#include "p_controls.h"
#include <map>

#include "../gfx/SuperMesh.h"
#include "../gfx/Camera.h"
#include "wp.h"

#define MAX_CAM_ANG 45
#define Max_Speed 0.01
using namespace std;
using namespace llgl;
Camera* cam = new Camera(35.0,0.1,500.0);


class Player
{
public:

    float yaw = 0;
    float pitch = 0;
    float camPitch,camYaw ,mouseCamPitch,mouseCamYaw;
    float zoom = 0;
    float roll = 0;
    float mouseX = 0;
    float mouseY = 0;
    float fogType = 0.0;
    float accel = 0.0001;
    float curSpeed = 0.01;
    int torpDelay = 0;
    vector<Wp_Torp*> torps;

    bool mouseOn = false;
    bool singlePress = true;
    bool angleReset = false;

    map<int, bool> keydown;
    map<int, bool> keyup;
    map<int,bool> mousebutton;
    vec4 dir = vec4(0,0,1,0.0);
    vec4 pos = vec4(0,10,-10,1.0);
    //SuperMesh* pl = new SuperMesh("Assets/models/player/plane/plane4.spec.mesh");
    SuperMesh* pl = new SuperMesh("Assets/models/player/sub/Sub.spec.mesh");
    vec4 eye = pos + (-30.0 *vec4(0,0,1,0.0));
    vec4 coi;


    void getMousePos(SDL_Event ev)
    {

        mouseX = ev.motion.x - (512 / 2);
        mouseY = ev.motion.y - (512 / 2);
    }


    void getMouseClick()
    {
        if(mousebutton[SDL_BUTTON_RIGHT])
        {
            mouseOn = true;

        }
        else
        {
            mouseOn = false;
        }
    }
/////////////////////////////////
// Code For the Mouse Movement //
// Will Be Moved To p_Controls //
/////////////////////////////////
    void mouseController(int elasped)
    {
        getMouseClick();

        if(mouseOn)
        {
            mouseCamYaw += mouseX * -0.00007;
            mouseCamPitch += mouseY * 0.00007;

            if(mouseCamPitch > 0.009)
                mouseCamPitch = 0.009;
            if(mouseCamPitch < -0.009)
                mouseCamPitch = -0.009;
            if(mouseCamYaw > 0.009)
                mouseCamYaw = 0.009;
            if(mouseCamYaw < -0.009)
                mouseCamYaw = -0.009;

            if(mouseX < 20 and mouseX > -20 and mouseY <20 and mouseY > -20)
            {
                mouseX = 0;
                mouseY = 0;
            }


        }
        else
        {
            mouseCamPitch = 0;
            mouseCamYaw = 0;
        }

    }

    ////////////////////////////////
    // Code For Keyboard Controls //
    // Maybe Moved To p_Controls  //
    ////////////////////////////////
    // Everything In This Will Be //
    // Rewritten Soon             //
    ////////////////////////////////
    void keyboardController(int elapsed)
    {

        if( keydown[SDLK_a] )
        {
            angleReset = false;
            yaw += 0.0007* elapsed;
            camYaw += 0.0007*elapsed;
        }

        if( keydown[SDLK_d] )
        {
            angleReset = false;
            yaw -= 0.0007* elapsed;
            camYaw -=0.0007 * elapsed;
        }

        if(keydown[SDLK_w])
        {
            angleReset = false;
            pitch -= 0.0005 * elapsed;
            //camPitch -= 0.0005 * elapsed;
        }

        if(keydown[SDLK_s])
        {
            angleReset = false;
            pitch += 0.0005 * elapsed;
           // camPitch += 0.0005 * elapsed;
        }

        if(keydown[SDLK_q])
        {
            angleReset = true;
            if(keydown[SDLK_ESCAPE])
                SDL_Quit();
        }
        if(keydown[SDLK_1])//Linear Fog
            fogType = 0.0;

        if(keydown[SDLK_2])//Exponential Fog
            fogType = 1.0;

        if(keydown[SDLK_r])
        {
            if(curSpeed >= Max_Speed)
                curSpeed = 0.01;
            curSpeed += accel;
        }
        if(keydown[SDLK_f])
        {
            if(curSpeed <= 0.0)
                curSpeed = 0.0;
            curSpeed-=accel;
        }
        if(keydown[SDLK_SPACE])
        {
            fireTorp(elapsed);
        }
    }


    void update(int elapsed,Program *p)
    {
        system("cls");
        pos = pos + elapsed * curSpeed * dir;
        eye = pos + (-30 * vec4(0,0,1,0));

        mouseController(elapsed);
        keyboardController(elapsed);
        cout<<dir<<endl;
        torpDelay += elapsed;

        for(int i = 0;i < torps.size(); i++)
        {
            if(get_distance(pos,torps[i]->get_pos()) > 300)
            {
                Wp_Torp* temp;
                temp = torps[torps.size()-1];
                torps[torps.size()-1] = torps[i];
                torps[i] = temp;
                torps.pop_back();
            }
        }

        for(int i = 0; i < torps.size();i++)
        {
            torps[i]->update(elapsed);
        }



        if(mouseOn)
        {
            cam->Set(cam->eye,pos);
            cam->CircleAround(vec4(1,0,0,0.0),pos,mouseCamPitch);
            cam->CircleAround(vec4(0,1,0,0.0),pos,mouseCamYaw);
        }
        else
        {
            cam->Set(eye,pos);
            cam->CircleAround(vec4(1,0,0,0.0),pos,camPitch);
            cam->CircleAround(vec4(0,1,0,0.0),pos,camYaw);

        }

    }


    void draw(Program &p, Program& edgeProg)
    {
        mat4 B = axisRotation(vec3(0,0,1),roll);
        mat4 M = axisRotation(vec3(0,1,0),yaw);
        mat4 P = axisRotation(vec3(1,0,0),pitch);
        M =  B * P * M * scaling(vec4(0.5,0.5,0.5,1.0))*translation(vec4(pos.x,pos.y,pos.z,0.0));
        dir = vec4(0,0,1,0) * M;
        p.use();
        p.setUniform("worldMatrix", M);
        cam->draw(p);
        cam->draw(edgeProg);
        pl->draw(p, edgeProg);
        for(int i = 0; i < torps.size();i++)
        {
            torps[i]->draw(p, edgeProg);
        }
    }

    void fireTorp(int elapsed)
    {
        if(torpDelay > 3000)
        {
            torps.push_back(new Wp_Torp(this->pos,this->dir,this->yaw,this->pitch));
            torpDelay = 0;
        }
    }

    float get_distance(vec4 pPos, vec4 mPos)
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


};

#endif _player_H_
