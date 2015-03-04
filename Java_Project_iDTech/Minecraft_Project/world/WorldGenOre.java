package com.DonLoughry.AllOfTheEverything.world;

import java.util.Random;

import com.DonLoughry.AllOfTheEverything.blocks.BlockRegistry;

import net.minecraft.block.Block;
import net.minecraft.init.Blocks;
import net.minecraft.world.*;
import net.minecraft.world.chunk.IChunkProvider;
import net.minecraft.world.gen.feature.WorldGenMinable;
import cpw.mods.fml.common.IWorldGenerator;

public class WorldGenOre implements IWorldGenerator
{
	
	@Override
	public void generate(Random random, int chunkX, int chunkZ, World world, IChunkProvider chunkGenerator, IChunkProvider chunkProvider) {
		switch (world.provider.dimensionId) {
		case -1:
			generateNether(random, chunkX * 16, chunkZ * 16, world);
			break;
		case 0:
			generateSurface(random, chunkX * 16, chunkZ * 16, world);
			break;
		case 1:
			generateEnd(random, chunkX * 16, chunkZ * 16, world);
			break;
		default:
			;
		}

	}

	private void addOre(Block block, Block blockSpawn, Random random, World world, int posX, int posZ, int minY, int maxY, int minVeinSize, int maxVeinSize, int spawnChance) {
		for (int i = 0; i < spawnChance; i++) {
			int defaultChunkSize = 16;

			int xPos = posX + random.nextInt(defaultChunkSize);
			int yPos = minY + random.nextInt(maxY - minY);
			int zPos = posZ + random.nextInt(defaultChunkSize);

			new WorldGenMinable(block, (minVeinSize + random.nextInt(maxVeinSize - minVeinSize)), blockSpawn).generate(world, random, xPos, yPos, zPos);
		}
	}

	private void generateEnd(Random random, int chunkX, int chunkZ, World world) {
		// It won't appear in the End

	}

	private void generateSurface(Random random, int chunkX, int chunkZ, World world) // here is where we add ores to our world.
	{
		addOre(BlockRegistry.deadStone, Blocks.stone, random, world, chunkX, chunkZ, 20, 60, 5, 10, 20);
		addOre(BlockRegistry.dragonStoneOre, BlockRegistry.dragonStone, random, world, chunkX, chunkZ, 20, 60, 5, 8, 10);
		addOre(Blocks.flowing_lava, BlockRegistry.dragonStone, random, world, chunkX, chunkZ, 20, 60, 5, 8, 20);
	}

	private void generateNether(Random random, int chunkX, int chunkZ, World world) {
		// It won't appear in the Nether

	}


}
