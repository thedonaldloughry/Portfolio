#include "llgl.h"
#include "Camera.h"
#include "assert.h"
#include <vector>
#include <stdexcept>
#include <math.h>
#include <iostream>

using namespace std;
using namespace llgl;


Camera::Camera(float viewAngle, float h, float y)
{
    /*
        For the constructor, we have these variables:
        screenWidth/screenHeight --> Pretty self-explanatory, just the screen's width and height.
        av --> A value that is meant to represent half of the user's total view angle, to make later calculations marginally simpler.
        hither --> How close something can get to the camera and still be visible.
        yon --> How far something can get to the camera and still be visible.
        computeMatrix() --> This uses the above information about the screen's dimensions and the view angle to create a projection matrix, which is the first
                                    step towards having the matrices necessary to create 3D objects on-screen.
        U, V, W, and eye --> Here's a slightly tricky one. The vectors that make the x, y, and z axis of the camera, along with an added component that
                                     serves as a reference to the eye's current position, can be made into a matrix, which begins as the
                                     identitiy matrix and then changes relative to the direction that the main character is facing. These vectors are used and updated
                                     in the function update_view_matrix(), and then referenced by many other functions throughout the program.
    */
    //screenWidth = screenW;
    //screenHeight = screenH;
    av = 0.5 * viewAngle;
    hither = h;
    yon = y;
    up = vec4(0,1,0,0);
    U = vec4(1,0,0,0);
    V = vec4(0,1,0,0);
    W = vec4(0,0,1,0);
    eye = vec4(0,0,0,1);
    computeMatrix(); // THIS SETS THE PROJECTION MATRIX
    update_view_matrix();
}

void Camera::update_view_matrix()
{
    /*
        In this function, we begin to see where that strange "eye" vector comes in handy. We form two matrices, one translation matrix (which is an identity
        matrix where the last row defines x, y, and z movement) and one matrix that represents our three axis. Multiplying the translation, axis values, and
        projection matrix (created in computeMatrix() using our screen and view angle values) in that order allows us to produce an updated View Projection
        Matrix, which is used in calculations to create objects in 3D space.

    mat4 eyeMat = mat4(1,0,0,0,
                       0,1,0,0,
                       0,0,1,0,
                       -eye.x, -eye.y, -eye.z, 1);

    mat4 axisMat = mat4(U.x, V.x, W.x, 0,
                        U.y, V.y, W.y, 0,
                        U.z, V.z, W.z, 0,
                        0,0,0,1);
    vpmatrix = eyeMat * axisMat * pm;*/


    // vpmatrix = vmatrix * pm;

    vmatrix = mat4(U.x, V.x, W.x, 0,
                   U.y, V.y, W.y, 0,
                   U.z, V.z, W.z, 0,
                   -dot(U,eye),-dot(V,eye),-dot(W,eye),1);

}

void Camera::resetPos(Camera* cam)
{

    U = cam->U;
    V = cam->V;
    W = cam->W;
    eye = cam->eye;
}

void Camera::holdPos(Camera* cam)
{
    cam->U = U;
    cam->V = V;
    cam->W = W;
    cam->eye = eye;
    update_view_matrix();
}

void Camera::Set(vec4 neye, vec4 ncoi) // NEW EYE, NEW CENTER OF INTEREST. *_* --------X
{
    /*
        This function sets what all of our values are as they are updated in the main program, using the ever-changing eye and center of interest.
    */
    eye = neye;
    W = normalize(eye - ncoi);
    U = normalize(vec4(cross(up.xyz(),W.xyz()),0));
    V = normalize(vec4(cross(W.xyz(), U.xyz()), 0));
    //U = vec4(cross(vec3(0,1,0), W.xyz()), 0);
    //V = vec4(cross(W.xyz(), U.xyz()), 0);
    // U = normalize(U);
    // V = normalize(V);


    update_view_matrix();
}

void Camera::walk(float amt)
{
    /*
        This would really only be useful for something like a first-person game. This essentially forces the camera to move forward. As our current game moves
        the camera almost as if it were being tugged by a rope by the main character, rather than moving of its own accord, this function will not see any use.
        However, used in tandem with turn(), you could create a simple first-person shooter.
    */
    eye = eye += amt * W;
    update_view_matrix();
}

void Camera::turn(float amt) // DEGREE (IN RADIANS) FOR TURNING.
{
    /*
        Referenced above, this turns the camera. Better for first-person simulations.
    */
    mat4 M = axisRotation(V.xyz(), amt);
    U = U * M;
    W = W * M;
    update_view_matrix();
}

void Camera:: CircleAround(vec4 rotationVector, vec4 position, float amt)
{
    /*
        This function was written using old 3D platformers as a reference. It takes an axis of rotation (most likely the "up" vector), the position of the thing
        that you're circling around, and a float value for how much you want to circle (it should be a value in RADIANS). It then takes the position that it's
        cirlcling around, moves it to the origin, circles around the point, and translates back to the original position. Every axis of the camera undergoes this
        movement, as does the eye vector. The view matrix is then updated.

    */

    /*mat4 T = mat4(1,0,0,0,
                                      0,1,0,0,
                                      0,0,1,0,
                                      -position.x, -position.y, -position.z, 1);
    /*mat4 T2 = mat4(1,0,0,0,
                                      0,1,0,0,
                                      0,0,1,0,
                                      position.x, position.y, position.z, 1);*/
    mat4 T = translation(vec4(-position.x, -position.y, -position.z, 0));
    mat4 R = axisRotation(rotationVector, amt);
    mat4 T2 = translation(vec4(position.x, position.y, position.z, 0));
    U = U * T * R * T2;
    W = W * T * R * T2;
    V = V * T * R * T2;
    eye = eye * T * R * T2;
    update_view_matrix();



}

void Camera::strafe(vec2 amt)
{
    /*
        Again, more useful for a first-person game. Moves the camera in a sideways manner. I wouldn't worry about this one.
    */
    eye = eye + amt.x * U + amt.y * V;
    update_view_matrix();
}



void Camera::computeMatrix()
{
    /*
        Uses information about the screen and the view angle to create a projection matrix.
    */
    float ah = (screenWidth / screenHeight) * av;
    float L = -hither * tan(ah * ( M_PI / 180));
    float T = hither * tan(av * ( M_PI / 180));
    float R = hither * tan(ah * ( M_PI / 180));
    float B = -hither * tan(av * ( M_PI / 180));

    pm = mat4((2*hither) / (R - L), 0, 0, 0,
              0, (2*hither) / (T - B), 0, 0,
              1 + ((2*L)/(R-L)), 1 + ((2*B)/(T-B)), (hither + yon) / (hither - yon), -1,
              0, 0, (2 * hither * yon) / (hither - yon), 0); // MATRICES TAKE ROW*COLUMN FLOATS!!!
}

void Camera::draw(Program& p)
{
    /*
        Sets the needed camera uniforms.
    */
    p.use();
    p.setUniform("projMatrix", pm);
    p.setUniform("vMatrix",vmatrix);
    // p.setUniform("viewProjMatrix", vpmatrix); // WAS WORLDVIEWPROJMATRIX IN HIS EXAMPLE. LOOK INTO THIS.
    p.setUniform("eyepos", eye);
}
