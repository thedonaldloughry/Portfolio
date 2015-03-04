#pragma once
#include <iostream>
#include <SDL.h>
#include <SDL_mixer.h>
#include <string>

class Sounds
{
    public:

        Uint32 len;
        Uint8* buff;
        Mix_Chunk* mc;

        Sounds()
        {
            mc = NULL;
        }
        void init()
        {
            cout << "sound initialized" << endl;
            Mix_Init(0);
            Mix_OpenAudio(MIX_DEFAULT_FREQUENCY, MIX_DEFAULT_FORMAT, 1, 1024);
            Mix_AllocateChannels(8);
        }
        int play(int volume, int rep = 0)
        {
            int ch = Mix_PlayChannel(-1,mc,rep);
            Mix_Volume(0,volume);
            return ch;
        }
        int fadein(int rep=-1)
        {
            int ch = Mix_FadeInChannel(-1,mc,rep,1000);
            return ch;
        }
};


