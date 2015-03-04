package com.DonLoughry.AllOfTheEverything.blocks;

/*
 * Source: https://github.com/alca259/alca/blob/master/java/alca259/life/blocks/BlockCherrySapling.java
 */

import java.util.List;
import java.util.Random;

import com.DonLoughry.AllOfTheEverything.lib.References;
import com.DonLoughry.AllOfTheEverything.world.*;

import net.minecraft.block.Block;
import net.minecraft.block.BlockFlower;
import net.minecraft.client.renderer.texture.IIconRegister;
import net.minecraft.creativetab.CreativeTabs;
import net.minecraft.init.Blocks;
import net.minecraft.item.Item;
import net.minecraft.item.ItemStack;
import net.minecraft.util.IIcon;
import net.minecraft.util.MathHelper;
import net.minecraft.world.IBlockAccess;
import net.minecraft.world.World;
import net.minecraft.world.gen.feature.WorldGenerator;
import net.minecraftforge.common.EnumPlantType;
import cpw.mods.fml.relauncher.Side;
import cpw.mods.fml.relauncher.SideOnly;

public class BlockDragonTreeSapling extends BlockFlower {

	/****************************************** VARIABLES *********************************************/
	public static final String[] typesSapling = new String[] { "DragonTreeSapling" };
	private static final IIcon[] textures = new IIcon[typesSapling.length];

	/****************************************** CONSTRUCTOR *********************************************/
	public BlockDragonTreeSapling() {
		super(0);

		// Properties
		this.stepSound = soundTypeGrass;
		this.setHardness(0.0F);
		float f = 0.4F;
		this.setBlockBounds(0.5F - f, 0.0F, 0.5F - f, 0.5F + f, f * 2.0F, 0.5F + f);
		this.setCreativeTab(CreativeTabs.tabDecorations);
		this.setBlockName("Dragon Tree Sapling");
		this.setTickRandomly(true);
	}

	/****************************************** PROPERTY METHODS *********************************************/
	/**
	 * Gets the block's texture. Args: side, meta
	 */
	@SideOnly(Side.CLIENT)
	public IIcon getIcon(int side, int meta) {
		meta &= 7;
		return textures[MathHelper.clamp_int(meta, 0, 5)];
	}

	@SideOnly(Side.CLIENT)
	public void registerBlockIcons(IIconRegister iconReg) {
		for (int i = 0; i < textures.length; ++i) {
			textures[i] = iconReg.registerIcon(References.MODID + ":" + typesSapling[i]);
		}
	}

    /**
     * Determines if the same sapling is present at the given location.
     */
    public boolean isSameSapling(World par1World, int par2, int par3, int par4, int par5)
    {
        return par1World.getBlock(par2, par3, par4) == this && (par1World.getBlockMetadata(par2, par3, par4) & 3) == par5;
    }
	/**
	 * Determines the damage on the item the block drops. Used in cloth and
	 * wood.
	 */
	public int damageDropped(int par1) {
		return par1 & 3;
	}

	/**
	 * returns a list of blocks with the same ID, but different meta (eg: wood
	 * returns 4 blocks)
	 */
	@SuppressWarnings("unchecked")
	@SideOnly(Side.CLIENT)
	public void getSubBlocks(Item item, CreativeTabs tab, @SuppressWarnings("rawtypes") List listSaplings) {
		listSaplings.add(new ItemStack(item, 1, 0));
	}

	/****************************************** ACTION METHODS *********************************************/
	/**
	 * Mark or Grow marked
	 * @param world
	 * @param x
	 * @param y
	 * @param z
	 * @param par1Random
	 */
	public void markOrGrowMarked(World world, int x, int y, int z,	Random par1Random) {
		int l = world.getBlockMetadata(x, y, z);

		if ((l & 8) == 0) {
			world.setBlockMetadataWithNotify(x, y, z, l | 8, 4);
		} else {
			this.growTree(world, x, y, z, par1Random);
		}
	}

	/**
	 * Grow tree function
	 ***/
	public void growTree(World world, int x, int y, int z, Random par1Random) {
		System.out.println("ATTEMPTED TO GROW A TREE");
		if (!net.minecraftforge.event.terraingen.TerrainGen.saplingGrowTree(world, par1Random, x, y, z)) return;
		int l = world.getBlockMetadata(x, y, z) & 7;
		Object object = null;
		int i1 = 0;
		int j1 = 0;

		// New Generate Tree Object
		object = new WorldGenDragonTree(true);

		// Eliminate the sapling.
		world.setBlock(x, y, z, Blocks.air, 0, 4);

		// Generate the tree.
		if (!((WorldGenerator) object).generate(world, par1Random, x + i1, y, z	+ j1)) {
			world.setBlock(x, y, z, this, l, 4);
		}
	}

	/****************************************** EVENT METHODS *********************************************/
	/**
	 * Ticks the block if it's been scheduled
	 */
	@Override
	public void updateTick(World world, int x, int y, int z, Random par1Random) {
		if (!world.isRemote) {
			super.updateTick(world, x, y, z, par1Random);

			if (world.getBlockLightValue(x, y + 1, z) >= 9 && par1Random.nextInt(7) == 0) {
				this.markOrGrowMarked(world, x, y, z, par1Random);
			}
		}
	}
	
	@Override
    public EnumPlantType getPlantType(IBlockAccess world, int x, int y, int z)
    {
        if (this == Blocks.wheat)          return EnumPlantType.Crop;
        if (this == Blocks.carrots)        return EnumPlantType.Crop;
        if (this == Blocks.potatoes)       return EnumPlantType.Crop;
        if (this == Blocks.melon_stem)     return EnumPlantType.Crop;
        if (this == Blocks.pumpkin_stem)   return EnumPlantType.Crop;
        if (this == Blocks.waterlily)      return EnumPlantType.Water;
        if (this == Blocks.red_mushroom)   return EnumPlantType.Cave;
        if (this == Blocks.brown_mushroom) return EnumPlantType.Cave;
        if (this == Blocks.nether_wart)    return EnumPlantType.Nether;
        if (this == Blocks.sapling)        return EnumPlantType.Plains;     
        return EnumPlantType.Plains;
    }

    @Override
    public Block getPlant(IBlockAccess world, int x, int y, int z)
    {
        return this;
    }

    @Override
    public int getPlantMetadata(IBlockAccess world, int x, int y, int z)
    {
        return world.getBlockMetadata(x, y, z);
    }

}
