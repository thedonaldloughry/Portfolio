package com.DonLoughry.AllOfTheEverything.render;

import net.minecraft.item.ItemStack;
import net.minecraftforge.client.IItemRenderer;

import com.DonLoughry.AllOfTheEverything.entity.TileEntityChair;
import com.DonLoughry.AllOfTheEverything.render.RenderChair;

public class RenderChairItem implements IItemRenderer{
	// this whole freaking class just renders a version of the model in your hand. woot.
	private RenderChair renderer = new RenderChair();

	@Override
	public boolean handleRenderType(ItemStack arg0, ItemRenderType arg1) {
		return true;
	}

	@Override
	public void renderItem(ItemRenderType arg0, ItemStack arg1, Object... arg2) {
		renderer.renderTileEntityAt(new TileEntityChair(), 0.0D, 0.0D, 0.0D, 0.0F);
	}

	@Override
	public boolean shouldUseRenderHelper(ItemRenderType arg0, ItemStack arg1,
			ItemRendererHelper arg2) {
		return true;
	}

}
