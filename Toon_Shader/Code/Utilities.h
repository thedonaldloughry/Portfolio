#include "llgl.h"
#include <iostream>
#include <vector>
#include <sstream>
#include <fstream>
#include "math.h"

using namespace std;
using namespace llgl;

//GLOBAL DEFINITIONS//
#define MAX_LIGHTS 4

//END GLOBAL DEFINITIONS//

class Utilities
{
    public:

    map<int,bool> keydown;     // keys that are pressed //
    map<int,bool> mousedown; // mouse buttons that are pressed //
    SDL_Event ev;                    // other event types //
    mat4 M;                             // matrix for current object orientation in world space //

    Utilities()
    {
        //ctor
    }

    /* STRUCTS */
    struct Light
    {
        /* Defines the position, color, and direction of a light. */
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

    struct Direction
    {
        vec3 dir;
        Direction(vec3 direction) // just to be safe, making the assumption that a struct needs a constructor. I will test this later.
        {
            dir = direction;
        }
    };

    struct Character
    {
        /* This is intended to define a local x, y, and z axis for a character, as well as other attributes specific to characters. */
        vec4 W;
        vec4 U;
        vec4 V;
        float shiny;
        Character(vec4 dirVector)
        {
            W = normalize(dirVector);
            vec4 U = vec4(cross(vec3(0,1,0), W.xyz()), 0);
            vec4 V = vec4(cross(W.xyz(), U.xyz()), 0);
            U = normalize(U);
            V = normalize(V);
            shiny = 50.0;
        }
        void Build(vec4 dir, vec4 pos)
        {
            W = normalize(dir);
            U = normalize(vec4(cross(vec3(0,1,0), W.xyz()), 0)* translation(pos));
            V = normalize(vec4(cross(W.xyz(), U.xyz()), 0)* translation(pos));
        }
    };
    /*END STRUCTS*/

    /*POINTERS TO BE DE-ALLOCATED*/
    vector<Light*> lights;
    vector<Direction*> waterDirections;
    SuperMesh* Mesh;
    /*POINTERS TO BE DE-ALLOCATED*/

    /*HELPER FUNCTIONS*/
    void cap(float& value, float lowerBound, float upperBound)
    {
        /* Takes a value and prevents it from exceeding an upper and lower boundary.
            BE WARNED: always factor in floating point inaccuracy!!! */
        if(value >= upperBound)
            value = upperBound;
        else if (value <= lowerBound)
            value = lowerBound;
    }

    void draw(vector<Program*> allProgs, Camera* cam, SuperMesh* testModel, vec4 Pos, float modelAngle, float yawAngle, vec4& Dir, float& lineWidth)
    {
        /* This handles all of the draw calls, matrix calculations, and LLGL function calls pertinent to rendering something to the screen.
            Uncomment all water-related functions to render the object as water.*/
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

        for (unsigned i = 0; i < allProgs.size(); i++)
        {
            allProgs[i]->use();
            cam->draw(allProgs[i]);
        }

        // UPDATE CALCULATIONS //
        M = translation(vec4(Pos.x,Pos.y,Pos.z,0.0)); // the movement in world space
        mat4 M1 = axisRotation(vec3(0,1,0),modelAngle); // rotation over y-axis
        mat4 M2 = axisRotation(normalize(cam->eye - Pos), yawAngle); // rotation over x-axis
        M = M2 * M1 * M;
        Dir =  vec4(0,0,1,0) * M;
        // END UPDATE CALCULATIONS //

        allProgs[0]->use();
        allProgs[0]->setUniform("worldMatrix",M);

        // DRAW LINES //
        allProgs[1]->use();
        allProgs[1]->setUniform("worldMatrix",M);
        cap(lineWidth, 0.2, 5.0);
        testModel->draw(allProgs[0]);
        //makeWater(allProgs[2], testModel);

        for(unsigned i = 0; i < testModel->m.size(); i++)
            testModel->m[i]->DrawLines(allProgs[1], lineWidth);
        // END DRAW LINES //

        llglSwapBuffers();
    }

