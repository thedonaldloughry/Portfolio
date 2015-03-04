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

	void draw() // WE NEED TO CALL THIS TO 'DRAW' THE VERTEX DATA INTO OUR FILE. JUST GO WITH IT.
	{
		for( unsigned i = 0; i < m.size(); i++)
		{
			m[i]->Draw();
			//p.setUniform(m[i]->)
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
			if(!in)
			{
				break;
			}

			if(s.find("binarymesh ") == 0)
			{
				s = s.substr(11);
				m.push_back(new Mesh(pfx + s));
				m.back()->Load();
			}
		}

		loaded = true;
	}
};
