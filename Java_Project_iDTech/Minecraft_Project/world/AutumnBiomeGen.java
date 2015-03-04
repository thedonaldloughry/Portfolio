package com.DonLoughry.AllOfTheEverything.world;

import java.util.Random;

import com.DonLoughry.AllOfTheEverything.blocks.*;
import cpw.mods.fml.common.IWorldGenerator;
import net.minecraft.world.World;
import net.minecraft.world.biome.BiomeGenBase;
import net.minecraft.world.chunk.IChunkProvider;

public class AutumnBiomeGen extends BiomeGenBase implements IWorldGenerator{
	
	protected static final WorldGenAutumnTree_V2 WorldGenAutumnTree = new WorldGenAutumnTree_V2(true);
	public int treesPerChunk;
	
	public AutumnBiomeGen(int id)
	{
		super(id);
		this.heightVariation = 3F;
		this.rootHeight = 4F;
		this.waterColorMultiplier = 0x00F0FF;
		//this.getSkyColorByTemp(10.0F); // what will this do???
		this.setColor(0xFF6600); // curious...
		//this.sky.color = 0xFF6600; // a thing to try...
		this.temperature = 10.0F; // because SERIOUSLY, IT NEEDS TO STOP FREEEEEEEEEEZZZZZZIIIIIIIINNNNNNNGGGGGGGG!!!!!!!!!!
		this.enableRain = false;
		this.enableSnow = false;
		this.topBlock = BlockRegistry.autumnGrass;
		this.fillerBlock = BlockRegistry.autumnStone;
		this.setColor(0x000066);
		this.addDefaultFlowers();
		this.setBiomeName("Autumn Forest");
		this.setHeight(height_Default);
		//this.setTemperatureRainfall(0.1F, 0.4F);
		//this.theBiomeDecorator.treesPerChunk = 5;
		this.treesPerChunk = 100;
		this.theBiomeDecorator.flowersPerChunk = 4;
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
		return 0xCC3300;
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
				WorldGenAutumnTree.generate(world, random, chunkX1, chunkY1, chunkZ1);
			}
        }
	}

	private void generateNether(World world, Random random, int chunkX, int chunkZ) {
		// stuff in the Nether...
	}
	
	/*public WorldGenAbstractTree getRandomWorldGenForTrees(Random par1Random)
    {
		System.out.println("ATTEMPTED TO INSERT TREE INTO AUTUMN BIOME");
		return (WorldGenAbstractTree)(par1Random.nextInt(5) == 0 ? this.WorldGenAutumnTree : (par1Random.nextInt(10) == 0 ? this.WorldGenAutumnTree : WorldGenAutumnTree));
    }*/
    
}
