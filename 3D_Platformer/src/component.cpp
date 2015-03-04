#pragma once
#include "stdafx.h"
#include "component.h"


namespace ssuge {

	Component::Component(GameObject* owner) : mOwner(owner)
	{
		mOwner->addComponent(this);
	}

	Component::~Component()
	{
	}





	RenderComponent::RenderComponent(GameObject* owner, std::string name, std::string mesh_fname, Ogre::SceneManager* manager, Ogre::SceneNode* parent) : 
		Component(owner)
	{
		mEntity = manager->createEntity(name, mesh_fname);
		mNode = parent->createChildSceneNode(name);
		mNode->attachObject(mEntity);
	}

	RenderComponent::~RenderComponent()
	{
	}

	void RenderComponent::update(float dt)
	{
	}

	void RenderComponent::handleEvents(const GameObjectEvent& e, float dt)
	{
	}

	ComponentTypes RenderComponent::getType()
	{
		const ComponentTypes type = ComponentTypes::RENDERCOMPONENT;
		return type;
	};

	Ogre::SceneNode* RenderComponent::getNode()
	{
		return mNode;
	}

	void RenderComponent::setUniformScale(float scale)
	{
		mNode->scale(scale, scale, scale);
	}

	void RenderComponent::setPosition(float x, float y, float z)
	{
		mNode->setPosition(x, y, z);
	}

	Ogre::Entity* RenderComponent::getEntity()
	{
		return mEntity;
	}
	

}