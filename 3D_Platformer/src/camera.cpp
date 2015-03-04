#include <stdafx.h>
#include <camera.h>
#include <application.h>

namespace ssuge{

	Camera::Camera(std::string name, Ogre::SceneNode *parent, Ogre::SceneManager* manager)
	{
		m_name = name;
		m_parent = parent->getParentSceneNode();
		m_sManager = manager;
		m_position = Ogre::Vector3(0,0,700);
		freeRoam = false;
		init();
	}

	Camera::~Camera()
	{

	}

	int Camera::init()
	{
		m_cameraYaw = m_parent->createChildSceneNode("cameraYaw");
		m_cameraElev = m_cameraYaw->createChildSceneNode("cameraElev");
		m_cameraNode = m_cameraElev->createChildSceneNode("cameraNode");
		o_camera = m_sManager->createCamera(m_name);
		o_camera->setPosition(m_position);
		Ogre::Viewport *vp = Application::getSingleton().getWindow()->addViewport(o_camera);
		o_camera->setAspectRatio((float)vp->getActualWidth()/vp->getActualHeight());
		vp->setBackgroundColour(Ogre::ColourValue(0.3f,0.3f,0.3f));
		m_cameraNode->attachObject(o_camera);
		m_cameraElev->rotate(Ogre::Quaternion(Ogre::Radian(-40*PI/180),Ogre::Vector3(1,0,0)));
		m_Height = 40*PI/180;
		m_curRotation= 0.0;
		return(0);
	}
	
	void Camera::handleInput(float dt)
	{
		const Uint8* keysPressed = SDL_GetKeyboardState(NULL);

		if (keysPressed[SDL_SCANCODE_KP_4]){
			adjustTargetYaw(dt, -1);
		}
		if (keysPressed[SDL_SCANCODE_KP_6]){
			adjustTargetYaw(dt, 1);
		}
		if (keysPressed[SDL_SCANCODE_KP_8]){
			adjustTargetPitch(dt, 1);
		}
		if (keysPressed[SDL_SCANCODE_KP_2]){
			adjustTargetPitch(dt, -1);
		}
		if (keysPressed[SDL_SCANCODE_KP_5]){
			setFreeRoam();
		}
		if (keysPressed[SDL_SCANCODE_KP_PLUS]){
			zoom(dt, 1);
		}
		if (keysPressed[SDL_SCANCODE_KP_MINUS]){
			zoom(dt, -1);
		}
	}

	void Camera::update(float dt)
	{
		handleInput(dt);
	}
	void Camera::adjustTargetYaw(float dt, int dir)
	{
		//rotate right around target
		if (dir > 0){
			m_cameraYaw->rotate(Ogre::Quaternion(Ogre::Radian(100*PI/180)*dt,Ogre::Vector3(0,1,0)));
			m_curRotation -= 100*PI/180*dt;
		}
		//rotate left around target
		if(dir < 0){
			m_cameraYaw->rotate(Ogre::Quaternion(Ogre::Radian(100*-PI/180)*dt,Ogre::Vector3(0,1,0)));
			m_curRotation += 100*PI/180*dt;
		}
	}
	void Camera::adjustTargetPitch(float dt, int dir)
	{
		//rotate up around target
		if (dir > 0){
			m_cameraElev->rotate(Ogre::Quaternion(Ogre::Radian(100*PI/180)*dt,Ogre::Vector3(1,0,0)));
			m_Height -= 100*PI/180*dt;
		//rotate down around target
		}
		if (dir < 0){
			m_cameraElev->rotate(Ogre::Quaternion(Ogre::Radian(100*-PI/180)*dt,Ogre::Vector3(1,0,0)));
			m_Height += 100*PI/180*dt;
		}

	}
	void Camera::adjustRoll(float dt, int dir)
	{
		if (dir > 0){
			m_cameraNode->rotate(Ogre::Quaternion(Ogre::Radian(100*-PI/180)*dt,Ogre::Vector3(0,0,1)));
		}
		if (dir < 0){
			m_cameraNode->rotate(Ogre::Quaternion(Ogre::Radian(100*PI/180)*dt,Ogre::Vector3(0,0,1)));
		}
	}
	void Camera::zoom(float dt, int dir)
	{
		Ogre::Vector3 pos = m_parent->_getDerivedPosition();
		float z = o_camera->getPosition().z;
		if (dir>0)
			o_camera->setPosition(0,0,z-dt*150);
		if (dir<0)
			o_camera->setPosition(0,0,z+dt*150);
		//o_camera->setAspectRatio(4/3);
	}
	void Camera::pan(float dt, float ammount)
	{
		return;
	}
	void Camera::shake(float dt, float ammount)
	{
		return;
	}

	void Camera::setARatio(int width, int height)
	{
		return;
		//o_camera->setAspectRatio(width/height);
	}

	int Camera::detectObstruction(Ogre::Node *target)
	{
		return 0;
	}

	void Camera::setFreeRoam(void)
	{
		if(!freeRoam){
			m_parent->removeChild("cameraYaw");
			m_prevParent = m_parent;
			m_sManager->getRootSceneNode()->addChild(m_cameraYaw);
			m_parent = m_sManager->getRootSceneNode();
			freeRoam = true;
			return;
		}
		else{
			m_sManager->getRootSceneNode()->removeChild("cameraYaw");
			m_parent = m_prevParent;
			m_parent->addChild(m_cameraYaw);
			o_camera->setPosition(m_position);
			m_curRotation= 0.0;

			freeRoam = false;
			return;
		}

	}

	void Camera::setParent(Ogre::SceneNode *new_parent)
	{
		m_parent->removeChild("cameraYaw");
		m_parent = new_parent;
		m_parent->addChild(m_cameraYaw);
	}

	void Camera::followPath(void)
	{
		return;
	}
}
