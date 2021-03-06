// Date: 6/7/2014 3:20:01 AM
// Template version 1.1
// Java generated by Techne
// Keep in mind that you still need to fill in some blanks
// - ZeuX






package com.DonLoughry.AllOfTheEverything.model;

import net.minecraft.client.model.ModelBase;
import net.minecraft.client.model.ModelRenderer;
import net.minecraft.entity.Entity;

public class ModelCouch extends ModelBase
{
  //fields
    ModelRenderer BottomCushion;
    ModelRenderer TopCushion;
    ModelRenderer CouchBack;
    ModelRenderer ArmLeft;
    ModelRenderer ArmRight;
  
  public ModelCouch()
  {
    textureWidth = 128;
    textureHeight = 128;
    
      BottomCushion = new ModelRenderer(this, 20, 97);
      BottomCushion.addBox(0F, 0F, 0F, 30, 5, 14);
      BottomCushion.setRotationPoint(-15F, 19F, -7F);
      BottomCushion.setTextureSize(128, 128);
      BottomCushion.mirror = true;
      setRotation(BottomCushion, 0F, 0F, 0F);
      TopCushion = new ModelRenderer(this, 20, 78);
      TopCushion.addBox(0F, 0F, 0F, 30, 3, 14);
      TopCushion.setRotationPoint(-15F, 16F, -7F);
      TopCushion.setTextureSize(128, 128);
      TopCushion.mirror = true;
      setRotation(TopCushion, 0F, 0F, 0F);
      CouchBack = new ModelRenderer(this, 30, 56);
      CouchBack.addBox(0F, 0F, 0F, 30, 16, 4);
      CouchBack.setRotationPoint(-15F, 8F, 4F);
      CouchBack.setTextureSize(128, 128);
      CouchBack.mirror = true;
      setRotation(CouchBack, 0F, 0F, 0F);
      ArmLeft = new ModelRenderer(this, 5, 26);
      ArmLeft.addBox(0F, 0F, 0F, 4, 12, 16);
      ArmLeft.setRotationPoint(12F, 12F, -8F);
      ArmLeft.setTextureSize(128, 128);
      ArmLeft.mirror = true;
      setRotation(ArmLeft, 0F, 0F, 0F);
      ArmRight = new ModelRenderer(this, 83, 26);
      ArmRight.addBox(0F, 0F, 0F, 4, 12, 16);
      ArmRight.setRotationPoint(-16F, 12F, -8F);
      ArmRight.setTextureSize(128, 128);
      ArmRight.mirror = true;
      setRotation(ArmRight, 0F, 0F, 0F);
  }
  
  public void render(Entity entity, float f, float f1, float f2, float f3, float f4, float f5)
  {
    super.render(entity, f, f1, f2, f3, f4, f5);
    setRotationAngles(f, f1, f2, f3, f4, f5, entity);
    BottomCushion.render(f5);
    TopCushion.render(f5);
    CouchBack.render(f5);
    ArmLeft.render(f5);
    ArmRight.render(f5);
  }
  
  public void renderModel(float f)
  {
    BottomCushion.render(f);
    TopCushion.render(f);
    CouchBack.render(f);
    ArmLeft.render(f);
    ArmRight.render(f);
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
