#QEMU ?= qemu-system-i386
#GCC ?= gcc -m32 -Wall -Werror

#for linux
#NASM ?= nasm -f elf32
#SUF ?= 
#LINK ?= ld -melf_i386
#RM ?= rm
#QEMU ?= qemu-system-i386
#GCC ?= gcc -m32 -Wall -Werror

#for windows
NASM ?= nasm -f win32 --prefix _
SUF ?= .exe
LINK ?= ld
RM ?= del
QEMU ?= qemu-system-i386
GCC ?= gcc -m32 -Wall -Werror

#for mac
#wget http://download.fedoraproject.org/pub/fedora/linux/releases/20/Live/x86_64/Fedora-Live-Desktop-x86_64-20-1.iso

CC=$(GCC)
CXX=g++ -Wall -g

all: tools
	
	$(NASM) kernelasm.s -o kernelasm.o
	
	$(GCC) -c kernelc.c  -o kernelc.o 
	$(GCC) -c kprintf.c -o kprintf.o 
	$(GCC) -c util.c -o util.o
	$(GCC) -c paging.c -o paging.o
	$(GCC) -c keyboard.c -o keyboard.o
	
	$(LINK) -Map kernelmap.txt -T linkerscript.txt -o kernel.tmp kernelasm.o kernelc.o kprintf.o util.o paging.o keyboard.o
	objcopy -O binary kernel.tmp kernel.bin 
	
	./mkdisk hd1.img 64 
	./mcp hd1.img kernel.bin KERNEL.BIN
	
	$(QEMU) -monitor vc:80Cx27C hd1.img
	
	
tools: mcp$(SUF) mfat$(SUF) mkdisk$(SUF) mls$(SUF) mrm$(SUF)

mfat$(SUF): mfat.cpp
	$(CXX) mfat.cpp -o mfat
mcp$(SUF): mcp.cpp
	$(CXX) mcp.cpp -o mcp
mkdisk$(SUF): mkdisk.cpp
	$(CXX) mkdisk.cpp -o mkdisk
mrm$(SUF): mrm.cpp
	$(CXX) mrm.cpp -o mrm
mls$(SUF): mls.cpp
	$(CXX) mls.cpp -o mls

clean: 
	$(RM) $(wildcard *.bin) $(wildcard *.tmp) $(wildcard *.o) $(wildcard *.exe) $(wildcard *.img) mfat mcp mkdisk mrm mls