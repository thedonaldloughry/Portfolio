package com.DonLoughry.AllOfTheEverything.blocks;

import java.util.ArrayList;
import java.util.Random;

import cpw.mods.fml.relauncher.Side;
import cpw.mods.fml.relauncher.SideOnly;
import net.minecraft.block.Block;
import net.minecraft.block.BlockLeavesBase;
import net.minecraft.block.material.Material;
import net.minecraft.client.renderer.texture.IIconRegister;
import net.minecraft.creativetab.CreativeTabs;
import net.minecraft.item.Item;
import net.minecraft.item.ItemStack;
import net.minecraft.util.IIcon;
import net.minecraft.world.IBlockAccess;
import net.minecraft.world.World;
import net.minecraftforge.common.IShearable;

public class GenericLeaves extends BlockLeavesBase implements IShearable
{
    public static final String[] LEAF_TYPES = new String[] {"Autumn", "Dragon"};
    protected World worldObj;
    
    // We care about this... //
    public static final String[][] namesList = new String[][] {{"alloftheeverything:AutumnLeavesLowRes", "alloftheeverything:DragonLeavesLowRes"}, {"alloftheeverything:AutumnLeavesHighRes", "alloftheeverything:DragonLeavesHighRes"}};
    // this String[][] names all of our leaf types... //
    
    @SideOnly(Side.CLIENT)
    private int[] arrayEntries;
    //private int field_94394_cP;
    private IIcon[][] iconArray = new IIcon[2][];
    private int whichTexture;
    private int texColor;
    int[] adjacentTreeBlocks;
    public static boolean graphicsLevel;

    protected GenericLeaves(int textureIndex, int textureColor)
    {
        super(Material.leaves, graphicsLevel);
        this.setHardness(0.1F);
		this.setTickRandomly(true);
		this.setLightOpacity(1);
        this.setCreativeTab(CreativeTabs.tabDecorations);
        this.whichTexture = textureIndex;
        this.texColor = textureColor;
    }
    
    //@Override
	/*public boolean isFlammable(IBlockAccess world, int x, int y, int z, net.minecraftforge.common.util.ForgeDirection face) {
		return true;
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
    /*public int getFlammability(IBlockAccess world, int x, int y, int z, ForgeDirection face)
    {
        return 40;
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
    /*public int getFireSpreadSpeed(IBlockAccess world, int x, int y, int z, ForgeDirection face)
    {
        return 10;
    }

    private void removeLeaves(World par1World, int par2, int par3, int par4)
    {
        this.dropBlockAsItem(par1World, par2, par3, par4, par1World.getBlockMetadata(par2, par3, par4), 0);
        par1World.setBlockToAir(par2, par3, par4);
    }
    
    @SideOnly(Side.CLIENT)
	@Override
	public int getBlockColor() {
		double d0 = 0.5D;
		double d1 = 1.0D;
		return this.texColor;
	}
    
    /**
	 * Returns a integer with hex for 0xrrggbb with this color multiplied
	 * against the blocks color. Note only called when first determining what to
	 * render.
	 */
	/*@SideOnly(Side.CLIENT)
	@Override
	public int colorMultiplier(IBlockAccess bloque, int x, int y, int z) {
		int l = 0;
		int i1 = 0;
		int j1 = 0;

		for (int k1 = -1; k1 <= 1; ++k1) {
			for (int l1 = -1; l1 <= 1; ++l1) {
				//int i2 = bloque.getBiomeGenForCoords(x + l1, z + k1).getBiomeFoliageColor(x + l1, y, z + k1);
				int i2 = this.texColor;
				l += (i2 & 16711680) >> 16;
				i1 += (i2 & 65280) >> 8;
				j1 += i2 & 255;
			}
		}

		return (l / 9 & 255) << 16 | (i1 / 9 & 255) << 8 | j1 / 9 & 255;
	}
	
	/**
	 * Returns the color this block should be rendered. Used by leaves.
	 */
	@SideOnly(Side.CLIENT)
	@Override
	public int getRenderColor(int meta) {
		return this.texColor;
	}

