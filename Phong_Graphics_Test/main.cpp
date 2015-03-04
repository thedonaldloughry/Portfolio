#include "llgl.h"
#include <iostream>
#include <vector>
#include "math.h"
#include "Camera.h"
#include "SuperMesh.h"
#include "Sounds.h"
#include <sstream>

using namespace std;
using namespace llgl;

#define winw 512
#define winh 512
#define MAX_LIGHTS 4

map<int,bool> keydown;
int recharge_time=0;
Camera* cam = new Camera(winw, winh, 35.0, 0.1, 500.0);
Program prog1("vs.txt","fs.txt");

// ANGLES!!! ///////////////
float planeangle=0;///////
float bankAngle = 0;//////
float tiltAngle = 0; ///////
float camAngle = 0;//////
float walkDist = 0;///////
////////////////////////////

vec4 planedir(0,0,1,0.0);
vec4 planepos(0,0,-10,1.0);
SuperMesh* plane = new SuperMesh("assets/planeLighting/plane/plane4.spec.mesh");
//SuperMesh* plane = new SuperMesh("assets/TheAnimatedStarfish/Starfish.spec.mesh");
SuperMesh* ground = new SuperMesh("assets/terrainLighting/terrain/terrain.spec.mesh");
vec4 eye = planepos + (-30 * planedir) + (10* vec4(0,1,0,0));
vec4 coi;

mat4 terrainwm = scaling(vec4(100,100,100,1.0)) * translation(vec4(0,-10,0,0));

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

struct Character
{
    vec4 W;
    vec4 U;
    vec4 V;
    float shiny = 50.0;
    // THIS MAY BE COMPLETELY USELESS AS OF RIGHT NOW...
    Character(vec4 dirVector)
    {
        W = normalize(dirVector);
        vec4 U = vec4(cross(vec3(0,1,0), W.xyz()), 0);
        vec4 V = vec4(cross(W.xyz(), U.xyz()), 0);
        U = normalize(U);
        V = normalize(V);
    }
    void Build(vec4 dir, vec4 pos)
    {
        W = normalize(dir);
        U = normalize(vec4(cross(vec3(0,1,0), W.xyz()), 0) * axisRotation(vec4(1,0,0,0.0), tiltAngle) * translation(pos));
        V = normalize(vec4(cross(W.xyz(), U.xyz()), 0)  * axisRotation(vec4(0,1,0,0.0), tiltAngle) * translation(pos));
    }
};

void reAdjust(float& angle)
{
    if(angle > 0.0005)
    {
        angle -= 0.005;
    }

    else if(angle < 0.0005)
    {
        angle += 0.005;
    }

    if(angle > 1.0003)
        angle = 1.0003;
    else if (angle < -1.0003)
        angle = -1.0003;
}


void update(int elapsed, Character& MainChar, vec4& eye, Camera* camera){

    planepos = planepos + elapsed * 0.01 * planedir;
    walkDist += 0.01 * elapsed;
    //eye = planepos + (-30 * planedir);
    eye += (walkDist * planedir);
    reAdjust(bankAngle);
    //Mouse controls?
    int mousePosX, mousePosY;
   //bankAngle +=


    if( keydown[SDLK_a] ){
        planeangle += 0.0005 * elapsed;
        bankAngle -= 0.0005 * elapsed;
    }

    if( keydown[SDLK_d] ){
        planeangle -= 0.0005 * elapsed;
        bankAngle += 0.0005 * elapsed;
    }

    if( keydown[SDLK_w] ){
            tiltAngle -= 0.0005 * elapsed;
    }
    if( keydown[SDLK_s] ){
            tiltAngle += 0.0005 * elapsed;
    }

    if( keydown[SDLK_j] ){
        camAngle += 0.0005 * elapsed;
    }

    if( keydown[SDLK_l] ){
        camAngle -= 0.0005 * elapsed;
    }

    if( keydown[SDLK_SPACE] && recharge_time == 0 ){
    }

    MainChar.Build(planedir, planepos);
    walkDist = 0;

    planeangle += (0.03 * -bankAngle);

    mat4 M = axisRotation(vec3(0,1,0),planeangle);
    mat4 M2 = axisRotation(vec3(0,0,1),bankAngle);
    mat4 M3 = axisRotation(vec3(1,0,0), tiltAngle);
    M = M2 * M3 * M;
    planedir = vec4(0,0,1,0) * M;
    cam->CircleAround(vec4(0,1,0,0.0), planepos, camAngle);
    coi = planepos;


    prog1.use();
    prog1.setUniform("ambient", vec4(0.01,0.01,0.01,1.0));
    prog1.setUniform("A0", 0.005);
    prog1.setUniform("A1", 0.005);
    prog1.setUniform("A2", 0.005);
}

