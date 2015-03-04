#include "stdafx.h"
#include "physics.h"
#include "component.h"

namespace ssuge {

	PhysicsComponent::PhysicsComponent(GameObject* owner) : Component(owner)
	{
		renderComponent = dynamic_cast<RenderComponent*>(mOwner->getComponent(ComponentTypes::RENDERCOMPONENT));
		if(renderComponent == nullptr) {
			DEBUGSTR("WARNING: Physics component added to a GameObject with no render component.");
		}
		loaded = false;
	}

	void PhysicsComponent::WakeComponent(btScalar newMass, btCollisionShape* newShape, Physics* newEng, float offset)
	{
		mass			= newMass;
		collShape		= newShape;
		engine			= newEng;
		inertia.setZero();

		Ogre::Vector3 pos = renderComponent->getNode()->getPosition();
		Ogre::Quaternion rot = renderComponent->getNode()->getOrientation();

		btTransform trans(btQuaternion(rot.x,rot.y,rot.z,rot.w), btVector3(pos.x,pos.y,pos.z));
		physTransform = trans;

		update(0.0f);

		motionState = new OgreMotionState(physTransform, renderComponent->getNode(),offset);
		//set rigidbody mass to 0 to create static.
		if(mass > 0) {
			collShape->calculateLocalInertia(mass,inertia);
		}
		btMotionState* tmpMotionState = dynamic_cast<btMotionState*>(motionState);
		btRigidBody::btRigidBodyConstructionInfo rbInfo(mass,tmpMotionState,collShape,inertia);	
		rBody = new btRigidBody(rbInfo);
		
		loaded = true;
		engine->AddObject(this);
	}

	void PhysicsComponent::handleCollisions(PhysicsComponent* other)
	{

	}

	void PhysicsComponent::update(float dt)
	{
		if(loaded) {
			Ogre::Vector3 pos = renderComponent->getNode()->getPosition();
			physTransform.setOrigin(btVector3(pos.x,pos.y,pos.z));
			mOwner->setPosition(pos);
			Ogre::Quaternion qt = renderComponent->getNode()->getOrientation(); //probably should just cache pointers to the position and the rotation...
			physTransform.setRotation(btQuaternion(qt.x, qt.y, qt.z, qt.w));
			if(motionState)
				motionState->UpdateTransform(physTransform);
		}
	}

	void PhysicsComponent::handleEvents(const GameObjectEvent& e, float dt)
	{
	}

	ComponentTypes PhysicsComponent::getType()
	{
		const ComponentTypes type = ComponentTypes::PHYSICSCOMPONENT;
		return type;
	};

	btRigidBody* PhysicsComponent::GetRigidBody()
	{
		return rBody;
	}

	OgreMotionState* PhysicsComponent::GetMotionState()
	{
		return motionState;
	}

	PhysicsComponent::~PhysicsComponent() 
	{
		delete collShape;
		delete rBody;
		delete motionState;
	}
	
	Physics::Physics(Ogre::SceneManager* scm) {
			sceneMgr = scm;
			InitObjects();
		}

	void Physics::InitObjects() {
		collisionConfig			= new btDefaultCollisionConfiguration();
		dispatcher				= new btCollisionDispatcher(collisionConfig);
		overlappingPairCache	= new btDbvtBroadphase();
		solver					= new btSequentialImpulseConstraintSolver();
		dynamicsWorld			= new btDiscreteDynamicsWorld(dispatcher, overlappingPairCache,solver, collisionConfig);
		dynamicsWorld->setGravity(btVector3(0,-98.0f,0));
		mDebugDrawer			= new OgreDebugDrawer(sceneMgr);
		mDebugDrawer->setDebugMode(btIDebugDraw::DBG_DrawWireframe);
		dynamicsWorld->setDebugDrawer(mDebugDrawer);

		btAlignedObjectArray<btCollisionShape*> collisionShapes;
	}

	void Physics::AddObject(PhysicsComponent* component) {
		compList.push_back(component);
		dynamicsWorld->addRigidBody(component->GetRigidBody());
		
	}

	void Physics::RemoveObject(PhysicsComponent* component) {}

	void Physics::StepSimulation(const float elapsedTime, int maxSubSteps, const float fixedTimestep) {
		dynamicsWorld->stepSimulation(elapsedTime, maxSubSteps, fixedTimestep);
		dynamicsWorld->debugDrawWorld();
		
    int numManifolds = dynamicsWorld->getDispatcher()->getNumManifolds();
    for (int i=0;i<numManifolds;i++)
    {
        btPersistentManifold* contactManifold =  dynamicsWorld->getDispatcher()->getManifoldByIndexInternal(i);
        const btCollisionObject* obA = static_cast<const btCollisionObject*>(contactManifold->getBody0());
        const btCollisionObject* obB = static_cast<const btCollisionObject*>(contactManifold->getBody1());

        int numContacts = contactManifold->getNumContacts();
		for (int j=0;j<numContacts;j++) 
		{
			GameObject* goA = static_cast<GameObject*>(obA->getUserPointer());
			GameObject* goB = static_cast<GameObject*>(obB->getUserPointer());

			if(goA != nullptr && goB != nullptr) {
				PhysicsComponent* pcA = static_cast<PhysicsComponent*>(goA->getComponent(ComponentTypes::PHYSICSCOMPONENT));
				PhysicsComponent* pcB = static_cast<PhysicsComponent*>(goB->getComponent(ComponentTypes::PHYSICSCOMPONENT));

			pcA->handleCollisions(pcB);
			pcB->handleCollisions(pcA);
			}

			
		}
    }
	}

	Physics::~Physics() {
		delete dynamicsWorld;
		delete solver;
		delete dispatcher;
		delete collisionConfig;
		delete overlappingPairCache;
	}

	OgreMotionState::OgreMotionState(const btTransform& initialPos, Ogre::SceneNode* node, float os) {
		mVisibleObj = node;
		mPos1 = initialPos;
		offset = os;
	}

	void OgreMotionState::SetNode(Ogre::SceneNode* node) {
		mVisibleObj = node;
	}

	void OgreMotionState::UpdateTransform(btTransform& newPos) {
		mPos1 = newPos;
	}

	void OgreMotionState::getWorldTransform(btTransform& worldTrans) const {
		worldTrans = mPos1;
	}

	void OgreMotionState::setWorldTransform(const btTransform& worldTrans) {

		if(mVisibleObj == NULL)
			return;

		btQuaternion rot = worldTrans.getRotation();
		Ogre::Quaternion q(rot.w(),rot.x(),rot.y(),rot.z());
		
		btVector3 pos = worldTrans.getOrigin();
		Ogre::Vector3 v(pos.x()*offset,pos.y()*offset,pos.z()*offset);

		v = mVisibleObj->getParentSceneNode()->convertWorldToLocalPosition(v);
		q = mVisibleObj->getParentSceneNode()->convertWorldToLocalOrientation(q);

		mVisibleObj->setOrientation(q);
		mVisibleObj->setPosition(v);
	}

	OgreMotionState::~OgreMotionState() {
		
		
	}

}