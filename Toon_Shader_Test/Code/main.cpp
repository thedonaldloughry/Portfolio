#include "llgl.h"
#include <vector>
#include <iostream>
#include "math.h"
#include "Code/gfx/Camera.h"
#include "Code/game/game.h"
#include "Code/gfx/gfx.h"

using namespace std;
using namespace llgl;

Program prog1("Code/gfx/vs.txt","Code/gfx/fs.txt");
Program prog2("Code/gfx/outlineVS.txt","Code/gfx/outlineFS.txt");

#define winw 512
#define winh 512
#define MAX_LIGHTS 4


//Camera* chaseCam = new Camera(winw, winh, 35.0,0.1,500.0);
Player* player = new Player();
Terrain* seafloor = new Terrain();
Terrain* sea = new Terrain();
Sky* sky = new Sky();
vector<AI_Ensub*> enemySubs;
vector<AI_Enship*> enemyShips;
Collision* collision = new Collision();
SuperMesh * torp = new SuperMesh("Assets/models/weapons/Missle.spec.mesh");
Framebuffer * fbo1 = new Framebuffer(512, 512);

////////////////////////////////////////////
// Leave Light system In The Main For Now //
////////////////////////////////////////////
struct Light
{
    vec4 pos;
    vec4 col;
    vec4 dir;
    Light(vec4 position, vec4 color, vec4 direction)
    {
        pos = position;
        col = color;
        dir = direction;
    }
};

Light* lights[MAX_LIGHTS];

void draw()
{
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
    prog1.use();

    seafloor->draw(prog1, prog2);
    sea->draw(prog1, prog2);
    player->draw(prog1, prog2);
    sky->draw(prog1,prog2);

    for(int i = 0;i < enemySubs.size();i++)
    {
        enemySubs[i]->draw(prog1, prog2);

    }
    for(int i = 0;i < enemyShips.size();i++)
    {
        enemyShips[i]->draw(prog1, prog2);

    }

    //chaseCam->draw(prog1);
    seafloor->draw(prog1, prog2);
    sea->draw(prog1, prog2);
    player->draw(prog1, prog2);
    sky->draw(prog1,prog2);
    /*for(int i = 0; i < seafloor->ground->m.size(); i++) // just curious to see if this will work... -Don
        seafloor->ground->m[i]->DrawLines(prog2);*/

        //Temporarily drawing a missile to serve as a reference point to where sun will be
        //mat4 M = axisRotation(vec3(0,1,0),0);
        //mat4 B = axisRotation(vec3(0,0,1),0);
        //mat4 T = axisRotation(vec3(1,0,0),0);
        //M = B*T* M * scaling(vec4(1.0,1.0,1.0,1.0))  * translation(vec4(0.0,100.0,100.0,0.0));
        //prog1.use();
        //prog1.setUniform("worldMatrix", M);
        //torp->draw(prog1, prog2);

    llglSwapBuffers();
}

void update()
{
    prog1.use();
    prog1.setUniform("ambient", vec4(0.01,0.01,0.01,1.0));

    prog1.setUniform("A0", 0.005);
    prog1.setUniform("A1", 0.005);
    prog1.setUniform("A2", 0.005);

    //Fog Start//

    vec4 fogColor;
    float fogStart;
    float fogEnd;

    if (player->pos.y > 20) //Above Ocean
    {
        fogStart = 400.0;
        fogEnd = 500.0;
        prog1.setUniform("fogOn", 1.0);
        glClearColor(0.0, 0.3, 0.8, 1.0);
        fogColor = vec4(0.0, 0.3, 0.8, 1.0);
    }

    if (player->pos.y < 20) //Below Ocean
    {
       fogStart = 10.0;
       fogEnd = 500.0;
       prog1.setUniform("fogOn", 1.0);
       glClearColor(0.0,0.3,0.8,1.0);
       fogColor = vec4(0.0, 0.3, 0.8, 1.0);
    }

    prog1.setUniform("fogColor", fogColor);  //This color and gl_ClearColor must be the same

    //Linear Fog//
    //float fogStart = 10.0; //Change this value to set how far the fog starts from you
    //float fogEnd = 500.0; //Change this value to set how far the fog goes into the distance
    prog1.setUniform("fogStart", fogStart);
    prog1.setUniform("deltaFog", fogEnd - fogStart);
    /////////////////

    //Exponential Fog
    float density = 0.001; //Change this to change the density of exponential fog
    prog1.setUniform("density", density);
    ////////////////

    if (player->fogType == 0.0) //Linear Fog
        prog1.setUniform("fogType", 0.0);
    if (player->fogType == 1.0) //Exponential Fog
        prog1.setUniform("fogType", 1.0);
    //Fog End//

    //Collisions --- NOT WORKING//
    collision->sub_ensub(player, enemySubs);
    collision->ensub_ensub(enemySubs);
    }


