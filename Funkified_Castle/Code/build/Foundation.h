#include <iostream>
#include <vector>
#include <SDL.h>
#include <stack>
#include "Card.h"

using namespace std;

class Foundation
{
    public:

        int xCoord, yCoord;
        Card* top;
        stack<Card*> fCards;

        Foundation(int x, int y)
        {
            xCoord = x; yCoord = y;
        }

        Card* getTopCard()
        {
            if (!fCards.empty())
                return fCards.top();
            else
                return NULL;
        }

        void addCard(Card* c)
        {
                fCards.push(c);
                fCards.top()->setLocation(xCoord, yCoord);
        }

        void removeTopCard()
        {
            if(!fCards.empty())
                fCards.pop();
        }

        void draw(SDL_Surface* win)
        {
            if (!fCards.empty())
                fCards.top()->draw(win);
        }
};
