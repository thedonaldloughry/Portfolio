#include "paging.h"

int is_writable(unsigned int frame_start)
{
	// "bool" is undefined in base C. return 1 for true, 0 for false. //
	if(frame_start >= 0xa0000 && frame_start <= 0xfffff)
	{
		return 1;
	}
	if(frame_start < 0x500)
	{
		return 1;
	}
	if(frame_start >= (unsigned int)outer_ptable && frame_start < (unsigned int)outer_ptable + sizeof(outer_ptable))
	{
		return 1;
	}
	if(frame_start >= (unsigned int)inner_ptables && frame_start < (unsigned int)inner_ptables + sizeof(inner_ptables))
	{
		return 1;
	}
	if(frame_start >= STACK_LOWER && frame_start <= STACK_UPPER)
	{
		return 1;
	}
	if(frame_start >= getDataStart() && frame_start <= getBssEnd())
	{
		return 1;
	}
	return 0;
}

void paging_init()
{
	unsigned int oti, iti, frame_start, p, k;
	oti = 0;
	iti = 0;
	for(oti = 0; oti <= 1023; oti++)
	{
		frame_start = oti*4*1024*1024;
		if(frame_start >= MEMORY_SIZE_BYTES)
		{
			outer_ptable[oti] = 0;
		}
		else
		{
			outer_ptable[oti] = (unsigned int)&inner_ptables[iti][0];
			outer_ptable[oti] |= 3; //  pseudocode says W and P...
			for(k = 0; k <= 1023; k++, frame_start += 4096)
			{
				p = (oti << 22) | (k << 12);
				if(is_writable(frame_start))
				{
					p |= 3;
				}
				else
				{
					p |= 1;
				}
				inner_ptables[iti][k] = p;
			}
			iti += 1;
		}
	}
	activate_paging((unsigned)outer_ptable);
}