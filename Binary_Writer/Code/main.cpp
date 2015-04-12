/*
* This is the BinaryWriter project, which creates outline-defining .txt files. Please see the documentation for more information.
*
* - Donald Loughry II, Programmer
*/

#include <iostream>
#include "llgl.h"
#include <fstream>
#include <vector>
#include "SuperMesh.h"

using namespace std;
using namespace llgl;

struct Vertex
{
    float x,y,z,w;
    float s,t,p,q;
    float nx,ny,nz,nw;
};

bool isFileAlright(string fName)
{
	/* Determine if the file given exists and is usable. */
    ifstream in(fName.c_str());
    if(!in.good())
        return false;
    return true;
}

int main(int argc, char* argv[])
{
    // INPUT FILE NAME //
    string fName;
    while(!isFileAlright(fName))
    {
        cout << "Enter the path to your spec.mesh file here: ";
        cin >> fName;
    }
    SuperMesh* Model = new SuperMesh(fName.c_str());
    // END INPUT //

    Model->load();
    Model->draw(); // this fake "draw" loads all the vertex data in our supermesh.//

	// Here is where we create the name of our .bin file, using the name of the model file given by the user. //
    string fname = Model->fname;
    string FileName = fname.substr(0, fname.size() - 10); // supposed to slash the last 10 characters off of the string, removing ".spec.mesh"...
    FileName = FileName + ".bin"; //... and then we make it a .bin file*/
    cout << FileName << endl;
	////////////////////////////////////////////////////////////////////////////////////////////////////////////

    ofstream out(FileName.c_str(), ios::binary);
    for (unsigned w = 0; w < Model->m.size(); w++)
    {
        vector<float> &vdata = Model->m[w]->vdata; // Get a reference to model vertex data.
        vector<char> &idata = Model->m[w]->idata; // Get a reference to model index data.

        //Create a vertex and index variable, a map for Edge Mesh, perform two loops to analyze all triangles on a mesh and write out their vertex values to a file.//
        Vertex* V = (Vertex*)(&vdata[0]);

        unsigned short* I16 = (unsigned short*)(&idata[0]);
        unsigned char* I8 = (unsigned char*)(&idata[0]);
        unsigned int* I32 = (unsigned int*)(&idata[0]);

        map<set<int>, vector<vec3> > EM;
        Mesh* curMesh = Model->m[w];
        for(unsigned i = 0; i < curMesh->ic; i += 3) // 3 because we're looking at triangles //
        {
			/*
				Here's the messy bit of our code. We need to iterate through every vertex on our model to create an
				edge map, which I have called EM. Here is an outline of our steps:
				
				1. Initialize three int variables, and then check to see if our mesh file is using bytes, shorts, or another data type,
				and depending on this, pack our ints into I8, I16, or I32 index data references accordingly.
				2. Create three vectors, one for each point on our current triangle. Then, use these vectors to create two more vectors,
				which both point from a corner of the triangle to a chosen third point. The cross product of these two vectors is our triangle's
				normal vector.
				3. For three pairs of triangle corners -- (point 1, point 2),(point 2, point 3), (point 3, point 1) -- create an integer set.
				Our edge map indexed at each integer set is given the triangle's normal position.
				
				*** A Note About the Edge Map ***
				Step 3 looks a little weird at first glance, so it is important to note that the purpose of our Edge Map's existence is to associate
				each vertex pair on a triangle with that triangle's normal -- this is vital when we go to do calculations that involve the camera,
				as we need a way to determine, given the edge's normal and the camera's "looking" vector, whether or not we need a line to be drawn
				at all.
				
				The for loop following this one iterates through our edge map and writes all of it's data to a file. The syntax here is funky, but
				hopefully the basic functionality can be understood.
			*/
			// STEP 1 //
            int i1;
            int i2;
            int i3;
            if( curMesh->ise == GL_UNSIGNED_BYTE)
            {
                i1 = I8[i];
                i2 = I8[i + 1];
                i3 = I8[i + 2];
            }
            else if( curMesh->ise == GL_UNSIGNED_SHORT)
            {
                i1 = I16[i];
                i2 = I16[i + 1];
                i3 = I16[i + 2];
            }
            else
            {
                i1 = I32[i];
                i2 = I32[i + 1];
                i3 = I32[i + 2];
            }
			////////////
			// STEP 2 //
            vec3 p = vec3(V[i1].x, V[i1].y, V[i1].z); // to represent the point in 3D space of each vertex on every triangle on the mesh
            vec3 q = vec3(V[i2].x, V[i2].y, V[i2].z);
            vec3 r = vec3(V[i3].x, V[i3].y, V[i3].z);
            vec3 v1 = p - q;
            vec3 v2 = r - q;
            vec3 n = cross(v2,v1); //important to make sure the order is correct here, do VECTOR TWO cross VECTOR ONE//
			////////////
			// STEP 3 //
            set<int> tmp;
            tmp.insert(i1); tmp.insert(i2);
            EM[tmp].push_back(n);
            set<int> tmp2;
            tmp2.insert(i2); tmp2.insert(i3);
            EM[tmp2].push_back(n);
            set<int> tmp3;
            tmp3.insert(i3); tmp3.insert(i1);
            EM[tmp3].push_back(n);
			////////////
            //we have now pushed every needed point into our edge map
        }
        vec3 norm2;
        for(map<set<int>, vector<vec3> >::iterator it = EM.begin(); it != EM.end(); ++it) // The problem is here. The for loop does not iterate through all of the edges.
        {
            //Now we will take our edge map and write its data to the file!//
            /* Information is written to the file in this form:
            Vertex One, Vertex Two, Normal One, Normal Two, r (where r, depending on its value, determines whether one edge is on top of the other in the case
                                                                                    where two edges are aligned with one another)
            */
			// Determine which vertex pair we are looking at. //
            set<int>::iterator tmp = it->first.begin();
            int pi = *tmp;
            tmp++;
            int qi = *tmp;
            Vertex One = V[pi];
            Vertex Two = V[qi];
			////////////////////////////////////////////////////
			// What is the normal vector associated with the current vertex pair? //
            vec3 norm1 = it->second[0];
            if(it->second.size() == 1) // Does the current vertex pair have only 1 normal associated with it? (Imagine a triangle that is NOT ATTACHED to any other triangle...)
                norm2 = -1 * norm1; // If so, the other normal that we'll use to do our calculations will be the opposite of the current normal. Edges will always be detected.
            else
                norm2 = it->second[1]; // Otherwise, we have a second normal that we can use.
			////////////////////////////////////////////////////////////////////////
			// Now, we write a bunch of data to our binary file! //
            out.write((char*) &One, 12);
            out.write((char*) &Two, 12);
            out.write((char*) &norm1, 12);
            out.write((char*) &norm2, 12);
            float r = 0;
			/*
				Note: the "r" variable is used to differentiate edges from each other. It is useful for determining if we have two edges that are disconnected
				but overlapping -- in which case, we only want to draw a line for one of the edges and not the other.
			*/
            out.write((char*) &r, 4);
            out.write((char*) &One, 12);
            out.write((char*) &Two, 12);
            out.write((char*) &norm1, 12);
            out.write((char*) &norm2, 12);
            r = 1;
            out.write((char*) &r, 4);
			///////////////////////////////////////////////////////
        }
    }
    return 0;
}
