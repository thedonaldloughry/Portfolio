package com.DonLoughry.AllOfTheEverything.model;

import org.lwjgl.opengl.GL11;

import java.util.Random;

import com.DonLoughry.AllOfTheEverything.entity.EntityFish;
import cpw.mods.fml.relauncher.Side;
import cpw.mods.fml.relauncher.SideOnly;
import net.minecraft.client.model.ModelBase;
import net.minecraft.client.model.ModelRenderer;
import net.minecraft.entity.Entity;

@SideOnly(Side.CLIENT)
public class ModelFish extends ModelBase
{
  //fields
    public ModelRenderer HeadPiece1;
    public ModelRenderer HeadPiece2;
    public ModelRenderer BodyPiece1;
    public ModelRenderer BodyPiece2;
    public ModelRenderer BodyPiece3;
    public ModelRenderer BodyPiece4;
    public ModelRenderer TailPiece1;
    public ModelRenderer TailPiece2;
    public ModelRenderer TailPiece3;
    
    // create an animation cycle
    // for movement based animations you need to measure distance moved
    // and perform number of cycles per block distance moved.
    protected double distanceMovedTotal = 0.0D;
    // don't make this too large or animations will be skipped
    protected Random randNumber = new Random();
    
    protected static final double CYCLES_PER_BLOCK = 2.0D; 
    protected int cycleIndex = randNumber.nextInt(14);
    protected float[][] undulationCycle = new float[][]
    {
        { -10F, 0F, 10F, 0F, -10F, 0F },
        { -5F, 0F, 5F, 0F, -5F, 0F },
        { 0F, 0F, 0F, 0F, 0F, 0F },
        { -10F, 5F, 0F, 0F, 5F, 10F },
        { -25F, -10F, 0F, 0F, 10F, 25F },
        { -10F, -5F, 5F, 0F, 5F, 10F },
        { 10F, 0F, -10F, 0F, 10F, 0F },
        { 5F, 0F, -5F, 0F, 5F, 0F },
        { 0F, 0F, 0F, 0F, 0F, 0F },
        { 10F, 5F, 0F, 0F, -5F, -10F },
        { 25F, 10F, 0F, 0F, -10F, -25F },
        { 10F, 5F, 0F, 0F, -5F, -10F },
        { 5F, 0F, -5F, 0F, 5F, 0F },
        { 0F, 0F, 0F, 0F, 0F, 0F },
    };
  
  public ModelFish()
  {
    textureWidth = 64;
    textureHeight = 32;
    
      HeadPiece1 = new ModelRenderer(this, 7, 5);
      HeadPiece1.addBox(-1F, -2F, -1F, 2, 5, 3);
      HeadPiece1.setRotationPoint(0F, 17.5F, -6F);
      HeadPiece1.setTextureSize(64, 32);
      setRotation(HeadPiece1, 0F, 0F, 0F);
      
      HeadPiece2 = new ModelRenderer(this, 1, 7);
      HeadPiece2.addBox(-1F, -18F, 5F, 2, 3, 1);
      HeadPiece2.setRotationPoint(0F, 17F, -7F);
      HeadPiece2.setTextureSize(64, 32);
      HeadPiece1.addChild(HeadPiece2);
      setRotation(HeadPiece2, 0F, 0F, 0F);
      
      BodyPiece1 = new ModelRenderer(this, 17, 3);
      BodyPiece1.addBox(-1.533333F, -3F, -1F, 3, 7, 3);
      BodyPiece1.setRotationPoint(0F, 0F, 3F);
      BodyPiece1.setTextureSize(64, 32);
      HeadPiece1.addChild(BodyPiece1);
      setRotation(BodyPiece1, 0F, undulationCycle[0][1], 0F);
      
      BodyPiece2 = new ModelRenderer(this, 29, 2);
      BodyPiece2.addBox(-1.5F, -3.5F, -1F, 3, 8, 3);
      BodyPiece2.setRotationPoint(0F, 0F, 3F);
      BodyPiece2.setTextureSize(64, 32);
      BodyPiece1.addChild(BodyPiece2);
      setRotation(BodyPiece2, 0F, undulationCycle[0][2], 0F);
      
      BodyPiece3 = new ModelRenderer(this, 41, 3);
      BodyPiece3.addBox(-1.5F, -3F, -1F, 3, 7, 3);
      BodyPiece3.setRotationPoint(0F, 0F, 3F);
      BodyPiece3.setTextureSize(64, 32);
      BodyPiece2.addChild(BodyPiece3);
      setRotation(BodyPiece3, 0F, undulationCycle[0][3], 0F);
      
      BodyPiece4 = new ModelRenderer(this, 53, 4);
      BodyPiece4.addBox(-1F, -2F, -1F, 2, 5, 3);
      BodyPiece4.setRotationPoint(0F, 0F, 3F);
      BodyPiece4.setTextureSize(64, 32);
      BodyPiece3.addChild(BodyPiece4);
      setRotation(BodyPiece4, 0F, undulationCycle[0][4], 0F);
      
      TailPiece1 = new ModelRenderer(this, 15, 19);
      TailPiece1.addBox(-1F, -1F, -2F, 2, 3, 4);
      TailPiece1.setRotationPoint(0F, 0F, 3F);
      TailPiece1.setTextureSize(64, 32);
      BodyPiece4.addChild(TailPiece1);
      setRotation(TailPiece1, 0F, undulationCycle[0][5], 0F);
      
      TailPiece2 = new ModelRenderer(this, 27, 16);
      TailPiece2.addBox(-1F, -14F, -10F, 2, 1, 3);
      TailPiece2.setRotationPoint(0F, 15.5F, 11.5F);
      TailPiece2.setTextureSize(64, 32);
      TailPiece1.addChild(TailPiece2);
      setRotation(TailPiece2, 0F, undulationCycle[0][5], 0F);
      
      TailPiece3 = new ModelRenderer(this, 27, 24);
      TailPiece3.addBox(-1F, -21F, -10F, 2, 1, 3);
      TailPiece3.setRotationPoint(0F, 19.5F, 11.5F);
      TailPiece3.setTextureSize(64, 32);
      TailPiece1.addChild(TailPiece3);
      setRotation(TailPiece3, 0F, undulationCycle[0][5], 0F);
  }
  
