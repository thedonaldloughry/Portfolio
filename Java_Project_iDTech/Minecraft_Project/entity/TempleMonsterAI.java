package com.DonLoughry.AllOfTheEverything.entity;

import com.DonLoughry.AllOfTheEverything.blocks.BlockRegistry;
import com.DonLoughry.AllOfTheEverything.items.ItemRegistry;

import net.minecraft.block.Block;
import net.minecraft.entity.SharedMonsterAttributes;
import net.minecraft.entity.monster.EntityMob;
import net.minecraft.world.World;
import net.minecraft.entity.ai.*;
import net.minecraft.init.Items;

public class TempleMonsterAI extends EntityMob{
	

	private double moveSpeed;

	public TempleMonsterAI(World par1World) {
		super(par1World);
		this.setSize(5.0F, 10.0F);
		this.moveSpeed = 0.3D;
		this.getNavigator().setAvoidsWater(true);
		this.getNavigator().setCanSwim(false);
		
		// Some basic passive AI, mimics the behavior of a dog. This is the most stable AI
		this.tasks.addTask(0, new EntityAIWander(this, this.moveSpeed));
		this.tasks.addTask(1, new EntityAIPanic(this, this.moveSpeed + 0.1D));
		this.tasks.addTask(2, new EntityAILookIdle(this));
		//this.tasks.addTask(3, new EntityAISwimming(this));
		this.tasks.addTask(3, new EntityAITempt(this, this.moveSpeed + 0.1D, Items.bone, false));	
		
		// And below is some basic super aggressive AI, courtesy of Wuppy29. Look him up, he has good tutorials!!!
		/*this.tasks.addTask(0, new EntityAISwimming(this));
		this.tasks.addTask(1, new EntityAILeapAtTarget(this, 0.7F));
		this.tasks.addTask(2, new EntityAIAttackOnCollide(this, EntityPlayer.class, this.moveSpeed, false));
		this.tasks.addTask(3, new EntityAIWatchClosest(this, EntityPlayer.class, 6.0F));
		this.tasks.addTask(4, new EntityAIWander(this, this.moveSpeed));
		this.targetTasks.addTask(1, new EntityAIHurtByTarget(this, false));
		this.targetTasks.addTask(2, new EntityAINearestAttackableTarget(this, EntityPlayer.class, 0, true));*/
		
		// This AI didn't work out too well with a large creature...
		/*this.tasks.addTask(0, new EntityAITempt(this, 0.5D, Items.bone, false));
		this.tasks.addTask(1, new EntityAIAttackOnCollide(this, EntityPlayer.class, moveSpeed, false));
		this.tasks.addTask(2, new EntityAIWatchClosest(this, EntityPlayer.class, 6.0F));
		this.targetTasks.addTask(0, new EntityAINearestAttackableTarget(this, EntityPlayer.class, 0, true));*/
	}
	
	public boolean isAIEnabled()
	{
		return true;
	}
	
	public int getTotalArmorValue()
	{
		return 6;
	}
	
	protected String getLivingSound()
	{
		return "mob.zombie.say"; // insert giant walking sound here...
	}
	
	protected String getHurtSound()
	{
		return "mob.skeleton.hurt";
	}
	
	protected String getDeathSound()
	{
		return "mob.ghast.death";
	}
	
	protected void playStepSound(int par1, int par2, int par3, int par4)
	{
		this.worldObj.playSoundAtEntity(this, "mob.zombie.wood", 0.15F, 1.0F);
		// (entity, sound file, volume, frequency [1.0 being normal])
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
		this.getEntityAttribute(SharedMonsterAttributes.maxHealth).setBaseValue(80.0D);
		this.getEntityAttribute(SharedMonsterAttributes.movementSpeed).setBaseValue(0.5D);
		// Could this conflict with the AI commands in the constructor???
		
	}

}
