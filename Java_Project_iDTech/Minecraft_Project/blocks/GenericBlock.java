package com.DonLoughry.AllOfTheEverything.blocks;

import java.util.Random;

import net.minecraft.block.Block;
import net.minecraft.block.material.Material;
import net.minecraft.item.Item;

public class GenericBlock extends Block
{
	// This is a block that uses just one texture for all six of its sides //
	Block blockToDrop = BlockRegistry.pooBlock;
	static String thisName;
	public GenericBlock(Material material, Block block) 
	{
		super(material);
		this.blockToDrop = block;
		GenericBlock.thisName = this.getUnlocalizedName();
	}
	
	//If the block's drop is a block.
    @Override
    public Item getItemDropped(int metadata, Random random, int fortune) {
        return Item.getItemFromBlock(blockToDrop);
    }
}
