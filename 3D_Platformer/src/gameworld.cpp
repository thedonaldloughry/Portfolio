#include "stdafx.h"
#include "gameworld.h"
#include "application.h"
#include "gameobject.h"
#include "camera.h"
#include "component.h"

#include <memory>

namespace ssuge {

	GameWorld::GameWorld(std::string world_filename) : mLoaded(false), mFile(world_filename)
	{
	}

	GameWorld::~GameWorld()
	{
		for ( auto ob : mObjects ) {
			delete ob;
			ob = nullptr;
		}
	}

	void GameWorld::update(float dt)
	{
		if ( !mLoaded ) {
			init();
		}

		for ( auto obj : mObjects ) {
			obj->update(dt);
		}
		mCam->update(dt);
		mPhysEng->StepSimulation(dt,1);
	}

	void GameWorld::init()
	{
		tinyxml2::XMLDocument doc;
		
		if ( doc.LoadFile(mFile.c_str()) != tinyxml2::XML_NO_ERROR ) {
			// Error happened! Throw some error, or just print it out
			doc.PrintError();
			return;
		}

		mSceneManager = Application::getSingleton().getRoot()->createSceneManager(Ogre::ST_GENERIC);
		mPhysEng = new Physics(mSceneManager);

		//g.addComponent(new RenderComponent(&g, "test_Car", "PinkCar.mesh", mSceneManager, mSceneManager->getRootSceneNode()));

		tinyxml2::XMLElement* root_elem = doc.RootElement();

		buildWorld(root_elem, mSceneManager->getRootSceneNode());

		mLoaded = true;
	
	}


	// Build the world!
	void GameWorld::buildWorld(tinyxml2::XMLElement* parent, Ogre::SceneNode* parent_node)
	{
		for ( auto child = parent->FirstChildElement(); child != nullptr; child = child->NextSiblingElement() ) {

			DEBUGSTR(child->Name());

			const std::string object_string = "object";
			const std::string light_string = "light";
			const std::string camera_string = "camera";
			const std::string x_string = "x";
			const std::string y_string = "y";
			const std::string z_string = "z";

			// Our starting values for position. The object defaults to these if they aren't present in the xml tag.
			float x_value = 0.0f;
			float y_value = 0.0f;
			float z_value = 0.0f;

			// Get the (optional) x, y, and z parameters (position)
			child->QueryFloatAttribute(x_string.c_str(), &x_value);
			child->QueryFloatAttribute(y_string.c_str(), &y_value);
			child->QueryFloatAttribute(z_string.c_str(), &z_value);

			// Create a game object (if we need it)
			GameObject* go = nullptr;
			if ( child->Name() == object_string ) {
				go = new GameObject();
				mObjects.push_back(go);
				go->setPosition(x_value, y_value, z_value);
			}

			// TO DO: Create a better way of getting the light stuff.
			if ( child->Name() == light_string ) {
				const std::string light_name = "name";

				std::string name = "";

				Ogre::Light* light = mSceneManager->createLight(name);
				parent_node->attachObject(light);
				light->setPosition(x_value, y_value, z_value);
			}

			// TO DO: 
			if ( child->Name() == camera_string ) {
				mCam = new Camera("main_camera", parent_node, mSceneManager);
			}

			// probably unnecessary check
			if ( go != nullptr ) {

				// Get all the components for this game object
				for ( auto component_child = child->FirstChildElement(); component_child != nullptr; component_child = component_child->NextSiblingElement() ) {
					const std::string render_component = "render";
					const std::string physics_component = "physics";
					const std::string input_component = "input";
					const std::string animation_component = "animation";
					const std::string sound_component = "sound";

					if ( component_child->Name() == render_component ) {
						const std::string name = "name";
						const std::string mesh = "mesh";
						const std::string scale = "scale";
						const std::string inherit_scale = "inherit_scale";

						std::string component_name = "";
						std::string mesh_name = "";
						float scale_value = 1.0f;
						bool use_parent_scale = true;

						component_name = component_child->Attribute(name.c_str());
						mesh_name = component_child->Attribute(mesh.c_str());
						component_child->QueryFloatAttribute(scale.c_str(), &scale_value);
						component_child->QueryBoolAttribute(inherit_scale.c_str(), &use_parent_scale);

						RenderComponent* ren = new RenderComponent(go, component_name, mesh_name, mSceneManager, parent_node);
						ren->setPosition(x_value, y_value, z_value);
						ren->getNode()->scale(scale_value, scale_value, scale_value);
						ren->getNode()->setInheritScale(use_parent_scale);
						buildWorld(component_child, ren->getNode());
					}
					if ( component_child->Name() == physics_component ) {
						PhysicsComponent* phys = new PhysicsComponent(go);
					}
					if ( component_child->Name() == input_component ) {
						InputComponent* input = new InputComponent(go);
					}
					if ( component_child->Name() == sound_component ) {
						SoundComponent* sound = new SoundComponent(go);
					}
					if ( component_child->Name() == animation_component ) {
						AnimationComponent* anim = new AnimationComponent(go);
					}
				}
			}
		}
	}

	Ogre::SceneManager* GameWorld::getManager()
	{
		return mSceneManager;
	}

	void GameWorld::addObject(GameObject* object)
	{
		mObjects.push_back(object);
	}

}