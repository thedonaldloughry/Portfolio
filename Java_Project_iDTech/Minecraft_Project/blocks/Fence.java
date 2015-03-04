package com.DonLoughry.AllOfTheEverything.blocks;

import java.util.Random;

import net.minecraft.block.*;
import net.minecraft.block.material.Material;
import net.minecraft.creativetab.CreativeTabs;
import net.minecraft.item.Item;

public class Fence extends BlockFence{

	public Fence(String name, Material material) {
		super(name, material);
		this.setCreativeTab(CreativeTabs.tabDecorations);
		// TODO Auto-generated constructor stub
	}
	
	@Override
    public Item getItemDropped(int metadata, Random random, int fortune) {
        return Item.getItemFromBlock(this);
    }
	
	

}
