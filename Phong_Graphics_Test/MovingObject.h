#include "llgl.h"
#include <vector>
#include <stdexcept>
#include <iostream>

class MovingObject
{
    public:
        Mesh m = Mesh("octagon_Plane.binary.mesh");
        vec4 pos;
        vec4 vel;
        vec4 glow;
        float radius = 0.15;
        float pct;
        MovingObject(vec4 position, vec4 velocity, vec4 glowColor)
        {
            pos = position; vel = velocity; glow = glowColor;
            m.Load();
        }
        void draw(Program& p)
        {
            p.use();
            p.setUniform("translate", pos);
            p.setUniform("scale", radius);
            p.setUniform("glow", glow);
            m.Draw(p);
        }
        void update(vector<MovingObject*>& e, int& elapsed, Program& prog)
        {
            this->pct -= 0.05;
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

                    if (dis < radius*2)
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
            this->draw(prog);
        }
};
