#include "kernelc.h"

int main(){ return 0;}
int _main(){ return 0;}
int __main(){ return 0;}

char buf[LINEBUF_SIZE+1];

void illegal_opcode(){
    asm (".byte 0xff,0xff");
}

void page_fault(){
    int start = uptime();
    int next_print = start + 1000;
    int counter = 5;
    kprintf("\nSelf destruct in %d...",counter);
    while( counter > 0 ){
        counter--;
        while( uptime() < next_print )
            ;
        next_print += 1000;
        kprintf("%d...",counter);
    }
    kprintf("\n***BOOM***\n");
    int* p = (int*) 0xdeadbeef;
    *p = 31337;
    kprintf("\nSelf destruct mechanism failed.\n");
}

void kmain(void)
{
    console_init();
    interrupt_init();
    paging_init();
    irq_init();
    keyboard_init();
    
    while(1){
        int n;
        
        kprintf("> ");
        n = keyboard_getline(buf, sizeof(buf)-1);
        buf[n]=0;
        if( n > 0 && buf[n-1] == '\n' )
            buf[n-1]=0;
        
        if( kstrcmp(buf,"opcode") == 0 ){
			kprintf("\nIllegal Opcode!\n");
            illegal_opcode();
        }
        else if( kstrcmp(buf,"destruct 0") == 0 ){
			kprintf("\nSelf-destruct sequence initiated...\n");
            page_fault();
        }
        else{
            //arithmetic
            char* p = buf;
            int op1 = katoi(buf,&p);
            char op = p[0];
            ++p;
            int op2 = katoi(p,&p);
            int res;
            if( op == '+' )
                res = op1+op2;
            else if( op == '-' )
                res = op1-op2;
            else if( op == '*' )
                res = op1*op2;
            else if( op == '/' )   
                res = op1/op2;
            else{
                kprintf("\nIllegal\n");
                continue;
            }
            
            kprintf("\n%d\n",res);
        }
     }
}