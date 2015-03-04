// ssu etec3701 fall 2007

#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <stdint.h>
#include <string.h>
#include <iostream>
#include "mbr.h"
#include "vbr.h"

using namespace std;
#pragma pack(push,1)
struct VBR{
        uint8_t           jmp[3];
        char                    oem[8];
        uint16_t          bytes_per_sector;
        uint8_t           sectors_per_cluster;
        uint16_t          vbr_sectors;
        uint8_t           num_fats;
        uint16_t          num_root_dir_entries;
        uint16_t          num_sectors_small;
        uint8_t           id;
        uint16_t          sectors_per_fat;
        uint16_t          sectors_per_track;
        uint16_t          num_heads;
        uint32_t            first_sector;
        uint32_t            num_sectors_big;
        uint8_t           drive_number;
        uint8_t           reserved;
        uint8_t           sig1;
        uint32_t            serial_number;
        char                    label[11];
        char                    fstype[8];
} ;
#pragma pack(pop)
#pragma pack(push,1)
struct PTE{
	uint8_t bootable;		//0x80=yes, 0x00=no
	uint8_t shead;		//start head

	//to get cylinder and sector: bytes are:
	// CCssssss CCCCCCCC   (sector field has two bits of cylinder too)
	uint8_t ssector;		//start sector
	uint8_t scyl;		//start cylinder

	uint8_t type;		//partition type; 0xe = DOS/Windows FAT16

	uint8_t ehead;		//end head
	uint8_t esector,ecyl;	//end sector and cylinder

	unsigned start;			//LBA start sector
	unsigned size;			//num sectors

} __attribute__((packed));
#pragma pack(pop)

//create an empty disk file
int mkdisk(const char* fname, unsigned size_in_mb){
	//arguments:
	//		argv[1] = disk file
	//		argv[2] = size of disk, in MB
	unsigned size = size_in_mb;

	if( size == 0 ){
		printf("bad size\n");
		return 1;
	}

	remove(fname);

	FILE* fp = fopen(fname,"wb");
	if(!fp){
		printf("bad disk file\n");
		return 1;
	}


	fseek(fp,size*1024*1024-1,SEEK_SET);
	fputc(0,fp);
	fclose(fp);

	//printf("---mkdisk: made %d MB disk\n",size);

	return 0;
}

//write the mbr and partition table to a virtual disk
int mkpartition(const char* fname){
	//argv[1] = filename

	FILE* fp = fopen(fname,"r+b");
	if(!fp){
		cerr << "Cannot open hard drive!\n";
		return 1;
	}
	fseek(fp,0,SEEK_END);
	unsigned sz = ftell(fp)/1024/1024;
	fseek(fp,0,SEEK_SET);

	PTE ptable[4];

	memset(ptable,0,sizeof(ptable));

	//Determine cyl/head/sector count
	//cyls must be a ten bit number
	//head is an 8 bit number
	//sector is a six bit number, but these start from one, not zero...

	int numheads;
	int numcyls;
	int numsects;

	//every head = 16MB
	numcyls = 1024;
	numsects = 32;

	//need to round down to nearest multiple of 16MB
	numheads = sz/16;


	if( numheads > 256 || numcyls > 1024 || numsects > 64 ){
		cerr << "Too big: chs=" << numcyls << ' ' << numheads << ' ' << numsects << "!\n";
		return 1;
	}

	//write to partition table entry 1
	ptable[0].bootable=0x80;
	ptable[0].shead = 1;
	ptable[0].ssector = 1;
	ptable[0].scyl = 0;

	ptable[0].type = 0xe;	//hardcode DOS type

	ptable[0].ehead = numheads-1;
	ptable[0].esector = (( (numcyls-1) & 0xff00 )>>2) | (numsects);
	ptable[0].ecyl = ( (numcyls-1) & 0xff) ;


	//always start on a track boundary
	ptable[0].start = numsects*( (rand()&7) + 1);
	ptable[0].size = sz*1024*1024/512-ptable[0].start;

	#if 0
		//write some debugging info
		cout << numheads << " heads\n";
		cout << numcyls << " cylinders\n";
		cout << numsects << " sectors per cylinder\n";
		cout << "Start C/H/S: " <<  (int)( ptable[0].scyl | ( (ptable[0].ssector<<2)&0xff00)) << "/"
			<< int(ptable[0].shead) << "/" << (int)(ptable[0].ssector & 0x3f)  << "*\n";
		cout << "End C/H/S: " <<  (int)( ptable[0].ecyl | ( ( int(ptable[0].esector)<<2)&0xff00)) << "/"
			<< int(ptable[0].ehead) << "/" << (int)(ptable[0].esector & 0x3f)  << "*\n";
		printf("start sec/size sec= %d/%d\n",ptable[0].start,ptable[0].size);
		cout << "(*=one based numbering)\n";
	#endif

	//write MBR code
	fwrite(mbrcode,1,sizeof(mbrcode),fp);
	if( sizeof(mbrcode) > 446 ){
		cout << "Warning! MBR code was truncated\n";
	}
	//write only the partition table
	fseek(fp,446,SEEK_SET);
	fwrite(ptable,1,64,fp);

	//write signature bytes
	fputc(0x55,fp);
	fputc(0xaa,fp);

	//cout << "---mkpartition: created one partition successfully\n";

	fclose(fp);
	return 0;
}

