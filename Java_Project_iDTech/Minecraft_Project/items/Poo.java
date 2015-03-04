package com.DonLoughry.AllOfTheEverything.items;

import net.minecraft.creativetab.CreativeTabs;
import net.minecraft.entity.player.EntityPlayer;
import net.minecraft.item.Item;
import net.minecraft.item.ItemStack;
import net.minecraft.world.World;

import com.DonLoughry.AllOfTheEverything.entity.EntityPoo;

public class Poo extends Item
{
	public Poo(int i)
	{
		super();
		this.setUnlocalizedName("Poo"); // was Obstick
		this.setTextureName("alloftheeverything:Poo"); // was tutorialmod:OStick, then DonsMod:Poo
		this.setCreativeTab(CreativeTabs.tabMisc);
	}
	/**
	* Called whenever this item is equipped and the right mouse button is pressed.
	* Args: itemStack, world, entityPlayer
	*/
	public ItemStack onItemRightClick(ItemStack stack, World world, EntityPlayer player) {
	if (!player.capabilities.isCreativeMode) {
	--stack.stackSize;
	}

	world.playSoundAtEntity(player, "random.bow", 0.5F, 0.4F / (itemRand.nextFloat() * 0.4F + 0.8F));

	// IMPORTANT! Only spawn new entities on the server. If the world is not remote,
	// that means you are on the server:
	if (!world.isRemote) {
	world.spawnEntityInWorld(new EntityPoo(world, player));
	}

	return stack;
	}
}
