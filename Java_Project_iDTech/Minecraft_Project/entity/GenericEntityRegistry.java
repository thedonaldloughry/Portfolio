// Credit to the tutorial at the following web address: http://www.youtube.com/watch?v=vzbTSaxf-5k&list=PLcug66V6cB_q_d6Dt5-k2TJevHOazm_VE

package com.DonLoughry.AllOfTheEverything.entity;

import net.minecraft.entity.EntityList;
import net.minecraft.entity.EnumCreatureType;
import net.minecraft.world.biome.BiomeGenBase;

import com.DonLoughry.AllOfTheEverything.AllOfTheEverything;
import com.DonLoughry.AllOfTheEverything.lib.*;

import cpw.mods.fml.common.Mod.Instance;
import cpw.mods.fml.common.registry.EntityRegistry;

public class GenericEntityRegistry {
	
	@Instance(References.MODID)
	public static AllOfTheEverything modInstance;
	
	public static void mainRegistry()
	{
		registerEntity();
	}
	
	public static void registerEntity()
	{
		//createEntity(TempleMonsterAI.class, "Temple Monster", 0xEC4545, 0x001EFF);// removing the Temple Monster permanently
		createEntity(EntityGoober.class, "Goober", 0x82FF82, 0x0000B2, BiomeGenBase.forest, BiomeGenBase.desert,
				BiomeGenBase.beach, 100, 4, 8);
		createEntity(EntityBlizzard.class, "Blizzard", 0xFFFFCCC, 0x0099CC, BiomeGenBase.icePlains, BiomeGenBase.iceMountains,
				BiomeGenBase.coldTaiga, 100, 3, 9);
		createEntity(EntityMimicTree.class, "Mimic Tree", 0x007A00, 0x7A2900, BiomeGenBase.forest, BiomeGenBase.savanna, 
				BiomeGenBase.taiga, 100, 1, 4);
		createEntity(EntityGentlemanCapybara.class, "Gentleman Capybara", 0x993300, 0xFFCC00, BiomeGenBase.forest, BiomeGenBase.savanna, 
				BiomeGenBase.savannaPlateau, 100, 2, 5);
		//createEntity(EntityGreenDragon.class, "Earth Dragon", 0x000000, 0xFFFFFF, BiomeGenBase.forest, BiomeGenBase.savanna, 
				//BiomeGenBase.savannaPlateau, 10, 1, 1); // 10% chance to spawn a freaking dragon. I can live with that.
		createEntity(EntitySerpent.class, "Serpent", 0x006600, 0x996600, BiomeGenBase.forest, BiomeGenBase.savanna, 
				BiomeGenBase.savannaPlateau, 100, 1, 2);
		createEntity(EntityFish.class, "Test Fish", 0x006666, 0xA23560, BiomeGenBase.deepOcean, BiomeGenBase.ocean, 
				BiomeGenBase.river, 100, 2, 5);
	}
	
	@SuppressWarnings({ "rawtypes", "unchecked" })
	public static void createEntity(Class entityClass, String entityName, int solidColor, int spotColor, BiomeGenBase spawnPlaceOne,
			BiomeGenBase spawnPlaceTwo, BiomeGenBase spawnPlaceThree, int probability, int minPack, int maxPack)
	{
		int randomId = EntityRegistry.findGlobalUniqueEntityId();
		EntityRegistry.registerGlobalEntityID(entityClass, entityName, randomId);
		EntityRegistry.registerModEntity(entityClass, entityName, randomId, modInstance, 64, 1, true);
		EntityRegistry.addSpawn(entityClass, probability, minPack, maxPack, EnumCreatureType.creature, spawnPlaceOne, 
				spawnPlaceTwo, spawnPlaceThree);
		//			...addSpawn(your entity, spawn probability, min pack size, max pack size, type, biome, biome, biome)
		createEgg(randomId, solidColor, spotColor);
	}

	@SuppressWarnings("unchecked")
	private static void createEgg(int ID, int solidColor, int spotColor) {
		EntityList.entityEggs.put(Integer.valueOf(ID), new EntityList.EntityEggInfo(ID, solidColor, spotColor));
		
	}

}
