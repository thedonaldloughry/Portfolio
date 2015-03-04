package com.DonLoughry.AllOfTheEverything.blocks;

import java.util.Random;

import cpw.mods.fml.relauncher.Side;
import cpw.mods.fml.relauncher.SideOnly;
import net.minecraft.block.*;
import net.minecraft.block.material.Material;
import net.minecraft.client.renderer.texture.IIconRegister;
import net.minecraft.entity.EnumCreatureType;
import net.minecraft.item.Item;
import net.minecraft.util.IIcon;
import net.minecraft.world.IBlockAccess;
import net.minecraftforge.common.IPlantable;
import net.minecraftforge.common.util.ForgeDirection;

public class GenericDirt extends Block
{//
		// Bottom = 0, Top = 1, Sides = 2 - 5 //
		Block blockToDrop = BlockRegistry.pooBlock;
		@SideOnly(Side.CLIENT) private IIcon texSide;   String side;
		
		public GenericDirt(String dirtName, String sideTex)
		{
			/*
			 * A file to cover all dirt-type mod blocks. The behavior of modded dirt is as follows:
			 * 1. Must allow the placement of plants and trees.
			 * 2. Must convert to/from a custom modded grass-type file. Dirt's spawning is not done in world generation,
			 * 	  but rather by its grass type when adequate sunlight cannot reach the block. This is done in the updateTick()
			 *    method.
			 * 3. Allows the spawning of creatures/monsters. By default, set to allow all creatures/monsters.
			 */
			super(Material.ground); // hope this is right
			this.blockToDrop = this;
			this.side = sideTex;
			this.setHardness(0.5F);
			this.setStepSound(soundTypeGrass);
			this.setBlockName(dirtName);
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
	    		return this.texSide;
	    	else if(par1 == 1)
	    		return this.texSide;
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
	    	this.texSide = par1IIconRegister.registerIcon(side);
	    }
	    
	    @Override
	    public boolean canSustainPlant(IBlockAccess world, int x, int y, int z, ForgeDirection direction,  IPlantable plantable)
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
	    	 * Things can spawn here unconditionally. Come to me, minions!
	    	 */
	    	return true;
	    }
	    
	}