package com.DonLoughry.AllOfTheEverything.blocks;

import java.util.Random;

import net.minecraft.block.BlockLadder;
import net.minecraft.creativetab.CreativeTabs;
import net.minecraft.entity.EntityLivingBase;
import net.minecraft.item.Item;
import net.minecraft.world.*;

public class LadderLike extends BlockLadder
{
	
	protected boolean isLadder;
	
	public LadderLike(boolean isThisALadder)
	{
		super();
		this.isLadder = isThisALadder;
		this.setCreativeTab(CreativeTabs.tabDecorations);
	}
	
	@Override
    public Item getItemDropped(int metadata, Random random, int fortune) {
        return Item.getItemFromBlock(this);
    }
	
	@Override
	public boolean isLadder(IBlockAccess world, int x, int y, int z, EntityLivingBase entity)
	{
		return this.isLadder; // ladder-like! not actually a ladder, but rather something that renders like one!
	}
	
	
	
	/*
	 * Here's some of the old code for Minecraft ladders, because you spent hours writing it and it deserves some
	 * respect. And it's kinda interesting.
	 * 
	 * public AxisAlignedBB getCollisionBoundingBoxFromPool(World par1World, int par2, int par3, int par4)
	{
		this.setBlockBoundsBasedOnState(par1World, par2, par3, par4);
		return super.getSelectedBoundingBoxFromPool(par1World, par2, par3, par4);
	}
	
	@SideOnly(Side.CLIENT)
	
	public AxisAlignedBB getSelectedBoundingBoxFromPool(World par1World, int par2, int par3, int par4)
	{
		this.setBlockBoundsBasedOnState(par1World, par2, par3, par4);
		return super.getSelectedBoundingBoxFromPool(par1World, par2, par3, par4);
	}
	
	public void setBlockBoundsBasedOnState(IBlockAccess par1BlockAccess, int par2, int par3, int par4)
	{
		this.updateLadderBounds(par1BlockAccess.getBlockMetadata(par2, par3, par4));
	}
	
	public void updateLadderBounds(int par1)
	{
		float var3 = 0.125F;
		
		if (par1 == 2)
			this.setBlockBounds(0.0F, 0.0F, 1.0F - var3, 1.0F, 1.0F, 1.0F);
		if (par1 == 3)
			this.setBlockBounds(0.0F, 0.0F, 0.0F, 1.0F, 1.0F, var3);
		if (par1 == 4)
			this.setBlockBounds(1.0F - var3, 0.0F, 0.0F, 1.0F, 1.0F, 1.0F);
		if (par1 == 5)
			this.setBlockBounds(1.0F - var3, 0.0F, 0.0F, 1.0F, 1.0F, 1.0F);
	}
	
	public boolean isOpaqueCube()
	{
		return false;
	}
	
	public boolean renderAsNormalBlock()
	{
		return false;
	}
	
	public int getRenderType()
	{
		return 8;
	}
	
	public boolean canPlaceBlockAt(World par1World, int par2, int par3, int par4)
	{
		return par1World.isSideSolid(par2 - 1, par3, par4, EAST) ||
			   par1World.isSideSolid(par2 + 1, par3, par4, WEST) ||
			   par1World.isSideSolid(par2, par3, par4 - 1, SOUTH)||
			   par1World.isSideSolid(par2, par3, par4 + 1, NORTH);
	}
	
	public int onBlockPlaced(World par1World, int par2, int par3, int par4, int par5, int par6, int par7, int par8, int par9)
	{
		int var10 = par9;
		
		if((var10 == 0 || par5 == 2) && par1World.isSideSolid(par2, par3, par4 + 1, NORTH))
			var10 = 2;
		if((var10 == 0 || par5 == 3) && par1World.isSideSolid(par2, par3, par4 - 1, SOUTH))
			var10 = 3;
		if((var10 == 0 || par5 == 4) && par1World.isSideSolid(par2 + 1, par3, par4, WEST))
			var10 = 4;
		if((var10 == 0 || par5 == 5) && par1World.isSideSolid(par2 - 1, par3, par4, EAST))
			var10 = 4;
		return var10;
	}
	
	public void onNeighborBlockChange(World par1World, int par2, int par3, int par4, Block par5)
	{
		int var6 = par1World.getBlockMetadata(par2, par3, par4);
		boolean var7 = false;
		
		if (var6 == 2 && par1World.isSideSolid(par2, par3, par4 + 1, NORTH))
			var7 = true;
		if (var6 == 3 && par1World.isSideSolid(par2, par3, par4 - 1, SOUTH))
			var7 = true;
		if (var6 == 4 && par1World.isSideSolid(par2 + 1, par3, par4, WEST))
			var7 = true;
		if (var6 == 5 && par1World.isSideSolid(par2 - 1, par3, par4, EAST))
			var7 = true;
		
		if (!var7)
		{
			this.dropBlockAsItem(par1World, par2, par3, par4, var6, 0);
			par1World.setBlockMetadataWithNotify(par2, par3, par4, par5, 0);
		}
		
		super.onNeighborBlockChange(par1World, par2, par3, par4, this.getBlockById(var6));// may the force be with me
	}
	
	public int quantityDropped(Random par1Random)
	{
		return 1;
	}
	
	@Override
	public boolean isLadder(IBlockAccess world, int x, int y, int z, EntityLivingBase entity)
	{
		return true;
	}*/

}
