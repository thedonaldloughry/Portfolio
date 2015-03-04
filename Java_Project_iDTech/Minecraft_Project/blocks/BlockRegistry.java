package com.DonLoughry.AllOfTheEverything.blocks;

import net.minecraft.block.Block;
import net.minecraft.block.material.Material;
import net.minecraft.creativetab.CreativeTabs;
import net.minecraft.init.Blocks;
import cpw.mods.fml.common.registry.GameRegistry;
import com.DonLoughry.AllOfTheEverything.entity.*;

public class BlockRegistry {
	
	public static Block pooBlock;
	public static Block blackTBlock;
	public static Block blackTFloor;
	public static Block blackTDBlock;
	public static Block greyBrick;
	public static Block deadStone;
	public static Block heartWood;
	public static Block heartGrass;
	public static Block cabinWall;
	public static Block cabinFloor;
	public static Block hearthStone;
	
	public static Block autumnGrass;
	public static Block autumnDirt;
	public static Block autumnStone;
	public static Block autumnWood;
	public static Block autumnLeaves;
	public static Block autumnTreeSapling;
	
	public static Block dragonGrass;
	public static Block dragonDirt;
	public static Block dragonStone;
	public static Block dragonWood;
	public static Block dragonLeaves;
	public static Block dragonTreeSapling;
	public static Block dragonStoneOre;
	
	public static ChairBlock chair;
	public static MugBlock mug;
	public static TableBlock largeTable;
	public static SmallTableBlock table;
	public static SwordStatueBlock swordStatue;
	public static LampBlock lamp;
	public static PictureFrameBlock picFrame;
	public static ComfyChairBlock comfyChair;
	public static CouchBlock couch;
	public static BookshelfBlock bookshelf;
	public static LeaningLadderBlock leaningLadder;
	public static StoolBlock stool;
	public static DeskLampBlock deskLamp;
	public static WallpaperBlock wallPaper1;
																							 

	public static void registerBlocks() {
		GameRegistry.registerBlock(pooBlock, "PooBlock");
		GameRegistry.registerBlock(blackTBlock, "Black Temple Block");
		GameRegistry.registerBlock(blackTFloor, "Black Temple Floor");
		GameRegistry.registerBlock(blackTDBlock, "Black Temple Dirty Block");
		GameRegistry.registerBlock(greyBrick, "Grey Brick");
		GameRegistry.registerBlock(deadStone, "DeadStone");
		GameRegistry.registerBlock(heartWood, "Heartwood");
		GameRegistry.registerBlock(heartGrass, "Heartgrass");
		GameRegistry.registerBlock(cabinWall, "Cabin Wall");
		GameRegistry.registerBlock(cabinFloor, "Cabin Floor");
		GameRegistry.registerBlock(hearthStone, "Hearthstone");
		
		GameRegistry.registerBlock(autumnGrass, "Autumn Grass");
		GameRegistry.registerBlock(autumnDirt, "Autumn Dirt");
		GameRegistry.registerBlock(autumnLeaves, "Autumn Leaves");
		GameRegistry.registerBlock(autumnStone, "Autumn Stone");
		GameRegistry.registerBlock(autumnWood, "Autumn Wood");
		GameRegistry.registerBlock(autumnTreeSapling, "Autumn Sapling");
		
		GameRegistry.registerBlock(dragonGrass, "Dragon Grass");
		GameRegistry.registerBlock(dragonDirt, "Dragon Dirt");
		GameRegistry.registerBlock(dragonLeaves, "DragonTree Leaves");
		GameRegistry.registerBlock(dragonStone, "Plain DragonStone");
		GameRegistry.registerBlock(dragonWood, "DragonTree Wood");
		GameRegistry.registerBlock(dragonTreeSapling, "Dragon Tree Sapling");
		GameRegistry.registerBlock(dragonStoneOre, "DragonStone Ore");
		
		GameRegistry.registerBlock(chair, "Chair");
		GameRegistry.registerBlock(mug, "Mug");
		GameRegistry.registerBlock(largeTable, "Large Table");
		GameRegistry.registerBlock(table, "Table");
		GameRegistry.registerBlock(swordStatue, "Sword Statue");
		GameRegistry.registerBlock(lamp, "Lamp");
		GameRegistry.registerBlock(picFrame, "Picture Frame");
		GameRegistry.registerBlock(comfyChair, "Comfy Chair");
		GameRegistry.registerBlock(couch, "Couch");
		GameRegistry.registerBlock(bookshelf, "Library Bookshelf");
		GameRegistry.registerBlock(leaningLadder, "Leaning Ladder");
		GameRegistry.registerBlock(stool, "Stool");
		GameRegistry.registerBlock(deskLamp, "Desk Lamp");
		GameRegistry.registerBlock(wallPaper1, "Wallpaper 1");
	}
	
