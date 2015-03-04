/*
This file will test graphical effects and shaders on individual object meshes. Meshes imported were made in the freely distributed Blender modeling
software, and then run through an .obj file parser from www.ssugames.org.  This project also utilizes the LLGL and SDL development libraries, included
with the program and also given at www.ssugames.org. The LLGL and SDL libraries belong to their respective developers, and I hereby claim no
right to any of the code contained in those libraries, nor do I take responsibility for any errors contained within them.

- Donald Loughry II, Programmer
*/

#include "llgl.h"
#include <iostream>
#include <vector>
#include "math.h"
#include "Camera.h"
#include "SuperMesh.h"
#include "Sounds.h"
#include "Utilities.h"
#include <sstream>
#include <fstream>

using namespace std;
using namespace llgl;

#define winw 512
#define winh 512

Camera* cam = new Camera(winw, winh, 35.0, 0.1, 500.0);
Utilities* toolBox = new Utilities();
Sounds* tehMusics = new Sounds();
Program* cellFillProg = new Program("Assets/Shaders/cellVS.txt","Assets/Shaders/cellFS.txt");
Program* regFill = new Program("Assets/Shaders/vs.txt","Assets/Shaders/fs.txt"); //STANDARD PHONG LIGHTING SHADER.
Program* outlineProg = new Program("Assets/Shaders/outlineVS.txt","Assets/Shaders/outlineFS.txt");
Program* waterProg = new Program("Assets/Shaders/waterVS.txt", "Assets/Shaders/waterFS.txt");

vector<Program*> allProgs;

float modelAngle = 0;
float yawAngle = 0;

vec4 Dir(0,0,1,0.0);
vec4 Pos(0,0,20,1.0);
SuperMesh* testModel;
vec4 eye = Pos + (20 * Dir);
vec4 coi;



int main(int argc, char* argv[]){

    allProgs.push_back(cellFillProg);
    //allProgs.push_back(regFill);
    allProgs.push_back(outlineProg);
    allProgs.push_back(waterProg);

    toolBox->prepareLLGL(winw, winh); // Initializes the LLGL game window, in Utilities.h
    //toolBox->setWaterDirections(waterProg);
    toolBox->askForMesh(allProgs, testModel);

    Utilities::Character Model(Dir);

    toolBox->setLights(cellFillProg);

    tehMusics->init();
    tehMusics->mc = Mix_LoadWAV("Assets/Music/Skipping_in_the_No_Standing_Zone.wav");
    tehMusics->play(255, -1); //255 for full blast, -1 for repeat

    testModel->load();

    float now,last;
    float passedTime = 0.0;
    last=now=SDL_GetTicks();

    while(toolBox->handleInput(modelAngle, yawAngle, Pos))
    {
        // GET ELAPSED TIME //
        now = SDL_GetTicks();
        float elapsed = now-last;
        // END GET ELAPSED TIME //

        passedTime += 0.1;
        if(passedTime >= 2*3.14) // for water, reset the sine waves to start position
            passedTime = 0.0;

        // SET CAMERA //
        cam->Set(eye, coi);
        // END SET CAMERA //

        // HANDLE EVENTS //
        //toolBox->handleInput(modelAngle, yawAngle, Pos);
        toolBox->setScene(Model, Dir, Pos, coi);
        // END HANDLE EVENTS //

        // DRAW //
        float lineWidth = 2.0 /*Pos.z / (eye.z / 2);*/;
        toolBox->draw(allProgs, cam, testModel, Pos, modelAngle, yawAngle, Dir, lineWidth);
        // END DRAW //

        // GET ELAPSED TIME & SET DELAY //
        last=now;
        now = SDL_GetTicks();
        float delay = 20-(now-last);
        if(delay>0)
            SDL_Delay(delay);
        // END GET ELAPSED TIME & SET DELAY //
    }
    return 0;
}
