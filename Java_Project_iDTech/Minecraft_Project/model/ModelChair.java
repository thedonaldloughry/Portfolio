package com.DonLoughry.AllOfTheEverything.model;

import net.minecraft.client.model.ModelBase;
import net.minecraft.client.model.ModelRenderer;
import net.minecraft.entity.Entity;

public class ModelChair extends ModelBase
{
  //fields
    ModelRenderer ChairBackBoard;
    ModelRenderer FrontRightLeg;
    ModelRenderer ChairBase;
    ModelRenderer FrontLeftLeg;
    ModelRenderer BackRightLeg;
    ModelRenderer BackLeftLeg;
  
  public ModelChair()
  {
    textureWidth = 64;
    textureHeight = 32;
    
      ChairBackBoard = new ModelRenderer(this, 16, 0);
      ChairBackBoard.addBox(0F, -18F, 0F, 16, 16, 1);
      ChairBackBoard.setRotationPoint(-8F, 16F, 5F);
      ChairBackBoard.setTextureSize(64, 32);
      ChairBackBoard.mirror = true;
      setRotation(ChairBackBoard, -0.1919862F, 0F, 0F);
      FrontRightLeg = new ModelRenderer(this, 57, 6);
      FrontRightLeg.addBox(0F, -10F, 0F, 1, 10, 1);
      FrontRightLeg.setRotationPoint(6F, 24F, -8F);
      FrontRightLeg.setTextureSize(64, 32);
      FrontRightLeg.mirror = true;
      setRotation(FrontRightLeg, -0.2443461F, 0F, 0F);
      ChairBase = new ModelRenderer(this, 5, 18);
      ChairBase.addBox(0F, 0F, 0F, 16, 1, 12);
      ChairBase.setRotationPoint(-8F, 14F, -6F);
      ChairBase.setTextureSize(64, 32);
      ChairBase.mirror = true;
      setRotation(ChairBase, 0F, 0F, 0F);
      FrontLeftLeg = new ModelRenderer(this, 11, 6);
      FrontLeftLeg.addBox(0F, -10F, 0F, 1, 10, 1);
      FrontLeftLeg.setRotationPoint(-7F, 24F, -8F);
      FrontLeftLeg.setTextureSize(64, 32);
      FrontLeftLeg.mirror = true;
      setRotation(FrontLeftLeg, -0.2443461F, 0F, 0F);
      BackRightLeg = new ModelRenderer(this, 51, 6);
      BackRightLeg.addBox(0F, -10F, 0F, 1, 10, 1);
      BackRightLeg.setRotationPoint(6F, 24F, 7F);
      BackRightLeg.setTextureSize(64, 32);
      BackRightLeg.mirror = true;
      setRotation(BackRightLeg, 0.2443461F, 0F, 0F);
      BackLeftLeg = new ModelRenderer(this, 5, 6);
      BackLeftLeg.addBox(0F, -10F, 0F, 1, 10, 1);
      BackLeftLeg.setRotationPoint(-7F, 24F, 7F);
      BackLeftLeg.setTextureSize(64, 32);
      BackLeftLeg.mirror = true;
      setRotation(BackLeftLeg, 0.2443461F, 0F, 0F);
  }
  
  public void render(Entity entity, float f, float f1, float f2, float f3, float f4, float f5)
  {
    super.render(entity, f, f1, f2, f3, f4, f5);
    setRotationAngles(f, f1, f2, f3, f4, f5, entity);
    ChairBackBoard.render(f5);
    FrontRightLeg.render(f5);
    ChairBase.render(f5);
    FrontLeftLeg.render(f5);
    BackRightLeg.render(f5);
    BackLeftLeg.render(f5);
  }
  
  public void renderModel(float f)
  {
	  // same as above, but stripped of animation preparation for simplicity's sake.
	  ChairBackBoard.render(f);
	  FrontRightLeg.render(f);
	  ChairBase.render(f);
	  FrontLeftLeg.render(f);
	  BackRightLeg.render(f);
	  BackLeftLeg.render(f);
  }
  
  private void setRotation(ModelRenderer model, float x, float y, float z)
  {
    model.rotateAngleX = x;
    model.rotateAngleY = y;
    model.rotateAngleZ = z;
  }
  
  public void setRotationAngles(float f, float f1, float f2, float f3, float f4, float f5, Entity entity)
  {
    super.setRotationAngles(f, f1, f2, f3, f4, f5, entity);
  }

}
