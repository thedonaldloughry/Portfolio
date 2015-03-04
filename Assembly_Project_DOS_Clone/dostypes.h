// ssu etec3701 fall 2007

#pragma once

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

struct DirEntry{
	char base[8];
	char ext[3];
	unsigned char attrib;
	char reserved[10];
	unsigned short time;
	unsigned short date;
	unsigned short start;
	unsigned int size;
} __attribute__((packed));

#pragma pack(pop)

