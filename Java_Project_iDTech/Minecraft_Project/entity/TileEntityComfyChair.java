package com.DonLoughry.AllOfTheEverything.entity;

import net.minecraft.tileentity.TileEntity;
import net.minecraft.nbt.NBTTagCompound;
import net.minecraft.network.NetworkManager;
import net.minecraft.network.Packet;
import net.minecraft.network.play.server.S35PacketUpdateTileEntity;

public class TileEntityComfyChair extends TileEntity{
	
	public int direction;
	
	@Override
    public void writeToNBT(NBTTagCompound par1)
    {
       super.writeToNBT(par1);
       par1.setInteger("direction", (int)direction);
    }

	@Override
	public void readFromNBT(NBTTagCompound par1)
	{
	    super.readFromNBT(par1);
	    direction = par1.getInteger("direction");
	}
	
	@Override
	public Packet getDescriptionPacket()
	{
		NBTTagCompound tileTag = new NBTTagCompound();
		this.writeToNBT(tileTag);
		return new S35PacketUpdateTileEntity(this.xCoord, this.yCoord, this.zCoord, 0, tileTag);
	}
	
	@Override
	public void onDataPacket(NetworkManager net, S35PacketUpdateTileEntity pkt)
	{
		this.readFromNBT(pkt.func_148857_g());
	}

}
