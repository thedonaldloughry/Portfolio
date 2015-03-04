package com.DonLoughry.AllOfTheEverything.model;

import net.minecraft.client.model.ModelBase;
import net.minecraft.client.model.ModelRenderer;
import net.minecraft.entity.Entity;

public class ModelDeskLamp extends ModelBase
{
  //fields
    ModelRenderer Base;
    ModelRenderer LampPiece1;
    ModelRenderer LampPiece2;
    ModelRenderer LampPiece3;
    ModelRenderer LampPiece4;
    ModelRenderer Lamp1;
    ModelRenderer Lamp2;
  
  public ModelDeskLamp()
  {
    textureWidth = 64;
    textureHeight = 64;
    
      Base = new ModelRenderer(this, 20, 56);
      Base.addBox(0F, 0F, 0F, 6, 1, 6);
      Base.setRotationPoint(-3F, 23F, -3F);
      Base.setTextureSize(64, 64);
      Base.mirror = true;
      setRotation(Base, 0F, 0F, 0F);
      LampPiece1 = new ModelRenderer(this, 28, 50);
      LampPiece1.addBox(0F, 0F, 0F, 2, 3, 2);
      LampPiece1.setRotationPoint(-1F, 21F, -1F);
      LampPiece1.setTextureSize(64, 64);
      LampPiece1.mirror = true;
      setRotation(LampPiece1, 0F, 0F, 0F);
      LampPiece2 = new ModelRenderer(this, 25, 38);
      LampPiece2.addBox(0F, -11F, 0F, 0, 11, 1);
      LampPiece2.setRotationPoint(-1F, 22F, 0F);
      LampPiece2.setTextureSize(64, 64);
      LampPiece2.mirror = true;
      setRotation(LampPiece2, -0.4363323F, 0F, 0F);
      LampPiece3 = new ModelRenderer(this, 37, 38);
      LampPiece3.addBox(0F, 0F, 0F, 0, 11, 1);
      LampPiece3.setRotationPoint(1F, 12F, 4.5F);
      LampPiece3.setTextureSize(64, 64);
      LampPiece3.mirror = true;
      setRotation(LampPiece3, -0.4363323F, 0F, 0F);
      LampPiece4 = new ModelRenderer(this, 29, 33);
      LampPiece4.addBox(0F, -8F, 0F, 2, 8, 1);
      LampPiece4.setRotationPoint(-1F, 13F, 4.3F);
      LampPiece4.setTextureSize(64, 64);
      LampPiece4.mirror = true;
      setRotation(LampPiece4, 1.047198F, 0F, 0F);
      Lamp1 = new ModelRenderer(this, 26, 27);
      Lamp1.addBox(0F, -3F, 0F, 4, 3, 2);
      Lamp1.setRotationPoint(-2F, 11F, -3F);
      Lamp1.setTextureSize(64, 64);
      Lamp1.mirror = true;
      setRotation(Lamp1, 0.4712389F, 0F, 0F);
      Lamp2 = new ModelRenderer(this, 22, 17);
      Lamp2.addBox(0F, -5F, 0F, 6, 5, 4);
      Lamp2.setRotationPoint(-3F, 14F, -6F);
      Lamp2.setTextureSize(64, 64);
      Lamp2.mirror = true;
      setRotation(Lamp2, 0.4712389F, 0F, 0F);
  }
  
  public void render(Entity entity, float f, float f1, float f2, float f3, float f4, float f5)
  {
    super.render(entity, f, f1, f2, f3, f4, f5);
    setRotationAngles(f, f1, f2, f3, f4, f5, entity);
    Base.render(f5);
    LampPiece1.render(f5);
    LampPiece2.render(f5);
    LampPiece3.render(f5);
    LampPiece4.render(f5);
    Lamp1.render(f5);
    Lamp2.render(f5);
  }
  
  public void renderModel(float f)
  {
	Base.render(f);
	LampPiece1.render(f);
    LampPiece2.render(f);
    LampPiece3.render(f);
    LampPiece4.render(f);
    Lamp1.render(f);
    Lamp2.render(f);
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
