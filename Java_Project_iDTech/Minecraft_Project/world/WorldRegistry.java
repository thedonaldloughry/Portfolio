package com.DonLoughry.AllOfTheEverything.world;

import net.minecraft.world.biome.*;
import net.minecraftforge.common.BiomeDictionary;
import net.minecraftforge.common.BiomeDictionary.Type;
import net.minecraftforge.common.BiomeManager;
import cpw.mods.fml.common.IWorldGenerator;
import cpw.mods.fml.common.registry.GameRegistry;

public class WorldRegistry {
	/*
	 * The main file for doing things concerning the generation of worlds, from small things like ore placement to biome creation.
	 */
	
	// BIOME LIST //
	//public static final BiomeGenBase testBiome = new TestBiomeGen(151).setBiomeName("test").setColor(0x223263);
	public static final BiomeGenBase autumnBiome = new AutumnBiomeGen(155).setColor(0x225842);
	public static final BiomeGenBase dragonBiome = new DragonRealmsBiomeGen(154);
	// END BIOME LIST //
	
	public static void mainRegistry()
	{
		initialiseWorldGen(); // British tutorial, British spelling.
		System.out.println("Main World Registry just ran.");
	}
	
	public static void initialiseWorldGen()
	{
		registerWorldGen(new WorldGenOre(), 1);
		registerWorldGen((IWorldGenerator) autumnBiome, 20);
		registerWorldGen((IWorldGenerator) dragonBiome, 15); // NOTE: Lower probability before first release
		System.out.println("Attempted to initialize world generation.");
	}
										// worldGenClass must extend IWorldGenerator...
	public static void registerWorldGen(IWorldGenerator worldGenClass, int weightedProbability)
	{
		GameRegistry.registerWorldGenerator(worldGenClass, weightedProbability);
		System.out.println("World generator loading complete.");
	}
	
	public static void registerModBiome(BiomeGenBase newBiome, Type biomeType)
	{
		/*
		 * This method is just to register a new biome. This is the full method for implementing a new biome:
		 * 1. Create a new biome generation file (see AutumnBiomeGen and WorldGenAutumnTree_V2 for reference).
		 * 2. Go into WorldGenLayer and look for the biomes list near the top of the file.
		 * 3. Make your biome a variable, just like AutumnBiomeGen.
		 * 4. Insert your biome into one, some, or all of the lists.
		 * Note: lists are separated by climate, i.e. hot, warm, cool, cold. The custom-made WorldBiomeEvent should take care of the rest.
		 */
		BiomeDictionary.registerBiomeType(newBiome, biomeType); // higher spawn chance, maybe?
		BiomeManager.addSpawnBiome(newBiome);
	}
	
	public static void addAllBiomes()
	{
		registerModBiome(autumnBiome, Type.FOREST);
		registerModBiome(dragonBiome, Type.FOREST);
		//... and others should follow
	}
}
