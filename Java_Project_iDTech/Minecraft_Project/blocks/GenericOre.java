// Credit to http://www.minecraftforge.net/wiki/Tutorials/Basic_Blocks for this. Refer to that site for more info. //

package com.DonLoughry.AllOfTheEverything.blocks;

import java.util.Random;

import net.minecraft.block.Block;
import net.minecraft.block.BlockOre;
import net.minecraft.item.Item;

public class GenericOre extends BlockOre
{
	Block oreToDrop = BlockRegistry.dragonStoneOre;
	
	public GenericOre(Block blockToDrop) 
	{
		super();
		this.oreToDrop = blockToDrop;
	}
	
	// if the thing dropped is a custom item //
	@Override
    public Item getItemDropped(int metadata, Random random, int fortune) {
        return Item.getItemFromBlock(this.oreToDrop);
    }
}