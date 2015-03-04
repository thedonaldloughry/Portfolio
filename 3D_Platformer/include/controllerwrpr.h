#pragma once
#include "stdafx.h"

namespace ssuge { 

	class ControllerWrpr { 

	public:
		ControllerWrpr();
		SDL_GameController *controller;
		void OnButtonDown(SDL_Event evt);
		void OnButtonUp(SDL_Event evt);
		void OnAxisMotion(SDL_Event evt);
		
	};

}


/*
SOURCES:
[1] "Game Controller API In SDL 2.0" Ryan C. Scott http://blog.5pmcasual.com/game-controller-api-in-sdl2.html ret 10/6/2014
*/