    /**
     * Returns the quantity of items to drop on block destruction.
     */
    /*public int quantityDropped(Random par1Random)
    {
        return par1Random.nextInt(20) == 0 ? 1 : 0;
    }

    /**
     * Gets the item to drop upon block destruction. -- Don
     */
    public Item getItemDropped(int x, Random yRandom, int z) {
		return Item.getItemFromBlock(BlockRegistry.autumnTreeSapling); // hard-coded for test
	}

    /**
	 * returns a list of blocks with the same ID, but different meta (eg: wood
	 * returns 4 blocks)
	 */
	/*@SideOnly(Side.CLIENT)
	public void getSubBlocks(Item item, CreativeTabs tab, List listLeaves) {
		listLeaves.add(new ItemStack(item, 1, 0));
	}
    
    /**
     * Called when the player destroys a block with an item that can harvest it. (i, j, k) are the coordinates of the
     * block and l is the block's subtype/damage.
     */
    /*public void harvestBlock(World par1World, EntityPlayer par2EntityPlayer, int par3, int par4, int par5, int par6)
    {
        super.harvestBlock(par1World, par2EntityPlayer, par3, par4, par5, par6);
    }

    /**
     * Determines the damage on the item the block drops. Used in cloth and wood.
     */
    /*public int damageDropped(int par1)
    {
        return par1 & 3;
    }

    @SideOnly(Side.CLIENT)
    /**
	 * Pass true to draw this block using fancy graphics, or false for fast
	 * graphics.
	 */
	/*public void setGraphicsLevel(boolean par1) {
		this.graphicsLevel = par1;
		this.graphicsPotential = par1 ? 0 : 1;
		System.out.println(this.graphicsPotential + " THIS IS THE INTEGER VALUE OF THE GRAPHICS SETTING!!!");
	}
	
    /**
     * Is this block (a) opaque and (b) a full 1m cube?  This determines whether or not to render the shared face of two
     * adjacent blocks and also whether the player can attach torches, redstone wire, etc to this block.
     */
    public boolean isOpaqueCube()
    {
    	return false; // why was this broken?
    }

    @SideOnly(Side.CLIENT)
    /**
     * From the specified side and block metadata retrieves the blocks texture. Args: side, metadata
     */
    public IIcon getIcon(int par1, int par2)
    {
        /*return (par2 & 3) == 1 ? this.iconArray[this.field_94394_cP][1] 
        		: ((par2 & 3) == 3 ? this.iconArray[this.field_94394_cP][3] 
        				: ((par2 & 3) == 2 ? this.iconArray[this.field_94394_cP][2] 
        						: this.iconArray[this.field_94394_cP][0]));*/
    	// My guess: return (if this thing) == condition ? what to return : what to return if previous check failed
    	if(this.whichTexture == 0)
    	{
    		return this.field_150121_P == true ? this.iconArray[0][0] : this.iconArray[1][0];
    	}
    	else
    	{
    		return this.field_150121_P == true ? this.iconArray[0][1] : this.iconArray[1][1];
    	}
    	
    	//return this.iconArray[this.field_150121_P][this.whichTexture];
    }

    @SideOnly(Side.CLIENT)

    /**
     * When this method is called, your block should register all the icons it needs with the given IconRegister. This
     * is the only chance you get to register icons.
     */
    public void registerBlockIcons(IIconRegister par1IconRegister)
    {
        for (int i = 0; i < namesList.length; ++i)
        {
            this.iconArray[i] = new IIcon[namesList[i].length];

            for (int j = 0; j < namesList[i].length; ++j)
            {
            	//System.out.println(this.iconArray[i][j].toString() + "THIS IS ONE OF 4 ICONS REGISTERED");
                this.iconArray[i][j] = par1IconRegister.registerIcon(namesList[i][j]);
            }
        }
    }
    
    @SideOnly(Side.CLIENT)