    float elapsedTime = 0.0;
    void makeWater(Program* p, SuperMesh* testModel)
    {
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
        p->use();
        p->setUniform("worldMatrix", M); // M is defined globally, as all shaders on a single object should use the same orientation.
        p->setUniform("timePassed", elapsedTime);
        elapsedTime += 0.1;
        for(unsigned i = 0; i < testModel->m.size(); i++)
            testModel->m[i]->DrawWater(p);
        // NOTE: MAIN DRAW SWAPS BUFFERS, DO NOT SWAP AGAIN WHILE MAIN DRAW IS IN USE!!!
    }

    void setScene(Character& MainChar, vec4& Dir, vec4& Pos, vec4& coi)
    {
        /* 'Builds' a character and sets what the camera is initially looking at. */
        MainChar.Build(Dir, Pos);
        coi = Pos;
    }

    void setLights(Program* prog1) // NOTE: ONLY CALL THIS FUNCTION ONCE IN MAIN()!!!!!!!
    {
        /* Sets the attributes for all of the lights in our program, and sends them as a uniform to the shaders. */
        //Light* lights[MAX_LIGHTS];
        lights.push_back(new Light(vec4(-10, 10, 0, 0.0), vec4(255,255,255,1.0), vec4(0, 1, 0, 0.0)));
        lights.push_back(new Light(vec4(0, 10, 10, 0.0), vec4(40,40,40,1.0), vec4(0, 0, 1, 0.0)));
        lights.push_back(new Light(vec4(0, 10, 0, 10.0), vec4(255,255,255,1.0), vec4(-10, 0, 0, 1.45)));
        lights.push_back(new Light(vec4(0, 10, 0, 0.0), vec4(255,255,255,1.0), vec4(0, -1, 0, 0.0)));
        // For the best view of our lighting effects, all lights should be set to natural white.

        prog1->use();
        for(int i = 0; i < MAX_LIGHTS; i++)
        {
            ostringstream oss, oss2, oss3;

            oss << "lights[" << i << "].pos";
            prog1->setUniform(oss.str(), lights[i]->pos);

            oss2 << "lights[" << i << "].col";
            prog1->setUniform(oss2.str(), lights[i]->col);

            oss3 << "lights[" << i << "].dir";
            prog1->setUniform(oss3.str(), lights[i]->dir);
        }
        //AMBIENT COLOR//
        prog1->use();
        prog1->setUniform("ambient", vec4(0.01,0.01,0.01,1.0));
        prog1->setUniform("A0", 0.005);
        prog1->setUniform("A1", 0.005);
        prog1->setUniform("A2", 0.005);
        //END AMBIENT COLOR//
    }

    void setWaterDirections(Program* waterProg) // DON'T WORRY ABOUT THIS FUNCTION, SHADER JUST DEFINES 3 VEC3'S AND USES THOSE.
    {
        waterDirections.push_back(new Direction(vec3(0,0,-1)));
        waterDirections.push_back(new Direction(vec3(.707,0,.707)));
        waterDirections.push_back(new Direction(vec3(-0.928,0,-0.371)));


        waterProg->use();
        for(unsigned i = 0; i < waterDirections.size(); i++)
        {
            ostringstream waterDir;
            waterDir << "waterDirs[" << i << "]";
            waterProg->setUniform(waterDir.str(), waterDirections[i]->dir);
        }
    }

    void handleEvents()
    {
        /* Keeps track of all keyboard and mouse events, and sends the information to the mousedown and keydown maps. */
        while(SDL_PollEvent(&ev))
        {
            if( ev.type == SDL_QUIT ){
                SDL_Quit();
            }
            else if( ev.type == SDL_MOUSEBUTTONDOWN ){
                    mousedown[ev.button.button] = true;
            }
            else if(ev.type == SDL_MOUSEBUTTONUP){
                    mousedown[ev.button.button] = false;
            }
            else if(ev.type == SDL_MOUSEMOTION){
                // TYPES INCLUDE EV.MOTION.X, EV.MOTION.Y, EV.MOTION.XREL, EV.MOTION.YREL
            }
            else if( ev.type == SDL_KEYDOWN){
                keydown[ev.key.keysym.sym] = true;
            }
            else if( ev.type == SDL_KEYUP ){
                keydown[ev.key.keysym.sym] = false;
            }
        }
    }

