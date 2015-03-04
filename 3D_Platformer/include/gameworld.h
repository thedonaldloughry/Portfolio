#pragma once

#include "stdafx.h"
#include "gameobject.h"
#include "camera.h"
#include "component.h"
#include "physics.h"

#include "tinyxml2.h"

namespace ssuge {
	
	class GameObject;
	class Component;
	class Camera;
	class Physics;

	/*
	GameWorld, parses an XML file (given through the constructor), and builds the world accordingly
	*/
	class GameWorld
	{
	public:
		GameWorld(std::string world_filename);
		virtual ~GameWorld();

		virtual void update(float dt);

		// Returns this world's Ogre Scene Manager
		Ogre::SceneManager* getManager();
		virtual void addObject(GameObject* object);

	protected:
		// Starts parsing the XML file and delegates to buildWorld once the root_node is reached
		virtual void init();
		virtual void buildWorld(tinyxml2::XMLElement* parent, Ogre::SceneNode* parent_node);

		std::string mFile;
		bool mLoaded;
		Ogre::SceneManager* mSceneManager;
		Camera* mCam; // World's camera
		std::vector< GameObject* > mObjects;
		Physics* mPhysEng;
		//Physics mPhysicsWorld;
	};

}
