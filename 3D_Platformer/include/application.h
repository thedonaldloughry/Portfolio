#pragma once

#include "stdafx.h"

#include "gameworld.h"
#include "controllerwrpr.h"
#include "state.h"

#include <memory>
#include <irrklang.h>
#include <stack>

namespace ssuge {

	class GameWorld;

	/*
	Base Application Class
	Responsible for initialization of all sub systems and running the game
	*/
	class Application
	{
	public:
		// Start the infinite game loop
		virtual void run();

		Ogre::Root* getRoot();
		Ogre::RenderWindow* getWindow();
		irrklang::ISoundEngine* getSoundEngine();

		// This is a Singleton, only one exists at all times
		static Application& getSingleton();
		virtual void pushState(GameStateTypes gs);

		void quit();
	protected:
		Application();
		virtual ~Application();

		bool mRunning;
		std::shared_ptr<Ogre::Root> mRoot;
		std::shared_ptr<GameWorld> mWorld;
		Ogre::RenderWindow* mWindow;
		irrklang::ISoundEngine* mEngine;
		std::stack<GameState*> mStateStack;
		
		virtual bool init();
		virtual void update(float dt=0.0f);
		virtual void handleEvents();
	};

}