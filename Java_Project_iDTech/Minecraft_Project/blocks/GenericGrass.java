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
import net.minecraft.world.World;
import net.minecraftforge.common.IPlantable;
import net.minecraftforge.common.util.ForgeDirection;

public class GenericGrass extends Block
{
	
	// This is a block that could use different textures for all of its sides.//
		// Bottom = 0, Top = 1, Sides = 2 - 5 //
		Block blockToDrop = BlockRegistry.pooBlock;
		Block dirt;
		@SideOnly(Side.CLIENT) private IIcon texBottom; String bottom;
		@SideOnly(Side.CLIENT) private IIcon texTop;    String top;
		@SideOnly(Side.CLIENT) private IIcon texSide;   String side;
		
		public GenericGrass(Block dirtBase, String grassName, String bottomTex, String topTex, String sideTex)
		{
			/*
			 * A file to cover all grass-type mod blocks. The behavior of modded grass is as follows:
			 * 1. Must allow the placement of plants and trees.
			 * 2. Must convert to/from a custom modded dirt-type file. Dirt's spawning is not done in world generation,
			 * 	  but rather by its grass type when adequate sunlight cannot reach the block. This is done in the updateTick()
			 *    method.
			 * 3. Allows the spawning of creatures/monsters. By default, set to allow all creatures/monsters.
			 */
			super(Material.grass);
			this.blockToDrop = this;
			this.dirt = dirtBase;
			this.bottom = bottomTex;
			this.top = topTex;
			this.side = sideTex;
			this.setHardness(0.5F);
			this.setStepSound(soundTypeGrass);
			this.setBlockName(grassName);
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
	    		return this.texBottom;
	    	else if(par1 == 1)
	    		return this.texTop;
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
	    	this.texBottom = par1IIconRegister.registerIcon(bottom);
	    	this.texTop = par1IIconRegister.registerIcon(top);
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
	    
		@Override
	    public void updateTick(World p_149674_1_, int p_149674_2_, int p_149674_3_, int p_149674_4_, Random p_149674_5_)
	    {
	    	/*
	    	 * A copypasta version of Minecraft's default dirt/grass generation code. Here's a quick explanation of what it's doing.
	    	 * Note that because of the way these variables are named (why, Minecraft, why???), I am not going to risk re-naming them,
	    	 * so bear with me as I make my best guess at what the heck this code is doing:
	    	 * 
	    	 * The outer if check, as you can tell, simply makes sure the world is not a remote world.
	    	 * The first inner if check takes a look at how much light is on a block. If the light conditions are poor, the
	    	 * block becomes dirt.
	    	 * The else-if check below that checks the opposite case. If the lighting conditions are adequate, not only does this 
	    	 * block become grass, but the grass is allowed to spread along the surface organically. In this way, Minecraft gives the
	    	 * grass layer of its biomes the appearance of being two layers, when in fact... it's all really just grass.
	    	 */
	        if (!p_149674_1_.isRemote)
	        {
	            if (p_149674_1_.getBlockLightValue(p_149674_2_, p_149674_3_ + 1, p_149674_4_) < 4 && p_149674_1_.getBlockLightOpacity(p_149674_2_, p_149674_3_ + 1, p_149674_4_) > 2)
	            {
	                p_149674_1_.setBlock(p_149674_2_, p_149674_3_, p_149674_4_, dirt); // put dirt here!!!
	            }
	            else if (p_149674_1_.getBlockLightValue(p_149674_2_, p_149674_3_ + 1, p_149674_4_) >= 9)
	            {
	                for (int l = 0; l < 4; ++l)
	                {
	                    int i1 = p_149674_2_ + p_149674_5_.nextInt(3) - 1;
	                    int j1 = p_149674_3_ + p_149674_5_.nextInt(5) - 3;
	                    int k1 = p_149674_4_ + p_149674_5_.nextInt(3) - 1;
	                    Block block = p_149674_1_.getBlock(i1, j1 + 1, k1);

	                    if (p_149674_1_.getBlock(i1, j1, k1) == dirt && p_149674_1_.getBlockMetadata(i1, j1, k1) == 0 && p_149674_1_.getBlockLightValue(i1, j1 + 1, k1) >= 4 && p_149674_1_.getBlockLightOpacity(i1, j1 + 1, k1) <= 2)
	                    {
	                        p_149674_1_.setBlock(i1, j1, k1, this);
	                    }
	                }
	            }
	        }
	    }
	    
	}
