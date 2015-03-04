#include <iostream>
#include <SDL.h>
#include <string>
#include <stack>
#include <list>
#include <cstdlib> //Needed for srand
#include <ctime> //Needed for time
#include "Foundation.h"
#include "Deck.h"
#include "Pile.h"
#include "FileIO.h"
#include "Sounds.h"

using namespace std;

struct Move
{
    Card* thisCard;
    int index;
    int whereItsGoing;
    bool isFoundation;
    Move(Card* card, int num, int dest, bool found)
    {
        thisCard = card;
        index = num;
        whereItsGoing = dest;
        isFoundation = found;
    }
};

void randColorNum(SDL_Surface* win)
{
    // Dat Funk...
    srand(time(NULL));
    int number = rand() % 255;
    int number2 = rand() % 255;
    int number3 = rand() % 255;
    SDL_FillRect(win, NULL, SDL_MapRGB(win->format, number,number2,number3));
}

void drawIT(SDL_Surface* win, vector<Pile*> ourPiles, vector<Foundation*> ourFounds, Card* dragging)
{
    randColorNum(win);

    for(unsigned i = 0; i < ourPiles.size(); i++)
    {
       ourPiles[i]->pileDraw(win);
    }

    for(unsigned j = 0; j < ourFounds.size(); j++)
    {
       ourFounds[j]->draw(win);
    }

     if(dragging)
    {
        dragging->draw(win);
    }

    SDL_Flip(win);

}

void unDeal(vector<Pile*> Piles, vector<Foundation*> Foundations)
{
    for (unsigned m = 0; m < Piles.size(); m++)
    {
        for(unsigned o = 0; o < Piles[m]->cards.size() + 8; o++)
        {
            if(!Piles[m]->isEmpty())
                Piles[m]->removeTopCard();
        }

    }
    for (unsigned r = 0; r < Foundations.size(); r++)
    {
            for(unsigned u = 0; u < Foundations[r]->fCards.size(); u++)
            {
                if(!Foundations[r]->fCards.empty())
                    Foundations[r]->removeTopCard();
            }
    }
}

void dealOut(vector<Pile*> Piles, vector<Foundation*> Foundations, Deck curDeck)
{
    curDeck.Shuffle();
    int foundCount = 0;
        for (unsigned y = 0; y < Piles.size(); y++)
        {
            for (int s = 0; s < 6; )
            {
                    Card* q = curDeck.deal();

                    if(q->rank == 1)
                    {
                        Foundations[foundCount]->addCard(q);
                        foundCount++;
                    }
                    else
                    {
                        Piles[y]->addCard(q);
                        s++;
                    }
            }
        }

        if(foundCount != 4)
        {
            Deck NewDeck;
            unDeal(Piles, Foundations);
            dealOut(Piles, Foundations, NewDeck); // YAY, RECURSION!
        }

}

