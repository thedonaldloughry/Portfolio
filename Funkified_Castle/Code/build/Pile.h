#pragma once
#include <iostream>
#include <vector>
#include <SDL.h>
#include "Card.h"

class Pile
{
    public:

        bool isLeft;
        int xCoord, yCoord;
        SDL_Rect rect;
        Card* top;

        vector<Card*> cards;

        Pile(int x, int y, bool L)
        {
            isLeft = L;
            xCoord = x; yCoord = y;
        }

        void removeTopCard()
        {
            cards.pop_back();
        }

        void addCard(Card* C)
        {
                cards.push_back(C);
                 if (isLeft == true)
                        cards[cards.size() - 1]->setLocation(xCoord - ((cards.size() - 1)*20), yCoord);
                else
                        cards[cards.size() - 1]->setLocation(xCoord + ((cards.size() - 1)*20), yCoord);
        }

        bool isEmpty()
        {
            if (cards.size() == 0)
                return true;
            else
                return false;
        }

        Card* getTopCard()
        {
            if(!isEmpty())
            {
                top = cards.back();
            }
            else
                top = NULL;

            return top;
        }

        void pileDraw(SDL_Surface* win)
        {
            if (cards.size() == 0)
            {
                rect = {xCoord - 48, yCoord - 48, 98, 130};
                SDL_FillRect(win, &rect, SDL_MapRGB(win->format, 0, 255, 0));
            }
            for(unsigned j = 0; j < cards.size(); j++)
            {
                cards[j]->draw(win);
            }
        }
};
