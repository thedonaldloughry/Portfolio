// Date: 7/25/2014 2:05:51 AM
// Template version 1.1
// Java generated by Techne
// Keep in mind that you still need to fill in some blanks
// - ZeuX






package com.DonLoughry.AllOfTheEverything.model;

import net.minecraft.client.model.ModelBase;
import net.minecraft.client.model.ModelRenderer;
import net.minecraft.entity.Entity;
import net.minecraft.util.MathHelper;

public class ModelBlizzard extends ModelBase
{
  //fields
    ModelRenderer Body;
    ModelRenderer Head;
    ModelRenderer BRLeg;
    ModelRenderer FRLeg;
    ModelRenderer BLLeg;
    ModelRenderer FLLeg;
    ModelRenderer Tail;
  
  public ModelBlizzard()
  {
    textureWidth = 64;
    textureHeight = 32;
    setTextureOffset("Body.BLShoulder", 44, 7);
    setTextureOffset("Body.BodyCenter", 18, 7);
    setTextureOffset("Body.BRShoulder", 12, 7);
    setTextureOffset("Body.FRShoulder", 12, 20);
    setTextureOffset("Body.FLShoulder", 44, 20);
    setTextureOffset("Head.HeadMain", 23, 24);
    setTextureOffset("Head.Neck", 28, 20);
    setTextureOffset("BRLeg.BRLegPiece1", 12, 11);
    setTextureOffset("BRLeg.BRLegPiece2", 12, 14);
    setTextureOffset("BRLeg.BRFoot", 10, 16);
    setTextureOffset("FRLeg.FRLegPiece1", 12, 24);
    setTextureOffset("FRLeg.FRLegPiece2", 12, 27);
    setTextureOffset("FRLeg.FRFoot", 10, 29);
    setTextureOffset("BLLeg.BLLegPiece1", 44, 11);
    setTextureOffset("BLLeg.BLLegPiece2", 46, 14);
    setTextureOffset("BLLeg.BLFoot", 44, 16);
    setTextureOffset("FLLeg.FLLegPiece1", 44, 24);
    setTextureOffset("FLLeg.FLLegPiece2", 46, 27);
    setTextureOffset("FLLeg.FLFoot", 46, 29);
    setTextureOffset("Tail.TailPiece1", 14, 1);
    setTextureOffset("Tail.TailPiece2", 26, 0);
    setTextureOffset("Tail.TailPiece3", 38, 0);
    
    Body = new ModelRenderer(this, "Body");
    Body.setRotationPoint(0F, 21F, 0F);
    setRotation(Body, 0F, 0F, 0F);
    Body.mirror = true;
      Body.addBox("BLShoulder", 2F, -1F, 3F, 1, 2, 2);
      Body.addBox("BodyCenter", -2F, -1F, -4F, 4, 3, 9);
      Body.addBox("BRShoulder", -3F, -1F, 3F, 1, 2, 2);
      Body.addBox("FRShoulder", -3F, -1F, -3F, 1, 2, 2);
      Body.addBox("FLShoulder", 2F, -1F, -3F, 1, 2, 2);
    Head = new ModelRenderer(this, "Head");
    Head.setRotationPoint(0F, 22F, -4F);
    setRotation(Head, 0F, 0F, 0F);
    Head.mirror = true;
      Head.addBox("HeadMain", -2F, -2F, -5F, 4, 3, 4);
      Head.addBox("Neck", -1F, -1F, -1F, 2, 2, 1);
    BRLeg = new ModelRenderer(this, "BRLeg");
    BRLeg.setRotationPoint(-3F, 21F, 4F);
    setRotation(BRLeg, 0F, 0F, 0F);
    BRLeg.mirror = true;
      BRLeg.addBox("BRLegPiece1", 0F, 0F, 0F, 1, 1, 2);
      BRLeg.addBox("BRLegPiece2", 0F, 1F, 1F, 1, 1, 1);
      BRLeg.addBox("BRFoot", -1F, 2F, 0F, 2, 1, 2);
    FRLeg = new ModelRenderer(this, "FRLeg");
    FRLeg.setRotationPoint(-3F, 21F, -2F);
    setRotation(FRLeg, 0F, 0F, 0F);
    FRLeg.mirror = true;
      FRLeg.addBox("FRLegPiece1", 0F, 0F, 0F, 1, 1, 2);
      FRLeg.addBox("FRLegPiece2", 0F, 1F, 1F, 1, 1, 1);
      FRLeg.addBox("FRFoot", -1F, 2F, 0F, 2, 1, 2);
    BLLeg = new ModelRenderer(this, "BLLeg");
    BLLeg.setRotationPoint(2F, 21F, 4F);
    setRotation(BLLeg, 0F, 0F, 0F);
    BLLeg.mirror = true;
      BLLeg.addBox("BLLegPiece1", 0F, 0F, 0F, 1, 1, 2);
      BLLeg.addBox("BLLegPiece2", 0F, 1F, 1F, 1, 1, 1);
      BLLeg.addBox("BLFoot", 0F, 2F, 0F, 2, 1, 2);
    FLLeg = new ModelRenderer(this, "FLLeg");
    FLLeg.setRotationPoint(2F, 21F, -2F);
    setRotation(FLLeg, 0F, 0F, 0F);
    FLLeg.mirror = true;
      FLLeg.addBox("FLLegPiece1", 0F, 0F, 0F, 1, 1, 2);
      FLLeg.addBox("FLLegPiece2", 0F, 1F, 1F, 1, 1, 1);
      FLLeg.addBox("FLFoot", 0F, 2F, 0F, 2, 1, 2);
    Tail = new ModelRenderer(this, "Tail");
    Tail.setRotationPoint(0F, 21F, 5F);
    setRotation(Tail, 0F, 0F, 0F);
    Tail.mirror = true;
      Tail.addBox("TailPiece1", -1.5F, -1F, 0F, 3, 3, 3);
      Tail.addBox("TailPiece2", -1F, -1F, 3F, 2, 3, 4);
      Tail.addBox("TailPiece3", -0.5F, -1F, 7F, 1, 3, 4);
  }
  
  public void render(Entity entity, float f, float f1, float f2, float f3, float f4, float f5)
  {
    super.render(entity, f, f1, f2, f3, f4, f5);
    setRotationAngles(f, f1, f2, f3, f4, f5, entity);
    Body.render(f5);
    Head.render(f5);
    BRLeg.render(f5);
    FRLeg.render(f5);
    BLLeg.render(f5);
    FLLeg.render(f5);
    Tail.render(f5);
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
    Head.rotateAngleX = -(f4 / 57.29578F);   
    Head.rotateAngleY = f3 / 57.29578F;              
    Body.rotateAngleX = 0.0F; // we don't really want to rotate the body.        
    FRLeg.rotateAngleX = MathHelper.cos(f * 0.6662F) * 1.4F * f1;        
    FLLeg.rotateAngleX = MathHelper.cos(f * 0.6662F + 3.141593F) * 1.4F * f1;       
    BRLeg.rotateAngleX = MathHelper.cos(f * 0.6662F + 3.141593F) * 1.4F * f1;        
    BLLeg.rotateAngleX = MathHelper.cos(f * 0.6662F) * 1.4F * f1;
    Tail.rotateAngleY =  MathHelper.cos(f * 0.6662F) * 1.4F * f1; // delete if derpy...
  }

}
