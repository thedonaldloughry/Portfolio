#include "stdafx.h"
#include <string.h>
#include <map>
#include <SDL_events.h>
#include <string.h>
//#include <gameObject.h>

#include "gameobject.h"

using namespace Ogre;

namespace ssuge {

	class MainCamera: public GameObject //the camera inherits from the "Entity" class
	{
		public:
			//I miss the super() Java method for some reason
			Camera *camera;
			float camera_Y_Min, camera_Y_Max, camera_X_Cur, camera_Y_Cur, dimX, dimY;
			Quaternion camRotationYaw, camRotationPitch, camOrientation;
			SceneNode *cameraNode, *cameraFocusPoint;
			SceneManager *mSceneManager;
			Vector3 placeToLookAt; //do we ever use facingdirection?
		//public:
			MainCamera(SceneManager *sceneManager, SceneNode *focusPoint, float dimensionX, float dimensionY, 
				Vector3 camPos, Vector3 lookAtPos);
			void cameraSetup();
			void incRotateValue(float& rotationValue, float rotationAmount, float dt, int isXorY);
			virtual ~MainCamera();
	};

}