void draw(){
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

    prog1.use();
    cam->draw(prog1);

    prog1.setUniform("worldMatrix",terrainwm);
    ground->draw(prog1);



    mat4 M = axisRotation(vec3(0,1,0),planeangle);
    mat4 M2 = axisRotation(vec3(0,0,1),bankAngle);
    mat4 M3 = axisRotation(vec3(1,0,0), tiltAngle);
    M = M2 * M3 * M * scaling(vec4(0.5,0.5,0.5,1.0)) * translation(vec4(planepos.x,planepos.y,planepos.z,0.0));
    prog1.setUniform("worldMatrix",M);
    plane->draw(prog1);

    llglSwapBuffers();
}


int main(int argc, char* argv[]){

    llglSetup(winw,winh);

    glEnable(GL_DEPTH_TEST);
    glDepthFunc(GL_LEQUAL);

    glClearColor(0.2,0.4,0.6,1);

    Character Spyro(planedir);

    // SETTING LIGHTS //////////////////////////////////////////////////
    lights[0] = new Light(vec4(-200, 10, 0, 0.0), vec4(255,0,255,1.0), vec4(0, 1, 0, 0.0));
    lights[1] = new Light(vec4(0, 10, 200, 0.0), vec4(0,255,255,1.0), vec4(0, 0, 1, 0.0));
    lights[2] = new Light(vec4(0, 10, 0, 10.0), vec4(0,255,0,1.0), vec4(-10, 0, 0, 1.45));
    lights[3] = new Light(vec4(0, 200, 0, 0.0), vec4(255,255,255,1.0), vec4(0, -1, 0, 0.0));


    prog1.use();
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

    Sounds ArtisansTheme;
    ArtisansTheme.init();

    plane->load();
    ground->load();

    int now,last;
    last=now=SDL_GetTicks();

    ArtisansTheme.mc = Mix_LoadWAV("assets/Spyro Music/Dark Hollow.wav");
    ArtisansTheme.play(255, -1);

    cout << "Use A and D to rotate the plane. Use J and L to control the camera. \nMusic by Stewart Copeland, from the game Spyro the Dragon,\n by Insomniac Games, all rights reserved.\n\n" << endl;

    while(1){
        now = SDL_GetTicks();
        int elapsed = now-last;
        SDL_Event ev;
        while(SDL_PollEvent(&ev)){
            if( ev.type == SDL_QUIT ){
                SDL_Quit();
                return 0;
            }
            else if(ev.type == SDL_MOUSEMOTION)
            {
                int mousePosX = ev.motion.x;
                int mousePosY = ev.motion.y;
                cout<<mousePosX<<" " << mousePosY<<endl;
            }
            else if( ev.type == SDL_MOUSEBUTTONDOWN ){
                    int mousePosX = ev.motion.x;
                int mousePosY = ev.motion.y;
                cout<<mousePosX<<" " << mousePosY<<endl;
            }
            else if( ev.type == SDL_KEYDOWN){
                keydown[ev.key.keysym.sym] = true;
            }
            else if( ev.type == SDL_KEYUP ){
                keydown[ev.key.keysym.sym] = false;
            }

        }
        cam->Set(eye, coi);
        update(elapsed, Spyro, eye, cam);
        draw();
        last=now;
        now = SDL_GetTicks();
        int delay = 20-(now-last);
        if(delay>0)
            SDL_Delay(delay);
    }

    return 0;
}
