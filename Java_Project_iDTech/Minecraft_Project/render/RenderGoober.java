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
public class RenderGoober extends RenderLiving {

	private static final ResourceLocation mobTextures = new ResourceLocation(References.MODID + ":textures/entity/Goober.png");
	private static final String __OBFID = "CL_00000985"; // eh... what the hell is this??? and will it be a problem???
	//										was "CL_00000984" before, changed to evade possible conflict with TempleMonster.
	public RenderGoober(ModelBase par1ModelBase, float par2)
	{
		super(par1ModelBase, par2);
	}
	
	protected String getEntityID()
	{
		return __OBFID;
	}
	
	protected ResourceLocation getEntityTexture(EntityGoober par1EntityGoober)
	{
		return mobTextures;
	}
	
	protected ResourceLocation getEntityTexture(Entity par1Entity)
	{
		return this.getEntityTexture((EntityGoober)par1Entity);
	}

}