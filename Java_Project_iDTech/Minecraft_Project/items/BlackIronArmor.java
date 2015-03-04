package com.DonLoughry.AllOfTheEverything.items;

import net.minecraft.entity.Entity;
import net.minecraft.entity.player.EntityPlayer;
import net.minecraft.item.ItemArmor;
import net.minecraft.item.ItemStack;
import net.minecraft.util.ChatComponentText;
import net.minecraft.world.World;
import com.DonLoughry.AllOfTheEverything.lib.*;

public class BlackIronArmor extends ItemArmor
{	
	public BlackIronArmor(ArmorMaterial material, int armorType, String name)
	{
		super(material, 0, armorType);
		this.setUnlocalizedName(name);
		this.setTextureName(References.MODID + ":" + this.getUnlocalizedName().substring(5));// do we want substring???
	}
	
	@Override
	public void onArmorTick(World world, EntityPlayer player, ItemStack itemstack)
	{
		if(!player.capabilities.isCreativeMode)
		{
			if (itemstack.getItem() == ItemRegistry.blackIronHelm)
			{
				player.setAir(1); // breathe underwater
				if(player.isBurning())
				{
					//EnchantmentHelper.getAquaAffinityModifier(player);
					/*
					 * It may be possible to use some of the default Potion Effects to achieve
					 * additional results, as the Enchantment Helper may not do much for us.
					 * Example:
					 * player.addPotionEffect(new PotionEffect(Potion.type.id, duration, amplifier));
					 */
					player.addChatMessage(new ChatComponentText("OUCH! You're on fire!!!"));
					player.capabilities.disableDamage = true;
					player.extinguish();
					
				}
				else
				{
					player.capabilities.disableDamage = false;
				}
			}
		}
		else
		{
			player.addChatMessage(new ChatComponentText("[ARMOR TICK] In Creative Mode, effects disabled."));
		}
	}
	
	@Override
	public String getArmorTexture(ItemStack stack, Entity entity, int slot, String type)
	{
		// here is where we check our item stack to see what texture we should use for what piece...
		if(stack.getItem() == ItemRegistry.blackIronHelm || 
				stack.getItem() == ItemRegistry.blackIronChestPlate || 
				stack.getItem() == ItemRegistry.blackIronBoots)
		{
			return References.MODID + ":models/armor/blackIronLayer1.png";
		}
		else if(stack.getItem() == ItemRegistry.blackIronPants)
		{
			return References.MODID + ":models/armor/blackIronLayer2.png"; // this had better work...
		}
		else
		{
			System.out.println("Could not find a texture for armor piece " + this.getUnlocalizedName());
		}
		return null;
	}
}