	public static void createBlocks()
	{
		pooBlock = new GenericOre(pooBlock).setStepSound(Block.soundTypeSnow).setBlockName("PooBlock")
    			.setCreativeTab(CreativeTabs.tabBlock).setBlockTextureName("AllOfTheEverything:PooBlock");
    	
    	blackTBlock = new GenericBlock(Material.ground, blackTBlock).setStepSound(Block.soundTypeStone).setBlockName("Black Temple Block")
    			.setCreativeTab(CreativeTabs.tabBlock).setBlockTextureName("AllOfTheEverything:BTBlock");
    	
    	blackTFloor = new GenericBlock(Material.ground, blackTFloor).setStepSound(Block.soundTypeStone).setBlockName("Black Temple Floor")
    			.setCreativeTab(CreativeTabs.tabBlock).setBlockTextureName("AllOfTheEverything:BTFloor");
    	
    	blackTDBlock = new GenericBlock(Material.ground, blackTDBlock).setStepSound(Block.soundTypeStone).setBlockName("Black Temple Dirty Block")
    			.setCreativeTab(CreativeTabs.tabBlock).setBlockTextureName("AllOfTheEverything:BTDirtyBlock");
    	
    	greyBrick = new GenericBlock(Material.ground, greyBrick).setStepSound(Block.soundTypeStone).setBlockName("Grey Brick")
    			.setCreativeTab(CreativeTabs.tabBlock).setBlockTextureName("AllOfTheEverything:GreyBrick");
    	
    	deadStone = new GenericOre(deadStone).setStepSound(Block.soundTypeStone).setBlockName("DeadStone")
    			.setCreativeTab(CreativeTabs.tabBlock).setBlockTextureName("AllOfTheEverything:DeadStone");
    	
    	cabinWall = new GenericBlock(Material.ground, cabinWall).setStepSound(Block.soundTypeWood).setBlockName("Cabin Wall")
    			.setCreativeTab(CreativeTabs.tabBlock).setBlockTextureName("AllOfTheEverything:Log_Siding2");
    	
    	cabinFloor = new GenericBlock(Material.ground, cabinFloor).setStepSound(Block.soundTypeWood).setBlockName("Cabin Floor")
    			.setCreativeTab(CreativeTabs.tabBlock).setBlockTextureName("AllOfTheEverything:logCabinFloor");
    	
    	hearthStone = new GenericBlock(Material.ground, cabinFloor).setStepSound(Block.soundTypeStone).setBlockName("Hearthstone")
    			.setCreativeTab(CreativeTabs.tabBlock).setBlockTextureName("AllOfTheEverything:hearthStone");
    	
    	heartWood = new MultiSidedBlock(Material.wood, heartWood, "AllOfTheEverything:HeartWoodRings", "AllOfTheEverything:HeartWoodRings", 
    			"AllOfTheEverything:HeartWoodSide").setStepSound(Block.soundTypeWood).setBlockName("Heartwood")
    			.setCreativeTab(CreativeTabs.tabBlock);
    	
    	/*heartGrass = new MultiSidedBlock(Material.grass, heartGrass, "AllOfTheEverything:HeartGrassBottom", "AllOfTheEverything:HeartGrassTop", 
    			"AllOfTheEverything:HeartGrassSide").setStepSound(Block.soundTypeGrass).setBlockName("Heartgrass")
    			.setCreativeTab(CreativeTabs.tabBlock);*/
    	
    	/*
    	 * NOTE: The method for creating blocks used above has proven  useful for creating many blocks quickly, but the 
    	 * "GenericBlock" architecture must be the same for all blocks of that type. Things like grass, wood, and special 
    	 * blocks like Netherrack have custom properties, and to create blocks that do something other than just look like a 
    	 * thing, you must create custom java files and copy the methods needed to make your block do what you want. For example,
    	 * a block that is given the material of Material.grass will not just magically act like grass, as shown above. 
    	 * Heartgrass cannot currently sustain plants, change textures dynamically, or be generated into the world. It just sounds
    	 * like grass when you step on it.
    	 */
    	heartGrass = new GenericGrass(Blocks.dirt, "Heartgrass", "AllOfTheEverything:HeartGrassBottom", "AllOfTheEverything:HeartGrassTop", 
    			"AllOfTheEverything:HeartGrassSide").setCreativeTab(CreativeTabs.tabBlock);
    	
    	// AUTUMN BIOME //
    	
    	autumnDirt = new GenericDirt("Autumn Dirt", "AllOfTheEverything:AutumnDirt").setCreativeTab(CreativeTabs.tabBlock)
    			.setCreativeTab(CreativeTabs.tabBlock);
    	// DO NOT SPAWN DIRT INTO A NEW WORLD!!! IT WILL NOT SPREAD GRASS ALONE!!!
    	
    	autumnGrass = new GenericGrass(autumnDirt, "Autumn Grass", "AllOfTheEverything:AutumnDirt", "AllOfTheEverything:AutumnGrassTop", 
    			"AllOfTheEverything:AutumnGrassSide").setCreativeTab(CreativeTabs.tabBlock);
    	
    	autumnStone = new GenericBlock(Material.rock, Blocks.cobblestone).setBlockName("Autumn Stone").setStepSound(Block.soundTypeStone)
    			.setBlockTextureName("AllOfTheEverything:AutumnStone").setCreativeTab(CreativeTabs.tabBlock);
    	
    	autumnWood = new GenericWood("Autumn Wood", "AllOfTheEverything:AutumnWoodTopAndBottom", "AllOfTheEverything:AutumnWoodSide")
    	.setCreativeTab(CreativeTabs.tabBlock);
    	
    	
    	
    	autumnTreeSapling = new BlockAutumnTreeSapling();
    	
    	// END AUTUMN BIOME //
    	
    	// DRAGON REALMS BIOME //
    	
    	dragonDirt = new GenericDirt("Dragon Dirt", "AllOfTheEverything:DragonDirt").setCreativeTab(CreativeTabs.tabBlock)
    			.setCreativeTab(CreativeTabs.tabBlock);
    	// DO NOT SPAWN DIRT INTO A NEW WORLD!!! IT WILL NOT SPREAD GRASS ALONE!!!
    	
    	dragonGrass = new GenericGrass(dragonDirt, "Dragon Grass", "AllOfTheEverything:DragonDirt", "AllOfTheEverything:DragonGrassTop", 
    			"AllOfTheEverything:DragonGrassSide").setCreativeTab(CreativeTabs.tabBlock);
    	
    	dragonStone = new GenericBlock(Material.rock, dragonStone).setBlockName("Plain DragonStone").setStepSound(Block.soundTypeStone)
    			.setBlockTextureName("AllOfTheEverything:DragonStone").setCreativeTab(CreativeTabs.tabBlock);
    	
    	dragonWood = new GenericWood("DragonTree Wood", "AllOfTheEverything:DragonWoodTopAndBottom", "AllOfTheEverything:DragonWoodSide")
    	.setCreativeTab(CreativeTabs.tabBlock);
    	
    	 
    	
    	/*dragonLeaves = new GenericLeaves("DragonTree Leaves", "AllOfTheEverything:DragonLeavesHighRes", "AllOfTheEverything:DragonLeavesLowRes", 
    			"DragonTree Wood", 0xfd9bcb).setCreativeTab(CreativeTabs.tabBlock);  
    	
    	autumnLeaves = new GenericLeaves("Autumn Leaves", "AllOfTheEverything:AutumnLeavesHighRes", "AllOfTheEverything:AutumnLeavesLowRes", 
    			"Autumn Wood", 0xfd9bcb).setCreativeTab(CreativeTabs.tabBlock); */
    	
    	/*
    	 * 0 = Autumn
    	 * 1 = Dragon
    	 */
    	
    	
    	dragonLeaves = new GenericLeaves(1, 0xfd9bcb).setBlockName("DragonTree Leaves").setStepSound(Block.soundTypeGrass);
    	autumnLeaves = new GenericLeaves(0, 0xfd9bcb).setBlockName("Autumn Leaves").setStepSound(Block.soundTypeGrass);
    	
    	dragonTreeSapling = new BlockDragonTreeSapling();
    	
    	dragonStoneOre = new GenericOre(dragonStoneOre).setStepSound(Block.soundTypeStone).setBlockName("DragonStone Ore")
    			.setCreativeTab(CreativeTabs.tabBlock).setBlockTextureName("AllOfTheEverything:DragonStoneOre");
    	
    	// END DRAGON REALMS BIOME //
		
    	chair = new ChairBlock(new TileEntityChair(), "Chair", "AllOfTheEverything:Chair");
    	chair.setBounds(0F, 0F, 0F, 1F, 1.7F, 1F);
		
    	mug = new MugBlock(new TileEntityMug(), "Mug", "AllOfTheEverything:Mug"); // for icon, follow pattern above, icon must be Mug.png
    	mug.setBounds(1F/16F * 3F, 0F, 1F/16F * 3F, 1F-1F/16F*3F, 1F-1F/16F*3F, 1F-1F/16F*3F); // hope this is right...
    	
    	
    	largeTable = new TableBlock(new TileEntityTable(), "Large Table", "AllOfTheEverything:Table");
    	largeTable.setBounds(-1F, 0F, -1F, 1F, 0.7F, 1F);
    	
    	table = new SmallTableBlock(new TileEntitySmallTable(), "Table", "AllOfTheEverything:Table");
    	table.setBounds(0F, 0F, 0F, 1F, 0.9F, 1F);
    	
    	swordStatue = new SwordStatueBlock(new TileEntitySwordStatue(), "Sword Statue", "AllOfTheEverything:SwordStatue");
    	swordStatue.setBounds(0F, 0F, 0F, 1F, 1F, 1F);
    	
    	lamp = new LampBlock(new TileEntityLamp(), "Lamp", "AllOfTheEverything:Lamp");
    	lamp.setBounds(0F, 0F, 0F, 1F, 2.0F, 1F);
    	
    	picFrame = new PictureFrameBlock(new TileEntityFramePicture(), "Picture Frame", "AllOfTheEverything:PictureFrame");
    	picFrame.setBounds(0F, 0F, 0F, 1F, 1F, 1F);
    	
    	comfyChair = new ComfyChairBlock(new TileEntityComfyChair(), "Comfy Chair", "AllOfTheEverything:ComfyChair");
    	comfyChair.setBounds(0F, 0F, 0F, 1F, 1F, 1F);
    	
    	couch = new CouchBlock(new TileEntityCouch(), "Couch", "AllOfTheEverything:Couch");
    	
    	bookshelf = new BookshelfBlock(new TileEntityBookshelf(), "Library Bookshelf", "AllOfTheEverything:Bookshelf");
    	bookshelf.setBounds(0F, 0F, 0F, 1F, 1F, 1F);
    	
    	leaningLadder = new LeaningLadderBlock(new TileEntityLeaningLadder(), "Leaning Ladder", "AllOfTheEverything:LeaningLadder");
    	leaningLadder.setBounds(0F, 0F, 0F, 1F, 3F, 1F);
    	
    	stool = new StoolBlock(new TileEntityStool(), "Stool", "AllOfTheEverything:Stool");
    	stool.setBounds(0F, 0F, 0F, 1F, 1F, 1F);
    	
    	deskLamp = new DeskLampBlock(new TileEntityDeskLamp(), "Desk Lamp", "AllOfTheEverything:DeskLamp");
    	deskLamp.setBounds(0F, 0F, 0F, 1F, 1F, 1F);
    	
    	wallPaper1 = new WallpaperBlock(new TileEntityWallpaper(), "Wallpaper 1", "AllOfTheEverything:Couch");// make icon texture
	}
	
	public static void setBlockReqs()
	{
		pooBlock.setHarvestLevel("shovel", 0);
    	//heartGrass.setHarvestLevel("shovel", 2);// you need at least an iron shovel to mine Heartgrass
    	blackTBlock.setHarvestLevel("pickaxe", 0);
    	blackTFloor.setHarvestLevel("pickaxe", 0);
    	heartWood.setHarvestLevel("axe", 2); // you need at least an iron axe to mine Heartwood
    	dragonStoneOre.setHarvestLevel("pickaxe", 4); // and a diamond pickaxe to mine DragonStone Ore.
	}

}
