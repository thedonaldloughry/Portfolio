#pragma once

#include "stdafx.h"

#include "component.h"

#include <vector>

namespace ssuge {

	/*
	Base System class, (may) handle updating of components in the future
	For example, InputSystem would update all InputComponents

	This allows us to update in "lock-step", so that certain things are always updated before others.
	An example "update loop":

	InputSystem->update(dt);
	PhysicsSystem->update(dt);
	RenderSystem->update(dt);
	*/
	class System
	{
	public:
		System();
		virtual ~System();

		virtual void registerComponent(Component* comp) final;
		virtual void detachComponent(Component* comp) final;

		virtual void update(float dt) = 0; // Purely virtual function

	protected:
		std::vector<Component*> mComponents;
	};


	// Input System
	class InputSystem : public System
	{
	public:
		InputSystem();
		virtual ~InputSystem();

		virtual void update(float dt) override;
	protected:
	};

	// Physics system
	class PhysicsSystem : public System
	{
	public:
		PhysicsSystem();
		virtual ~PhysicsSystem();

		virtual void update(float dt) override;
	protected:
	};

}