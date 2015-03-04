// Date: 6/7/2014 12:54:54 AM
// Template version 1.1
// Java generated by Techne
// Keep in mind that you still need to fill in some blanks
// - ZeuX






package com.DonLoughry.AllOfTheEverything.model;

import net.minecraft.client.model.ModelBase;
import net.minecraft.client.model.ModelRenderer;
import net.minecraft.entity.Entity;

public class ModelFramePicture extends ModelBase
{
  //fields
    ModelRenderer Picture;
    ModelRenderer FramePart1;
    ModelRenderer FramePart2;
    ModelRenderer FramePart3;
    ModelRenderer FramePart4;
    ModelRenderer PictureStand;
  
  public ModelFramePicture()
  {
    textureWidth = 64;
    textureHeight = 64;
    
      Picture = new ModelRenderer(this, 16, 24);
      Picture.addBox(0F, -13F, 0F, 14, 13, 1);
      Picture.setRotationPoint(-7F, 23F, -3F);
      Picture.setTextureSize(64, 64);
      Picture.mirror = true;
      setRotation(Picture, -0.2094395F, 0F, 0F);
      FramePart1 = new ModelRenderer(this, 47, 24);
      FramePart1.addBox(0F, -13F, 0F, 1, 13, 1);
      FramePart1.setRotationPoint(7F, 23F, -3F);
      FramePart1.setTextureSize(64, 64);
      FramePart1.mirror = true;
      setRotation(FramePart1, -0.2094395F, 0F, 0F);
      FramePart2 = new ModelRenderer(this, 11, 24);
      FramePart2.addBox(0F, -13F, 0F, 1, 13, 1);
      FramePart2.setRotationPoint(-8F, 23F, -3F);
      FramePart2.setTextureSize(64, 64);
      FramePart2.mirror = true;
      setRotation(FramePart2, -0.2094395F, 0F, 0F);
      FramePart3 = new ModelRenderer(this, 14, 21);
      FramePart3.addBox(0F, -1F, -1F, 16, 1, 1);
      FramePart3.setRotationPoint(-8F, 10.6F, 0.65F);
      FramePart3.setTextureSize(64, 64);
      FramePart3.mirror = true;
      setRotation(FramePart3, -0.2094395F, 0F, 0F);
      FramePart4 = new ModelRenderer(this, 14, 39);
      FramePart4.addBox(0F, 0F, 0F, 16, 1, 1);
      FramePart4.setRotationPoint(-8F, 23F, -3F);
      FramePart4.setTextureSize(64, 64);
      FramePart4.mirror = true;
      setRotation(FramePart4, -0.2094395F, 0F, 0F);
      PictureStand = new ModelRenderer(this, 27, 42);
      PictureStand.addBox(0F, 0F, 0F, 2, 8, 2);
      PictureStand.setRotationPoint(-1F, 18F, -1.8F);
      PictureStand.setTextureSize(64, 64);
      PictureStand.mirror = true;
      setRotation(PictureStand, 0.5061455F, 0F, 0F);
  }
  
  public void render(Entity entity, float f, float f1, float f2, float f3, float f4, float f5)
  {
    super.render(entity, f, f1, f2, f3, f4, f5);
    setRotationAngles(f, f1, f2, f3, f4, f5, entity);
    Picture.render(f5);
    FramePart1.render(f5);
    FramePart2.render(f5);
    FramePart3.render(f5);
    FramePart4.render(f5);
    PictureStand.render(f5);
  }
  
  public void renderModel(float f)
  {
	Picture.render(f);
    FramePart1.render(f);
    FramePart2.render(f);
    FramePart3.render(f);
    FramePart4.render(f);
    PictureStand.render(f);
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
