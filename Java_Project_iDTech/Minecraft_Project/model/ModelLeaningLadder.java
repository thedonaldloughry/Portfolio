// Date: 6/9/2014 12:33:45 AM
// Template version 1.1
// Java generated by Techne
// Keep in mind that you still need to fill in some blanks
// - ZeuX






package com.DonLoughry.AllOfTheEverything.model;

import net.minecraft.client.model.ModelBase;
import net.minecraft.client.model.ModelRenderer;
import net.minecraft.entity.Entity;

public class ModelLeaningLadder extends ModelBase
{
  //fields
    ModelRenderer PostLeft;
    ModelRenderer PostRight;
    ModelRenderer Rung1;
    ModelRenderer Rung2;
    ModelRenderer Rung3;
    ModelRenderer Rung4;
    ModelRenderer Rung5;
    ModelRenderer Rung6;
    ModelRenderer Top;
  
  public ModelLeaningLadder()
  {
    textureWidth = 64;
    textureHeight = 64;
    
      PostLeft = new ModelRenderer(this, 10, 14);
      PostLeft.addBox(0F, -48F, 0F, 1, 48, 1);
      PostLeft.setRotationPoint(-8F, 24F, -8F);
      PostLeft.setTextureSize(64, 64);
      PostLeft.mirror = true;
      setRotation(PostLeft, -0.2094395F, 0F, 0F);
      PostRight = new ModelRenderer(this, 48, 14);
      PostRight.addBox(0F, -48F, 0F, 1, 48, 1);
      PostRight.setRotationPoint(7F, 24F, -8F);
      PostRight.setTextureSize(64, 64);
      PostRight.mirror = true;
      setRotation(PostRight, -0.2094395F, 0F, 0F);
      Rung1 = new ModelRenderer(this, 16, 59);
      Rung1.addBox(0F, -3F, 0F, 14, 3, 1);
      Rung1.setRotationPoint(-7F, 20F, -7.1F);
      Rung1.setTextureSize(64, 64);
      Rung1.mirror = true;
      setRotation(Rung1, -0.2094395F, 0F, 0F);
      Rung2 = new ModelRenderer(this, 16, 50);
      Rung2.addBox(0F, 0F, 0F, 14, 3, 1);
      Rung2.setRotationPoint(-7F, 10F, -5F);
      Rung2.setTextureSize(64, 64);
      Rung2.mirror = true;
      setRotation(Rung2, -0.2094395F, 0F, 0F);
      Rung3 = new ModelRenderer(this, 16, 41);
      Rung3.addBox(0F, 0F, 0F, 14, 3, 1);
      Rung3.setRotationPoint(-7F, 3F, -3.5F);
      Rung3.setTextureSize(64, 64);
      Rung3.mirror = true;
      setRotation(Rung3, -0.2094395F, 0F, 0F);
      Rung4 = new ModelRenderer(this, 16, 32);
      Rung4.addBox(0F, 0F, 0F, 14, 3, 1);
      Rung4.setRotationPoint(-7F, -4F, -2F);
      Rung4.setTextureSize(64, 64);
      Rung4.mirror = true;
      setRotation(Rung4, -0.2094395F, 0F, 0F);
      Rung5 = new ModelRenderer(this, 16, 23);
      Rung5.addBox(0F, 0F, 0F, 14, 3, 1);
      Rung5.setRotationPoint(-7F, -11F, -0.5F);
      Rung5.setTextureSize(64, 64);
      Rung5.mirror = true;
      setRotation(Rung5, -0.2094395F, 0F, 0F);
      Rung6 = new ModelRenderer(this, 16, 14);
      Rung6.addBox(0F, 0F, 0F, 14, 3, 1);
      Rung6.setRotationPoint(-7F, -18F, 1F);
      Rung6.setTextureSize(64, 64);
      Rung6.mirror = true;
      setRotation(Rung6, -0.2094395F, 0F, 0F);
      Top = new ModelRenderer(this, 5, 4);
      Top.addBox(0F, 0F, 0F, 18, 1, 8);
      Top.setRotationPoint(-9F, -23F, 0F);
      Top.setTextureSize(64, 64);
      Top.mirror = true;
      setRotation(Top, 0F, 0F, 0F);
  }
  
  public void render(Entity entity, float f, float f1, float f2, float f3, float f4, float f5)
  {
    super.render(entity, f, f1, f2, f3, f4, f5);
    setRotationAngles(f, f1, f2, f3, f4, f5, entity);
    PostLeft.render(f5);
    PostRight.render(f5);
    Rung1.render(f5);
    Rung2.render(f5);
    Rung3.render(f5);
    Rung4.render(f5);
    Rung5.render(f5);
    Rung6.render(f5);
    Top.render(f5);
  }
  
  public void renderModel(float f)
  {
    PostLeft.render(f);
    PostRight.render(f);
    Rung1.render(f);
    Rung2.render(f);
    Rung3.render(f);
    Rung4.render(f);
    Rung5.render(f);
    Rung6.render(f);
    Top.render(f);
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
