#pragma once

#include "llgl.h"
#include "assert.h"
#include <vector>
#include <stdexcept>
#include <iostream>

#define winw 512
#define winh 512

using namespace std;
using namespace llgl;


class Camera
{
    public:
        mat4 pm, vmatrix, vpmatrix;
         float av, hither, yon, screenWidth = winw, screenHeight = winh;
        vec4 U, V, W, eye, up;

        Camera(float viewAngle, float h, float y);
        void computeMatrix();
        void update_view_matrix();
        void holdPos(Camera* cam);
        void resetPos(Camera* cam);
        void Set(vec4 neye, vec4 ncoi);
        void walk(float amt);
        void turn(float amt);
        void CircleAround(vec4 rotationVector, vec4 position, float amt);
        void strafe(vec2 amt);
        void draw(Program& p);
};