    /**
     * Returns true if the given side of this block type should be rendered, if the adjacent block is at the given
     * coordinates.  Args: blockAccess, x, y, z, side
     */
    @Override
    public boolean shouldSideBeRendered(IBlockAccess par1IBlockAccess, int par2, int par3, int par4, int par5)
    {
        return true;
    }

    @Override
	public ArrayList<ItemStack> onSheared(ItemStack item, IBlockAccess world, int x, int y, int z, int fortune) {
		ArrayList<ItemStack> ret = new ArrayList<ItemStack>();
		ret.add(new ItemStack(this, 1, world.getBlockMetadata(x, y, z) & 3));
		return ret;
	}

    @Override
    public void beginLeavesDecay(World world, int x, int y, int z)
    {
        world.setBlockMetadataWithNotify(x, y, z, world.getBlockMetadata(x, y, z) | 8, 4);
    }

    /**
	 * Drops the block items with a specified chance of dropping the specified
	 * items
	 */
	/*public void dropBlockAsItemWithChance(World world, int x, int y, int z,	int meta, float par1, int par2) {
		if (!world.isRemote) {
			int j1 = this.func_150123_b(meta);

			if (par2 > 0) {
				j1 -= 2 << par2;

				if (j1 < 10) {
					j1 = 10;
				}
			}

			if (j1 <= 0) j1 = 20;

			if (world.rand.nextInt(j1) == 0) {
				Item item = this.getItemDropped(meta, world.rand, par2);
				this.dropBlockAsItem(world, x, y, z, new ItemStack(item, 1,
						this.damageDropped(meta)));
			}

			j1 = 20;

			if (par2 > 0) {
				j1 -= 10 << par2;

				if (j1 < 10) {
					j1 = 10;
				}
			}

			this.func_150124_c(world, x, y, z, meta, j1);
		}
	}*/
    
	@Override
	public void breakBlock(World world, int x, int y, int z, Block bloque, int meta) {
		byte b0 = 1;
		int i1 = b0 + 1;

		if (world.checkChunksExist(x - i1, y - i1, z - i1, x + i1, y + i1, z
				+ i1)) {
			for (int j1 = -b0; j1 <= b0; ++j1) {
				for (int k1 = -b0; k1 <= b0; ++k1) {
					for (int l1 = -b0; l1 <= b0; ++l1) {
						Block block = world.getBlock(x + j1, y + k1, z + l1);
						if (block.isLeaves(world, x + j1, y + k1, z + l1)) {
							block.beginLeavesDecay(world, x + j1, y + k1, z
									+ l1);
						}
					}
				}
			}
		}
	}
	
    @Override
    public boolean isLeaves(IBlockAccess world, int x, int y, int z)
    {
        return true;
    }

	@Override
	public boolean isShearable(ItemStack arg0, IBlockAccess arg1, int arg2, int arg3, int arg4) 
	{
		return true;
	}

