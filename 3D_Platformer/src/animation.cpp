#include "stdafx.h"

#include "component.h"
#include "gameobject.h"

namespace ssuge {

	AnimationComponent::AnimationComponent(GameObject* owner) : Component(owner)
	{
		rComponent = dynamic_cast<RenderComponent*>(owner->getComponent(ComponentTypes::RENDERCOMPONENT));
		if(rComponent != nullptr)
		{
			mEntity = rComponent->getEntity();
			mMoving = false;
			mPrevAnimID = ANIM_NONE;
			setupAnimations();
		}
	}

	AnimationComponent::~AnimationComponent()
	{
		delete aStateCurrent;
	}

	const float AnimationComponent::ANIM_FADE_SPEED = 7.5f;

	void AnimationComponent::update(float dt)
	{
		/* 
		TODO OVER BREAK:
		Update needs to handle specific animation cases, such as holding your sword arm up
		during the "block" animation and smoothing out the end of the walk cycle.
		Aside from that, the basic component is ready for implementation.
		*/
		Ogre::Real animationSpeed = 1;
		mTimer += dt; // timer for general use

		if(mPrevAnimID == ANIM_JUMP && mTimer >= animList[mPrevAnimID].anim->getLength())
		{
			//you have landed.
			if(mTimer >= animList[mPrevAnimID].anim->getLength())
			{
				if(mMoving)
				{
					setAnimation(ANIM_WALK, true);
				}
				else
				{
					setAnimation(ANIM_IDLE1, true);
				}
				mTimer = 0; //reset moving timer
			}
		}
		if(mPrevAnimID != ANIM_NONE)
			animList[mPrevAnimID].anim->addTime(dt * animationSpeed);
		if(animList[mPrevAnimID].anim->getTimePosition() >= (animList[mPrevAnimID].anim->getLength() - 0.01F))
		{
			/* We have reached the end of the previous animation. */
			if(mPrevAnimID == ANIM_WALK && mMoving)
			{
				setAnimation(ANIM_WALK, false);
			}
			else
			{
				animList[mPrevAnimID].isActive = false;
				setAnimation(ANIM_IDLE1, false);
			}
		}
			
		fadeAnimations(dt);
	}

	void AnimationComponent::setupAnimations()
	{
		mEntity->getSkeleton()->setBlendMode(Ogre::SkeletonAnimationBlendMode::ANIMBLEND_CUMULATIVE);
		// More with bone-based animation blending??? //
		mPrevAnimID = ANIM_IDLE1;
		mTimer = 0;
		const Ogre::String animNames[] = 
		{
			"Attack1",
			"Attack2",
			"Attack3",
			"Backflip",
			"Block",
			"Climb",
			"Crouch",
			"Death1",
			"Death2",
			"HighJump",
			"Idle1",
			"Idle2",
			"Idle3",
			"Jump",
			"JumpNoHeight",
			"Kick",
			"SideKick",
			"Spin",
			"Stealth",
			"Walk"
		};

		for(int i = 0; i < NUMBER_ANIMS; i++)
		{
			Animation animation;
			animation.anim = mEntity->getAnimationState(animNames[i]);
			animation.anim->setLoop(true);
			animation.isFadingIn = false;
			animation.isFadingOut = false;
			animList.push_back(animation);
			/*We can now do animList[id] to get animations!*/
		}
		setAnimation(ANIM_IDLE1, false); // true sets time pos to 0
		animList[ANIM_IDLE1].anim->setEnabled(true);
	}

	void AnimationComponent::setAnimation(AnimationID id, bool reset)
	{
		if(mPrevAnimID != id && (animList[mPrevAnimID].isActive == false || mPrevAnimID == ANIM_IDLE1)) // we don't want to activate an animation while another is active...
		{
			DEBUGVAR(mPrevAnimID);
			if(mPrevAnimID >= 0 && mPrevAnimID < NUMBER_ANIMS && id != ANIM_NONE)
			{
				//fade out any old animations
				animList[mPrevAnimID].isFadingIn = false;
				animList[mPrevAnimID].isFadingOut = true;

				//if animation, enable and fade in!
				animList[id].anim->setEnabled(true);
				animList[id].anim->setWeight(0);
				animList[id].isFadingOut = false;
				animList[id].isFadingIn = true;
				animList[id].isActive = true;

				
				mPrevAnimID = id;

				if(reset)
					animList[id].anim->setTimePosition(0);
			}
		}
		
	}

	void AnimationComponent::fadeAnimations(float dt)
	{
		for(unsigned int i = 0; i < animList.size(); i++)
		{
			if(animList[i].isFadingIn == true)
			{
				//do fade in
				Ogre::Real newWeight = animList[i].anim->getWeight() + (dt * ANIM_FADE_SPEED);
				animList[i].anim->setWeight(Ogre::Math::Clamp<Ogre::Real>(newWeight, 0, 1));

				if(newWeight >= 1)
					animList[i].isFadingIn = false;
			}
			else if(animList[i].isFadingOut == true)
			{
				//do fade out
				Ogre::Real newWeight = animList[i].anim->getWeight() - (dt * ANIM_FADE_SPEED);
				animList[i].anim->setWeight(Ogre::Math::Clamp<Ogre::Real>(newWeight, 0, 1));

				if(newWeight <= 0)
					animList[i].isFadingOut = false;
			}
		}
	}

	void AnimationComponent::setIsMoving(bool isMoving)
	{
		/*
			Note: it will be important that we implement this in our physics code!
			The check will be: if you're moving OR you've hit the ground while moving
			in any horizontal direction, do setIsMoving(true). Else, do setIsMoving(false).
		*/
		mMoving = isMoving;
	}

	void AnimationComponent::handleEvents(const GameObjectEvent& e, float dt)
	{
		setAnimation((AnimationID)e.animID, e.reset);
	}

	ComponentTypes AnimationComponent::getType()
	{
		const ComponentTypes type = ComponentTypes::ANIMATIONCOMPONENT;
		return type;
	}
}