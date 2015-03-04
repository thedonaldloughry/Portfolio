/* Not original work.
Source: http://www.ogre3d.org/tikiwiki/tiki-index.php?page=BulletDebugDrawer
*/

#include "stdafx.h"
#include "DebugDrawer.h"
#include "OgreBulletUtils.h"
 
using namespace Ogre;

//Interpreting the debug draw output
//
//    If your object is drawn with a red wireframe that indicates the object is 'deactivated' and will not be subject to forces in the simulation.
//    A green wireframe indicates it's active. 
 
OgreDebugDrawer::OgreDebugDrawer( SceneManager *scm )
{
    mContactPoints = &mContactPoints1;
    mLines = new ManualObject("physics lines");
    //ASSERT( mLines );
    mTriangles = new ManualObject("physics triangles");
    //ASSERT( mTriangles );
    mLines->setDynamic(true);
    mTriangles->setDynamic(true);
    //mLines->estimateVertexCount( 100000 );
    //mLines->estimateIndexCount( 0 );
 
    scm->getRootSceneNode()->attachObject( mLines );
    scm->getRootSceneNode()->attachObject( mTriangles );
 
    static const char * matName = "OgreBulletCollisionsDebugDefault";
    MaterialPtr mtl = MaterialManager::getSingleton().getDefaultSettings()->clone(matName);
    mtl->setReceiveShadows(false);
    mtl->setSceneBlending( SBT_TRANSPARENT_ALPHA );
    mtl->setDepthBias( 0.1f, 0 );
    TextureUnitState * tu = mtl->getTechnique(0)->getPass(0)->createTextureUnitState();
   // ASSERT( tu );
    tu->setColourOperationEx( LBX_SOURCE1, LBS_DIFFUSE );
    mtl->getTechnique(0)->setLightingEnabled(false);
    //mtl->getTechnique(0)->setSelfIllumination( ColourValue::White ); 
 
    mLines->begin( matName, RenderOperation::OT_LINE_LIST );
    mLines->position( Vector3::ZERO );
    mLines->colour( ColourValue::Blue );
    mLines->position( Vector3::ZERO );
    mLines->colour( ColourValue::Blue );
 
    mTriangles->begin( matName, RenderOperation::OT_TRIANGLE_LIST );
    mTriangles->position( Vector3::ZERO );
    mTriangles->colour( ColourValue::Blue );
    mTriangles->position( Vector3::ZERO );
    mTriangles->colour( ColourValue::Blue );
    mTriangles->position( Vector3::ZERO );
    mTriangles->colour( ColourValue::Blue );
 
    mDebugModes = (DebugDrawModes) DBG_DrawWireframe;
    Root::getSingleton().addFrameListener(this);
}
 
OgreDebugDrawer::~OgreDebugDrawer()
{
    Root::getSingleton().removeFrameListener(this);
    delete mLines;
    delete mTriangles;
}
 
void OgreDebugDrawer::drawLine( const btVector3 &from, const btVector3 &to, const btVector3 &color )
{
    ColourValue c( color.getX(), color.getY(), color.getZ() );  
    c.saturate();
    mLines->position( cvt(from) );
    mLines->colour( c );
    mLines->position( cvt(to) );
    mLines->colour( c );
}
 
void OgreDebugDrawer::drawTriangle( const btVector3 &v0, const btVector3 &v1, const btVector3 &v2, const btVector3 &color, btScalar alpha )
{
    ColourValue c( color.getX(), color.getY(), color.getZ(), alpha );  
    c.saturate();
    mTriangles->position( cvt(v0) );
    mTriangles->colour( c );
    mTriangles->position( cvt(v1) );
    mTriangles->colour( c );
    mTriangles->position( cvt(v2) );
    mTriangles->colour( c );
}
 
void OgreDebugDrawer::drawContactPoint( const btVector3 &PointOnB, const btVector3 &normalOnB, btScalar distance, int lifeTime, const btVector3 &color )
{
    mContactPoints->resize( mContactPoints->size() + 1 );
    ContactPoint p = mContactPoints->back();
    p.from = cvt( PointOnB );
    p.to = p.from + cvt( normalOnB ) * distance;
    p.dieTime = Root::getSingleton().getTimer()->getMilliseconds() + lifeTime;
    p.color.r = color.x();
    p.color.g = color.y();
    p.color.b = color.z();
}
 
bool OgreDebugDrawer::frameStarted( const Ogre::FrameEvent& evt )
{
    size_t now = Root::getSingleton().getTimer()->getMilliseconds();
    std::vector< ContactPoint > *newCP = mContactPoints == &mContactPoints1 ? &mContactPoints2 : &mContactPoints1;
    for ( std::vector< ContactPoint >::iterator i = mContactPoints->begin(); i < mContactPoints->end(); i++ ){
        ContactPoint &cp = *i;
        mLines->position( cp.from );
        mLines->colour( cp.color );
        mLines->position( cp.to );
        if ( now <= cp.dieTime  )
            newCP->push_back( cp );
    }
    mContactPoints->clear();
    mContactPoints = newCP;
 
    mLines->end();
    mTriangles->end();
 
    return true;
}
 
bool OgreDebugDrawer::frameEnded( const Ogre::FrameEvent& evt )
{
    mLines->beginUpdate(0);
    mTriangles->beginUpdate(0);
    return true;
}
 
void OgreDebugDrawer::reportErrorWarning( const char *warningString )
{
    LogManager::getSingleton().getDefaultLog()->logMessage( warningString );
}
 
void OgreDebugDrawer::draw3dText( const btVector3 &location, const char *textString )
{
 
}
 
void OgreDebugDrawer::setDebugMode( int debugMode )
{
    mDebugModes = (DebugDrawModes) debugMode;
}
 
int OgreDebugDrawer::getDebugMode() const
{
    return mDebugModes;
}

/*
Source: http://www.ogre3d.org/tikiwiki/tiki-index.php?page=BulletDebugDrawer
*/