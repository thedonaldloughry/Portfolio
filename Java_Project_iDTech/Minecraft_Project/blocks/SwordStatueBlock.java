package com.DonLoughry.AllOfTheEverything.blocks;

import cpw.mods.fml.relauncher.Side;
import cpw.mods.fml.relauncher.SideOnly;
import net.minecraft.block.Block;
import net.minecraft.block.BlockContainer;
import net.minecraft.block.material.Material;
import net.minecraft.client.renderer.texture.IIconRegister;
import net.minecraft.creativetab.CreativeTabs;
import net.minecraft.entity.EntityLivingBase;
import net.minecraft.item.ItemStack;
import net.minecraft.tileentity.TileEntity;
import net.minecraft.util.MathHelper;
import net.minecraft.world.World;

import com.DonLoughry.AllOfTheEverything.entity.*;

public class SwordStatueBlock extends BlockContainer
{
	
	public TileEntity tEntity;
	public String tName;
	public String bName;
	public int BlockID;
	public int facingAngle;
	
	public SwordStatueBlock(TileEntity tileEntity, String blockName, String texName)
	{
		super(Material.rock);
		this.setCreativeTab(CreativeTabs.tabDecorations);
		this.tEntity = tileEntity;
		this.tName = texName;
		this.setBlockName(blockName);
	}

	public TileEntity createNewTileEntity(World arg0, int arg1)
	{
		return new TileEntitySwordStatue(); // please work
	}
	
	public int getRenderType()
	{
		return -1;
	}
	
	public boolean isOpaqueCube()
	{
		return false;
	}
	
	public boolean renderAsNormalBlock()
	{
		return false;
	}
	
	public void setBounds(float minx, float miny, float minz, float maxx, float maxy, float maxz)
	{
		this.setBlockBounds(minx, miny, minz, maxx, maxy, maxz);
		// an example was (1F/16F * 3F, 0F, 1F/16F * 3F, 1F-1F/16F*3F, 1F-1F/16F*3F, 1F-1F/16F*3F)
		// note: 1F is the size of one block. 1F / 16F is one pixel in the block (imagine a block has
		// a volume of 256 smaller blocks. So something like 1F/16F * 3F is 3/16ths, or a distance
		// of 3 pixels. This call basically says:
		// (3 pixels in the x direction, no y movement, 3 pixels in the y direction, 
		// 3 pixels less in the x direction, 3 pixels less in the y direction, 3 pixels less in the z direction)
		// By moving the mins in a positive direction and the max's in a negative direction, you shrink the box.
	}
	
	public void onBlockAdded(World world, int x, int y, int z)
	{
		super.onBlockAdded(world, x, y, z);
		this.setDefaultDirection(world, x, y, z);
	}
	
	private void setDefaultDirection(World world, int x, int y, int z)
	{
		// important to note that int names are arbitrary and have no real meaning.
		Block l = world.getBlock(x, y, z - 1); // this is a guess, since there is no getBlockId method in forge 1.7.2
		Block il = world.getBlock(x, y, z + 1); 
		Block jl = world.getBlock(x - 1, y, z);
		Block kl = world.getBlock(x + 1, y, z - 1);
		
		if(!world.isRemote)
		{
			byte b0 = 3;
			
			if(l.isNormalCube() && !il.isNormalCube())
			{
				b0 = 3;
			}
			if(il.isNormalCube() && !l.isNormalCube())
			{
				b0 = 2;
			}
			if(kl.isNormalCube() && !jl.isNormalCube())
			{
				b0 = 5;
			}
			if(jl.isNormalCube() && !kl.isNormalCube())
			{
				b0 = 4;
			}
			
			world.setBlockMetadataWithNotify(x, y, z, b0, 2);
		}
		
	}
	
	@Override
	public void onBlockPlacedBy(World world, int x, int y, int z, EntityLivingBase entityLivingBase, ItemStack itemStack)
	{
		//int l = MathHelper.floor_double((double)(entityLivingBase.rotationYaw * 4.0F / 360.0F) + 0.5D) & 3;
		TileEntitySwordStatue tile = (TileEntitySwordStatue) world.getTileEntity(x, y, z);
		//tile.direction = MathHelper.floor_double((double)(entityLivingBase.rotationYaw * 4.0F / 360.0F) + 0.5D) & 3;
		int dir = MathHelper.floor_double((double)((entityLivingBase.rotationYaw * 4F) / 360F) + 0.5D) & 3;
		//world.setBlockMetadataWithNotify(x, y, z, dir, 0);
		
		if(dir == 0)
		{
			tile.direction = 0;
			world.setBlockMetadataWithNotify(x, y, z, 2, 2);
		}
		if(dir == 1)
		{
			tile.direction = 90;
			world.setBlockMetadataWithNotify(x, y, z, 5, 2);
		}
		if(dir == 2)
		{
			tile.direction = 180;
			world.setBlockMetadataWithNotify(x, y, z, 3, 2);
		}
		if(dir == 3)
		{
			tile.direction = 270;
			world.setBlockMetadataWithNotify(x, y, z, 4, 2);
		}
		if(itemStack.hasDisplayName())
		{
			world.getTileEntity(x, y, z);
		}
		
	}
	
	@Override
	public void breakBlock(World world, int x, int y, int z, Block arg4, int arg5)
	{
		world.removeTileEntity(x, y, z);
	}
	
	@SideOnly(Side.CLIENT)
	@Override
	public void registerBlockIcons(IIconRegister icon)
	{
		System.out.println(this.tName + " was actually loaded HEYLOOKATMEIMAFUNCTIONTHATACTUALLYRAN!!!!!!!");
		this.blockIcon = icon.registerIcon(this.tName);
	}
	
	

}
