#include "llgl.h"
#include <vector>
#include <stdexcept>
#include <iostream>
#include "Cannonball.h"

Cannonball::Cannonball(vec4 position, vec4 velocity)
{
    pos = position;
    vel = velocity;
}

void Cannonball::draw(Program& p)
{
        p.setUniform("translate", pos);
		m.Draw(p);
}

void Cannonball::update(int elapsed)
{
        pos = pos + elapsed*vel;
		vel = vel + elapsed*vec4(0, -0.0001, 0.0, 0);
		lifeLeft -= elapsed;
}
