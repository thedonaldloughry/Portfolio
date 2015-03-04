#include "llgl.h"
#include "assert.h"
#include <vector>
#include <stdexcept>
#include <iostream>

using namespace std;
using namespace llgl;

class Camera
{
    public:
        mat4 pm, vmatrix, vpmatrix;
        float av, hither, yon, screenWidth, screenHeight;
        vec4 U, V, W, eye;

        Camera(float screenW, float screenH, float viewAngle, float h, float y);
        // if Camera ever uses memory allocation, write a destructor to manage possible memory leaks.
        void computeMatrix();
        void update_view_matrix();
        void Set(vec4 neye, vec4 ncoi);
        void walk(float amt);
        void turn(float amt);
        void CircleAround(vec4 rotationVector, vec4 position, float amt);
        void strafe(vec2 amt);
        void draw(Program* p);
};