//make FAT-16 filesystem
int mkfs(const char* fname){
	//argv[1] = filename
	FILE* fp = fopen(fname,"r+b");
	if(!fp){
		cerr << "Cannot open hard drive!\n";
		return 1;
	}

	char mbr[512];

	fread(mbr,1,512,fp);

	if(  mbr[510] != 0x55 || mbr[511] != (char) 0xaa ){
		cerr << "No valid partition table found\n";
		return 1;
	}


	PTE* ptable = (PTE*) (mbr + 446);


	int es = ptable[0].esector & 0x3f;

	//sectors per cluster
	int spc;

	//size of disk in megabytes
	int szm = ptable[0].size * 512/1024/1024 + 1;

	//compute sectors per cluster
	if( szm <= 16)		spc = 4;
	else if( szm <= 32)	spc = 1;	//(!)
	else if( szm <= 64)	spc = 2;
	else if( szm <= 128)	spc = 4;
	else if( szm <= 256)	spc = 8;
	else if( szm <= 512)	spc = 16;
	else if( szm <= 1024)	spc = 32;
	else if( szm <= 2048)	spc = 64;
	else			spc = 128;


	#if 0
		int ec = int(ptable[0].endcyl) | int( (ptable[0].endsect << int(2) ) & 0xff00);
		cerr << "Size of partition: " << szm << " MB\n";
		cerr << "Sectors per cluster = " << spc << "\n";
		cerr << "C/H/S: " << ec+1 << "/" << ptable[0].endhead+1 << "/" << es << "\n";
	#endif


	//create a vbr

	VBR vbr;
	memset(&vbr,0,sizeof(vbr));

    if( sizeof(vbr) != 62 ){
        cerr << "VBR has wrong size: " << sizeof(vbr) << ": Expected 62\n";
        
        #define X(y) cerr << #y << " = " << sizeof( vbr . y ) << "\n";
    
        X(jmp);
        X(oem);
        X(bytes_per_sector)
        X(sectors_per_cluster);
        X(vbr_sectors);
        X(num_fats);
        X(num_root_dir_entries);
        X(num_sectors_small);
        X(id);
        X(sectors_per_fat);
        X(num_heads);
        X(first_sector);
        X(num_sectors_big);
        X(drive_number);
        X(reserved);
        X(sig1);
        X(serial_number);
        X(label);
        X(fstype);
        exit(1);
    }
    
	strncpy(vbr.oem,"mkfs    ",8);
	vbr.bytes_per_sector = 512;
	vbr.sectors_per_cluster = spc;
	vbr.vbr_sectors = 1;
	vbr.num_fats = 2;
    
    int nrde = 512-32*(rand()&3);
	vbr.num_root_dir_entries = nrde;
	if( szm < 32 )
		vbr.num_sectors_small = ptable[0].size;
	vbr.id = 0xf8;
        vbr.sectors_per_fat = (ptable[0].size / spc * 2) / 512;
        vbr.sectors_per_track = es;
        vbr.num_heads = ptable[0].ehead+1;
        vbr.first_sector = ptable[0].start;
	if( szm >= 32 )
		vbr.num_sectors_big = ptable[0].size;
	vbr.drive_number = 0x80;
        vbr.sig1 = 0x29;
        vbr.serial_number = 314159265;
        strncpy(vbr.label,"hello world",11);
        strncpy(vbr.fstype,"FAT16   ",8);


	//write vbr
	char zeros32[32];
	memset(zeros32,0,32);

	fseek(fp,ptable[0].start*512,SEEK_SET);
	for(int i=0;i<16;++i)
		fwrite(zeros32,1,32,fp);
	fseek(fp,ptable[0].start*512,SEEK_SET);
	fwrite(&vbr,1,sizeof(vbr),fp);
	fseek(fp,ptable[0].start*512+510,SEEK_SET);
	fputc(0x55,fp);
	fputc(0xaa,fp);

	//now write FAT 1
	unsigned pos1 = ftell(fp);
	for(int i=0;i<vbr.sectors_per_fat;++i){
		for(int i=0;i<16;++i)
			fwrite(zeros32,1,32,fp);
	}
	unsigned pos2 = ftell(fp);

	//mark first two clusters as used
	fseek(fp,pos1,SEEK_SET);
	fputc(0xf8,fp);
	fputc(0xff,fp);
	fputc(0xff,fp);
	fputc(0xff,fp);
	fseek(fp,pos2,SEEK_SET);


	//write FAT 2
	pos1 = ftell(fp);
	for(int i=0;i<vbr.sectors_per_fat;++i){
		for(int i=0;i<16;++i)
			fwrite(zeros32,1,32,fp);
	}
	pos2 = ftell(fp);
	//mark first two clusters as used
	fseek(fp,pos1,SEEK_SET);
	fputc(0xf8,fp);
	fputc(0xff,fp);
	fputc(0xff,fp);
	fputc(0xff,fp);
	fseek(fp,pos2,SEEK_SET);


	//write root directory
	for(int i=0;i<vbr.num_root_dir_entries;++i)
		fwrite(zeros32,1,32,fp);


	//cout << "---mkfs: created empty FAT16 filesystem\n";

	fclose(fp);
	return 0;
}

