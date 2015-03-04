// Date: 5/23/2014 6:10:46 PM
// Template version 1.1
// Java generated by Techne
// Keep in mind that you still need to fill in some blanks
// - ZeuX






package com.DonLoughry.AllOfTheEverything.model;

import net.minecraft.client.model.ModelBase;
import net.minecraft.client.model.ModelRenderer;
import net.minecraft.entity.Entity;
import net.minecraft.util.MathHelper;

public class TempleMonster extends ModelBase
{
  //fields
    ModelRenderer Body;
    ModelRenderer RightBackLeg;
    ModelRenderer LeftBackLeg;
    ModelRenderer LeftFrontLeg;
    ModelRenderer RightFrontLeg;
    ModelRenderer Tail;
    ModelRenderer Head;
  
  public TempleMonster()
  {
    textureWidth = 2160;
    textureHeight = 2160;
    setTextureOffset("Body.BodyShapeBack", 564, 727);
    setTextureOffset("Body.BodyShapeFront", 419, 1046);
    setTextureOffset("RightBackLeg.ShoulderRightBack", 127, 730);
    setTextureOffset("RightBackLeg.LegRightBack", 94, 930);
    setTextureOffset("LeftBackLeg.ShoulderLeftBack", 1450, 730);
    setTextureOffset("LeftBackLeg.LegLeftBack", 1589, 930);
    setTextureOffset("LeftFrontLeg.ShoulderLeftFront", 1325, 1514);
    setTextureOffset("LeftFrontLeg.LegLeftFront", 1417, 1745);
    setTextureOffset("RightFrontLeg.ShoulderRightFront", 177, 1514);
    setTextureOffset("RightFrontLeg.LegRightFront", 255, 1749);
    setTextureOffset("Tail.TailFront", 800, 534);
    setTextureOffset("Tail.TailMiddle", 800, 339);
    setTextureOffset("Tail.TailBack", 818, 169);
    setTextureOffset("Head.HeadBase", 700, 1800);
    setTextureOffset("Head.HeadDetailOne", 74, 2114);
    setTextureOffset("Head.HeadDetailTwo", 161, 2114);
    setTextureOffset("Head.HeadDetailThree", 252, 2114);
    setTextureOffset("Head.HeadDetailFour", 340, 2114);
    setTextureOffset("Head.HeadDetailFive", 430, 2114);
    setTextureOffset("Head.HeadDetailSix", 520, 2114);
    setTextureOffset("Head.HeadDetailSeven", 610, 2114);
    setTextureOffset("Head.HeadDetailEight", 700, 2114);
    setTextureOffset("Head.HeadDetailNine", 790, 2114);
    setTextureOffset("Head.HeadDetailTen", 880, 2114);
    setTextureOffset("Head.HeadDetailEleven", 970, 2114);
    setTextureOffset("Head.HeadDetailTwelve", 1060, 2114);
    setTextureOffset("Head.HeadDetail13", 1150, 2114);
    setTextureOffset("Head.Neck", 679, 1512);
    setTextureOffset("Head.HeadDetail14", 1240, 2114);
    
    Body = new ModelRenderer(this, "Body");
    Body.setRotationPoint(-153F, -225F, -189F);
    setRotation(Body, 0F, 0F, 0F);
    Body.mirror = true;
      Body.addBox("BodyShapeBack", 8F, 20F, 282F, 270, 135, 162);
      Body.addBox("BodyShapeFront", -1F, -1F, -1F, 288, 162, 288);
    RightBackLeg = new ModelRenderer(this, "RightBackLeg");
    RightBackLeg.setRotationPoint(-242F, -167F, 130F);
    setRotation(RightBackLeg, 0F, 0F, 0F);
    RightBackLeg.mirror = true;
      RightBackLeg.addBox("ShoulderRightBack", 0F, 0F, 0F, 108, 81, 99);
      RightBackLeg.addBox("LegRightBack", -14F, 7F, 9F, 72, 198, 81);
    LeftBackLeg = new ModelRenderer(this, "LeftBackLeg");
    LeftBackLeg.setRotationPoint(117F, -167F, 130F);
    setRotation(LeftBackLeg, 0F, 0F, 0F);
    LeftBackLeg.mirror = true;
      LeftBackLeg.addBox("ShoulderLeftBack", 0F, 0F, 0F, 108, 81, 99);
      LeftBackLeg.addBox("LegLeftBack", 51F, 5F, 8F, 72, 198, 81);
    LeftFrontLeg = new ModelRenderer(this, "LeftFrontLeg");
    LeftFrontLeg.setRotationPoint(123F, -167F, -180F);
    setRotation(LeftFrontLeg, 0F, 0F, 0F);
    LeftFrontLeg.mirror = true;
      LeftFrontLeg.addBox("ShoulderLeftFront", 0F, 0F, 0F, 126, 99, 117);
      LeftFrontLeg.addBox("LegLeftFront", 69F, 9F, 18F, 72, 198, 81);
    RightFrontLeg = new ModelRenderer(this, "RightFrontLeg");
    RightFrontLeg.setRotationPoint(-264F, -167F, -180F);
    setRotation(RightFrontLeg, 0F, 0F, 0F);
    RightFrontLeg.mirror = true;
      RightFrontLeg.addBox("ShoulderRightFront", -1F, -1F, -1F, 126, 99, 117);
      RightFrontLeg.addBox("LegRightFront", -18F, 9F, 18F, 72, 198, 81);
    Tail = new ModelRenderer(this, "Tail");
    Tail.setRotationPoint(-56F, -154F, 228F);
    setRotation(Tail, 0F, 0F, 0F);
    Tail.mirror = true;
      Tail.addBox("TailFront", -1F, -1F, -1F, 99, 81, 99);
      Tail.addBox("TailMiddle", 16F, 25F, 94F, 63, 45, 144);
      Tail.addBox("TailBack", 26F, 45F, 234F, 45, 18, 144);
    Head = new ModelRenderer(this, "Head");
    Head.setRotationPoint(-70F, -170F, -340F); // may need to reduce z-coordinate... changed from -370 to -340
    setRotation(Head, 0F, 0F, 0F);
    Head.mirror = true;
      Head.addBox("HeadBase", -4F, -42F, -145F, 129, 126, 162);
      Head.addBox("HeadDetailOne", 107F, -60F, -145F, 18, 18, 18);
      Head.addBox("HeadDetailTwo", 70F, -60F, -145F, 18, 18, 18);
      Head.addBox("HeadDetailThree", 33F, -60F, -145F, 18, 18, 18);
      Head.addBox("HeadDetailFour", -4F, -60F, -145F, 18, 18, 18);
      Head.addBox("HeadDetailFive", -4F, -60F, -110F, 18, 18, 18);
      Head.addBox("HeadDetailSix", -4F, -60F, -74F, 18, 18, 18);
      Head.addBox("HeadDetailSeven", -4F, -60F, -38F, 18, 18, 18);
      Head.addBox("HeadDetailEight", -4F, -60F, -1F, 18, 18, 18);
      Head.addBox("HeadDetailNine", 32F, -60F, -1F, 18, 18, 18);
      Head.addBox("HeadDetailTen", 68F, -60F, -1F, 18, 18, 18);
      Head.addBox("HeadDetailEleven", 107F, -60F, -1F, 18, 18, 18);
      Head.addBox("HeadDetailTwelve", 107F, -60F, -36F, 18, 18, 18);
      Head.addBox("HeadDetail13", 107F, -60F, -72F, 18, 18, 18);
      Head.addBox("Neck", -2F, -2F, 14F, 126, 81, 189);
      Head.addBox("HeadDetail14", 107F, -60F, -108F, 18, 18, 18);
  }
  
  public void render(Entity entity, float f, float f1, float f2, float f3, float f4, float f5)
  {
    super.render(entity, f, f1, f2, f3, f4, f5);
    setRotationAngles(f, f1, f2, f3, f4, f5, entity);
    Body.render(f5);
    RightBackLeg.render(f5);
    LeftBackLeg.render(f5);
    LeftFrontLeg.render(f5);
    RightFrontLeg.render(f5);
    Tail.render(f5);
    Head.render(f5);
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
    RightFrontLeg.rotateAngleX = MathHelper.cos(f * 0.6662F) * 1.4F * f1;        
    LeftFrontLeg.rotateAngleX = MathHelper.cos(f * 0.6662F + 3.141593F) * 1.4F * f1;       
    RightBackLeg.rotateAngleX = MathHelper.cos(f * 0.6662F + 3.141593F) * 1.4F * f1;        
    LeftBackLeg.rotateAngleX = MathHelper.cos(f * 0.6662F) * 1.4F * f1;
  }

}
