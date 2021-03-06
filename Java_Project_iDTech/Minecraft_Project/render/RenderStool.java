package com.DonLoughry.AllOfTheEverything.render;

import org.lwjgl.opengl.GL11;

import net.minecraft.client.renderer.tileentity.TileEntitySpecialRenderer;
import net.minecraft.tileentity.TileEntity;
import net.minecraft.util.ResourceLocation;
import net.minecraft.world.World;

import com.DonLoughry.AllOfTheEverything.blocks.BlockRegistry;
import com.DonLoughry.AllOfTheEverything.entity.TileEntityStool;
import com.DonLoughry.AllOfTheEverything.model.*;

public class RenderStool extends TileEntitySpecialRenderer{
	
	public ModelStool model;
	public World worldObj;
	public BlockRegistry blockReg;
	
	
	public RenderStool()
	{
		this.model = new ModelStool();
	}

	
	public void renderTileEntityAt(TileEntity arg0, double x, double y,
			double z, float arg4) {
		GL11.glPushMatrix();
		GL11.glTranslatef((float)x + 0.5F, (float)y + 1.5F, (float)z + 0.5F);
		GL11.glRotatef(180, 0F, 0F, 1F);
		TileEntityStool myTile = (TileEntityStool) arg0;
	    int direction = myTile.direction;
		GL11.glRotatef(direction, 0F, 1F, 0F);
		this.bindTexture(new ResourceLocation("donsmod:textures/entity/ModelStool.png"));
		GL11.glPushMatrix();
		model.renderModel(0.0625F); // method not there yet in default model, remember this!
		GL11.glPopMatrix();
		GL11.glPopMatrix();
	}
}
