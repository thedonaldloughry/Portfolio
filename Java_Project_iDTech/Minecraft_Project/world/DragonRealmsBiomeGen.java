package com.DonLoughry.AllOfTheEverything.world;

import java.util.Random;

import com.DonLoughry.AllOfTheEverything.blocks.BlockRegistry;

import cpw.mods.fml.common.IWorldGenerator;
import net.minecraft.world.World;
import net.minecraft.world.biome.BiomeGenBase;
import net.minecraft.world.chunk.IChunkProvider;

public class DragonRealmsBiomeGen extends BiomeGenBase implements IWorldGenerator{
	
	//private static Random rand = new Random();
	protected static final WorldGenDragonTree WorldGenDragonTree = new WorldGenDragonTree(true);
	public int treesPerChunk;
	
	public DragonRealmsBiomeGen(int id)
	{
		super(id);
		this.heightVariation = 40F;
		this.rootHeight = 20F;
		this.waterColorMultiplier = 0x000000;
		this.setColor(0xFF6600);
		this.temperature = 50.0F; // oh yeah...
		this.enableRain = true;
		this.enableSnow = false;
		this.topBlock = BlockRegistry.dragonGrass;
		this.fillerBlock = BlockRegistry.dragonStone;
		this.setColor(0x000000);
		this.setBiomeName("Dragon Realms Mountains");
		this.treesPerChunk = 65; // should be sparse...
		//this.setHeight(height_Default); // NOTE: height_Default sets a biome to be relatively flat.
		//this.setTemperatureRainfall(0.1F, 0.4F); // maybe rain???
		//this.getSkyColorByTemp(par1)
		
		this.spawnableCreatureList.clear();
		this.spawnableMonsterList.clear();
        //this.spawnableMonsterList.add(new BiomeGenBase.SpawnListEntry(EntityMimicTree.class, 10, 10, 10));
        //this.spawnableCreatureList.add(new BiomeGenBase.SpawnListEntry(EntityGoober.class, 10, 10, 10));
        //this.spawnableCreatureList.add(new BiomeGenBase.SpawnListEntry(EntityBlizzard.class, 10, 3, 10));
	}
	
	@Override
	public int getSkyColorByTemp(float par1)
	{
		return 0xFF0000;
	}
	
	@Override
	public void generate(Random random, int chunkX, int chunkZ, World world, IChunkProvider chunkGenerator, IChunkProvider chunkProvider) {
        switch(world.provider.dimensionId){
        case -1:
            generateNether(world, random, chunkX * 16, chunkZ * 16);
            break;
        case 0:
            generateSurface(world, random, chunkX * 16, chunkZ * 16);
            break;
        case 1:
            generateEnd(world, random, chunkX * 16, chunkZ * 16);
            break;
        }
	}

	private void generateEnd(World world, Random random, int chunkX, int chunkZ) {
		// stuff in the End...
	}

	private void generateSurface(World world, Random random, int chunkX, int chunkZ) {
		int minHeight = 40;
		int treesPerChunk = this.treesPerChunk;
        for(int k = 0; k < treesPerChunk; k++){
			int chunkX1 = chunkX + random.nextInt(16);
			int chunkY1 = minHeight + random.nextInt(40);
			int chunkZ1 = chunkZ + random.nextInt(16);

			BiomeGenBase b = world.getBiomeGenForCoords(chunkX, chunkZ);
			if(b == this)
			{
				WorldGenDragonTree.generate(world, random, chunkX1, chunkY1, chunkZ1);
			}
        }
	}

	private void generateNether(World world, Random random, int chunkX, int chunkZ) {
		// stuff in the Nether...
	}
    
}
