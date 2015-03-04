#pragma once
#include "kprintf.h"
#include "keyboard.h"

int row;
int col;

typedef struct
{
	//volatile int int_num;
	//int eax, ecx, edx, ebx, esp, ebp, esi, cs, eflags, int_num;
	unsigned int ds, es, fs, gs, ss, eax, ebx, ecx, edx, esi, edi, ebp, esp, int_num, errcode, eip, cs, eflags;
	//what else will this need? and how does the system tell us what interupt it needs to throw?
}__attribute__((packed))StateBlock;

volatile int jiffies; //because why not!
unsigned int sv;
void highLevelHandler(StateBlock *sb);
void console_init();
void kmemcpy(void* dest, void* src, int n);
void console_clear();
void console_putc(char x);
extern void outb(unsigned char value, unsigned short port);
extern int inb(unsigned short port);
extern void activate_paging(unsigned outer_table_loc);
extern void interrupt_init();
void irq_init();
void halt();
int uptime();
void remap_PIC1();
void remap_PIC2();