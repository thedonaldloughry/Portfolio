package com.DonLoughry.AllOfTheEverything.render;

import net.minecraft.client.renderer.entity.RenderDragon;
import net.minecraft.entity.Entity;
import net.minecraft.util.ResourceLocation;
import cpw.mods.fml.relauncher.Side;
import cpw.mods.fml.relauncher.SideOnly;

@SideOnly(Side.CLIENT)
public class RenderGreenDragon extends RenderDragon
{
    
    private static final ResourceLocation mobTextures = new ResourceLocation("alloftheeverything:textures/entity/Test.png");
    //private static final ResourceLocation eyesTexture = new ResourceLocation("/mob/enderdragon/ender_eyes.png");
    private static final String __OBFID = "CL_00000999";

    public RenderGreenDragon()
    {
        super();
    }
    
    protected String getEntityID()
	{
		return __OBFID;
	}

	@Override
	protected ResourceLocation getEntityTexture(Entity arg0) {
		return mobTextures;
	}
}