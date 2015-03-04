#include "stdafx.h"

#include "state.h"

namespace ssuge {

	GameState::GameState() : mFinished(false)
	{
	}

	GameState::~GameState()
	{
	}

	bool GameState::isFinished()
	{
		return mFinished;
	}

	void GameState::update(float dt)
	{
		if ( mFinished ) {
			return;
		}
	}

	PlayingState::PlayingState() : GameState(), mWorld(new GameWorld("../media/3Dplatformer_assets/test.xml"))
	{

	}
	

	PlayingState::~PlayingState()
	{
		delete mWorld;
		mWorld = nullptr;
	}

	void PlayingState::update(float dt)
	{
		if ( mFinished ) {
			return;
		}

		mWorld->update(dt);
	}

	PausedState::PausedState()
	{
	}

	PausedState::~PausedState()
	{
	}

	void PausedState::update(float dt)
	{
	}
}