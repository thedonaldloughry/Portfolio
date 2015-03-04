#include "util.h"

void console_init()
{
	//setup the program
	row = 0;
	col = 0;
	console_clear();
}

void irq_init()
{
	interrupt_init();
	remap_PIC1();
	remap_PIC2(); // could error if incorrect
	outb((char)0xa, (short)0x70);
	sv = inb((short)0x71);
	outb((char)0xa, (short)0x70);
	outb((char)0x8|(sv&0xf0), (short)0x71); // modified, 8 to 0x8
	outb((char)0xb, (short)0x70);
	sv = inb((short)0x71);
	outb((char)0xb, (short)0x70);
	outb((char)sv|0x40, (short)0x71);
	outb((char)0xc, (short)0x70);
	inb((short)0x71);
	asm volatile ("sti");
}

void console_clear()
{
	char *c = (char*)0xB8000;
	char *x = "";
	int i;
	for(i=0;i < 80*24;i++)
	{
		*c = *x;
		c = c+2;
	}
}

void console_putc(char x)
{
	int p = row*80+col;
	char *c = 2*p+(char*)0xB8000;
		
	col++;
	if(col==80)				
	{
		col = 0;		
		row++;
	}
	if(x == 10) //this needs to tell the program to NOT write the character!!!
	{
		col = 0;
		row++;
	}
	else if(x == 9) //9 is apparently the tab character
	{
		col += 5;
	}
	else if(x == 127)
	{
		if(row == 0 && col == 0)
		{
			kprintf("return case");
			return;
		}
		else if(col == 0)
		{
			kprintf("end of row case");
			row--;
			col = 79;
			x = '\0';
			//would edit video memory location... couldn't get it to not error, i.e. character weirdness.
		}
		else
		{
			col--;
			//move the cursor back to where p now is...
			x = '\0';
		}
	}
	else
	{
		*c = x;
		c++;
		*c = 0x07;
		c++;
		outb(15, 0x3D4);
		outb((unsigned char)p, 0x3D5);
		outb(14, 0x3D4);
		outb((unsigned char)(p>>8), 0x3D5);
	}
	if(row > 24)
	{
		kmemcpy((char*)0xB8000, (char*)0xB8000+160, 80*24*2);
		row = 24;
	}
}

void highLevelHandler(StateBlock *sb)
{
	if(sb->int_num < 32)
	{
		//"bad" error
		kprintf("\nError:%i", sb->int_num);
		halt();
	}
	if(sb->int_num >= 32 && sb->int_num <= 39)
	{
		//we just want to acknowledge PIC1
		outb((char)0x20, (short)0x20);
	}
	if(sb->int_num >= 40 && sb->int_num <= 47)
	{
		//acknowledge PIC1 and PIC2
		outb((char)0x20, (short)0x20);
		outb((char)0x20, (short)0xa0);
	}
	if(sb->int_num == 40)
	{
		jiffies += 1;
	}
	if(sb->int_num == 32)
	{
		jiffies += 55;
	}
	if(sb->int_num == 33)
	{
		keyboard_interrupt();
	}
}

void halt()
{
	while(1)
	{
		asm("hlt");
	}
}

int uptime()
{
	return jiffies; //finally, jiffies has a purpose
}

void remap_PIC1()
{
	outb(0x11, 0x20); // set base value, primary/secondary setup,...
	outb(0x20, 0x21); // "base", for us, is 20...
	outb(0x4, 0x21);  // tells us this is the primary PIC
	outb(0x1, 0x21);	// says "use 8086 PIC conventions"
	outb(0x0, 0x21);	// tells PIC that all 8 IRQ lines enabled
}

void remap_PIC2()
{
	outb(0x11, 0xa0); // output to command port
	outb(0x28, 0xa1); // set 40 as base int
	outb(0x2, 0xa1); // indicates that this is the secondary PIC
	outb(0x1, 0xa1); // use 8086 PIC conventions
	outb(0x0, 0x21); // all 8 IRQ lines enabled
}