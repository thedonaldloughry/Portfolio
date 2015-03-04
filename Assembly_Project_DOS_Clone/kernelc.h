#pragma once
#include "kprintf.h"
#include "util.h"
#include "paging.h"

void illegal_opcode();
void page_fault();
void kmain();
