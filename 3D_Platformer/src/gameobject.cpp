#include "stdafx.h"

#include "gameobject.h"

namespace ssuge {

	GameObjectEvent::GameObjectEvent()
	{
	}

	GameObjectEvent::GameObjectEvent(const GameObjectEvent& other)
	{
			args = other.args;
			animID = other.animID;
			reset = other.reset;
			EVENT_TYPE = other.EVENT_TYPE;
	};

	GameObject::GameObject()
	{
	}

	GameObject::~GameObject()
	{
		for ( auto comp : mComponents ) {
			delete comp;
			comp = nullptr;
		}
	}

	void GameObject::update(float dt)
	{
		for ( auto comp : mComponents ) {
			comp->update(dt);
		}

		// Send events to components
		GameObjectEvent ev;
		if ( !mEvents.empty() ) {
			ev = mEvents.front();
			auto comp = getComponent(ev.EVENT_TYPE);
			if ( comp != nullptr ) {
				comp->handleEvents(ev, dt);
			}
			mEvents.pop();
		}
	}

	void GameObject::addComponent(Component* comp)
	{

		mComponents.push_back(comp);
	}

	void GameObject::setPosition(Ogre::Vector3 pos)
	{
		mPos = pos;
	}

	void GameObject::setPosition(float x, float y, float z)
	{
		mPos = Ogre::Vector3(x, y, z);
	}

	Ogre::Vector3 GameObject::getPosition()
	{
		return mPos;
	}

	Component* GameObject::getComponent(ComponentTypes type)//passed as ComponentTypes::WHATEVER
	{
		for ( auto i : mComponents ) {
			if ( type == i->getType() ) {
				return i;
			}
		}
		// Maybe should return a component that does nothing?
		// Default return
		return nullptr;
	}

	void GameObject::pushEvent(ComponentTypes event_type, std::vector<std::string> args)
	{
		GameObjectEvent ev;
		ev.args = args;
		ev.EVENT_TYPE = event_type;
		mEvents.push(ev);
	}

	void GameObject::pushAnimationEvent(int id, bool reset)
	{
		GameObjectEvent ev;
		ev.EVENT_TYPE = ComponentTypes::ANIMATIONCOMPONENT;
		ev.animID = id;
		ev.reset = reset;
		mEvents.push(ev);
	}

}