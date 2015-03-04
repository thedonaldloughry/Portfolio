#pragma once

#include "stdafx.h"

#include "component.h"

#include <vector>
#include <queue>

namespace ssuge {

	class Component;
	enum class ComponentTypes;

	// Struct for Game Object events, push it onto the event stack
	struct GameObjectEvent
	{
		GameObjectEvent();

		// Copy constructor
		GameObjectEvent(const GameObjectEvent& other);

		std::vector<std::string> args;

		//ANIMATION ATTRIBUTES//
		int animID;
		bool reset;
		//END ANIMATION ATTRIBUTES//

		ComponentTypes EVENT_TYPE;
	};

	/*
	Base Game Object, basically a container of components which represent something in the game (player, enemies, platforms, etc.)
	*/
	class GameObject
	{
	public:
		GameObject();
		virtual ~GameObject();

		void update(float dt);

		// Adds a component to this GameObject
		virtual void addComponent(Component* comp) final;

		void setPosition(Ogre::Vector3 pos);
		void setPosition(float x, float y, float z);

		Ogre::Vector3 getPosition();

		Component* getComponent(ComponentTypes type);
		void pushEvent(ComponentTypes event_type, std::vector<std::string> args);
		void pushAnimationEvent(int id, bool reset);
		
	protected:
		std::queue<GameObjectEvent> mEvents;
		std::vector< Component* > mComponents;
		Ogre::Vector3 mPos;
	};

}