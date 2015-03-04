#include "llgl.h"
#include "Camera.h"
#include "assert.h"
#include <vector>
#include <stdexcept>
#include <math.h>
#include <iostream>

using namespace std;
using namespace llgl;

Camera::Camera(float screenW, float screenH, float viewAngle, float h, float y)
{
    screenWidth = screenW;
    screenHeight = screenH;
    av = 0.5 * viewAngle;
    hither = h;
    yon = y;
    computeMatrix(); // THIS SETS THE PROJECTION MATRIX
    U = vec4(1,0,0,0);
    V = vec4(0,1,0,0);
    W = vec4(0,0,1,0);
    eye= vec4(0,0,0,1);
}

void Camera::update_view_matrix()
{
    mat4 eyeMat = mat4(1,0,0,0,
                                      0,1,0,0,
                                      0,0,1,0,
                                      -eye.x, -eye.y, -eye.z, 1);
    mat4 axisMat = mat4(U.x, V.x, W.x, 0,
                                       U.y, V.y, W.y, 0,
                                       U.z, V.z, W.z, 0,
                                       0,0,0,1);
    vpmatrix = eyeMat * axisMat * pm;
}

void Camera::Set(vec4 neye, vec4 ncoi) // NEW EYE, NEW CENTER OF INTEREST. *_* --------X
{
    W = normalize(neye - ncoi);
    U = vec4(cross(vec3(0,1,0), W.xyz()), 0);
    V = vec4(cross(W.xyz(), U.xyz()), 0);
    U = normalize(U);
    V = normalize(V);
    eye = neye;
    update_view_matrix();
}

void Camera::walk(float amt)
{
    eye = eye += amt * W;
    update_view_matrix();
}

void Camera::turn(float amt) // DEGREE (IN RADIANS) FOR TURNING.
{
    mat4 M = axisRotation(V.xyz(), amt);
    U = U * M;
    W = W * M;
    update_view_matrix();
}

void Camera:: CircleAround(vec4 rotationVector, vec4 position, float amt)
{
    mat4 R = axisRotation(rotationVector, amt);
    mat4 T = mat4(1,0,0,0,
                                      0,1,0,0,
                                      0,0,1,0,
                                      -position.x, -position.y, -position.z, 1);
    mat4 T2 = mat4(1,0,0,0,
                                      0,1,0,0,
                                      0,0,1,0,
                                      position.x, position.y, position.z, 1);
    V = V * T * R * T2;
    U = U * T * R * T2;
    W = W * T * R * T2;
    eye = eye * T * R * T2;
    update_view_matrix();
}

void Camera::strafe(vec2 amt)
{
    eye = eye + amt.x * U + amt.y * V;
    update_view_matrix();
}

void Camera::computeMatrix()
{
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
    p.setUniform("projMatrix", pm);
    p.setUniform("viewProjMatrix", vpmatrix); // WAS WORLDVIEWPROJMATRIX IN HIS EXAMPLE. LOOK INTO THIS.
    p.setUniform("eyepos", eye);
}
