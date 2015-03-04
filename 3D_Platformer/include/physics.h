#pragma once

#include "stdafx.h"
#include "DebugDrawer.h"


namespace ssuge {

	class PhysicsComponent;

	class Physics{
	public:
		Physics(Ogre::SceneManager* scm);
		void InitObjects();
		void AddObject(PhysicsComponent* component);
		void RemoveObject(PhysicsComponent* component);
		void StepSimulation(const Ogre::Real elapsedTime, int maxSubSteps, const float = 1.0f/60.0f);
		std::vector<btCollisionShape*> GetCollisionShapes();
		~Physics();
		//void CreatePhysicsAsset(Ogre::Entity * ent, btVector3 position, btTransform startTransform, btVector3 localIntertia = btVector3(0,0,0));

	protected:
		Ogre::SceneManager* sceneMgr;
		btDefaultCollisionConfiguration* collisionConfig;
		btCollisionDispatcher* dispatcher;
		btBroadphaseInterface* overlappingPairCache;
		btSequentialImpulseConstraintSolver* solver;
		btDiscreteDynamicsWorld* dynamicsWorld;
		std::vector<btCollisionShape *> collShapes;
		std::map<std::string, btRigidBody *> physicsAccessors;
		std::vector<PhysicsComponent*> compList;
		OgreDebugDrawer* mDebugDrawer;
	};

	class OgreMotionState : public btMotionState {
	protected:
		Ogre::SceneNode* mVisibleObj;
		btTransform mPos1;
		float offset;
	public:
		OgreMotionState(const btTransform& initialPos, Ogre::SceneNode* node, float os = 1);
		virtual ~OgreMotionState();

		void SetNode(Ogre::SceneNode* node);

		void UpdateTransform(btTransform& newPos);

		virtual void getWorldTransform(btTransform& worldTrans) const;
		virtual void setWorldTransform(const btTransform& worldTrans);
	};

}



/*
Sources:

[1] Ogre + Bullet -  Beginner's Tutorial http://oramind.com/ogre-bullet-a-beginners-basic-guide/				ret 10/7/2014
[2] University of Texas CS378 Lecture 11 http://www.cs.utexas.edu/~fussell/courses/cs378/lectures/cs378-11.pdf	ret 10/18/2014
	
*/