    bool handleInput(float& modelAngle, float& yawAngle, vec4& Pos)
    {
        handleEvents();
            /* SDL events are:
                Key Events ___ toolbox->keydown['char']
                Mouse Events _ toolbox->mousedown['1, 2, or 3'] 1 is left click, 2 is middle, 3 is right
            */
        if(keydown['a'])
            modelAngle -= .03;
        else if(keydown['d'])
            modelAngle += .03;
        else if(keydown['w'])
            yawAngle += .03;
        else if(keydown['s'])
            yawAngle -= .03;
        else if(keydown['i'])
            Pos  = Pos + vec4(0,0,-0.5,0.0);
        else if(keydown['k'])
            Pos  = Pos + vec4(0,0,0.5,0.0);


        else if(keydown[0x1B] || ev.type == SDL_QUIT) // 0x1B corresponds to the "arrow" unicode character, a.k.a the ESC key.
            return false; // indicates that we are done handling input
        return true;
    }

    bool isFileAlright(string fName)
    {
        ifstream in(fName.c_str());
        if(!in.good())
            return false;
        return true;
    }

    SuperMesh* getCustomMesh(string fName, float tolerance)
    {
        Mesh = new SuperMesh(fName.c_str(), tolerance);
        return Mesh;
    }

    void askForMesh(vector<Program*> allProgs, SuperMesh*& testModel)
    {
        /*
        TODO: Calculate tolerance as a function depending on the camera's distance from the object, increasing line tolerance
        when distance decreases, and vice versa. Using a spherical object as a guide, determine the threshold at which line tolerance
        should stop increasing by finding out at what point a spherical object begins to show the boundaries between individual polygons.
        Also, note the "spider-webbing" effect on the outer parts of a rotating mesh... is this worth attempting to fix?
        */
        char wantCustomMesh;
        float tolerance;
        cout << "Welcome to Don's Shader Test Program! Press A and D to rotate the model,\nW and S to roll the model, and I and K to zoom in/out.\nClick on the red X to exit, or hit escape." << endl;
        cout << "Do you want to use your own mesh? Type y for yes and n for no. " << endl;
        cin >> wantCustomMesh;
        if(wantCustomMesh == 'y' || wantCustomMesh == 'Y')
        {
            string fName;
            cout << "Please type the path to your spec.mesh file. An example of this would be Assets/Models/YourFolder/YourObject.spec.mesh." << endl;
            cin >> fName;
            while(!isFileAlright(fName))
            {
                cout << "Invalid path name, please try again: ";
                cin >> fName;
            }
            cout << "Please type the line tolerance for this mesh on a scale of 0.0 to -1.0.\nThe more negative the tolerance, the fewer lines are drawn." << endl;
            cin >> tolerance;
            while(tolerance > 0.0 && tolerance < -1.0)
            {
                cout << "Invalid tolerance, please enter a float value from 0.0 to -1.0: ";
                cin >> tolerance;
            }
            testModel = getCustomMesh(fName, tolerance);
        }
        else
            testModel = new SuperMesh("Assets/Models/Water/water.spec.mesh", 0.0);
    }

    void prepareLLGL(int winw, int winh)
    {
        llglSetup(winw,winh); // just curious to see if winw and winh, being defined as macros, work here like they do in main, where they are defined

        glEnable(GL_DEPTH_TEST);
        glDepthFunc(GL_LEQUAL);

        glClearColor(1.0,1.0,1.0,1);
    }
    /*END HELPER FUNCTIONS*/

    virtual ~Utilities()
    {
        for(unsigned i = 0; i < lights.size(); i++)
        {
            delete lights[i];
        }
        for(unsigned j = 0; j < waterDirections.size(); j++)
        {
            delete waterDirections[j];
        }
        delete Mesh;
    }
};
