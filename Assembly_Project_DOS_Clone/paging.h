#pragma once
#include "util.h"

#define MEMORY_SIZE_BYTES (128*1024*1024)
#define MEMORY_PAGES (MEMORY_SIZE_BYTES/4096)
//#define STACK_LOWER?
#define STACK_UPPER 0x9FC00  //stack grows down, lower should be
							 //[memory space] LESS than 0x9FC00
#define STACK_LOWER 0x50000 //here, you will just put something workable
// what is iti and oti, and where do they come from?

unsigned outer_ptable[1024]__attribute__((aligned(4096)));
unsigned inner_ptables[MEMORY_PAGES/1024][1024]__attribute__((aligned(4096)));
extern int getDataStart();
extern int getBssEnd();
void paging_init();