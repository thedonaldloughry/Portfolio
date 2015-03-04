package com.DonLoughry.AllOfTheEverything;

import net.minecraft.init.Blocks;
import net.minecraft.block.Block;
import net.minecraft.block.material.Material;
import net.minecraft.creativetab.CreativeTabs;
import net.minecraft.item.ItemStack;
import net.minecraftforge.common.MinecraftForge;
import cpw.mods.fml.common.Mod;
import cpw.mods.fml.common.Mod.EventHandler;
import cpw.mods.fml.common.SidedProxy;
import cpw.mods.fml.common.event.FMLInitializationEvent;
import cpw.mods.fml.common.event.FMLPreInitializationEvent;
import cpw.mods.fml.common.registry.EntityRegistry;
import cpw.mods.fml.common.registry.GameRegistry;

import com.DonLoughry.AllOfTheEverything.blocks.*;
import com.DonLoughry.AllOfTheEverything.entity.*;
import com.DonLoughry.AllOfTheEverything.event.BonemealAutumnTreeEvent;
import com.DonLoughry.AllOfTheEverything.event.BonemealDragonTreeEvent;
import com.DonLoughry.AllOfTheEverything.items.*;
import com.DonLoughry.AllOfTheEverything.lib.*;
import com.DonLoughry.AllOfTheEverything.world.*;

@Mod(modid = References.MODID, version = References.VERSION)
public class AllOfTheEverything
{
	@SidedProxy(clientSide = References.Client, serverSide = References.Common)
	
	public static ProxyCommon proxy;
	public static BlockRegistry blockReg;
	public static WorldRegistry worldReg;
	public static ItemRegistry itemReg;
	public static WorldBiomeEvent worldEvent;
	
	//public static AutumnTreeSapling autumnTreeSapling;
	
	/*public static Item Poo;
	public static Item blackIronHelm;
	public static Item blackIronPants;
	public static Item blackIronBoots;
	public static Item blackIronChestPlate; */
	
	public static Block blackTFence;
	public static Block wallVeins;
	
	
	@EventHandler
	public void PreInit(FMLPreInitializationEvent event)
	{
		int modEntityID = 0;
		
		GenericEntityRegistry.mainRegistry();
		
		BlockRegistry.registerBlocks();
		
		MinecraftForge.TERRAIN_GEN_BUS.register(new WorldBiomeEvent());
		MinecraftForge.EVENT_BUS.register(new BonemealAutumnTreeEvent());
		MinecraftForge.EVENT_BUS.register(new BonemealDragonTreeEvent());
		
		WorldRegistry.mainRegistry();
		ItemRegistry.registerItems();
		
		
		System.out.println("Pulled out the World Registry in AOTE");
		
		
		
		//Item Registry
		//GameReg
			/*GameRegistry.registerItem(Poo, "Poo");
			GameRegistry.registerItem(blackIronHelm, "Black Iron Helm");
			GameRegistry.registerItem(blackIronPants, "Black Iron Leggings");
			GameRegistry.registerItem(blackIronBoots, "Black Iron Boots");
			GameRegistry.registerItem(blackIronChestPlate, "Black Iron Chestplate");*/
			
			GameRegistry.registerBlock(wallVeins, "Wall Veins");
			GameRegistry.registerBlock(blackTFence, "Black Temple Fence");
			GameRegistry.registerTileEntity(TileEntityChair.class, "Chair");
			GameRegistry.registerTileEntity(TileEntityMug.class, "Mug");
			GameRegistry.registerTileEntity(TileEntityTable.class, "Table");
			GameRegistry.registerTileEntity(TileEntitySmallTable.class, "Small Table");
			GameRegistry.registerTileEntity(TileEntitySwordStatue.class, "Sword Statue");
			GameRegistry.registerTileEntity(TileEntityLamp.class, "Lamp");
			GameRegistry.registerTileEntity(TileEntityFramePicture.class, "Picture Frame");
			GameRegistry.registerTileEntity(TileEntityComfyChair.class, "Comfy Chair");
			GameRegistry.registerTileEntity(TileEntityCouch.class, "Couch");
			GameRegistry.registerTileEntity(TileEntityStool.class, "Stool");
			GameRegistry.registerTileEntity(TileEntityBookshelf.class, "Library Bookshelf");
			GameRegistry.registerTileEntity(TileEntityLeaningLadder.class, "Leaning Ladder");
			GameRegistry.registerTileEntity(TileEntityDeskLamp.class, "Desk Lamp");
			GameRegistry.registerTileEntity(TileEntityWallpaper.class, "Wallpaper"); // note, could cause conflicts later
			
		//LangReg								      
			/*LanguageRegistry.addName(Poo, "Poo");
			
			LanguageRegistry.addName(blackIronHelm, "Black Iron Helm");
			LanguageRegistry.addName(blackIronPants, "Black Iron Leggings");
			LanguageRegistry.addName(blackIronBoots, "Black Iron Boots");
			LanguageRegistry.addName(blackIronChestPlate, "Black Iron Chestplate");
			
			LanguageRegistry.addName(wallVeins, "Wall Veins");
			LanguageRegistry.addName(blackTFence, "Black Temple Fence");*/
		//EntityReg
			EntityRegistry.registerModEntity(EntityPoo.class, "Poo", ++modEntityID, this, 64, 10, true);
			// Above code is written to note that while poo is an entity, it is not a LIVING entity.
			//EntityRegistry.registerModEntity(TempleMonsterAI.class, "Temple Monster", ++modEntityID, this, 64, 10, true);
			
		//Recipe Registry (yay!!!)
		//GameReg
			ItemStack pooStack = new ItemStack(ItemRegistry.Poo);
			ItemStack BTStack = new ItemStack(BlockRegistry.blackTBlock);
			GameRegistry.addShapelessRecipe(new ItemStack(BlockRegistry.greyBrick, 1), pooStack, pooStack, pooStack, // pooBlock
																				pooStack, pooStack, pooStack,
																				pooStack, pooStack, pooStack);
			GameRegistry.addShapelessRecipe(pooStack, Blocks.dirt);
			GameRegistry.addShapelessRecipe(BTStack, Blocks.sand);

		// Now that we've registered the entity, tell the proxy to register the renderer
		proxy.registerRenderInformation();
    	System.out.println("preinitialization HAHAHAHAHAHHAHAHAHAHAHAHAHAHAHHAHA");
	}
    
