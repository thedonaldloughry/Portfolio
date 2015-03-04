package com.DonLoughry.AllOfTheEverything.lib;

import net.minecraft.client.model.ModelBiped;
import net.minecraft.client.renderer.entity.RenderSnowball;

import com.DonLoughry.AllOfTheEverything.blocks.BlockRegistry;
import com.DonLoughry.AllOfTheEverything.entity.*;
import com.DonLoughry.AllOfTheEverything.items.ItemRegistry;
import com.DonLoughry.AllOfTheEverything.model.*;
import com.DonLoughry.AllOfTheEverything.render.*;

import cpw.mods.fml.client.registry.ClientRegistry;
import cpw.mods.fml.client.registry.RenderingRegistry;

public class ProxyClient extends ProxyCommon{
	
	BlockRegistry bRegister = new BlockRegistry();
	private static final ModelAetherialArmor aetherChest = new ModelAetherialArmor(0.9f); 
	private static final ModelAetherialArmor aetherLegs = new ModelAetherialArmor(0.4f); // may need to be 1.0F...
	
	public void registerRenderInformation()
	{
		System.out.println("The Client was actually doing something WTFWTFOHSHITOHSHITOHSHITTAKEMUSHROOMS");
		// Register renderers for "living" entities//
		RenderingRegistry.registerEntityRenderingHandler(EntityPoo.class, new RenderSnowball(ItemRegistry.Poo));
		RenderingRegistry.registerEntityRenderingHandler(TempleMonsterAI.class, new RenderTempleMonster(new TempleMonster(), 0));
		RenderingRegistry.registerEntityRenderingHandler(EntityGoober.class, new RenderGoober(new ModelGoober(), 0));
		RenderingRegistry.registerEntityRenderingHandler(EntityBlizzard.class, new RenderBlizzard(new ModelBlizzard(), 0));
		RenderingRegistry.registerEntityRenderingHandler(EntityMimicTree.class, new RenderMimicTree(new ModelMimicTree(), 0));
		RenderingRegistry.registerEntityRenderingHandler(EntityGentlemanCapybara.class, new RenderGentlemanCapybara(new ModelGentlemanCapybara(), 0));
		RenderingRegistry.registerEntityRenderingHandler(EntityGreenDragon.class, new RenderGreenDragon());
		RenderingRegistry.registerEntityRenderingHandler(EntitySerpent.class, new RenderSerpent(new ModelSerpent(), 0));
		RenderingRegistry.registerEntityRenderingHandler(EntityFish.class, new RenderFish(new ModelFish(), 0));
		// End living entity renderers //
		
		// Register renderers for tile entities (custom model blocks) //
		ClientRegistry.bindTileEntitySpecialRenderer(TileEntityChair.class, new RenderChair());
		ClientRegistry.bindTileEntitySpecialRenderer(TileEntityMug.class, new RenderMug());
		ClientRegistry.bindTileEntitySpecialRenderer(TileEntityTable.class, new RenderTable());
		ClientRegistry.bindTileEntitySpecialRenderer(TileEntitySmallTable.class, new RenderSmallTable());
		ClientRegistry.bindTileEntitySpecialRenderer(TileEntitySwordStatue.class, new RenderSwordStatue());
		ClientRegistry.bindTileEntitySpecialRenderer(TileEntityLamp.class, new RenderLamp());
		ClientRegistry.bindTileEntitySpecialRenderer(TileEntityFramePicture.class, new RenderFramePicture());
		ClientRegistry.bindTileEntitySpecialRenderer(TileEntityComfyChair.class, new RenderComfyChair());
		ClientRegistry.bindTileEntitySpecialRenderer(TileEntityCouch.class, new RenderCouch());
		ClientRegistry.bindTileEntitySpecialRenderer(TileEntityBookshelf.class, new RenderBookshelf());
		ClientRegistry.bindTileEntitySpecialRenderer(TileEntityLeaningLadder.class, new RenderLeaningLadder());
		ClientRegistry.bindTileEntitySpecialRenderer(TileEntityStool.class, new RenderStool());
		ClientRegistry.bindTileEntitySpecialRenderer(TileEntityDeskLamp.class, new RenderDeskLamp());
		ClientRegistry.bindTileEntitySpecialRenderer(TileEntityWallpaper.class, new RenderWallpaper("ModelWallpaper1.png"));
		// End tile entity renderers //
	}
	
	@Override 
	public ModelBiped getArmorModel(int id, String name)
	{ 
		if(name == "aether")
		{
			switch (id) 
			{ 
				case 0: return aetherChest; 
				case 1: return aetherLegs; 
				default: break; 
			} return aetherChest; //default, if whenever you should have passed on a wrong id
		}
		else
		{
			return null; // may throw exception, and rightfully so. We need to know what custom armor to look at!
		}
	}

}
