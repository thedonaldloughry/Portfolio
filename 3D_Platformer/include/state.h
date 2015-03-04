#pragma once

#include "stdafx.h"

#include "gameworld.h"

namespace ssuge {

	enum class GameStateTypes
	{
		GS_NULLSTATE,
		GS_PLAYING,
		GS_PAUSED,
		GS_QUIT,
	};

	class GameState
	{
	public:
		GameState();
		virtual ~GameState() = 0;

		static const GameStateTypes TYPE = GameStateTypes::GS_NULLSTATE;

		virtual bool isFinished();
		virtual void update(float dt);

	protected:
		bool mFinished;
	};

	class PlayingState : public GameState
	{
	public:
		PlayingState();
		virtual ~PlayingState();

		static const GameStateTypes TYPE = GameStateTypes::GS_PLAYING;

		virtual void update(float dt) override;
		

	protected:
		GameWorld* mWorld;
	};


	class PausedState : public GameState
	{
	public:
		PausedState();
		virtual ~PausedState();

		static const GameStateTypes TYPE = GameStateTypes::GS_PAUSED;

		virtual void update(float dt) override;
	protected:
	};
}