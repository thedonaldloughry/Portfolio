package com.DonLoughry.AllOfTheEverything.items;

import net.minecraft.client.model.ModelBiped;
import net.minecraft.client.renderer.texture.IIconRegister;
import net.minecraft.entity.Entity;
import net.minecraft.entity.EntityLivingBase;
import net.minecraft.entity.player.EntityPlayer;
import net.minecraft.item.ItemArmor;
import net.minecraft.item.ItemStack;
import net.minecraft.world.World;
import com.DonLoughry.AllOfTheEverything.AllOfTheEverything;
import cpw.mods.fml.relauncher.Side;
import cpw.mods.fml.relauncher.SideOnly;

public class AetherialPlateArmor extends ItemArmor
{	
	public AetherialPlateArmor(ArmorMaterial material, int armorType, String name)
	{
		super(material, 0, armorType);
		this.setUnlocalizedName(name);
		//this.setTextureName(References.MODID + ":" + this.getUnlocalizedName().substring(5));
	}
	
	@Override
	public void onArmorTick(World world, EntityPlayer player, ItemStack itemstack)
	{
		super.onArmorTick(world, player, itemstack);
		if(player.inventory.armorInventory[0] == null || player.inventory.armorInventory[1] == null
				|| player.inventory.armorInventory[2] == null || player.inventory.armorInventory[3] == null)
		{
			/*
			 * Player is missing armor in one or more spots.
			 */
			player.capabilities.setPlayerWalkSpeed(0.1F);
			return;
		}
		else if(player.inventory.armorInventory[0].getItem() instanceof AetherialPlateArmor && 
				player.inventory.armorInventory[1].getItem() instanceof AetherialPlateArmor &&
				player.inventory.armorInventory[2].getItem() instanceof AetherialPlateArmor &&
				player.inventory.armorInventory[3].getItem() instanceof AetherialPlateArmor)
		{
			/*
			 * Player has all armor spots filled with AetherialPlateArmor objects.
			 */
			player.capabilities.setPlayerWalkSpeed(0.5F);
			return;
		}
		else
		{
			/*
			 * Player has all armor spots filled, but NOT with AetherialPlateArmor objects.
			 */
			player.capabilities.setPlayerWalkSpeed(0.1F);
			return;
		}
	}
	
	@Override 
	public String getArmorTexture(ItemStack stack, Entity entity, int slot, String type) 
	{ 
		switch(slot)
		{ 
			case 2: return "alloftheeverything:models/armor/ModelAetherArmor_Layer2.png"; //2 is legs... 
			default: return "alloftheeverything:models/armor/ModelAetherArmor_Layer1.png";
		}	
	}
	
	@Override 
	@SideOnly(Side.CLIENT) 
	public ModelBiped getArmorModel(EntityLivingBase entityLiving, ItemStack itemStack, int armorSlot) 
	{ 
		ModelBiped armorModel = null;
		if(itemStack != null)
		{ 
			if(itemStack.getItem() instanceof AetherialPlateArmor) // note: proper usage of instanceof operator!
			{
				int type = ((ItemArmor)itemStack.getItem()).armorType; 
				
				if(type == 1 || type == 3)
				{ 
					armorModel = AllOfTheEverything.proxy.getArmorModel(0, "aether"); 
				}
				else
				{ 
					armorModel = AllOfTheEverything.proxy.getArmorModel(1, "aether"); 
				}
			} 
		}
		if(armorModel != null)
		{ 
			armorModel.bipedHead.showModel = armorSlot == 0; 
			armorModel.bipedHeadwear.showModel = armorSlot == 0; 
			armorModel.bipedBody.showModel = armorSlot == 1 || armorSlot == 2; 
			armorModel.bipedRightArm.showModel = armorSlot == 1; 
			armorModel.bipedLeftArm.showModel = armorSlot == 1; 
			armorModel.bipedRightLeg.showModel = armorSlot == 2 || armorSlot == 3; 
			armorModel.bipedLeftLeg.showModel = armorSlot == 2 || armorSlot == 3; 
			armorModel.isSneak = entityLiving.isSneaking(); 
			armorModel.isRiding = entityLiving.isRiding(); 
			armorModel.isChild = entityLiving.isChild(); 
			armorModel.heldItemRight = entityLiving.getHeldItem() != null ? 1 :0; 
			if(entityLiving instanceof EntityPlayer)
			{ 
				armorModel.aimedBow =((EntityPlayer)entityLiving).getItemInUseDuration() > 2; 
			} 
			return armorModel; 
		}
		return null;
	}
	
	/*@Override
	public String getArmorTexture(ItemStack stack, Entity entity, int slot, String type)
	{
		// here is where we check our item stack to see what texture we should use for what piece...
		if(stack.getItem() == AllOfTheEverything.itemReg.blackIronHelm || 
				stack.getItem() == AllOfTheEverything.itemReg.blackIronChestPlate || 
				stack.getItem() == AllOfTheEverything.itemReg.blackIronBoots)
		{
			return References.MODID + ":models/armor/blackIronLayer1.png";
		}
		else if(stack.getItem() == AllOfTheEverything.itemReg.blackIronPants)
		{
			return References.MODID + ":models/armor/blackIronLayer2.png"; // this had better work...
		}
		else
		{
			System.out.println("Could not find a texture for armor piece " + this.getUnlocalizedName());
		}
		return null;
	}*/
	
	@Override 
	@SideOnly(Side.CLIENT) 
	public void registerIcons(IIconRegister par1IconRegister) 
	{ 
		String itemName = getUnlocalizedName().substring(getUnlocalizedName().lastIndexOf(".") + 1);
		this.itemIcon = par1IconRegister.registerIcon(itemName); 
	}
}
