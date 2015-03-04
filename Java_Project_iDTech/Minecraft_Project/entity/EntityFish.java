package com.DonLoughry.AllOfTheEverything.entity;

import com.DonLoughry.AllOfTheEverything.blocks.BlockRegistry;
import com.DonLoughry.AllOfTheEverything.items.ItemRegistry;

import net.minecraft.block.Block;
import net.minecraft.entity.SharedMonsterAttributes;
import net.minecraft.entity.ai.EntityAILookIdle;
import net.minecraft.entity.ai.EntityAIPanic;
import net.minecraft.entity.ai.EntityAIWander;
import net.minecraft.entity.passive.EntityWaterMob;
import net.minecraft.world.World;

public class EntityFish extends EntityWaterMob {
	
	public double moveSpeed;
	public float scaleFactor = 1.0F;
	public float moveTimer = 0F;
	public double moveY = 0D;
	
	public EntityFish(World par1World)
	{
		super(par1World);
		this.setSize(1.0F, 1.0F);// trying to make a small, simple creature fit inside a single block
		this.moveSpeed = this.getEntityAttribute(SharedMonsterAttributes.movementSpeed).getAttributeValue();
		this.getNavigator().setAvoidsWater(false);
		this.getNavigator().setAvoidSun(true); // maybe this will make them want to stay in the water... where the sun does not affect them?
		
		// Some basic passive AI, mimics the behavior of a dog. This is the most stable AI
		this.tasks.addTask(0, new EntityAIWander(this, this.moveSpeed));
		this.tasks.addTask(1, new EntityAIWander(this, this.moveSpeed));
		this.tasks.addTask(2, new EntityAIWander(this, this.moveSpeed));
		this.tasks.addTask(3, new EntityAIWander(this, this.moveSpeed));
		this.tasks.addTask(4, new EntityAIWander(this, this.moveSpeed));
		this.tasks.addTask(5, new EntityAIPanic(this, this.moveSpeed + 0.2D));
		this.tasks.addTask(6, new EntityAIPanic(this, this.moveSpeed + 0.2D));
		this.tasks.addTask(7, new EntityAIPanic(this, this.moveSpeed + 0.2D));
		this.tasks.addTask(8, new EntityAILookIdle(this));
	}
	
	public float getScaleFactor()
	{
		return this.scaleFactor;
	}

	public boolean isAIEnabled()
	{
		return true;
	}
	
	public int getTotalArmorValue()
	{
		return 1;
	}
	// NOTE: record Blizzard sounds
	protected String getLivingSound()
	{
		return "mob.Blizzard.say";
	}
	
	protected String getHurtSound()
	{
		return "mob.Blizzard.hurt";
	}
	
	protected String getDeathSound()
	{
		return "mob.Blizzard.death";
	}

	protected String getSwimSound()
	{
		return "donsmod:N/A";
	}
	
	protected String getSplashSound()
	{
		return "donsmod:N/A";
	}
	
	protected int getDropItemId()
	{
		return Block.getIdFromBlock(BlockRegistry.blackTBlock);
	}
	
	protected void dropRareDrop(int par1)
	{
		switch(this.rand.nextInt(4))
		{
		case 0:
			this.dropItem(ItemRegistry.blackIronChestPlate, 1);
		case 1:
			this.dropItem(ItemRegistry.blackIronHelm, 1);
		case 2:
			this.dropItem(ItemRegistry.blackIronPants, 1);
		case 3:
			this.dropItem(ItemRegistry.blackIronBoots, 1);
		}
	}
	
	protected void dropFewItems(boolean par1, int par2)
	{
		if(this.rand.nextInt(4) == 0)
		{
			this.dropItem(ItemRegistry.Poo, 1);
		}
	}
	
	protected void applyEntityAttributes()
	{
		super.applyEntityAttributes();
		this.getEntityAttribute(SharedMonsterAttributes.maxHealth).setBaseValue(10.0D);
		this.getEntityAttribute(SharedMonsterAttributes.movementSpeed).setBaseValue(0.7D);
		//this.getEntityAttribute(SharedMonsterAttributes.followRange).setBaseValue(20.0D);
		//this.getEntityAttribute(SharedMonsterAttributes.knockbackResistance).setBaseValue(0.2D);
		//this.getEntityAttribute(SharedMonsterAttributes.attackDamage).setBaseValue(1.0D);
		// Could this conflict with the AI commands in the constructor?
		// Answer: yes it could, which is why instead of hard-coding these values, use
		// this.getEntityAttribute(SharedMonsterAttributes.whatever).getAttributeValue() for the double value that you need.
		
	}
	
	@Override
	public void onLivingUpdate()
	{
		super.onLivingUpdate();
		if(!this.isInWater())
		{
			this.moveEntity(0D, -2D, 0D); // meant to push the fish WAY down if it touches the water's surface.
		}
		else
		{
			this.moveTimer += 0.001F;
			this.moveEntity(0D, 0.1D, 0D); // so the thing doesn't rub against the ground and make step sounds...
			this.moveEntity(0D, this.moveY, 0D);
			
			if(this.moveTimer <= 0.5F)
			{
				this.moveY -= 0.0002D;
			}
			else if(this.moveTimer > 0.5F && this.moveTimer <= 1.0F)
			{
				this.moveY += 0.0005D;
			}
			else
			{
				this.moveTimer = 0F;
				this.moveY = 0D;
			}
		}
	}

}