	/**
	 * Ticks the block if it's been scheduled
	 */
	/*public void updateTick(World world, int x, int y, int z, Random parRandom1) {
		if (!world.isRemote) {
			int l = world.getBlockMetadata(x, y, z);

			if ((l & 8) != 0 && (l & 4) == 0) {
				byte b0 = 4;
				int i1 = b0 + 1;
				byte b1 = 32;
				int j1 = b1 * b1;
				int k1 = b1 / 2;

				if (this.arrayEntries == null) {
					this.arrayEntries = new int[b1 * b1 * b1];
				}

				int l1;

				if (world.checkChunksExist(x - i1, y - i1, z - i1, x + i1, y
						+ i1, z + i1)) {
					int i2;
					int j2;

					for (l1 = -b0; l1 <= b0; ++l1) {
						for (i2 = -b0; i2 <= b0; ++i2) {
							for (j2 = -b0; j2 <= b0; ++j2) {
								Block block = world.getBlock(x + l1, y + i2, z
										+ j2);

								if (!block.canSustainLeaves(world, x + l1, y
										+ i2, z + j2)) {
									if (block.isLeaves(world, x + l1, y + i2, z
											+ j2)) {
										this.arrayEntries[(l1 + k1) * j1
												+ (i2 + k1) * b1 + j2 + k1] = -2;
									} else {
										this.arrayEntries[(l1 + k1) * j1
												+ (i2 + k1) * b1 + j2 + k1] = -1;
									}
								} else {
									this.arrayEntries[(l1 + k1) * j1
											+ (i2 + k1) * b1 + j2 + k1] = 0;
								}
							}
						}
					}

					for (l1 = 1; l1 <= 4; ++l1) {
						for (i2 = -b0; i2 <= b0; ++i2) {
							for (j2 = -b0; j2 <= b0; ++j2) {
								for (int k2 = -b0; k2 <= b0; ++k2) {
									if (this.arrayEntries[(i2 + k1) * j1
											+ (j2 + k1) * b1 + k2 + k1] == l1 - 1) {
										if (this.arrayEntries[(i2 + k1 - 1)
												* j1 + (j2 + k1) * b1 + k2 + k1] == -2) {
											this.arrayEntries[(i2 + k1 - 1)
													* j1 + (j2 + k1) * b1 + k2
													+ k1] = l1;
										}

										if (this.arrayEntries[(i2 + k1 + 1)
												* j1 + (j2 + k1) * b1 + k2 + k1] == -2) {
											this.arrayEntries[(i2 + k1 + 1)
													* j1 + (j2 + k1) * b1 + k2
													+ k1] = l1;
										}

										if (this.arrayEntries[(i2 + k1) * j1
												+ (j2 + k1 - 1) * b1 + k2 + k1] == -2) {
											this.arrayEntries[(i2 + k1) * j1
													+ (j2 + k1 - 1) * b1 + k2
													+ k1] = l1;
										}

										if (this.arrayEntries[(i2 + k1) * j1
												+ (j2 + k1 + 1) * b1 + k2 + k1] == -2) {
											this.arrayEntries[(i2 + k1) * j1
													+ (j2 + k1 + 1) * b1 + k2
													+ k1] = l1;
										}

										if (this.arrayEntries[(i2 + k1) * j1
												+ (j2 + k1) * b1
												+ (k2 + k1 - 1)] == -2) {
											this.arrayEntries[(i2 + k1) * j1
													+ (j2 + k1) * b1
													+ (k2 + k1 - 1)] = l1;
										}

										if (this.arrayEntries[(i2 + k1) * j1
												+ (j2 + k1) * b1 + k2 + k1 + 1] == -2) {
											this.arrayEntries[(i2 + k1) * j1
													+ (j2 + k1) * b1 + k2 + k1
													+ 1] = l1;
										}
									}
								}
							}
						}
					}
				}

				l1 = this.arrayEntries[k1 * j1 + k1 * b1 + k1];

				if (l1 >= 0) {
					world.setBlockMetadataWithNotify(x, y, z, l & -9, 4);
				} else {
					this.removeLeaves(world, x, y, z);
				}
			}
		}
	}*/

	/**
	 * A randomly called display update to be able to add particles or other
	 * items for display
	 */
	@SideOnly(Side.CLIENT)
	public void randomDisplayTick(World world, int x, int y, int z,	Random parRandom1) {
		if (world.canLightningStrikeAt(x, y + 1, z)
				&& !World.doesBlockHaveSolidTopSurface(world, x, y - 1, z)
				&& parRandom1.nextInt(15) == 1) {
			double d0 = (double) ((float) x + parRandom1.nextFloat());
			double d1 = (double) y - 0.05D;
			double d2 = (double) ((float) z + parRandom1.nextFloat());
			world.spawnParticle("dripWater", d0, d1, d2, 0.0D, 0.0D, 0.0D);
		}
		else if(this.whichTexture == 0) // 0 = Autumn Leaves
		{
			double d0 = (double) ((float) x + parRandom1.nextFloat());
			double d1 = (double) y - 0.05D;
			double d2 = (double) ((float) z + parRandom1.nextFloat());
			world.spawnParticle("dripWater", d0, d1, d2, 0.0D, 0.0D, 0.0D); // just a test...
		}
	}
	
}
