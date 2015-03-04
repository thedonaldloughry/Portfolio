#pragma once
#include <iostream>
#include <SDL.h>

using namespace std;

enum Suit
{
    HEARTS,DIAMONDS,CLUBS,SPADES
};

class Card
{
public:

    int x,y;
    int rank;   //A=1, 2,3,4,...,j=11,q=12,k=13
    Suit suit;



    static SDL_Surface* tilesheet1;

    Card(int r, Suit s)
    {
        rank=r;
        suit=s;
        x = 0; y = 0;

        if( tilesheet1 == NULL )
        {
            SDL_Surface* tempTilesheet = SDL_LoadBMP("assets/allcards.bmp");

            if(!tempTilesheet)
            {
                cerr << "No tilesheet\n";
            }

            tilesheet1 = SDL_CreateRGBSurface(SDL_SWSURFACE, tempTilesheet->w, tempTilesheet->h, 32, 0xff, 0xff00, 0xff0000, 0);
            SDL_BlitSurface(tempTilesheet,NULL,tilesheet1,NULL);

            unsigned keypix = SDL_MapRGB(tilesheet1->format,255,1,255);

            if( SDL_SetColorKey(tilesheet1,SDL_SRCCOLORKEY,keypix) )
            {
                cerr << "No key\n";
            }

        }
    }

    bool containsPoint(int xCoord, int yCoord)
    {
        if (this->x <= xCoord and xCoord<= this->x + 97)
        {
            if (this->y <= yCoord and yCoord <= this->y + 129)
            {
                return true;
            }
            else
                return false;
        }
        else
            return false;
    }

    void setLocation(int xCoord, int yCoord)
    {
        this->x = xCoord - 48;
        this->y = yCoord - 48;
    }

    void draw(SDL_Surface* win)
    {
        SDL_Rect src;
        src.x = (rank * 97) - 97; src.w = 98; src.h = 130;
        if (suit == DIAMONDS)
            src.y = 0;
        else if (suit == HEARTS)
            src.y = 129;
        else if (suit == SPADES)
            src.y = 258;
        else if (suit == CLUBS)
            src.y = 387;


        SDL_Rect dst;
        dst.x = x; dst.y = y;

        SDL_BlitSurface(tilesheet1, &src, win, &dst);

    }



};