int main(int argc, char* argv[])
{
    llglSetup(winw, winh);
    //SDL_WM_GrabInput(SDL_GRAB_ON);
    SDL_WarpMouse(512/2, 512/2);

    glEnable(GL_DEPTH_TEST);
    glDepthFunc(GL_LEQUAL);

    glClearColor(0.0,0.3,0.8,1);

    torp->load();

    prog1.use();

    enemySubs.push_back(new AI_Ensub(vec4(24,0,-10,1.0)));
    enemySubs.push_back(new AI_Ensub(vec4(24,24,-10,1.0)));
    //enemySubs.push_back(new AI_Ensub(vec4(24,0,-30,1.0)));
    //enemySubs.push_back(new AI_Ensub(vec4(24,24,20,1.0)));
    //enemySubs.push_back(new AI_Ensub(vec4(24,-24,-10,1.0)));
    enemyShips.push_back(new AI_Enship(vec4(24,20,10,1.0)));
    seafloor->ground->load();
    //sea->water->load();
    player->pl->load();
    sky->sky->load();

    // SETTING LIGHTS //////////////////////////////////////////////////
    lights[0] = new Light(vec4(0, 200, 0, 0.0), vec4(0,0,0,1.0), vec4(0, -1, 0, 0.0));
    lights[1] = new Light(vec4(0, 10, 200, 0.0), vec4(0,0,0,1.0), vec4(0, 0, 1, 0.0));
    lights[2] = new Light(vec4(0, 10, 0, 10.0), vec4(0,0,0,1.0), vec4(-10, 0, 0, 0.0));
    lights[3] = new Light(vec4(0, 200, 0, 0.0), vec4(0,0,0,1.0), vec4(0, -1, 0, 0.0));

    for(int i = 0; i < MAX_LIGHTS; i++)
    {
        ostringstream oss, oss2, oss3;

        oss << "lights[" << i << "].pos";
        prog1.setUniform(oss.str(), lights[i]->pos);

        oss2 << "lights[" << i << "].col";
        prog1.setUniform(oss2.str(), lights[i]->col);

        oss3 << "lights[" << i << "].dir";
        prog1.setUniform(oss3.str(), lights[i]->dir);
    }
    /////////////////////////////////////////////////////////////////////////

    int now,last;
    last=now=SDL_GetTicks();
    while(1)
    {
        now = SDL_GetTicks();
        int elapsed = now-last;

        SDL_Event ev;
        while(SDL_PollEvent(&ev))
        {
            if(ev.type == SDL_QUIT)
            {
                SDL_Quit();
                return 0;
            }

            else if(ev.type == SDL_KEYDOWN)
            {

                player->keydown[ev.key.keysym.sym] = true;
                player->keyup[ev.key.keysym.sym] = false;

            }
            else if(ev.type == SDL_KEYUP)
            {
                player->keydown[ev.key.keysym.sym] = false;
                player->keyup[ev.key.keysym.sym] = true;
            }
            else if(ev.type == SDL_MOUSEMOTION)
            {
                player->getMousePos(ev);

            }
            else if(ev.type == SDL_MOUSEBUTTONDOWN)
            {
                player->mousebutton[ev.button.button] = true;
            }
            else if(ev.type == SDL_MOUSEBUTTONUP)
                player->mousebutton[ev.button.button] = false;

        }
        //cam->Set(player->eye,player->coi);
        //player->eyeSet(chaseCam);
        player->update(elapsed,&prog1);
        for(int i = 0; i < enemySubs.size();i++)
        {
            float eDist = enemySubs[i]->get_distance(player->pos);
            enemySubs[i]->update(elapsed);
            if(eDist < 30)
                enemySubs[i]->chase_player(player->pos,elapsed);
            /*if(eDist < 4.0 || eDist > 150.0)
            {
                AI_Ensub * temp;
                temp = enemySubs[enemySubs.size()-1];
                enemySubs[enemySubs.size()-1] = enemySubs[i];
                enemySubs[i] = temp;
                enemySubs.pop_back();
                int x = rand()%50+player->pos.x / 2;
                int y = rand()%20+player->pos.y / 2;
                int z = rand()%50+player->pos.z / 2;
                enemySubs.push_back(new AI_Ensub(vec4(x,y,z,1.0)));
                enemySubs.push_back(new AI_Ensub(vec4(x + 30,y + 20,z + 30,1.0)));
            }*/
        }
        for(int i = 0; i < enemyShips.size(); i++)
        {
            enemyShips[i]->update(elapsed);
        }
        update();

        draw();
        last=now;
        now = SDL_GetTicks();
        int delay = 20-(now-last);
        if(delay>0)
            SDL_Delay(delay);
    }
    return 0;
}
