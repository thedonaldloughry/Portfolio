#include "stdafx.h"

#include "component.h"
#include "application.h"

namespace ssuge {

	InputComponent::InputComponent(GameObject* owner) : Component(owner), mCaptured(false), mJoystick(nullptr)
	{
		
	}

	InputComponent::~InputComponent()
	{
		if ( mJoystick != nullptr ) {
			// This (probably) won't error out
			SDL_JoystickClose(mJoystick);
		}
	}

	void InputComponent::handleEvents(const GameObjectEvent& e, float dt)
	{
		/*handle gameObject events, which come into play when components need to tell things to each other.*/
	}

	void InputComponent::update(float dt)
	{
		aComponent = dynamic_cast<AnimationComponent*>(this->mOwner->getComponent(ComponentTypes::ANIMATIONCOMPONENT));
		SDL_Event ev;
		state = SDL_GetKeyboardState(nullptr);
		if ( SDL_PollEvent(&ev) ) { //poll events for the game controller
			switch ( ev.type ) {
			case SDL_JOYDEVICEADDED:
				onControllerAdded();
			case SDL_JOYDEVICEREMOVED:
				onControllerRemoved();
				break;
			case SDL_QUIT:
				Application::getSingleton().quit();
				break;
				/*
			case SDL_CONTROLLERBUTTONDOWN:
				break;
			case SDL_CONTROLLERBUTTONUP:
				break;
			case SDL_CONTROLLERAXISMOTION:
				break;
				*/
			case SDL_KEYDOWN:
				if ( state[SDL_SCANCODE_Q] ) {
					Application::getSingleton().pushState(GameStateTypes::GS_PAUSED);
				}
				if ( state[SDL_SCANCODE_P] ) {
					if ( !ev.key.repeat ) {
						DEBUGSTR("JUMP");
						std::vector<std::string> tmp;
						tmp.push_back("../media/3dplatformer_assets/audio/jump.wav");
						mOwner->pushEvent(ComponentTypes::SOUNDCOMPONENT, tmp);
					}
				}
				if ( state[SDL_SCANCODE_O] ) {
					if ( !ev.key.repeat ) {
						DEBUGSTR("JUMP2");
						std::vector<std::string> tmp;
						tmp.push_back("../media/3dplatformer_assets/audio/jump2.wav");
						mOwner->pushEvent(ComponentTypes::SOUNDCOMPONENT, tmp);
						//mOwner->getComponent(ComponentTypes::PHYSICSCOMPONENT)->... we could test applying a single upward force?
					}
				}
				break;
			default:
				break;
			}
		}

		handleKeyboard();
	}

	ComponentTypes InputComponent::getType()
	{
		const ComponentTypes type = ComponentTypes::INPUTCOMPONENT;
		return type;
	};

	void InputComponent::onControllerAdded()
	{
		if ( mJoystick == nullptr ) {
			for ( int i = 0; i < SDL_NumJoysticks(); i++ ) {
				mJoystick = SDL_JoystickOpen(i);
				if ( mJoystick != nullptr ) {
					return;
				}
			}
		}
	}

	void InputComponent::onControllerRemoved()
	{
		if ( !SDL_JoystickGetAttached(mJoystick) ) {
			SDL_JoystickClose(mJoystick);
		}
	}

	void InputComponent::handleKeyboard()
	{
		if(state[SDL_SCANCODE_SPACE])
		{
			mOwner->pushAnimationEvent(AnimationComponent::ANIM_ATTACK1, true);
		}
		if(state[SDL_SCANCODE_F])
		{
			mOwner->pushAnimationEvent(AnimationComponent::ANIM_BLOCK, true);
		}
		if(state[SDL_SCANCODE_W])
		{
			mOwner->pushAnimationEvent(AnimationComponent::ANIM_WALK, true);
		}
		if(!state[SDL_SCANCODE_W] && !state[SDL_SCANCODE_A] && !state[SDL_SCANCODE_S] && !state[SDL_SCANCODE_D])
		{
			if(aComponent != nullptr)
				aComponent->setIsMoving(false);
		}
		else
		{
			if(aComponent != nullptr)
				aComponent->setIsMoving(true);
		}
	}

}