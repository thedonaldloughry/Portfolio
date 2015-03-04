#ifndef LIGHTS_H_INCLUDED
#define LIGHTS_H_INCLUDED
#define MAX_LIGHTS 4

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

class lighting
{
public:


    void setup(Light* lights,Program &p)
    {
        // SETTING LIGHTS //////////////////////////////////////////////////
        lights[0] = new Light(vec4(-200, 10, 0, 0.0), vec4(255,25,255,1.0), vec4(0, 1, 0, 0.0));
        lights[1] = new Light(vec4(0, 10, 200, 0.0), vec4(0,255,255,1.0), vec4(0, 0, 1, 0.0));
        lights[2] = new Light(vec4(0, 10, 0, 10.0), vec4(0,255,20,1.0), vec4(-10, 0, 0, 1.45));
        lights[3] = new Light(vec4(0, 200, 0, 0.0), vec4(255,255,255,1.0), vec4(0, -1, 0, 0.0));

        for(int i = 0; i < MAX_LIGHTS; i++)
        {
            ostringstream oss, oss2, oss3;

            oss << "lights[" << i << "].pos";
            p.setUniform(oss.str(), lights[i]->pos);

            oss2 << "lights[" << i << "].col";
            p.setUniform(oss2.str(), lights[i]->col);

            oss3 << "lights[" << i << "].dir";
            p.setUniform(oss3.str(), lights[i]->dir);
        }
        /////////////////////////////////////////////////////////////////////////
    }

    void update(Program &p)
    {
        p.use();
        p.setUniform("ambient", vec4(0.01,0.01,0.01,1.0));
        p.setUniform("A0", 0.005);
        p.setUniform("A1", 0.005);
        p.setUniform("A2", 0.005);
        p.setUniform("fogColor", vec4(0.0, 0.0, 0.5, 1.0));
    }

};

#endif // LIGHTS_H_INCLUDED
