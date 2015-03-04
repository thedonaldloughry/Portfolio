#include "llgl.h"
#include <vector>
#include <stdexcept>
#include <iostream>

// NOT BEING USED IN THIS LAB, BUT USEFUL AS A REFERENCE FOR MESH MOVEMENT.
// INCLUDED WITH THE LAB SUBMISSION SO THAT YOU MIGHT SEE WHERE "MOVINGOBJECT"
// WAS DERIVED FROM.

using namespace std;
using namespace llgl;

class circle
{
    public:

    unsigned vb;
    unsigned eb;
    vec4 pos;
    vec4 vel;
    float radius = 0.15;
    float pct;
    bool is_initialized;


    circle(vec4 position, vec4 velocity)
    {
        pos = position; vel = velocity;
        is_initialized = false;
    }

    void init()
    {
        float vdata[] =
            {
                 1.0, 1.0,
                 1.0,-1.0,
                -1.0, 1.0,
                -1.0,-1.0,
            };

        uint16_t idata[] = {0,2,1,3,2,1};
        glGenBuffers(1,&vb);
        glBindBuffer(GL_ARRAY_BUFFER,vb);
        glBufferData(GL_ARRAY_BUFFER,sizeof(vdata),vdata,GL_STATIC_DRAW);

        glGenBuffers(1,&eb);
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER,eb);
        glBufferData(GL_ELEMENT_ARRAY_BUFFER,sizeof(idata),idata,GL_STATIC_DRAW);

        is_initialized = true;
    }

    void draw(Program& p, Texture2D& text1, Texture2D& text2)
    {
        if (!is_initialized)
        {
            init();
        }
        glBindBuffer(GL_ARRAY_BUFFER,vb);
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER,eb);
        p.use();
        p.setVertexFormat("position",2,GL_FLOAT);
        p.setUniform("scale", radius);
        p.setUniform("translate", pos);
        p.setUniform("tex1", text1);
        p.setUniform("tex2", text2);
        glDrawElements(GL_TRIANGLES,6,GL_UNSIGNED_SHORT,0);
    }

    void update(vector<circle*>& e, int& elapsed, Program& prog, Texture2D& text1, Texture2D& text2)
    {
        this->pct -= 0.01;
        if (this-> pct <= 0.0)
            this->pct = 0.0;

        this->pos = this->pos + (elapsed * this->vel);

        if(this->pos.x > 1.0 - radius) // LEFT AND RIGHT WALLS
        {
            this->vel.x *= -1.0;
            this-> pos.x = 1.0 - radius;
        }

         if(this->pos.x < -1.0 + radius)
         {
            this->vel.x *= -1.0;
            this-> pos.x = -1.0 + radius;
         }

        if(this->pos.y > 1.0 - radius) // TOP AND BOTTOM WALLS
        {
            this->vel.y *= -1.0;
            this-> pos.y = 1.0 - radius;
        }


        if(this->pos.y < -1.0 + radius)
        {
            this->vel.y *= -1.0;
             this-> pos.y = -1.0 + radius;
        }


        //HIT DETECTION
        for (unsigned j = 0; j < e.size(); j++)
        {
            if (this != e[j])
            {
                float dis = length(e[j]->pos - this->pos);

                if (dis < 0.30)
                {
                    this->pct = 1.0;

                    vec4 d = (this->pos - e[j]->pos);
                    d = normalize(d);

                    this->vel = length(this->vel) * d;
                }
            }
        }
        prog.use();
        prog.setUniform("translate", this->pos);
        prog.setUniform("pct", this->pct);
        this->draw(prog, text1, text2);
    }
};