//overlay a vbr on partition 1
int overlayvbr(const char* fname){
	FILE* ofp = fopen(fname,"r+b");

    if( vbrcode_size > 510 ){
        cerr << "VBR too large\n";
        return 1;
    }
    
	//go to location where partition offset is located
	fseek(ofp,454,SEEK_SET);

	unsigned ns = 0;
	fread(&ns,4,1,ofp);

	//now, ns has number of sectors before first sector of partition 1 on HD
	//seek to that spot, bytewise
	fseek(ofp,ns*512,SEEK_SET);

	//now write the vbr, but don't write volume parameters
	fwrite(vbrcode,1,3,ofp);
	fseek(ofp,ns*512+62,SEEK_SET);
	fwrite(vbrcode+62,1,vbrcode_size-62,ofp);
    fseek(ofp,ns*512+510,SEEK_SET);
    fputc(0x55,ofp);
    fputc(0xaa,ofp);
	fclose(ofp);

	return 0;
}

int main(int argc, char* argv[]){
    const char* fname = argv[1];
    int size_in_mb = atoi(argv[2]);
    srand(time(0));
    if( mkdisk(fname,size_in_mb) ||
        mkpartition(fname) ||
        mkfs(fname) ||
        overlayvbr(fname) ){
        cerr << "Failure\n";
        return 1;
    }
    return 0;
}

