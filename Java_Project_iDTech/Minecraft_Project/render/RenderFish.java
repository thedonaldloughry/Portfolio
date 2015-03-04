package com.DonLoughry.AllOfTheEverything.render;

import com.DonLoughry.AllOfTheEverything.entity.*;
import com.DonLoughry.AllOfTheEverything.lib.*;

import net.minecraft.client.renderer.entity.RenderLiving;
import net.minecraft.entity.Entity;
import net.minecraft.util.ResourceLocation;
import net.minecraft.client.model.ModelBase;
import cpw.mods.fml.relauncher.Side;
import cpw.mods.fml.relauncher.SideOnly;

@SideOnly(Side.CLIENT)
public class RenderFish extends RenderLiving {

	private static final ResourceLocation mobTextures = new ResourceLocation(References.MODID + ":textures/entity/Test.png");
	private static final String __OBFID = "CL_00000995";
	
	public RenderFish(ModelBase par1ModelBase, float par2)
	{
		super(par1ModelBase, par2);
	}
	
	protected String getEntityID()
	{
		return __OBFID;
	}
	
	protected ResourceLocation getEntityTexture(EntityFish par1EntityBlizzard)
	{
		return mobTextures;
	}
	
	protected ResourceLocation getEntityTexture(Entity par1Entity)
	{
		return this.getEntityTexture((EntityFish)par1Entity);
	}

}
