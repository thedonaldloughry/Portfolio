#pragma once

#include "stdafx.h"
#include "gameobject.h"
#include "physics.h"
#include <vector>
#include <irrKlang.h>
#include <bullet\btBulletCollisionCommon.h>


namespace ssuge {

	// Pre-declaration to resolve circular dependencies
	class GameObject;
	struct GameObjectEvent;

	enum class ComponentTypes
	{
		NULLCOMPONENT, // For placeholding/error purposes
		RENDERCOMPONENT,
		PHYSICSCOMPONENT,
		INPUTCOMPONENT,
		SOUNDCOMPONENT,
		ANIMATIONCOMPONENT,
		CAMERACOMPONENT,
	};

	/*
	Base Component class, all other components inherit from this
	DO NOT USE, update method is non callable (purely virtual)
	*/
	class Component
	{
	public:
		Component(GameObject* owner);
		virtual ~Component() = 0;

		virtual void update(float dt) = 0; // Purely virtual function
		virtual void handleEvents(const GameObjectEvent& e, float dt) = 0;
		virtual ComponentTypes getType() = 0;
	protected:
		GameObject* mOwner;
	};

	/*
	RenderComponent, responsible for all Ogre based rendering on a game object.
	*/
	class RenderComponent : public Component
	{
	public:
		// TODO REFACTOR THIS, IT'S TERRIBLE
		RenderComponent(GameObject* owner, std::string name, std::string mesh_fname, Ogre::SceneManager* manager, Ogre::SceneNode* parent);
		virtual ~RenderComponent();

		virtual void update(float dt) override;
		virtual void handleEvents(const GameObjectEvent& e, float dt) override;
		virtual ComponentTypes getType() override;

		Ogre::SceneNode* getNode();
		Ogre::Entity* getEntity();

		void setUniformScale(float scale);
		void setPosition(float x, float y, float z);

		//void setPosition(Ogre::Vector3 pos);
	protected:
		// Probably want to split this up??
		Ogre::SceneNode* mNode;
		Ogre::Entity* mEntity;
	};

	// Camera component, can attach to any game object. THIS IS JUST A TEST COMPONENT
	class CameraComponent : public Component
	{
	public:
		CameraComponent(GameObject* owner);
		virtual ~CameraComponent();

		virtual void update(float dt) override;
		virtual void handleEvents(const GameObjectEvent& e, float dt) override;
		virtual ComponentTypes getType() override;

	private:


	};

	/*
	PhysicsComponent, responsible for physics on a game object
	*/
	class PhysicsComponent : public Component
	{
	public:
		PhysicsComponent(GameObject* owner);
		virtual ~PhysicsComponent();
		virtual void update(float dt) override;
		virtual void handleEvents(const GameObjectEvent& e, float dt) override;
		virtual ComponentTypes getType() override;
		btRigidBody* GetRigidBody();
		void WakeComponent(btScalar newMass, btCollisionShape* newShape, Physics* newEng, float offset = 1);
		OgreMotionState* GetMotionState();
		void handleCollisions(PhysicsComponent* other);
		//   WakeComponent function is a band-aid to try to get things working. 
	protected:
		int count;
		bool loaded;
		bool whatever;
		btCollisionShape* collShape;
		btScalar mass;
		btRigidBody* rBody;
		btTransform physTransform;
		btVector3 inertia; //could potentially use our custom vector class, but, it won't matter much as it must be a btVector internally in the physics wrapper/engine.
		OgreMotionState* motionState;
		RenderComponent* renderComponent;
		Physics* engine;
		//need pointer to physics engine to call stepSimulation() or perhaps not if instead the engine iterates through all awake physics component
	};

	/*
	AnimationComponent, responsible for handling the playback and updating of animation.
	Assumes the presence of an "idle" animation, blends between this and current playing animation.
	TODO: Switch between "idle" and "walk" animation smoothly, handling at least one "one-shot" animation.
	TODO: Begin using bone masking to handle blending looping and "one-shot" animations.
	NOTE: When using bone masking, lower body should use looping anim, upper body should use one-shot animation.
	 */
	class AnimationComponent : public Component
	{
		//reference: http://codefreax.org/tutorials/view/id/3
		//fix to have private and public parts
	public:
		static const int NUMBER_ANIMS = 20;
		static const float ANIM_FADE_SPEED;

		enum AnimationID
		{
			ANIM_ATTACK1,
			ANIM_ATTACK2,
			ANIM_ATTACK3,
			ANIM_BACKFLIP,
			ANIM_BLOCK,
			ANIM_CLIMB,
			ANIM_CROUCH,
			ANIM_DEATH1,
			ANIM_DEATH2,
			ANIM_HIGHJUMP,
			ANIM_IDLE1,
			ANIM_IDLE2,
			ANIM_IDLE3,
			ANIM_JUMP,
			ANIM_JUMPNOHEIGHT,
			ANIM_KICK,
			ANIM_SIDEKICK,
			ANIM_SPIN,
			ANIM_STEALTH,
			ANIM_WALK,
			ANIM_NONE // note that this MUST be at the end!
		};

		struct Animation
		{
			Ogre::AnimationState *anim;
			bool isFadingIn, isFadingOut, isActive;
		};

		float tLength; //note that this may be temporary
		Ogre::AnimationState *aStateCurrent;
		Animation aStateIdle, curAnim;
		AnimationID mPrevAnimID;
		std::vector<Animation> animList;
		Ogre::Real mTimer;
		bool mMoving; //so that we can figure out what animation to play upon landing on surface
		

		AnimationComponent(GameObject* owner);
		virtual ~AnimationComponent();

		virtual void update(float dt) override;
		virtual void handleEvents(const GameObjectEvent& e, float dt) override;
		virtual ComponentTypes getType() override;
		void setupAnimations();
		void setAnimation(AnimationID id, bool reset);
		void fadeAnimations(float dt);
		void setIsMoving(bool isMoving);
	protected:
		RenderComponent* rComponent;
		Ogre::Entity* mEntity;
	};

	/*
	InputComponent, responsible for handling input on a certain game object
	TODO: Update method should poll for events for this object, maybe on a per controller basis?
	TODO: Figure out how input should interact with the Render/Physics Components, if the object has them
	*/
	class InputComponent : public Component
	{
	public:
		const Uint8* state; //important for passing buttons pressed to the AnimationComponent
		AnimationComponent* aComponent;
		InputComponent(GameObject* owner);
		virtual ~InputComponent();

		virtual void handleEvents(const GameObjectEvent& e, float dt) override; //to be made in the same format as the original handleEvents below?
		virtual void update(float dt) override;
		virtual ComponentTypes getType() override;

	protected:
		//SDL_GameController* mController;
		void onControllerAdded(); // Check if we need to capture our controller
		void onControllerRemoved(); // Check if we need to remove our controller
		void handleKeyboard(); // Handle the keyboard state

		SDL_Joystick* mJoystick;
		bool mCaptured; // Captured by a controller/joystick
	};	


	/*
	SoundComponent, responsible for playing sounds for this object
	TODO: Fire off sounds based on events (collisions- Physics, or other events- Input)
	*/
	class SoundComponent : public Component
	{
	public:
		SoundComponent(GameObject* owner);
		virtual ~SoundComponent();

		virtual void update(float dt) override;
		virtual void handleEvents(const GameObjectEvent& e, float dt) override;
		virtual ComponentTypes getType() override;
	protected:
		irrklang::ISoundEngine* mEngine;
		std::vector< irrklang::ISound* > mSounds;
	};

}