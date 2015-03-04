
#include "AI_Main.h"
#include "time.h"
#include "AI_Mine.h"
#include <vector>
 static SuperMesh * shipMesh = new SuperMesh("Assets/models/player/ship/ship.spec.mesh");
 class AI_Enship : public AI_Main
 {
public:
     SuperMesh * mMesh;
     int moveRand = -1;
     vector<AI_Mine*> shipMines;
     int mineDelay = 0;
     int numMines = 0;
     AI_Enship(vec4 pos,SuperMesh * mesh)
    {
        this->mPos = pos;
        mMesh = mesh; // Alternative way to make a ship with any mesh wanted.
        mMesh->load();
        srand(time(NULL));
        chooseRand();

    }
    AI_Enship(vec4 pos)
    {
        this->mPos = pos;
        mMesh = shipMesh; // default enemy ship static mesh loaded.
        mMesh->load();
        srand(time(NULL));
        chooseRand();
    }

    void chooseRand()
    {
        moveRand = rand()%3 + 1; //chooses which way it will randomly move..
    }


    void update(int elapsed)
    {
        AI_Main::update(elapsed); // put ship specific things here..
        move_random(elapsed);
        dropMines(elapsed);

        for(int i = 0; i < shipMines.size();i++)
        {
            shipMines[i]->update(elapsed);
        }
    }
    void move_random(int elapsed)
    {
        if(moveRand == 1)
            rotMesh('y',0.0,elapsed);
        else if(moveRand == 2)
            rotMesh('y',1.0,elapsed);
        else
            rotMesh('y',-1.0,elapsed);
    }

    void draw(Program& p, Program& edgeProg)
    {
        AI_Main::draw(p,edgeProg,mMesh);
        for(int i = 0; i < shipMines.size();i++)
        {
            shipMines[i]->draw(p, edgeProg);
        }
    }
    void dropMines(int elapsed)
    {
        mineDelay += elapsed;
        if(numMines < 10)
        {
            if(mineDelay > 5000)
            {
                chooseRand();
                if(rand() % 4 == 2)
                {
                    shipMines.push_back(new AI_Mine(mPos));
                    numMines++;
                }
                mineDelay = 0;
            }
        }
    }


 };
