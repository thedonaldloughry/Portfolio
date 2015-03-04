#include "stdafx.h"

#include "system.h"

namespace ssuge {

	System::System()
	{
	}

	System::~System()
	{
	}

	void System::registerComponent(Component* comp)
	{
		mComponents.push_back(comp);
	}

	void System::detachComponent(Component* comp)
	{

	}


	InputSystem::InputSystem()
	{
	}

	InputSystem::~InputSystem()
	{
		for ( auto comp : mComponents ) {
			detachComponent(comp);
		}
	}

	void InputSystem::update(float dt)
	{
		for ( auto comp : mComponents ) {
			comp->update(dt);
		}
	}
}