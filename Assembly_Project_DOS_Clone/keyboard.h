#pragma once
#include "kprintf.h"


#define LINEBUF_SIZE 40

extern void outb(unsigned char value, unsigned short port);
extern int inb(unsigned short port);
void keyboard_init();
void enable_mouse();
void keyboard_interrupt();
int keyboard_getline(char* q, int size);
int isNumericChar(char x);
int is_number(char c);
int katoi(char* a, char** s);
int kstrcmp(const char* s1, const char* s2);
void kmemcpy(void* dest, void* src, int n);