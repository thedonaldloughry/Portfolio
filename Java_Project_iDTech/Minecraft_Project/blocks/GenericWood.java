package com.DonLoughry.AllOfTheEverything.blocks;

import java.util.List;
import java.util.Random;

import cpw.mods.fml.relauncher.Side;
import cpw.mods.fml.relauncher.SideOnly;
import net.minecraft.block.*;
import net.minecraft.block.material.Material;
import net.minecraft.client.renderer.texture.IIconRegister;
import net.minecraft.creativetab.CreativeTabs;
import net.minecraft.entity.EnumCreatureType;
import net.minecraft.item.Item;
import net.minecraft.item.ItemStack;
import net.minecraft.util.IIcon;
import net.minecraft.world.IBlockAccess;
import net.minecraft.world.World;
import net.minecraftforge.common.util.ForgeDirection;

public class GenericWood extends Block
{
	
	// This is a block that could use different textures for all of its sides.//
		// Bottom = 0, Top = 1, Sides = 2 - 5 //
		Block blockToDrop = BlockRegistry.pooBlock;
		@SideOnly(Side.CLIENT) private IIcon texInner;    String inner;
		@SideOnly(Side.CLIENT) private IIcon texSide;   String side;
		
		public GenericWood(String woodName, String innerTex, String sideTex)
		{
			/*
			 * A file to cover all wood-type mod blocks. The behavior of modded grass is as follows:
			 * 1. Must sustain leaves.
			 */
			super(Material.wood);
			this.blockToDrop = this;
			this.inner = innerTex;
			this.side = sideTex;
			this.setHardness(0.5F);
			this.setStepSound(soundTypeWood);
			this.setBlockName(woodName);
		}
		
		/**
	     * Chance that fire will spread and consume this block.
	     * 300 being a 100% chance, 0, being a 0% chance.
	     *
	     * @param world The current world
	     * @param x The blocks X position
	     * @param y The blocks Y position
	     * @param z The blocks Z position
	     * @param face The face that the fire is coming from
	     * @return A number ranging from 0 to 300 relating used to determine if the block will be consumed by fire
	     */
	    public int getFlammability(IBlockAccess world, int x, int y, int z, ForgeDirection face)
	    {
	        return 20;
	    }

	    /**
	     * Called when fire is updating on a neighbor block.
	     * The higher the number returned, the faster fire will spread around this block.
	     *
	     * @param world The current world
	     * @param x The blocks X position
	     * @param y The blocks Y position
	     * @param z The blocks Z position
	     * @param face The face that the fire is coming from
	     * @return A number that is used to determine the speed of fire growth around the block
	     */
	    public int getFireSpreadSpeed(IBlockAccess world, int x, int y, int z, ForgeDirection face)
	    {
	        return 5;
	    }
		
		@Override
		public int damageDropped(int damage) {
			return 20;
		}

		/**
		 * Limit to valid metadata
		 * @param par1
		 * @return a number between 0 and 3
		 */
		public static int func_150165_c(int par1)
	    {
	        return par1 & 3;
	    }
		
		//If the block's drop is a block.
	    @Override
	    public Item getItemDropped(int metadata, Random random, int fortune) {
	        return Item.getItemFromBlock(blockToDrop);
	    }
	    
	    @SideOnly(Side.CLIENT)
	    public IIcon getIcon(int par1, int par2)
	    {
	    	//par1 is which side of the block is currently being set. There are 6 sides on each block (yay basic geometry!)
	    	//par2 is... something else that we don't need here. Now, prepare for a system of crappy-looking if statements!
	    	if(par1 == 0)
	    		return this.texInner;
	    	else if(par1 == 1)
	    		return this.texInner;
	    	else if(par1 == 2)
	    		return this.texSide;
	    	else if(par1 == 3)
	    		return this.texSide;
	    	else if(par1 == 4)
	    		return this.texSide;
	    	else
	    		return this.texSide;
	    }
	    
	    @SideOnly(Side.CLIENT)
	    public void registerBlockIcons(IIconRegister par1IIconRegister)
	    {
	    	this.texInner = par1IIconRegister.registerIcon(inner);
	    	this.texSide = par1IIconRegister.registerIcon(side);
	    }
	    
	    @Override
	    public boolean canSustainLeaves(IBlockAccess world, int x, int y, int z)
	    {
	    	/*
	    	 * note: wood needs this same function, but in the form of canSustainLeaves...
	    	 */
	    	return true;
	    }
	    
	    @Override
	    public boolean canCreatureSpawn(EnumCreatureType type, IBlockAccess world, int x, int y, int z)
	    {
	    	/*
	    	 * Things cannot spawn here. It's... a tree.
	    	 */
	    	return false;
	    }
	    
	    @Override
	    public boolean isWood(IBlockAccess block, int x, int y, int z)
	    {
	        return true;
	    }
	    
	    /**
	     * returns a list of blocks with the same ID, but different meta (eg: wood returns 4 blocks)
	     */
	    @SuppressWarnings("unchecked")
		@SideOnly(Side.CLIENT)
	    public void getSubBlocks(Item item, CreativeTabs tab, @SuppressWarnings("rawtypes") List blockList)
	    {
	        blockList.add(new ItemStack(item, 1, 0));
	    }
	    
	    
	    /********************************************** Event Methods **************************************************/
	    @Override
	    public void breakBlock(World world, int x, int y, int z, Block bloque, int meta)
	    {
	        byte b0 = 4;
	        int i1 = b0 + 1;

	        if (world.checkChunksExist(x - i1, y - i1, z - i1, x + i1, y + i1, z + i1))
	        {
	            for (int j1 = -b0; j1 <= b0; ++j1)
	            {
	                for (int k1 = -b0; k1 <= b0; ++k1)
	                {
	                    for (int l1 = -b0; l1 <= b0; ++l1)
	                    {
	                        Block block = world.getBlock(x + j1, y + k1, z + l1);
	                        if (block.isLeaves(world, x + j1, y + k1, z + l1))
	                        {
	                            block.beginLeavesDecay(world, x + j1, y + k1, z + l1);
	                        }
	                    }
	                }
	            }
	        }
	    }
}
