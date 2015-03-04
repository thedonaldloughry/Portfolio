#include "stdafx.h"

#include "component.h"
#include "application.h"

#include <irrKlang.h>

namespace ssuge {

	SoundComponent::SoundComponent(GameObject* owner) : Component(owner)
	{
		mEngine = Application::getSingleton().getSoundEngine();
	}

	SoundComponent::~SoundComponent()
	{
	}

	void SoundComponent::update(float dt)
	{
		// Need to play shit here if it is needed. Like, if something collides with something else
		// Temp list to prevent mutating the list while iterating over it
		std::vector< irrklang::ISound* > t_soundlist = mSounds;
		
		for ( auto sound : mSounds ) {
			// These need to be in this order so that we can remove the sound from the vector
			// TO DO: Need to (possibly) figure out a better data structure for fast add and removal. Maybe a HashSet or Heap?
			if ( sound == nullptr || sound->isFinished() ) {
				// Need to figure out a good way of removing sounds from the vector
				t_soundlist.erase(std::remove(t_soundlist.begin(), t_soundlist.end(), sound), t_soundlist.end());
				continue;
			}

			// Convert position from OGRE to irrklang
			Ogre::Vector3 temp_pos = mOwner->getPosition();
			irrklang::vec3d<float> dest_pos;
			dest_pos.X = temp_pos.x;
			dest_pos.Y = temp_pos.y;
			dest_pos.Z = temp_pos.z;

			sound->setPosition(dest_pos);
		}
		// Assign the temp vector to the class vector
		mSounds = t_soundlist;
	}

	void SoundComponent::handleEvents(const GameObjectEvent& e, float dt)
	{
		// Process the events and push back a new sound to play
		// TODO: Decide on syntax in events to play a sound. Maybe the args should be the file name?
		// Convert position from OGRE to irrklang
		Ogre::Vector3 temp_pos = mOwner->getPosition();
		DEBUGVAR(temp_pos);
		irrklang::vec3d<float> dest_pos;
		dest_pos.X = temp_pos.x;
		dest_pos.Y = temp_pos.y;
		dest_pos.Z = temp_pos.z;

		irrklang::ISound* sound = mEngine->play3D(e.args[0].c_str(), dest_pos);

		if ( sound != nullptr ) {
			mSounds.push_back(sound);
		}
	}

	ComponentTypes SoundComponent::getType()
	{
		const ComponentTypes type = ComponentTypes::SOUNDCOMPONENT;
		return type;
	};

}