package com.DonLoughry.AllOfTheEverything.items;

import cpw.mods.fml.common.registry.GameRegistry;
import net.minecraft.item.Item;
import net.minecraft.item.ItemArmor.ArmorMaterial;
import net.minecraftforge.common.util.EnumHelper;

public class ItemRegistry {
	
	public static Item Poo;
	public static Item blackIronHelm;
	public static Item blackIronPants;
	public static Item blackIronBoots;
	public static Item blackIronChestPlate; 
	public static Item aetherialPlateHelm;
	public static Item aetherialPlatePants;
	public static Item aetherialPlateBoots;
	public static Item aetherialPlateChestPlate;
	
	public static void registerItems()
	{
		GameRegistry.registerItem(Poo, "Poo");
		GameRegistry.registerItem(blackIronHelm, "Black Iron Helm");
		GameRegistry.registerItem(blackIronPants, "Black Iron Leggings");
		GameRegistry.registerItem(blackIronBoots, "Black Iron Boots");
		GameRegistry.registerItem(blackIronChestPlate, "Black Iron Chestplate");
		GameRegistry.registerItem(aetherialPlateHelm, "Dragon Plate Helm");
		GameRegistry.registerItem(aetherialPlatePants, "Dragon Plate Pants");
		GameRegistry.registerItem(aetherialPlateBoots, "Dragon Plate Boots");
		GameRegistry.registerItem(aetherialPlateChestPlate, "Dragon Plate Chestplate");
	}
	
	public static void createItems()
	{
		// ARMOR TYPES //
		ArmorMaterial armorBlackIron = EnumHelper.addArmorMaterial("BlackIron", 29, new int[]{5,5,5,5}, 11);
		ArmorMaterial armorAetherialPlate = EnumHelper.addArmorMaterial("DragonPlate", 35, new int[]{3,7,9,8}, 16);
		// END ARMOR TYPES //
		
		// ITEM CREATION //
    	Poo = new Poo(4999);
    	
    	blackIronHelm = new BlackIronArmor(armorBlackIron, 0, "Black Iron Helm");
    	blackIronChestPlate = new BlackIronArmor(armorBlackIron, 1, "Black Iron Chestplate");
    	blackIronPants = new BlackIronArmor(armorBlackIron, 2, "Black Iron Pants");
    	blackIronBoots = new BlackIronArmor(armorBlackIron, 3, "Black Iron Boots");
    	
    	aetherialPlateHelm = new AetherialPlateArmor(armorAetherialPlate, 0, "aether.iron_helmet");   	
    	aetherialPlatePants = new AetherialPlateArmor(armorAetherialPlate, 2, "aether.iron_leggings");    	
    	aetherialPlateBoots = new AetherialPlateArmor(armorAetherialPlate, 3, "aether.iron_boots");   	
    	aetherialPlateChestPlate = new AetherialPlateArmor(armorAetherialPlate, 1, "aether.iron_chestplate");
    	// END ITEM CREATION //
	}

}