int main(int argc, char* argv[])
{
    SDL_Init(SDL_INIT_EVERYTHING);
    SDL_Surface* win = SDL_SetVideoMode(900,700,32,SDL_SWSURFACE);

    if(!win)
    {
        cerr << "Oh noes!" << endl;
        exit(1);
    }

    cout << "Welcome to Beleaguered Castle! Click and drag a card to move it\nonto a pile. Press z to undo, y to redo, n for a new game, s to save a file,\nand L to load a file." << endl;

    Deck curDeck;

    Sounds Kalimba;
    Kalimba.init();

    Sounds woosh;
    woosh.init();

    Card* dragging;
    vector<Pile*> Piles;
    vector<Foundation*> Foundations;
    list<Move>::iterator I;
    list<Move> L;
    I = L.end();

    for (int i = 0; i < 4; i++)
    {
        Piles.push_back(new Pile(300, 150 * (i + 1), true));
        Piles.push_back(new Pile(600, 150 * (i + 1), false));
        Foundations.push_back(new Foundation(450, 150 * (i + 1)));
    }

    FileIO saveFile(Piles, Foundations);

    int pileNum = -1;
    dealOut(Piles, Foundations, curDeck);

    Kalimba.mc = Mix_LoadWAV("assets/Kalimba.wav");
    Kalimba.play(255, -1);

    while(1)
    {
        SDL_Event ev;
        drawIT(win, Piles, Foundations, dragging);

        while(SDL_PollEvent(&ev))
        {
            if( ev.type == SDL_QUIT)
            {
                SDL_Quit();
                return 0;
            }

            else if( ev.type == SDL_VIDEOEXPOSE )
            {
                cout << "expose!!" << endl;
                drawIT(win, Piles, Foundations, dragging);
            }
            else if( ev.type == SDL_MOUSEBUTTONDOWN )
            {

                if (ev.button.button == 3) // RE-DEALS, FOR DEBUGGING PURPOSES
                {
                    woosh.mc = Mix_LoadWAV("assets/woosh.wav");
                    woosh.play(255);
                    Deck NewDeck;
                    unDeal(Piles, Foundations);
                    dealOut(Piles, Foundations, NewDeck);
                }


                else if(ev.button.button == 1)
                {
                        for(unsigned k = 0; k < Piles.size(); k++)
                        {
                            if(!Piles[k]->isEmpty())
                            {
                                if(Piles[k]->getTopCard()->containsPoint(ev.button.x, ev.button.y))
                                {
                                    dragging = Piles[k]->getTopCard();
                                    dragging->setLocation(ev.motion.x, ev.motion.y); // ALLOWS A "SNAP-TO" EFFECT THAT I LIKE.
                                    pileNum = k;
                                }
                            }

                        }
                }

            }
            else if( ev.type == SDL_MOUSEBUTTONUP )
            {
                int x = ev.motion.x;
                int y = ev.motion.y;

                if(pileNum != -1)
                {
                    for (unsigned foundNum = 0; foundNum < Foundations.size(); foundNum++)
                    {
                        if(Foundations[foundNum]->getTopCard()->containsPoint(x, y))
                        {
                            Piles[pileNum]->removeTopCard();
                            if(dragging->rank == Foundations[foundNum]->getTopCard()->rank + 1 && dragging->suit == Foundations[foundNum]->getTopCard()->suit)
                            {
                                Foundations[foundNum]->addCard(dragging);
                                L.erase(I, L.end());
                                L.push_back(Move(dragging, pileNum, foundNum, true));
                                I = L.end();
                                cout << (*I).whereItsGoing << " " << (*I).index << " " << (*I).thisCard << " " << (*I).isFoundation << endl;
                            }
                            else
                                Piles[pileNum]->addCard(dragging);
                        }
                    }

                    for (unsigned whatPile = 0; whatPile < Piles.size(); whatPile++)
                    {
                        if(!Piles[whatPile]->isEmpty())
                        {

                            if(Piles[whatPile]->getTopCard()->containsPoint(ev.motion.x, ev.motion.y))
                            {
                                if(dragging->rank == Piles[whatPile]->getTopCard()->rank - 1)
                                {
                                    Piles[pileNum]->removeTopCard();
                                    Piles[whatPile]->addCard(dragging);
                                    L.erase(I, L.end());
                                    L.push_back(Move(dragging, pileNum, whatPile, false));
                                    I = L.end();
                                    cout << (*I).whereItsGoing << endl;
                                }
                                else
                                {
                                    Piles[pileNum]->removeTopCard();
                                    Piles[pileNum]->addCard(dragging);
                                }
                            }

                        }
                        else
                        {
                            if(x >= Piles[whatPile]->xCoord - 48 && x <= Piles[whatPile]->xCoord + 48)
                            {
                                if(y >= Piles[whatPile]->yCoord - 65 && y <= Piles[whatPile]->yCoord + 65)
                                {
                                    Piles[pileNum]->removeTopCard();
                                    Piles[whatPile]->addCard(dragging);
                                }
                            }
                        }
                    }
                    dragging = NULL;
                    pileNum = -1;
                }


            }
            else if( ev.type == SDL_MOUSEMOTION )
            {
                if (SDL_PeepEvents(&ev, 1, SDL_PEEKEVENT, SDL_MOUSEMOTIONMASK) == 0)
                {
                    drawIT(win, Piles, Foundations, dragging);
                    if(pileNum != -1)
                    {
                        int x = ev.motion.x;
                        int y = ev.motion.y;
                        dragging->setLocation(x,y);
                    }
                }

            }
            else if(ev.type == SDL_KEYDOWN)
            {
                int sym = ev.key.keysym.sym;
                if(sym == 'z' && I != L.begin())
                {
                    I--;
                    if((*I).isFoundation == true)
                    {
                        if(Foundations[(*I).whereItsGoing]->fCards.size() != 1)
                        {
                            Foundations[(*I).whereItsGoing]->removeTopCard();
                            Piles[(*I).index]->addCard((*I).thisCard);
                        }
                    }
                    else if((*I).isFoundation == false)
                    {
                            Piles[(*I).whereItsGoing]->removeTopCard();
                            Piles[(*I).index]->addCard((*I).thisCard);
                    }
                }

                else if(sym == 'y' && I != L.end())
                {
                    if((*I).isFoundation == true)
                    {
                        if(Piles[(*I).index]->cards.size() != 0)
                        {
                            Piles[(*I).index]->removeTopCard();
                            Foundations[(*I).whereItsGoing]->addCard((*I).thisCard);
                        }

                    }
                    else if((*I).isFoundation == false)
                    {
                        if(Piles[(*I).index]->cards.size() != 0)
                        {
                            Piles[(*I).index]->removeTopCard();
                            Piles[(*I).whereItsGoing]->addCard((*I).thisCard);
                        }
                    }
                    I++;
                }

                else if(sym == 'n') // NEW GAME.
                {
                    woosh.mc = Mix_LoadWAV("woosh.wav");
                    woosh.play(255);
                    Deck NewDeck;
                    unDeal(Piles, Foundations);
                    dealOut(Piles, Foundations, NewDeck);
                }

                else if(sym == 's')
                {
                    string temp;
                    cout << "File name? Must include '.txt' at the end of the name." << endl;
                    /* THIS IS TO PREVENT YOU FROM SAVING TO, SAY, A PDF FILE, OR SOME UNDEFINED "FILE" FILE. IT BOTHERED ME THAT THE
                       USER HAD THIS CAPABILITY, AND MY GUT TELLS ME THAT IT COULD CAUSE ISSUES, BUT FOR NOW THIS IS ONLY HERE
                       BECAUSE OF MY OCD. */
                    cin >> temp;

                    unsigned idx = temp.find(".txt");
                    if(idx == temp.npos)
                        cout << "Save Failed. Reason: Bad File Name" << endl;
                    else
                        saveFile.Save(temp);
                }

                else if(sym == 'l')
                {
                    string temp;
                    cout << "File name?" << endl;
                    cin >> temp;

                    L.erase(L.begin(), L.end());
                    saveFile.Load(temp);
                }

            }
        }
    }
    return 0;
}
