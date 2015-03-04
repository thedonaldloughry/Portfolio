#include <iostream>
#include <SDL.h>
#include <fstream>
#include <sstream>
#include "Deck.h"
#include "Pile.h"

void emptyOut(vector<Pile*> Piles, vector<Foundation*> Foundations) // needed for load
{
    for (unsigned m = 0; m < Piles.size(); m++)
    {
        for(int o = 0; o < Piles[m]->cards.size() + 6; o++)
        {
            if(!Piles[m]->cards.empty())
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


class FileIO
{
    public:
        vector<Pile*> Piles;
        vector<Foundation*> Foundations;

        FileIO(vector<Pile*>& P, vector<Foundation*>& F)
        {
            Piles = P;
            Foundations = F;
        }

        void Save(string fname)
        {

            ofstream out(fname.c_str(), ios::trunc);

            for (unsigned i = 0; i < Piles.size(); i++)
            {

                for(unsigned j = 0; j < Piles[i]->cards.size(); j++)
                {
                    out << Piles[i]->cards[j]->rank << " " << Piles[i]->cards[j]->suit <<  "\n";
                }
                out << "%" << "\n";
            }

            for (unsigned f = 0; f < Foundations.size(); f++)
            {
                out << Foundations[f]->fCards.top()->rank << " " << Foundations[f]->fCards.top()->suit << "\n";
                out << "$"<< "\n";
            }

            cout << "Save completed." << endl;
        }

        void Load(string fname)
        {


            ifstream in(fname.c_str());
            if(!in)
            {
                cout << "Load Failed. Reason: No File Found." << endl;
                return; // do not run this function if there is no file to be read.
            }

            int r, s, fr, fs;
            string str, foundStr;

            emptyOut(Piles, Foundations);


            for(unsigned p = 0; p < Piles.size(); p++)
            {
                getline(in, str, '%');
                istringstream iss(str);
                while(1)
                {
                    Suit tempSuit;
                    iss >> r >> s;
                    if(iss.fail())
                    {
                        break;
                    }

                    // temporary fix for enumerators
                    if(s == 0)
                        tempSuit = HEARTS;
                    else if(s == 1)
                        tempSuit = DIAMONDS;
                    else if(s == 2)
                        tempSuit = CLUBS;
                    else
                        tempSuit = SPADES;

                    Piles[p]->addCard(new Card(r, tempSuit));
                }
            }

            for(unsigned f = 0; f < Foundations.size(); f++)
            {
                getline(in, foundStr, '$');
                istringstream iss2(foundStr);
                while(1)
                {
                    Suit fTempSuit;
                    iss2 >> fr >> fs;
                    if(iss2.fail()) break;
                    cout << fr << " " << fs << endl;

                    // temporary fix for enumerators. may be more permanent than I thought.
                    if(fs == 0)
                        fTempSuit = HEARTS;
                    else if(fs == 1)
                        fTempSuit = DIAMONDS;
                    else if(fs == 2)
                        fTempSuit = CLUBS;
                    else
                        fTempSuit = SPADES;

                    Foundations[f]->addCard(new Card(fr, fTempSuit));
                }
            }

            cout << "Load completed" << endl;
        }

};
