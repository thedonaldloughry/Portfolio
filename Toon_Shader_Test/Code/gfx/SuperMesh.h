#ifndef _SuperMesh_H_
#define _SuperMesh_H_ NULL
#pragma once

#include "llgl.h"
#include "Mesh.h"
#include "assert.h"
#include <string>
#include <vector>
#include <stdexcept>
#include <iostream>
#include <fstream>
class SuperMesh
{
public:

	bool loaded;
	vector<Mesh*> m;
	string fname;

	SuperMesh(string fname)
	{
		this->fname = fname;
		loaded = false;
	}

	void makeOutlines()
	{
	    string FileName = fname.substr(0, fname.size() - 10); // slash the last 10 characters off of the string, removing ".spec.mesh"...
        FileName = FileName + ".bin"; //... and then we make it a .txt file*/
	    for( unsigned i = 0; i < m.size(); i++)
		{
		    m[i]->lineFileName = FileName;
            cout << "Loaded: " << FileName << endl; // this currently does not show up in the cmd window. I wonder why?
		}
	}

	void draw(Program& p, Program& lineProg)
	{
	    /*Drawing our objects now requires the program with the line-drawing vertex and fragment shader.*/
		for( unsigned i = 0; i < m.size(); i++)
		{
			m[i]->Draw(p);
			m[i]->DrawLines(lineProg);
		}
	}
	void load()
	{
		if(loaded) return;
		string pfx;
		string::size_type si = fname.rfind("/");
		if(si != string::npos)
			pfx = fname.substr(0, si + 1);

		ifstream in(fname.c_str());
		if(!in.good())
			throw runtime_error("No file:" + fname + "!");

		while(1)
		{
			string s;
			getline(in, s);
			cout << s << endl;
			if(!in)
			{
				break;
			}

			if(s.find("binarymesh ") == 0)
			{
				s = s.substr(11);
				m.push_back(new Mesh(pfx + s));
			}
		}
		makeOutlines();
		loaded = true;
	}
};

#endif _SuperMesh_H_
