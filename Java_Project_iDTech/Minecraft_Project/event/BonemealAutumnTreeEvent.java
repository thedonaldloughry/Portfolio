package com.DonLoughry.AllOfTheEverything.event;

import java.util.Random;

import com.DonLoughry.AllOfTheEverything.blocks.BlockAutumnTreeSapling;
import com.DonLoughry.AllOfTheEverything.blocks.BlockRegistry;

import cpw.mods.fml.common.eventhandler.Event.Result;
import cpw.mods.fml.common.eventhandler.SubscribeEvent;
import net.minecraft.block.Block;
import net.minecraft.item.ItemStack;
import net.minecraft.world.World;
import net.minecraftforge.event.entity.player.BonemealEvent;

public class BonemealAutumnTreeEvent {

	@SubscribeEvent
	public void onUseBonemeal(BonemealEvent event)
	{
	  World world = event.world;
	  int x = event.x;
	  int y = event.y;
	  int z = event.z;
	  Block block = event.block;
	 
	  Random rand = new Random();
	  int i = rand.nextInt(13);
	 
	  if (block == BlockRegistry.autumnTreeSapling && event.world.getBlockMetadata(x, y, z) == 0)
	  {
	   int var14 = y + 1;
	   for (int i1 = 0; i1 < 128; ++i1)
	   {
	    for (int i2 = 0; i2 < i1 / 16; ++i2)
	    {
		 x += event.world.rand.nextInt(3) - 1;
		 var14 += (event.world.rand.nextInt(3) - 1) * event.world.rand.nextInt(3) / 2;
		 z += event.world.rand.nextInt(3) - 1;
	    }
	    if (event.world.getBlock(x, var14, z).isAir(world, x, var14, z))
	    {
		 if (BlockRegistry.autumnTreeSapling.canReplace(world, x, var14, z, 0, new ItemStack(BlockRegistry.autumnTreeSapling, 1, i)))
		 {
		  event.setResult(Result.ALLOW);
		  if (!event.world.isRemote)
		  {
			  ((BlockAutumnTreeSapling)BlockRegistry.autumnTreeSapling).markOrGrowMarked(event.world, event.x, event.y, event.z, event.world.rand);
		  }
		 }
	    }
	   }
	  }
	}

}
