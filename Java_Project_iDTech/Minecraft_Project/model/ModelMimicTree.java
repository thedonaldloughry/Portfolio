// Date: 7/25/2014 10:42:57 PM
// Template version 1.1
// Java generated by Techne
// Keep in mind that you still need to fill in some blanks
// - ZeuX






package com.DonLoughry.AllOfTheEverything.model;

import net.minecraft.client.model.ModelBase;
import net.minecraft.client.model.ModelRenderer;
import net.minecraft.entity.Entity;

public class ModelMimicTree extends ModelBase
{
  //fields
    ModelRenderer MimicTree;
  
  public ModelMimicTree()
  {
    textureWidth = 128;
    textureHeight = 128;
    setTextureOffset("MimicTree.Base1", 64, 64);
    setTextureOffset("MimicTree.Base2", 64, 32);
    setTextureOffset("MimicTree.Base3", 64, 0);
    setTextureOffset("MimicTree.Leaves1", 0, 0);
    setTextureOffset("MimicTree.Leaves2", 0, 0);
    setTextureOffset("MimicTree.Leaves3", 0, 0);
    setTextureOffset("MimicTree.Leaves4", 0, 0);
    setTextureOffset("MimicTree.Leaves5", 0, 0);
    setTextureOffset("MimicTree.Leaves6", 0, 0);
    setTextureOffset("MimicTree.Leaves7", 0, 0);
    setTextureOffset("MimicTree.Leaves8", 0, 0);
    setTextureOffset("MimicTree.Leaves9", 0, 0);
    setTextureOffset("MimicTree.Leaves10", 0, 0);
    setTextureOffset("MimicTree.Leaves11", 0, 0);
    setTextureOffset("MimicTree.Leaves12", 0, 0);
    setTextureOffset("MimicTree.Leaves12", 0, 0);
    setTextureOffset("MimicTree.Leaves13", 0, 0);
    setTextureOffset("MimicTree.Leaves14", 0, 0);
    setTextureOffset("MimicTree.Leaves15", 0, 0);
    setTextureOffset("MimicTree.Leaves16", 0, 0);
    setTextureOffset("MimicTree.Leaves17", 0, 0);
    setTextureOffset("MimicTree.Leaves18", 0, 0);
    setTextureOffset("MimicTree.Leaves19", 0, 0);
    setTextureOffset("MimicTree.Leaves20", 0, 0);
    setTextureOffset("MimicTree.Leaves21", 0, 0);
    setTextureOffset("MimicTree.Leaves22", 0, 0);
    setTextureOffset("MimicTree.Leaves23", 0, 0);
    setTextureOffset("MimicTree.Leaves24", 0, 0);
    setTextureOffset("MimicTree.Leaves25", 0, 0);
    setTextureOffset("MimicTree.Leaves26", 0, 0);
    setTextureOffset("MimicTree.Leaves27", 0, 0);
    setTextureOffset("MimicTree.Leaves28", 0, 0);
    setTextureOffset("MimicTree.Leaves29", 0, 0);
    setTextureOffset("MimicTree.Leaves30", 0, 0);
    setTextureOffset("MimicTree.Leaves31", 0, 0);
    setTextureOffset("MimicTree.Leaves32", 0, 0);
    setTextureOffset("MimicTree.Leaves33", 0, 0);
    setTextureOffset("MimicTree.Leaves34", 0, 0);
    setTextureOffset("MimicTree.Leaves35", 0, 0);
    setTextureOffset("MimicTree.Leaves36", 0, 0);
    setTextureOffset("MimicTree.Leaves37", 0, 0);
    setTextureOffset("MimicTree.Leaves38", 0, 0);
    setTextureOffset("MimicTree.Leaves39", 0, 0);
    setTextureOffset("MimicTree.Leaves40", 0, 0);
    setTextureOffset("MimicTree.Leaves41", 0, 0);
    setTextureOffset("MimicTree.Leaves42", 0, 0);
    setTextureOffset("MimicTree.Leaves43", 0, 0);
    setTextureOffset("MimicTree.Leaves44", 0, 0);
    setTextureOffset("MimicTree.Leaves45", 0, 0);
    setTextureOffset("MimicTree.Leaves46", 0, 0);
    setTextureOffset("MimicTree.Leaves47", 0, 0);
    setTextureOffset("MimicTree.Leaves48", 0, 0);
    setTextureOffset("MimicTree.Leaves49", 0, 0);
    
    MimicTree = new ModelRenderer(this, "MimicTree");
    MimicTree.setRotationPoint(0F, 0F, 0F);
    setRotation(MimicTree, 0F, 0F, 0F);
    MimicTree.mirror = true;
      MimicTree.addBox("Base1", -8F, 8F, -8F, 16, 16, 16);
      MimicTree.addBox("Base2", -8F, -8F, -8F, 16, 16, 16);
      MimicTree.addBox("Base3", -8F, -24F, -8F, 16, 16, 16);
      MimicTree.addBox("Leaves1", 8F, -40F, -8F, 16, 16, 16);
      MimicTree.addBox("Leaves2", -8F, -40F, -24F, 16, 16, 16);
      MimicTree.addBox("Leaves3", -24F, -40F, -8F, 16, 16, 16);
      MimicTree.addBox("Leaves4", -8F, -40F, 8F, 16, 16, 16);
      MimicTree.addBox("Leaves5", 8F, -40F, 8F, 16, 16, 16);
      MimicTree.addBox("Leaves6", 8F, -40F, -24F, 16, 16, 16);
      MimicTree.addBox("Leaves7", -24F, -40F, -24F, 16, 16, 16);
      MimicTree.addBox("Leaves8", -24F, -40F, 8F, 16, 16, 16);
      MimicTree.addBox("Leaves9", -40F, -40F, -40F, 16, 16, 16);
      MimicTree.addBox("Leaves10", -40F, -40F, -24F, 16, 16, 16);
      MimicTree.addBox("Leaves11", -40F, -40F, -8F, 16, 16, 16);
      MimicTree.addBox("Leaves12", -40F, -40F, 8F, 16, 16, 16);
      MimicTree.addBox("Leaves12", -40F, -40F, 24F, 16, 16, 16);
      MimicTree.addBox("Leaves13", -40F, -56F, 8F, 16, 16, 16);
      MimicTree.addBox("Leaves14", -40F, -56F, -8F, 16, 16, 16);
      MimicTree.addBox("Leaves15", -40F, -56F, -24F, 16, 16, 16);
      MimicTree.addBox("Leaves16", -40F, -56F, -40F, 16, 16, 16);
      MimicTree.addBox("Leaves17", -24F, -40F, -40F, 16, 16, 16);
      MimicTree.addBox("Leaves18", -8F, -40F, -40F, 16, 16, 16);
      MimicTree.addBox("Leaves19", 8F, -40F, -40F, 16, 16, 16);
      MimicTree.addBox("Leaves20", 24F, -40F, -40F, 16, 16, 16);
      MimicTree.addBox("Leaves21", -24F, -56F, -40F, 16, 16, 16);
      MimicTree.addBox("Leaves22", -8F, -56F, -40F, 16, 16, 16);
      MimicTree.addBox("Leaves23", 8F, -56F, -40F, 16, 16, 16);
      MimicTree.addBox("Leaves24", 24F, -56F, -40F, 16, 16, 16);
      MimicTree.addBox("Leaves25", -24F, -72F, 8F, 16, 16, 16);
      MimicTree.addBox("Leaves26", -24F, -72F, -8F, 16, 16, 16);
      MimicTree.addBox("Leaves27", -24F, -88F, -8F, 16, 16, 16);
      MimicTree.addBox("Leaves28", -8F, -72F, -24F, 16, 16, 16);
      MimicTree.addBox("Leaves29", -8F, -88F, -24F, 16, 16, 16);
      MimicTree.addBox("Leaves30", 8F, -72F, -8F, 16, 16, 16);
      MimicTree.addBox("Leaves31", 8F, -88F, -8F, 16, 16, 16);
      MimicTree.addBox("Leaves32", -8F, -72F, 8F, 16, 16, 16);
      MimicTree.addBox("Leaves33", -8F, -88F, 8F, 16, 16, 16);
      MimicTree.addBox("Leaves34", 24F, -40F, -24F, 16, 16, 16);
      MimicTree.addBox("Leaves35", 24F, -40F, -8F, 16, 16, 16);
      MimicTree.addBox("Leaves36", 24F, -40F, 8F, 16, 16, 16);
      MimicTree.addBox("Leaves37", 24F, -56F, -24F, 16, 16, 16);
      MimicTree.addBox("Leaves38", 24F, -56F, -8F, 16, 16, 16);
      MimicTree.addBox("Leaves39", 24F, -56F, 8F, 16, 16, 16);
      MimicTree.addBox("Leaves40", -24F, -40F, 24F, 16, 16, 16);
      MimicTree.addBox("Leaves41", -8F, -40F, 24F, 16, 16, 16);
      MimicTree.addBox("Leaves42", 8F, -40F, 24F, 16, 16, 16);
      MimicTree.addBox("Leaves43", 8F, -56F, 24F, 16, 16, 16);
      MimicTree.addBox("Leaves44", -8F, -56F, 24F, 16, 16, 16);
      MimicTree.addBox("Leaves45", -24F, -56F, 24F, 16, 16, 16);
      MimicTree.addBox("Leaves46", 8F, -56F, 8F, 16, 16, 16);
      MimicTree.addBox("Leaves47", 8F, -56F, -24F, 16, 16, 16);
      MimicTree.addBox("Leaves48", -24F, -56F, -24F, 16, 16, 16);
      MimicTree.addBox("Leaves49", -8F, -88F, -8F, 16, 16, 16);
  }
  
  public void render(Entity entity, float f, float f1, float f2, float f3, float f4, float f5)
  {
    super.render(entity, f, f1, f2, f3, f4, f5);
    setRotationAngles(f, f1, f2, f3, f4, f5, entity);
    MimicTree.render(f5);
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