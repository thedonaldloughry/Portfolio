#include "stdafx.h"

#include "application.h"
#include "state.h"
#include "controllerwrpr.h"

namespace ssuge {


	// APPLICATION METHODS
	Application::Application() : mRunning(false), mEngine(nullptr)
	{
	}

	Application::~Application() 
	{
		SDL_Quit();
		if ( mEngine != nullptr ) {
			mEngine->drop();
		}
		while ( !mStateStack.empty() ) {
			delete mStateStack.top();
			mStateStack.pop();
		}
	}

	bool Application::init()
	{
		if ( SDL_Init(SDL_INIT_VIDEO | SDL_INIT_EVENTS | SDL_INIT_GAMECONTROLLER) == -1 ) {
			DEBUGSTR(SDL_GetError());
			return false;
		}

	#ifdef _DEBUG 
		std::string plugins_cfg = "plugins_d.cfg";
	#else
		std::string plugins_cfg = "plugins.cfg";
	#endif

		mRoot.reset(new Ogre::Root(plugins_cfg));
		if ( !mRoot->showConfigDialog() ) {
			// User cancelled.
			DEBUGSTR("User Cancelled");
			return false;
		}

		mWindow = mRoot->initialise(true);
		if ( mWindow == nullptr ) {
			DEBUGSTR("Window could not be initialized.");
			return false;
		}

		mWindow->setDeactivateOnFocusChange(false);
		
		size_t window_handle = 0; // Apparently this works to get the HWND found in an OGRE tutorial.
		mWindow->getCustomAttribute("WINDOW", &window_handle);
		if ( !SDL_CreateWindowFrom( (void*)window_handle ) ) {
			DEBUGSTR(SDL_GetError());
			return false;
		}

		mEngine = irrklang::createIrrKlangDevice();
		if ( mEngine == nullptr ) {
			DEBUGSTR("Audio engine could not be initialized.");
			return false;
		}

		// Set up the resources
		Ogre::ResourceGroupManager::getSingleton().addResourceLocation("../media/3Dplatformer_assets", "FileSystem", "General");
		Ogre::ResourceGroupManager::getSingleton().addResourceLocation("../media/3Dplatformer_assets/room", "FileSystem", "General");
		Ogre::ResourceGroupManager::getSingleton().initialiseAllResourceGroups();

		return true;
	}

	void Application::run()
	{
		if ( !init() ) {
			return;
		}

		mRunning = true;

		//Ogre::Timer game_timer;
		unsigned int previous_time = SDL_GetTicks();
		//unsigned int accum = 0;

		// Background music
		/*
		irrklang::ISound* sound = mEngine->play2D("../media/3Dplatformer_assets/audio/background01.mp3", true);
		if ( sound ) {
			sound->setVolume(0.5f);
		}
		*/
		
		mStateStack.push(new PlayingState());

		mEngine->setListenerPosition(irrklang::vec3df(0, 0, 300), irrklang::vec3df(0, 0, 1));
		
		int accum = 0;
		while (mRunning) {
			unsigned int current_time = SDL_GetTicks();
			unsigned int elapsed = current_time - previous_time;
			previous_time = current_time;
			accum += elapsed;

			if ( accum >= 1000) {
				DEBUGSTR("FPS: " << mWindow->getAverageFPS());
				accum = 0;
			}

			handleEvents();
			update(elapsed/1000.0f);
			mRoot->renderOneFrame();
		}

	}

	void Application::update(float dt)
	{
		mStateStack.top()->update(dt);
		mEngine->update();
		if ( mStateStack.top()->isFinished() ) {
			mStateStack.pop();
		}
	}

	void Application::handleEvents() 
	{
	}

	Ogre::Root* Application::getRoot()
	{
		return mRoot.get();
	}

	Application& Application::getSingleton()
	{
		static Application app;
		return app;
	}

	Ogre::RenderWindow* Application::getWindow()
	{
		return mWindow;
	}

	irrklang::ISoundEngine* Application::getSoundEngine()
	{
		return mEngine;
	}

	void Application::quit()
	{
		mRunning = false;
	}

	void Application::pushState(GameStateTypes gs)
	{
	}

} // ssuge