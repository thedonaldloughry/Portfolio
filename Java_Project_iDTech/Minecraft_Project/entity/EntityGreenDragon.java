package com.DonLoughry.AllOfTheEverything.entity;

import net.minecraft.entity.boss.EntityDragon;
import net.minecraft.entity.boss.EntityDragonPart;
import net.minecraft.entity.boss.IBossDisplayData;
import net.minecraft.entity.item.EntityXPOrb;
import net.minecraft.entity.player.EntityPlayer;
import net.minecraft.util.DamageSource;
import net.minecraft.util.MathHelper;
import net.minecraft.util.ResourceLocation;
import net.minecraft.world.EnumSkyBlock;
import net.minecraft.world.World;
import net.minecraft.entity.monster.IMob;

public class EntityGreenDragon extends EntityDragon implements IMob, IBossDisplayData
{
    private static float damageModifier = 25F;
    private static final ResourceLocation mobTextures = new ResourceLocation("donsmod:textures/entity/Test.png");
    public boolean isDead = false;

    public EntityGreenDragon(World par1World)
    {
        super(par1World);
        this.setHealth(this.getMaxHealth());
        //this.texture = "/mob/enderdragon/ender.png";
        //this.setSize(16.0F, 8.0F); // may be useful...
    }

    @Override
    protected void entityInit()
    {
        super.entityInit();
    }
    
    @Override
    protected float getSoundVolume()
    {
    	/*
    	 * Every time that the dragon makes a sound, it will be forced to search for a new target. BE WARNED: Although this does make
    	 * it so that the dragon can "lose" you at long distances, at short ranges it will make the dragon hunt you down with increased
    	 * vigor. This is because of the frequency at which the dragon flaps its wings! The greater the distance between you and the
    	 * dragon, the more wing flaps the dragon has to make to get to you. This gives it a much greater opportunity to get lost, and
    	 * after a certain distance, the dragon is too far away for the game to continue to render it. However, over a short distance,
    	 * the dragon has a 1/2 chance per wing flap to choose you as its target. This gives it a sort of aggressive "hovering" 
    	 * behavior. So, long story short, you DO have a chance to escape the dragon, if you get lucky. However, if you allow it to close
    	 * in on you... prepare to finish the fight that you started.
    	 */
    	this.forceNewTarget = true;
    	return 3.0F;
    }
    
    @Override
    public boolean attackEntityFromPart(EntityDragonPart par1EntityDragonPart, DamageSource par2DamageSource, float par3)
    {
        if (par1EntityDragonPart != this.dragonPartHead)
        {
            par3 = par3 / 4 + 1;
        }
        else
        {
        	System.out.println("BOOM, HEADSHOT!!!");
        }

        float f = this.rotationYaw * (float)Math.PI / 180.0F;
        float f1 = MathHelper.sin(f);
        float f2 = MathHelper.cos(f);
        this.targetX = this.posX + (double)(f1 * 5.0F) + (double)((this.rand.nextFloat() - 0.5F) * 2.0F);
        this.targetY = this.posY + (double)(this.rand.nextFloat() * 3.0F) + 1.0D;
        this.targetZ = this.posZ - (double)(f2 * 5.0F) + (double)((this.rand.nextFloat() - 0.5F) * 2.0F);
        //this.target = null;

        if (par2DamageSource.getEntity() instanceof EntityPlayer || par2DamageSource.isExplosion())
        {
        	this.setHealth(this.getHealth() - EntityGreenDragon.damageModifier);
        	System.out.println("Attempted to apply modified damage!");
            this.func_82195_e(par2DamageSource, par3);
        }

        return true;
    }

    /**
     * Called when the entity is attacked.
     */
    public boolean attackEntityFrom(DamageSource par1DamageSource, float par2)
    {
    	System.out.println("Dragon was hit by something!!!(attackEntityFrom)");
        return false;
    }

    /**
     * handles entity death timer, experience orb and particle creation
     */
    @Override
    protected void onDeathUpdate()
    {
        ++this.deathTicks;

        if (this.deathTicks >= 180 && this.deathTicks <= 200)
        {
            float f = (this.rand.nextFloat() - 0.5F) * 8.0F;
            float f1 = (this.rand.nextFloat() - 0.5F) * 4.0F;
            float f2 = (this.rand.nextFloat() - 0.5F) * 8.0F;
            this.worldObj.spawnParticle("hugeexplosion", this.posX + (double)f, this.posY + 2.0D + (double)f1, this.posZ + (double)f2, 0.0D, 0.0D, 0.0D);
        }

        int i;
        int j;

        if (!this.worldObj.isRemote)
        {
            if (this.deathTicks > 150 && this.deathTicks % 5 == 0)
            {
                i = 1000;

                while (i > 0)
                {
                    j = EntityXPOrb.getXPSplit(i);
                    i -= j;
                    this.worldObj.spawnEntityInWorld(new EntityXPOrb(this.worldObj, this.posX, this.posY, this.posZ, j));
                }
            }

            /*if (this.deathTicks == 1)
            {
                this.worldObj.func_82739_e(1018, (int)this.posX, (int)this.posY, (int)this.posZ, 0);
            }*/
        }

        this.moveEntity(0.0D, 0.10000000149011612D, 0.0D);
        this.renderYawOffset = this.rotationYaw += 20.0F;

        if (this.deathTicks >= 100 && !this.worldObj.isRemote)
        {
            i = 100;

            while (i > 0)
            {
                j = EntityXPOrb.getXPSplit(i);
                i -= j;
                this.worldObj.spawnEntityInWorld(new EntityXPOrb(this.worldObj, this.posX, this.posY, this.posZ, j));
            }

           this.setDead();
        }
    }
    
    //////////////////////// SPAWN CODE ////////////////////////
    
    /**
     * Checks to make sure the light is not too bright where the mob is spawning
     */
    protected boolean isValidLightLevel()
    {
        int i = MathHelper.floor_double(this.posX);
        int j = MathHelper.floor_double(this.boundingBox.minY);
        int k = MathHelper.floor_double(this.posZ);

        if (this.worldObj.getSavedLightValue(EnumSkyBlock.Sky, i, j, k) > this.rand.nextInt(32))
        {
            return false;
        }
        else
        {
            int l = this.worldObj.getBlockLightValue(i, j, k);

            if (this.worldObj.isThundering())
            {
                int i1 = this.worldObj.skylightSubtracted;
                this.worldObj.skylightSubtracted = 10;
                l = this.worldObj.getBlockLightValue(i, j, k);
                this.worldObj.skylightSubtracted = i1;
            }

            return l <= this.rand.nextInt(8);
        }
    }
    
    /**
     * Checks if the entity's current position is a valid location to spawn this entity.
     */
    public boolean getCanSpawnHere()
    {
        return this.worldObj.difficultySetting.getDifficultyId() > 0 && this.isValidLightLevel();
    }

	public ResourceLocation getTexture() {
		return mobTextures;
	}

}
