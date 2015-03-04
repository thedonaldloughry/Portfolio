#include "keyboard.h"

static char* keyboardChars[] = {"\0", "ESC", "1", "2", "3", "4", "5", "6", "7", "8",
					"9", "0", "-", "=", "BACKSPACE", "TAB", "q", "w",
					"e", "r", "t", "y", "u", "i", "o", "p", "[", "]",
					"\n", "LCTRL", "a", "s", "d", "f", "g", "h", "j",
					"k", "l", ";", "'", "`", "LSHIFT", "\\", "z", "x",
					"c", "v", "b", "n", "m", ",", ".", "/", "RSHIFT",
					"PRNTSC", "LALT", " ", "CAPLK", "F1", "F2", "F3",
					"F4", "F5", "F6", "F7", "F8", "F9", "F10", "NMLK", "SCRLK",
					"7*", "8*", "9*", "-*", "4*", "5*", "6*", "+*", "1*", "2*", 
					"3*", "0*", ".*", "SYSRQ", "", "", "F11", "F12", ""};
//note: strings are char[]'s, so... you have a 2-D array here.
static char* spKeyboardChars[] = {"\0", "\0", "!", "@", "#", "$", "%", "^", "&", "*",
					"(", ")", "_", "+", "\0", "\0", "Q", "W",
					"E", "R", "T", "Y", "U", "I", "O", "P", "{", "}",
					"\0", "\0", "A", "S", "D", "F", "G", "H", "J",
					"K", "L", ":", "\0", "~", "\0", "|", "Z", "X",
					"C", "V", "B", "N", "M", "<", ">", "?", "\0",
					"\0", "\0", " ", "\0", "\0", "\0", "\0",
					"\0", "\0", "\0", "\0", "\0", "\0", "\0", "\0", "\0",
					"7*", "8*", "9*", "-*", "4*", "5*", "6*", "+*", "1*", "2*", 
					"3*", "0*", ".*", "\0", "", "", "\0", "\0", ""};
static char linebuff[LINEBUF_SIZE];
static int linesize = 0;
static volatile int buffer_ready = 0;

void keyboard_init()
{
	return;
}

void keyboard_interrupt()
{
	unsigned char q = inb((short)0x60); //ports are shorts, correct?
	int press = !(q&0x80); // note that 0 = false, 1 = true
	int isShifted;
	q &= 0x7f;
	//q comes in as a "scancode"... a.k.a. a number that maps to a key.
	//we must handle the kkprintf calls for all pressable keys.
	//note that for special characters, we need to look for cases where
	//we get 0xe0 as the first part of our scancode, then a number.
	//best done as if-statements.
	if(buffer_ready == 1)
	{
		return;
	}
	if((keyboardChars[q] == (char*)"LSHIFT") || (keyboardChars[q] == (char*)"RSHIFT"))
	{
		if(press)
		{
			isShifted = 1;
		}
		else
		{
			isShifted = 0;
		}
	}
	if((keyboardChars[q] == (char*)"BACKSPACE") && press)
	{
		if( linesize > 0)
		{
			linesize -= 1;
			kprintf("%c", 127);
		}
	}
	else if((keyboardChars[q] == (char*)"\n") && press)
	{
		buffer_ready = 1;
	}
	else if(q && (linesize < LINEBUF_SIZE) && press)
	{
		if(!isShifted)
		{
			linebuff[linesize++] = *keyboardChars[q];
			kprintf(keyboardChars[q]);
		}
		else if(isShifted && (keyboardChars[q] != (char*)"LSHIFT") && (keyboardChars[q] != (char*)"RSHIFT"))
		{
			//don't fill buffer with the "LSHIFT" or "RSHIFT" tags...
			linebuff[linesize++] = *spKeyboardChars[q];
			kprintf(spKeyboardChars[q]);
		}	
	}
}

int keyboard_getline(char* q, int size) // pass array to function...
{
	while(buffer_ready == 0)
	{
		asm("hlt");
	}
	kmemcpy(q, linebuff, linesize);
	q[linesize] = 0;
	int tmpLineSize = linesize;
	linesize = 0;
	buffer_ready = 0;
	return tmpLineSize;
}

int is_number(char c) //to act like a boolean function
{
	return ( c >= '0') && ( c <= '9' );
}

int katoi(char* a, char** s)
{
	//source: http://www.geeksforgeeks.org/write-your-own-atoi/
	//due credit to Stephanie Hopper for her help here.
	int result = 0;
	int i = 0;
	while(is_number(a[i]))
	{
		result = result * 10 + a[i] - '0';
		i++;
		++*s;
	}
	return result;
}

int kstrcmp(const char* s1, const char* s2)
{
	while(*s1 == *s2 && *s1 && *s2)
	{
		s1++;
		s2++;
	}
	if(*s1 > *s2) {return 1;}
	else if(*s1 < *s2) {return -1;}
	else {return 0;}
}

void kmemcpy(void* dest, void* src, int n)
{
	int i;
	char* d = dest;
	char* s = src;
	for(i = 0; i < n; i++)
	{
		*(d+i) = *(s+i);
	}
}