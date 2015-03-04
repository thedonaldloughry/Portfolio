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
	float tolerance;

	SuperMesh(string fname, float tolerance = -1.0) // added tolerance attribute for outlines, defaults to -1.0, which doesn't draw outlines.
	{
		this->fname = fname;
		this->tolerance = tolerance;
		loaded = false;
	}

	void draw(Program* p)
	{
		for( unsigned i = 0; i < m.size(); i++)
		{
			m[i]->Draw(p);
			m[i]->tolerance = tolerance; // all meshes have the same outline tolerance, for simplicity's sake
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
        string FileName = fname.substr(0, fname.size() - 10); // slash the last 10 characters off of the string, removing ".spec.mesh"...
        FileName = FileName + ".bin"; //... and then we make it a .bin file*/
		for(unsigned i = 0;i < m.size(); i++)
        {
            m[i]->lineFileName = FileName;
            cout << "Loaded: " << FileName << endl;
        }

		loaded = true;
	}

	virtual ~SuperMesh()
	{
	    for(unsigned i = 0;i < m.size(); i++)
        {
            delete m[i]; //free memory allocated to every mesh in the Supermesh
        }
	}
};
