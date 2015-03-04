package com.DonLoughry.AllOfTheEverything.world;

import com.DonLoughry.AllOfTheEverything.blocks.BlockRegistry;
import com.DonLoughry.AllOfTheEverything.entity.*;

import net.minecraft.world.biome.BiomeGenBase;

public class TestBiomeGen extends BiomeGenBase{
	
	@SuppressWarnings("unchecked")
	public TestBiomeGen(int id)
	{
		/*
		 * This is just a test. If you are running on eclipse, and type in "this.", you should see all of the fields that need to be
		 * filled out for a well-working biome. This is just supposed to test whether or not I actually spawned a biome into the world.
		 * If this works... people will flip out over this mod, man.
		 */
		super(id);
		
		this.heightVariation = 7F;
		this.rootHeight = 5F;
		this.waterColorMultiplier = 0x000066;
		this.temperature = 0.5F;
		this.enableRain = true;
		this.enableSnow = false;
		this.topBlock = BlockRegistry.heartGrass;
		this.fillerBlock = BlockRegistry.heartWood;
		this.setColor(0x000066);
		this.addDefaultFlowers();
		this.setBiomeName("Midnight Garden");
		this.setHeight(height_Default);
		this.setTemperatureRainfall(0.3F, 0.7F);
		
		this.spawnableCreatureList.clear();
		this.spawnableMonsterList.clear();
        this.spawnableMonsterList.add(new BiomeGenBase.SpawnListEntry(EntityMimicTree.class, 10, 10, 10));
        //this.spawnableCreatureList.add(new BiomeGenBase.SpawnListEntry(EntityGoober.class, 10, 10, 10));
        this.spawnableCreatureList.add(new BiomeGenBase.SpawnListEntry(EntityBlizzard.class, 10, 3, 10));
        
		System.out.println("BIIIIIIIIIIIIIOOOOOOOOOOOOOOMMMMMMMMMMMMMMMMEEEEEEEEEE!!!!!!!!!!!!");
	}

}
