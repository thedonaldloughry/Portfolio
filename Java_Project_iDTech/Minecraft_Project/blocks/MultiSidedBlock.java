package com.DonLoughry.AllOfTheEverything.blocks;

import java.util.Random;

import cpw.mods.fml.relauncher.Side;
import cpw.mods.fml.relauncher.SideOnly;
import net.minecraft.block.Block;
import net.minecraft.block.material.Material;
import net.minecraft.client.renderer.texture.IIconRegister;
import net.minecraft.item.Item;
import net.minecraft.util.IIcon;

public class MultiSidedBlock extends Block
{
	// This is a block that could use different textures for all of its sides.//
	// Bottom = 0, Top = 1, Sides = 2 - 5 //
	Block blockToDrop = BlockRegistry.pooBlock;
	@SideOnly(Side.CLIENT) private IIcon texBottom;String bottom;
	@SideOnly(Side.CLIENT) private IIcon texTop;String top;
	@SideOnly(Side.CLIENT) private IIcon texSide1;
	@SideOnly(Side.CLIENT) private IIcon texSide2;
	@SideOnly(Side.CLIENT) private IIcon texSide3;
	@SideOnly(Side.CLIENT) private IIcon texSide4;	
	String side1;
	String side2;
	String side3;
	String side4;
	
	public MultiSidedBlock(Material material, Block block, 
			String bottomTex, String topTex, String sideTex1, String sideTex2, String sideTex3, String sideTex4) 
	{
		super(material);
		this.blockToDrop = block;
		this.bottom = bottomTex;
		this.top = topTex;
		this.side1 = sideTex1;
		this.side2 = sideTex2;
		this.side3 = sideTex3;
		this.side4 = sideTex4;
	}
	
	public MultiSidedBlock(Material material, Block block, 
			String bottomTex, String topTex, String sideTex)
	{
		this(material, block, bottomTex, topTex, sideTex, sideTex, sideTex, sideTex);
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
    		return this.texSide1;
    	else if(par1 == 3)
    		return this.texSide2;
    	else if(par1 == 4)
    		return this.texSide3;
    	else
    		return this.texSide4;
    }
    
    @SideOnly(Side.CLIENT)
    public void registerBlockIcons(IIconRegister par1IIconRegister)
    {
    	this.texBottom = par1IIconRegister.registerIcon(bottom);
    	this.texTop = par1IIconRegister.registerIcon(top);
    	this.texSide1 = par1IIconRegister.registerIcon(side1);
    	this.texSide2 = par1IIconRegister.registerIcon(side2);
    	this.texSide3 = par1IIconRegister.registerIcon(side3);
    	this.texSide4 = par1IIconRegister.registerIcon(side4);
    }
}