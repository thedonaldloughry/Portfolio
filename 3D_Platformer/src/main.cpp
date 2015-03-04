#include "stdafx.h"

#ifdef main
#undef main
#endif

#include "application.h"

#if defined _WIN32 && !(_DEBUG)
#define WIN32_LEAN_AND_MEAN
#include <Windows.h>
int CALLBACK WinMain(_In_  HINSTANCE hInstance,
					  _In_  HINSTANCE hPrevInstance,
					  _In_  LPSTR lpCmdLine,
					  _In_  int nCmdShow)
#else
int main()
#endif
{
	try {
		//ssuge::Application::getSingleton().run(); //uncomment to run main application
		ssuge::Application::getSingleton().run();
	} catch ( Ogre::Exception &e ) {
		DEBUGSTR(e.getDescription());
	}
	return 0;
}