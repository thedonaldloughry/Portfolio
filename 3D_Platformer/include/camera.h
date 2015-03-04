#pragma once
#include <stdafx.h>
#define PI 3.14f
#include <string>

#include "gameobject.h"

namespace ssuge{

	class Camera
	{
	public:
		Camera(std::string name, Ogre::SceneNode *parent, Ogre::SceneManager *manager);
		virtual ~Camera();

		Ogre::SceneManager *m_sManager;
		Ogre::SceneNode *m_parent;
		Ogre::SceneNode *m_prevParent;
		Ogre::SceneNode *m_cameraYaw; 
		Ogre::SceneNode *m_cameraElev;
		Ogre::SceneNode *m_cameraNode; //where the Ogre camera attaches
		Ogre::Camera *o_camera;
		
		float m_Height;
		float m_Yaw;
		float m_Pitch;
		float m_Roll;
		float m_curRotation;

		bool freeRoam;
		Ogre::Vector3 m_position;
		Ogre::Vector3 m_dir;
		std::string m_name;

		virtual int init();
		virtual void update(float dt);
		virtual void handleInput(float dt);

		//these functions adjust camera based off of its target parent
		virtual void adjustTargetYaw(float dt, int dir);
		virtual void adjustTargetPitch(float dt, int dir);
		virtual void adjustRoll(float dt, int dir);

		//misc camera functions that may or may not be useful
		virtual void zoom(float dt, int dir);
		virtual void pan(float dt, float ammount);
		virtual void shake(float dt, float ammount);

		//set aspect ratio of camera
		virtual void setARatio(int width, int height);

		//more misc camera functions
		virtual void setFreeRoam(void);
		virtual void setParent(Ogre::SceneNode *new_parent); //sets a new target for the camera. Potentially needs some adjusting
		virtual int detectObstruction(Ogre::Node *target);
		virtual void followPath(void);
	};
}