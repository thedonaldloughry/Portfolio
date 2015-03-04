//jh ssu etec3701 au 2007

//mrm: remove a file from a virtual hard disk (FAT-16 format)

//syntax:
//mrm hard_disk_image filename


#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <iostream>
#include <vector>
#include <time.h>
#include <assert.h>

using namespace std;

#pragma pack(push,1)
struct PTE{
	unsigned char bootable;
	unsigned char starthead;

	//to get cs: bytes are:
	// CCssssss CCCCCCCC
	unsigned char startsect;
	unsigned char startcyl;

	unsigned char type;

	unsigned char endhead;
	unsigned char endsect,endcyl;
	

	unsigned start;
	unsigned size;
} __attribute__((packed));

struct VBR
{
        unsigned char           jmp[3];
        char                    oem[8];
        unsigned short          bytes_per_sector;
        unsigned char           sectors_per_cluster;
        unsigned short          vbr_sectors;
        unsigned char           num_fats;
        unsigned short          num_root_dir_entries;
        unsigned short          num_sectors_small;
        unsigned char           id;
        unsigned short          sectors_per_fat;
        unsigned short          sectors_per_track;
        unsigned short          num_heads;
        unsigned int            first_sector;
        unsigned int            num_sectors_big;
        unsigned char           drive_number;
        unsigned char           reserved;
        unsigned char           sig1;
        unsigned int            serial_number;
        char                    label[11];
        char                    fstype[8];
} __attribute__((packed));

struct DirEntry{
	char name[8];
	char ext[3];
	unsigned char attrib;
	char reserved[10];
	unsigned short time;
	unsigned short date;
	unsigned short start;
	unsigned int size;
} __attribute__((packed));

#pragma pack(pop)

int main(int argc, char* argv[])
{
	//argv[1] = disk file
	//argv[2] = filename on disk
	assert(argc == 3);
	
	char* diskfile = argv[1];
	char* outfile = argv[2];
	
	FILE* fp = fopen(diskfile,"r+b");
	if(!fp){
		cout << "Cannot open hard drive!\n";
		return 1;
	}
	
	//get partition table
	char mbr[512];
	fread(mbr,1,512,fp);
	PTE* ptable = (PTE*) (mbr + 446);
	
	//get volume boot record
	fseek( fp, ptable[0].start * 512 , SEEK_SET);	
	VBR vbr;
	fread(&vbr,1,sizeof(vbr),fp);
	
	
	//read in FAT
	unsigned short* fat = new unsigned short[65536];
	assert(fat);
	memset(fat,0xff,65536*2);
	fseek( fp, (ptable[0].start + vbr.vbr_sectors )* 512, SEEK_SET);
	fread(fat,1,vbr.sectors_per_fat*512,fp);
	
	
	//split destination filename into base + ext
	char base[8]; 
	char ext[3];
	
	char* p = strstr(outfile,".");		//pointer to dot or end of string
	if( !p ){
		p = outfile+strlen(outfile);
	}

	char* q;			//current character
	int i = 0;			//counter for destination location
	for(q=outfile; q!=p; ++q){
		if( i == 8 ){
			cout << "Destination filename too long\n";
			return 1;
		}
		if( !isalnum(*q) ){
			cout << "Illegal character in destination filename\n";
			return 1;
		}
		base[i] = toupper(*q);
		++i;
	}
	while( i < 8 )				//pad with spaces
		base[i++] = ' ';
	i=0;
	if( *p ){
		for(q=p+1;*q!=0;++q){
			if( i == 3 ){
				cout << "Destination filename too long\n";
				return 1;
			}
			if( !isalnum(*q) ){
				cout << "Illegal character in destination filename\n";
				return 1;
			}
			ext[i] = toupper(*q);
			++i;
		}
	}
	while(i<3)				//pad with spaces
		ext[i++] = ' ';
	
		
	//scan root directory looking for a file that matches
	//the one we're passing in. 
	fseek( fp, (ptable[0].start + vbr.vbr_sectors + vbr.num_fats * vbr.sectors_per_fat )* 512, SEEK_SET);
	DirEntry de;
	int direntryloc=0;
	for(int i=0;i<vbr.num_root_dir_entries;++i){
		fread(&de,32,1,fp);
		if( strncmp(de.name,base,8) == 0 && strncmp(de.ext,ext,3) == 0){
			//found it
			direntryloc = ftell(fp)-32;
			break;
		}
	}
		
	if( direntryloc == 0 ){
		cout << "File not found!\n";
		return 1;
	}

	//start deleting!
	int cn = de.start;
	while(cn != 0xffff && cn != 0){
		int next = fat[cn];
		fat[cn] = 0;
		cn = next;
	}
	
	//mark as deleted
	fseek(fp,direntryloc,SEEK_SET);
	fputc(0xe5,fp);
	

	//write fats
	fseek( fp, (ptable[0].start + vbr.vbr_sectors )* 512, SEEK_SET);
	fwrite(fat,1,vbr.sectors_per_fat*512,fp);
	
	fseek( fp, (ptable[0].start + vbr.vbr_sectors + vbr.sectors_per_fat )* 512, SEEK_SET);
	fwrite(fat,1,vbr.sectors_per_fat*512,fp);
	
	
	fclose(fp);
	
	return 0;
}
