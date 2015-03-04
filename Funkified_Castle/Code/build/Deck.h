#pragma once
#include <iostream>
#include <SDL.h>
#include <vector>
#include "Card.h"
#include <algorithm>

using namespace std;

class Deck
{
    public:

    vector<Card*> NewDeck;

        Deck()
        {
            for(int i = 0; i < 13; i++)
            {
                     NewDeck.push_back(new Card(i + 1, SPADES));
                     NewDeck.push_back(new Card(i + 1, CLUBS));
                     NewDeck.push_back(new Card(i + 1, DIAMONDS));
                     NewDeck.push_back(new Card(i + 1, HEARTS));
            }
        }


        void Shuffle()
        {
            random_shuffle(NewDeck.begin(), NewDeck.end());
        }

        Card* deal()
        {
            if (!isEmpty())
            {
                Card* top = NewDeck.back();
                NewDeck.pop_back();
                return top;
            }
            else
                return NULL;
        }

        bool isEmpty()
        {
            if(this->NewDeck.size() == 0)
                return true;
            else
                return false;
        }
};