  /**
   * Sets the model's various rotation angles then renders the model.
   */
  @Override
  public void render(Entity parEntity, float parTime, float parSwingSuppress, 
        float par4, float parHeadAngleY, float parHeadAngleX, float par7)
  {
      // best to cast to actual expected entity, to allow access to custom fields 
      // related to animation
      renderFish((EntityFish) parEntity, parTime, parSwingSuppress, par4, 
            parHeadAngleY, parHeadAngleX, par7);
  }
  
  public void renderFish(EntityFish parEntity, float parTime, float parSwingSuppress, 
        float par4, float parHeadAngleY, float parHeadAngleX, float par7)
  {
      setRotationAngles(parTime, parSwingSuppress, par4, parHeadAngleY, parHeadAngleX, 
            par7, parEntity);

      // scale the whole thing for big or small entities
      GL11.glPushMatrix();
      GL11.glScalef(parEntity.getScaleFactor(), parEntity.getScaleFactor(), 
            parEntity.getScaleFactor());

      if (this.isChild)
      {
          float childScaleFactor = 0.5F;
          GL11.glPushMatrix();
          GL11.glScalef(1.0F * childScaleFactor, 1.0F * childScaleFactor, 1.0F 
                * childScaleFactor);
          GL11.glTranslatef(0.0F, 24.0F * par7, 0.0F);
          //HeadPiece2.render(par7);
          this.HeadPiece1.render(par7);
          //TailPiece2.render(par7);
          //TailPiece3.render(par7);
          
          // Do a single - frame idle animation.

          if (parEntity.ticksExisted%60==0 && parSwingSuppress <= 0.1F) 
          {
        	  //tongue.render(par7);
        	  System.out.println("Trigger Idle Animation on Fish Child");
          } 
          //BodyPiece1.render(par7); // all rest of body are children of body1
          GL11.glPopMatrix();
      }
      else
      {
          //HeadPiece2.render(par7);
          this.HeadPiece1.render(par7);
          //TailPiece2.render(par7);
          //TailPiece3.render(par7);
          
          // flick tongue occasionally

          if (parEntity.ticksExisted%60==0 && parSwingSuppress <= 0.1F) 
          {
        	  //tongue.render(par7);
        	  System.out.println("Trigger Idle Animation on Fish");
          } 
          //BodyPiece1.render(par7); // all rest of body are children of body1
      }

      // don't forget to pop the matrix for overall scaling
      GL11.glPopMatrix();
  }

  @Override
  public void setRotationAngles(float parTime, float parSwingSuppress, float par3, 
        float parHeadAngleY, float parHeadAngleX, float par6, Entity parEntity)
  {
      // animate if moving        
      updateDistanceMovedTotal(parEntity);
      cycleIndex = (int) ((getDistanceMovedTotal(parEntity)*CYCLES_PER_BLOCK)
            %undulationCycle.length);
      // DEBUG
      //System.out.println("ModelSerpent setRotationAngles(), distanceMoved ="
            //+getDistanceMovedTotal(parEntity)+", cycleIndex ="+cycleIndex);
      this.HeadPiece1.rotateAngleY = degToRad(undulationCycle[cycleIndex][0]) ;
      this.BodyPiece1.rotateAngleY = degToRad(undulationCycle[cycleIndex][1]) ;
      this.BodyPiece2.rotateAngleY = degToRad(undulationCycle[cycleIndex][2]) ;
      this.BodyPiece3.rotateAngleY = degToRad(undulationCycle[cycleIndex][3]) ;
      this.BodyPiece4.rotateAngleY = degToRad(undulationCycle[cycleIndex][4]) ;
      this.TailPiece1.rotateAngleY = degToRad(undulationCycle[cycleIndex][5]) ;
  }
  
  protected void updateDistanceMovedTotal(Entity parEntity) 
  {
      distanceMovedTotal += parEntity.getDistance(parEntity.prevPosX, parEntity.prevPosY, 
            parEntity.prevPosZ);
  }
  
  protected double getDistanceMovedTotal(Entity parEntity) 
  {
      return (distanceMovedTotal);
  }

  protected float degToRad(float degrees)
  {
      return degrees * (float)Math.PI / 180 ;
  }
  
  protected void setRotation(ModelRenderer model, float rotX, float rotY, float rotZ)
  {
      model.rotateAngleX = degToRad(rotX);
      model.rotateAngleY = degToRad(rotY);
      model.rotateAngleZ = degToRad(rotZ);        
  }

  // spin methods are good for testing and debug rotation points and offsets in the model
  protected void spinX(ModelRenderer model)
  {
      model.rotateAngleX += degToRad(0.5F);
  }
  
  protected void spinY(ModelRenderer model)
  {
      model.rotateAngleY += degToRad(0.5F);
  }
  
  protected void spinZ(ModelRenderer model)
  {
      model.rotateAngleZ += degToRad(0.5F);
  }

}