    @EventHandler
    public void Init(FMLInitializationEvent event)
    {
    	System.out.println("The main Init function just ran");
    }
    
    @EventHandler
    public void Load(FMLInitializationEvent event)
    {
    	proxy.registerRenderInformation();
    	System.out.println("The main Load function just ran");
    }
    
    public AllOfTheEverything()
    {
    	// Keep in mind, all this is in the constructor to AVOID annoying errors. However, this structure could actually cause them.
    	// Eventually, we'll want to put all of these operations in their proper places. For now, they're good here.
    	// BLOCK/ITEM ATTRIBUTES //
    	//pooBlock.setHarvestLevel("shovel", 0);
    	BlockRegistry.createBlocks();
    	ItemRegistry.createItems();
    	wallVeins = new LadderLike(true).setBlockName("Wall Veins").setCreativeTab(CreativeTabs.tabDecorations)
    			.setBlockTextureName("alloftheeverything:WallVeins");
    	blackTFence = new Fence("alloftheeverything:BTBlock", Material.wood)
    		.setBlockTextureName("alloftheeverything:BTBlock");
    	
    	/*ArmorMaterial armorBlackIron = EnumHelper.addArmorMaterial("BlackIron", 29, new int[]{5,5,5,5}, 11);
    	Poo = new Poo(4999);	
    	blackIronHelm = new GenericArmor(armorBlackIron, 0, "Black Iron Helm");
    	blackIronChestPlate = new GenericArmor(armorBlackIron, 1, "Black Iron Chestplate");
    	blackIronPants = new GenericArmor(armorBlackIron, 2, "Black Iron Pants");
    	blackIronBoots = new GenericArmor(armorBlackIron, 3, "Black Iron Boots");*/
    	// END BLOCK/ITEM ATTRIBUTES //
    	// BLOCK REQUIREMENTS //
    	BlockRegistry.setBlockReqs();
    	// END BLOCK REQUIREMENTS //
    	System.out.println("Constructor ran.");
    }
}
