section .data
	interrupt_table:
		times 256 dq 0x0008e0000100000;
		;initializes interrupt_table to have 256 idt entries with static parts
	idtloc:
		dw 2048 ; 256*8=2048
		dd 0
section .bss
; contents of .bss
section .stack 
; contents of stack
section .text
	extern kmain
	extern sdata ; what is this?
	extern highLevelHandler
	extern sbss
	extern ebss
	global outb
	global inb
	global getDataStart
	global getBssEnd
	global interrupt_init
	global activate_paging
	
	mov ebx, sbss
	mov ecx, ebss
	
	wloop:
		cmp ebx, ecx
		je endwloop
		mov byte [ebx], 0
		inc ebx
		jmp wloop
	endwloop:
		mov esp, 0x9FC00 ;this MAY BE where STACK_UPPER is.
		jmp kmain
	outb:
		mov edx, [esp+8]
		mov eax, [esp+4]
		out dx, al
	inb:
		mov edx,[esp+4]
		xor eax,eax
		in al,dx
		ret
	
	interrupt_init:
		jmp initIDT
		ret
		
	activate_paging:
		mov eax, [esp+4] ;get table location
		mov cr3, eax ;put location in the cr3 register
		mov eax, cr0 ;get the cr0 register
		or eax, 0x80010000 ;turn on bits 31 and 16
		mov cr0, eax ;set cr0: activate paging
		jmp flushqueue ;because Intel is our master...
	
	flushqueue:
		nop
		ret ;nice.
	
	midlevel_handler:
		push ds
		push es
		push fs
		push gs
		push ss
		push eax
		push ebx
		push ecx
		push edx
		push esi
		push edi
		push ebp
		push esp
		push esp
		call highLevelHandler
		add dword esp, 4
		pop esp
		pop ebp
		pop edi
		pop esi
		pop edx
		pop ecx
		pop ebx
		pop eax
		pop ss
		pop gs
		pop fs
		pop es
		pop ds
		
		add esp, 8
		iret
	
	getDataStart:
		mov eax, sdata
		ret
	
	getBssEnd:
		mov eax, ebss
		ret
	
	lowlevel_handler_0:
		push dword 0xdeadbeef
		push dword 0
		jmp midlevel_handler

	 lowlevel_handler_1:
		push dword 0xdeadbeef
		push dword 1
		jmp midlevel_handler

	 lowlevel_handler_2:
		push dword 0xdeadbeef
		push dword 2
		jmp midlevel_handler

	 lowlevel_handler_3:
		push dword 0xdeadbeef
		push dword 3
		jmp midlevel_handler

	 lowlevel_handler_4:
		push dword 0xdeadbeef
		push dword 4
		jmp midlevel_handler

	 lowlevel_handler_5:
		push dword 0xdeadbeef
		push dword 5
		jmp midlevel_handler

	 lowlevel_handler_6:
		push dword 0xdeadbeef
		push dword 6
		jmp midlevel_handler

	 lowlevel_handler_7:
		push dword 0xdeadbeef
		push dword 7
		jmp midlevel_handler

	 lowlevel_handler_8:
		push dword 0xdeadbeef
		push dword 8
		jmp midlevel_handler

	 lowlevel_handler_9:
		push dword 0xdeadbeef
		push dword 9
		jmp midlevel_handler

	 lowlevel_handler_10:
		push dword 0xdeadbeef
		push dword 10
		jmp midlevel_handler

	 lowlevel_handler_11:
		push dword 0xdeadbeef
		push dword 11
		jmp midlevel_handler

	 lowlevel_handler_12:
		push dword 0xdeadbeef
		push dword 12
		jmp midlevel_handler

	 lowlevel_handler_13:
		push dword 0xdeadbeef
		push dword 13
		jmp midlevel_handler

	 lowlevel_handler_14:
		push dword 14
		jmp midlevel_handler

	 lowlevel_handler_15:
		push dword 0xdeadbeef
		push dword 15
		jmp midlevel_handler

	 lowlevel_handler_16:
		push dword 0xdeadbeef
		push dword 16
		jmp midlevel_handler

	 lowlevel_handler_17:
		push dword 0xdeadbeef
		push dword 17
		jmp midlevel_handler

	 lowlevel_handler_18:
		push dword 0xdeadbeef
		push dword 18
		jmp midlevel_handler

	 lowlevel_handler_19:
		push dword 0xdeadbeef
		push dword 19
		jmp midlevel_handler

	 lowlevel_handler_20:
		push dword 0xdeadbeef
		push dword 20
		jmp midlevel_handler

	 lowlevel_handler_21:
		push dword 0xdeadbeef
		push dword 21
		jmp midlevel_handler

	 lowlevel_handler_22:
		push dword 0xdeadbeef
		push dword 22
		jmp midlevel_handler

	 lowlevel_handler_23:
		push dword 0xdeadbeef
		push dword 23
		jmp midlevel_handler

	 lowlevel_handler_24:
		push dword 0xdeadbeef
		push dword 24
		jmp midlevel_handler

	 lowlevel_handler_25:
		push dword 0xdeadbeef
		push dword 25
		jmp midlevel_handler

	 lowlevel_handler_26:
		push dword 0xdeadbeef
		push dword 26
		jmp midlevel_handler

	 lowlevel_handler_27:
		push dword 0xdeadbeef
		push dword 27
		jmp midlevel_handler

	 lowlevel_handler_28:
		push dword 0xdeadbeef
		push dword 28
		jmp midlevel_handler

	 lowlevel_handler_29:
		push dword 0xdeadbeef
		push dword 29
		jmp midlevel_handler

	 lowlevel_handler_30:
		push dword 0xdeadbeef
		push dword 30
		jmp midlevel_handler

	 lowlevel_handler_31:
		push dword 0xdeadbeef
		push dword 31
		jmp midlevel_handler

	 lowlevel_handler_32:
		push dword 0xdeadbeef
		push dword 32
		jmp midlevel_handler

	 lowlevel_handler_33:
		push dword 0xdeadbeef
		push dword 33
		jmp midlevel_handler

	 lowlevel_handler_34:
		push dword 0xdeadbeef
		push dword 34
		jmp midlevel_handler

	 lowlevel_handler_35:
		push dword 0xdeadbeef
		push dword 35
		jmp midlevel_handler

	 lowlevel_handler_36:
		push dword 0xdeadbeef
		push dword 36
		jmp midlevel_handler

	 lowlevel_handler_37:
		push dword 0xdeadbeef
		push dword 37
		jmp midlevel_handler

	 lowlevel_handler_38:
		push dword 0xdeadbeef
		push dword 38
		jmp midlevel_handler

	 lowlevel_handler_39:
		push dword 0xdeadbeef
		push dword 39
		jmp midlevel_handler

	 lowlevel_handler_40:
		push dword 0xdeadbeef
		push dword 40
		jmp midlevel_handler

	 lowlevel_handler_41:
		push dword 0xdeadbeef
		push dword 41
		jmp midlevel_handler

	 lowlevel_handler_42:
		push dword 0xdeadbeef
		push dword 42
		jmp midlevel_handler

	 lowlevel_handler_43:
		push dword 0xdeadbeef
		push dword 43
		jmp midlevel_handler

	 lowlevel_handler_44:
		push dword 0xdeadbeef
		push dword 44
		jmp midlevel_handler

	 lowlevel_handler_45:
		push dword 0xdeadbeef
		push dword 45
		jmp midlevel_handler

	 lowlevel_handler_46:
		push dword 0xdeadbeef
		push dword 46
		jmp midlevel_handler

	 lowlevel_handler_47:
		push dword 0xdeadbeef
		push dword 47
		jmp midlevel_handler

	 lowlevel_handler_48:
		push dword 0xdeadbeef
		push dword 48
		jmp midlevel_handler

	 lowlevel_handler_49:
		push dword 0xdeadbeef
		push dword 49
		jmp midlevel_handler

	 lowlevel_handler_50:
		push dword 0xdeadbeef
		push dword 50
		jmp midlevel_handler

	 lowlevel_handler_51:
		push dword 0xdeadbeef
		push dword 51
		jmp midlevel_handler

	 lowlevel_handler_52:
		push dword 0xdeadbeef
		push dword 52
		jmp midlevel_handler

	 lowlevel_handler_53:
		push dword 0xdeadbeef
		push dword 53
		jmp midlevel_handler

	 lowlevel_handler_54:
		push dword 0xdeadbeef
		push dword 54
		jmp midlevel_handler

	 lowlevel_handler_55:
		push dword 0xdeadbeef
		push dword 55
		jmp midlevel_handler

	 lowlevel_handler_56:
		push dword 0xdeadbeef
		push dword 56
		jmp midlevel_handler

	 lowlevel_handler_57:
		push dword 0xdeadbeef
		push dword 57
		jmp midlevel_handler

	 lowlevel_handler_58:
		push dword 0xdeadbeef
		push dword 58
		jmp midlevel_handler

	 lowlevel_handler_59:
		push dword 0xdeadbeef
		push dword 59
		jmp midlevel_handler

	 lowlevel_handler_60:
		push dword 0xdeadbeef
		push dword 60
		jmp midlevel_handler

	 lowlevel_handler_61:
		push dword 0xdeadbeef
		push dword 61
		jmp midlevel_handler

	 lowlevel_handler_62:
		push dword 0xdeadbeef
		push dword 62
		jmp midlevel_handler

	 lowlevel_handler_63:
		push dword 0xdeadbeef
		push dword 63
		jmp midlevel_handler

	 lowlevel_handler_64:
		push dword 0xdeadbeef
		push dword 64
		jmp midlevel_handler

	 lowlevel_handler_65:
		push dword 0xdeadbeef
		push dword 65
		jmp midlevel_handler

	 lowlevel_handler_66:
		push dword 0xdeadbeef
		push dword 66
		jmp midlevel_handler

	 lowlevel_handler_67:
		push dword 0xdeadbeef
		push dword 67
		jmp midlevel_handler

	 lowlevel_handler_68:
	push dword 0xdeadbeef
		push dword 68
		jmp midlevel_handler

	 lowlevel_handler_69:
		push dword 0xdeadbeef
		push dword 69
		jmp midlevel_handler

	 lowlevel_handler_70:
		push dword 0xdeadbeef
		push dword 70
		jmp midlevel_handler

	 lowlevel_handler_71:
		push dword 0xdeadbeef
		push dword 71
		jmp midlevel_handler

	 lowlevel_handler_72:
		push dword 0xdeadbeef
		push dword 72
		jmp midlevel_handler

	 lowlevel_handler_73:
		push dword 0xdeadbeef
		push dword 73
		jmp midlevel_handler

	 lowlevel_handler_74:
		push dword 0xdeadbeef
		push dword 74
		jmp midlevel_handler

	 lowlevel_handler_75:
		push dword 0xdeadbeef
		push dword 75
		jmp midlevel_handler

	 lowlevel_handler_76:
		push dword 0xdeadbeef
		push dword 76
		jmp midlevel_handler

	 lowlevel_handler_77:
		push dword 0xdeadbeef
		push dword 77
		jmp midlevel_handler

	 lowlevel_handler_78:
		push dword 0xdeadbeef
		push dword 78
		jmp midlevel_handler

	 lowlevel_handler_79:
		push dword 0xdeadbeef
		push dword 79
		jmp midlevel_handler

	 lowlevel_handler_80:
		push dword 0xdeadbeef
		push dword 80
		jmp midlevel_handler

	 lowlevel_handler_81:
		push dword 0xdeadbeef
		push dword 81
		jmp midlevel_handler

	 lowlevel_handler_82:
		push dword 0xdeadbeef
		push dword 82
		jmp midlevel_handler

	 lowlevel_handler_83:
		push dword 0xdeadbeef
		push dword 83
		jmp midlevel_handler

	 lowlevel_handler_84:
		push dword 0xdeadbeef
		push dword 84
		jmp midlevel_handler

	 lowlevel_handler_85:
		push dword 0xdeadbeef
		push dword 85
		jmp midlevel_handler

	 lowlevel_handler_86:
		push dword 0xdeadbeef
		push dword 86
		jmp midlevel_handler

	 lowlevel_handler_87:
		push dword 0xdeadbeef
		push dword 87
		jmp midlevel_handler

	 lowlevel_handler_88:
		push dword 0xdeadbeef
		push dword 88
		jmp midlevel_handler

	 lowlevel_handler_89:
		push dword 0xdeadbeef
		push dword 89
		jmp midlevel_handler

	 lowlevel_handler_90:
		push dword 0xdeadbeef
		push dword 90
		jmp midlevel_handler

	 lowlevel_handler_91:
		push dword 0xdeadbeef
		push dword 91
		jmp midlevel_handler

	 lowlevel_handler_92:
		push dword 0xdeadbeef
		push dword 92
		jmp midlevel_handler

	 lowlevel_handler_93:
		push dword 0xdeadbeef
		push dword 93
		jmp midlevel_handler

	 lowlevel_handler_94:
		push dword 0xdeadbeef
		push dword 94
		jmp midlevel_handler

	 lowlevel_handler_95:
		push dword 0xdeadbeef
		push dword 95
		jmp midlevel_handler

	 lowlevel_handler_96:
		push dword 0xdeadbeef
		push dword 96
		jmp midlevel_handler

	 lowlevel_handler_97:
		push dword 0xdeadbeef
		push dword 97
		jmp midlevel_handler

	 lowlevel_handler_98:
		push dword 0xdeadbeef
		push dword 98
		jmp midlevel_handler

	 lowlevel_handler_99:
		push dword 0xdeadbeef
		push dword 99
		jmp midlevel_handler

	 lowlevel_handler_100:
		push dword 0xdeadbeef
		push dword 100
		jmp midlevel_handler

	 lowlevel_handler_101:
		push dword 0xdeadbeef
		push dword 101
		jmp midlevel_handler

	 lowlevel_handler_102:
		push dword 0xdeadbeef
		push dword 102
		jmp midlevel_handler

	 lowlevel_handler_103:
		push dword 0xdeadbeef
		push dword 103
		jmp midlevel_handler

	 lowlevel_handler_104:
		push dword 0xdeadbeef
		push dword 104
		jmp midlevel_handler

	 lowlevel_handler_105:
		push dword 0xdeadbeef
		push dword 105
		jmp midlevel_handler

	 lowlevel_handler_106:
		push dword 0xdeadbeef
		push dword 106
		jmp midlevel_handler

	 lowlevel_handler_107:
		push dword 0xdeadbeef
		push dword 107
		jmp midlevel_handler

	 lowlevel_handler_108:
		push dword 0xdeadbeef
		push dword 108
		jmp midlevel_handler

	 lowlevel_handler_109:
		push dword 0xdeadbeef
		push dword 109
		jmp midlevel_handler

	 lowlevel_handler_110:
		push dword 0xdeadbeef
		push dword 110
		jmp midlevel_handler

	 lowlevel_handler_111:
		push dword 0xdeadbeef
		push dword 111
		jmp midlevel_handler

	 lowlevel_handler_112:
		push dword 0xdeadbeef
		push dword 112
		jmp midlevel_handler

	 lowlevel_handler_113:
		push dword 0xdeadbeef
		push dword 113
		jmp midlevel_handler

	 lowlevel_handler_114:
		push dword 0xdeadbeef
		push dword 114
		jmp midlevel_handler

	 lowlevel_handler_115:
		push dword 0xdeadbeef
		push dword 115
		jmp midlevel_handler

	 lowlevel_handler_116:
		push dword 0xdeadbeef
		push dword 116
		jmp midlevel_handler

	 lowlevel_handler_117:
		push dword 0xdeadbeef
		push dword 117
		jmp midlevel_handler

	 lowlevel_handler_118:
		push dword 0xdeadbeef
		push dword 118
		jmp midlevel_handler

	 lowlevel_handler_119:
		push dword 0xdeadbeef
		push dword 119
		jmp midlevel_handler

	 lowlevel_handler_120:
		push dword 0xdeadbeef
		push dword 120
		jmp midlevel_handler

	 lowlevel_handler_121:
		push dword 0xdeadbeef
		push dword 121
		jmp midlevel_handler

	 lowlevel_handler_122:
		push dword 0xdeadbeef
		push dword 122
		jmp midlevel_handler

	 lowlevel_handler_123:
		push dword 0xdeadbeef
		push dword 123
		jmp midlevel_handler

	 lowlevel_handler_124:
		push dword 0xdeadbeef
		push dword 124
		jmp midlevel_handler

	 lowlevel_handler_125:
		push dword 0xdeadbeef
		push dword 125
		jmp midlevel_handler

	 lowlevel_handler_126:
		push dword 0xdeadbeef
		push dword 126
		jmp midlevel_handler

	 lowlevel_handler_127:
		push dword 0xdeadbeef
		push dword 127
		jmp midlevel_handler

	 lowlevel_handler_128:
		push dword 0xdeadbeef
		push dword 128
		jmp midlevel_handler

	 lowlevel_handler_129:
		push dword 0xdeadbeef
		push dword 129
		jmp midlevel_handler

	 lowlevel_handler_130:
		push dword 0xdeadbeef
		push dword 130
		jmp midlevel_handler

	 lowlevel_handler_131:
		push dword 0xdeadbeef
		push dword 131
		jmp midlevel_handler

	 lowlevel_handler_132:
		push dword 0xdeadbeef
		push dword 132
		jmp midlevel_handler

	 lowlevel_handler_133:
		push dword 0xdeadbeef
		push dword 133
		jmp midlevel_handler

	 lowlevel_handler_134:
		push dword 0xdeadbeef
		push dword 134
		jmp midlevel_handler

	 lowlevel_handler_135:
		push dword 0xdeadbeef
		push dword 135
		jmp midlevel_handler

	 lowlevel_handler_136:
		push dword 0xdeadbeef
		push dword 136
		jmp midlevel_handler

	 lowlevel_handler_137:
		push dword 0xdeadbeef
		push dword 137
		jmp midlevel_handler

	 lowlevel_handler_138:
		push dword 0xdeadbeef
		push dword 138
		jmp midlevel_handler

	 lowlevel_handler_139:
		push dword 0xdeadbeef
		push dword 139
		jmp midlevel_handler

	 lowlevel_handler_140:
		push dword 0xdeadbeef
		push dword 140
		jmp midlevel_handler

	 lowlevel_handler_141:
		push dword 0xdeadbeef
		push dword 141
		jmp midlevel_handler

	 lowlevel_handler_142:
		push dword 0xdeadbeef
		push dword 142
		jmp midlevel_handler

	 lowlevel_handler_143:
		push dword 0xdeadbeef
		push dword 143
		jmp midlevel_handler

	 lowlevel_handler_144:
		push dword 0xdeadbeef
		push dword 144
		jmp midlevel_handler

	 lowlevel_handler_145:
		push dword 0xdeadbeef
		push dword 145
		jmp midlevel_handler

	 lowlevel_handler_146:
		push dword 0xdeadbeef
		push dword 146
		jmp midlevel_handler

	 lowlevel_handler_147:
		push dword 0xdeadbeef
		push dword 147
		jmp midlevel_handler

	 lowlevel_handler_148:
		push dword 0xdeadbeef
		push dword 148
		jmp midlevel_handler

	 lowlevel_handler_149:
		push dword 0xdeadbeef
		push dword 149
		jmp midlevel_handler

	 lowlevel_handler_150:
		push dword 0xdeadbeef
		push dword 150
		jmp midlevel_handler

	 lowlevel_handler_151:
		push dword 0xdeadbeef
		push dword 151
		jmp midlevel_handler

	 lowlevel_handler_152:
		push dword 0xdeadbeef
		push dword 152
		jmp midlevel_handler

	 lowlevel_handler_153:
		push dword 0xdeadbeef
		push dword 153
		jmp midlevel_handler

	 lowlevel_handler_154:
		push dword 0xdeadbeef
		push dword 154
		jmp midlevel_handler

	 lowlevel_handler_155:
		push dword 0xdeadbeef
		push dword 155
		jmp midlevel_handler

	 lowlevel_handler_156:
		push dword 0xdeadbeef
		push dword 156
		jmp midlevel_handler

	 lowlevel_handler_157:
		push dword 0xdeadbeef
		push dword 157
		jmp midlevel_handler

	 lowlevel_handler_158:
		push dword 0xdeadbeef
		push dword 158
		jmp midlevel_handler

	 lowlevel_handler_159:
		push dword 0xdeadbeef
		push dword 159
		jmp midlevel_handler

	 lowlevel_handler_160:
		push dword 0xdeadbeef
		push dword 160
		jmp midlevel_handler

	 lowlevel_handler_161:
		push dword 0xdeadbeef
		push dword 161
		jmp midlevel_handler

	 lowlevel_handler_162:
		push dword 0xdeadbeef
		push dword 162
		jmp midlevel_handler

	 lowlevel_handler_163:
		push dword 0xdeadbeef
		push dword 163
		jmp midlevel_handler

	 lowlevel_handler_164:
		push dword 0xdeadbeef
		push dword 164
		jmp midlevel_handler

	 lowlevel_handler_165:
		push dword 0xdeadbeef
		push dword 165
		jmp midlevel_handler

	 lowlevel_handler_166:
		push dword 0xdeadbeef
		push dword 166
		jmp midlevel_handler

	 lowlevel_handler_167:
		push dword 0xdeadbeef
		push dword 167
		jmp midlevel_handler

	 lowlevel_handler_168:
		push dword 0xdeadbeef
		push dword 168
		jmp midlevel_handler

	 lowlevel_handler_169:
		push dword 0xdeadbeef
		push dword 169
		jmp midlevel_handler

	 lowlevel_handler_170:
		push dword 0xdeadbeef
		push dword 170
		jmp midlevel_handler

	 lowlevel_handler_171:
		push dword 0xdeadbeef
		push dword 171
		jmp midlevel_handler

	 lowlevel_handler_172:
		push dword 0xdeadbeef
		push dword 172
		jmp midlevel_handler

	 lowlevel_handler_173:
		push dword 0xdeadbeef
		push dword 173
		jmp midlevel_handler

	 lowlevel_handler_174:
		push dword 0xdeadbeef
		push dword 174
		jmp midlevel_handler

	 lowlevel_handler_175:
		push dword 0xdeadbeef
		push dword 175
		jmp midlevel_handler

	 lowlevel_handler_176:
		push dword 0xdeadbeef
		push dword 176
		jmp midlevel_handler

	 lowlevel_handler_177:
		push dword 0xdeadbeef
		push dword 177
		jmp midlevel_handler

	 lowlevel_handler_178:
		push dword 0xdeadbeef
		push dword 178
		jmp midlevel_handler

	 lowlevel_handler_179:
		push dword 0xdeadbeef
		push dword 179
		jmp midlevel_handler

	 lowlevel_handler_180:
		push dword 0xdeadbeef
		push dword 180
		jmp midlevel_handler

	 lowlevel_handler_181:
		push dword 0xdeadbeef
		push dword 181
		jmp midlevel_handler

	 lowlevel_handler_182:
		push dword 0xdeadbeef
		push dword 182
		jmp midlevel_handler

	 lowlevel_handler_183:
		push dword 0xdeadbeef
		push dword 183
		jmp midlevel_handler

	 lowlevel_handler_184:
		push dword 0xdeadbeef
		push dword 184
		jmp midlevel_handler

	 lowlevel_handler_185:
		push dword 0xdeadbeef
		push dword 185
		jmp midlevel_handler

	 lowlevel_handler_186:
		push dword 0xdeadbeef
		push dword 186
		jmp midlevel_handler

	 lowlevel_handler_187:
		push dword 0xdeadbeef
		push dword 187
		jmp midlevel_handler

	 lowlevel_handler_188:
		push dword 0xdeadbeef
		push dword 188
		jmp midlevel_handler

	 lowlevel_handler_189:
		push dword 0xdeadbeef
		push dword 189
		jmp midlevel_handler

	 lowlevel_handler_190:
		push dword 0xdeadbeef
		push dword 190
		jmp midlevel_handler

	 lowlevel_handler_191:
		push dword 0xdeadbeef
		push dword 191
		jmp midlevel_handler

	 lowlevel_handler_192:
		push dword 0xdeadbeef
		push dword 192
		jmp midlevel_handler

	 lowlevel_handler_193:
		push dword 0xdeadbeef
		push dword 193
		jmp midlevel_handler

	 lowlevel_handler_194:
		push dword 0xdeadbeef
		push dword 194
		jmp midlevel_handler

	 lowlevel_handler_195:
		push dword 0xdeadbeef
		push dword 195
		jmp midlevel_handler

	 lowlevel_handler_196:
		push dword 0xdeadbeef
		push dword 196
		jmp midlevel_handler

	 lowlevel_handler_197:
		push dword 0xdeadbeef
		push dword 197
		jmp midlevel_handler

	 lowlevel_handler_198:
		push dword 0xdeadbeef
		push dword 198
		jmp midlevel_handler

	 lowlevel_handler_199:
		push dword 0xdeadbeef
		push dword 199
		jmp midlevel_handler

	 lowlevel_handler_200:
		push dword 0xdeadbeef
		push dword 200
		jmp midlevel_handler

	 lowlevel_handler_201:
		push dword 0xdeadbeef
		push dword 201
		jmp midlevel_handler

	 lowlevel_handler_202:
		push dword 0xdeadbeef
		push dword 202
		jmp midlevel_handler

	 lowlevel_handler_203:
		push dword 0xdeadbeef
		push dword 203
		jmp midlevel_handler

	 lowlevel_handler_204:
		push dword 0xdeadbeef
		push dword 204
		jmp midlevel_handler

	 lowlevel_handler_205:
		push dword 0xdeadbeef
		push dword 205
		jmp midlevel_handler

	 lowlevel_handler_206:
		push dword 0xdeadbeef
		push dword 206
		jmp midlevel_handler

	 lowlevel_handler_207:
		push dword 0xdeadbeef
		push dword 207
		jmp midlevel_handler

	 lowlevel_handler_208:
		push dword 0xdeadbeef
		push dword 208
		jmp midlevel_handler

	 lowlevel_handler_209:
		push dword 0xdeadbeef
		push dword 209
		jmp midlevel_handler

	 lowlevel_handler_210:
		push dword 0xdeadbeef
		push dword 210
		jmp midlevel_handler

	 lowlevel_handler_211:
		push dword 0xdeadbeef
		push dword 211
		jmp midlevel_handler

	 lowlevel_handler_212:
		push dword 0xdeadbeef
		push dword 212
		jmp midlevel_handler

	 lowlevel_handler_213:
		push dword 0xdeadbeef
		push dword 213
		jmp midlevel_handler

	 lowlevel_handler_214:
		push dword 0xdeadbeef
		push dword 214
		jmp midlevel_handler

	 lowlevel_handler_215:
		push dword 0xdeadbeef
		push dword 215
		jmp midlevel_handler

	 lowlevel_handler_216:
		push dword 0xdeadbeef
		push dword 216
		jmp midlevel_handler

	 lowlevel_handler_217:
		push dword 0xdeadbeef
		push dword 217
		jmp midlevel_handler

	 lowlevel_handler_218:
		push dword 0xdeadbeef
		push dword 218
		jmp midlevel_handler

	 lowlevel_handler_219:
		push dword 0xdeadbeef
		push dword 219
		jmp midlevel_handler

	 lowlevel_handler_220:
		push dword 0xdeadbeef
		push dword 220
		jmp midlevel_handler

	 lowlevel_handler_221:
		push dword 0xdeadbeef
		push dword 221
		jmp midlevel_handler

	 lowlevel_handler_222:
		push dword 0xdeadbeef
		push dword 222
		jmp midlevel_handler

	 lowlevel_handler_223:
		push dword 0xdeadbeef
		push dword 223
		jmp midlevel_handler

	 lowlevel_handler_224:
		push dword 0xdeadbeef
		push dword 224
		jmp midlevel_handler

	 lowlevel_handler_225:
		push dword 0xdeadbeef
		push dword 225
		jmp midlevel_handler

	 lowlevel_handler_226:
		push dword 0xdeadbeef
		push dword 226
		jmp midlevel_handler

	 lowlevel_handler_227:
		push dword 0xdeadbeef
		push dword 227
		jmp midlevel_handler

	 lowlevel_handler_228:
		push dword 0xdeadbeef
		push dword 228
		jmp midlevel_handler

	 lowlevel_handler_229:
		push dword 0xdeadbeef
		push dword 229
		jmp midlevel_handler

	 lowlevel_handler_230:
		push dword 0xdeadbeef
		push dword 230
		jmp midlevel_handler

	 lowlevel_handler_231:
		push dword 0xdeadbeef
		push dword 231
		jmp midlevel_handler

	 lowlevel_handler_232:
		push dword 0xdeadbeef
		push dword 232
		jmp midlevel_handler

	 lowlevel_handler_233:
		push dword 0xdeadbeef
		push dword 233
		jmp midlevel_handler

	 lowlevel_handler_234:
		push dword 0xdeadbeef
		push dword 234
		jmp midlevel_handler

	 lowlevel_handler_235:
		push dword 0xdeadbeef
		push dword 235
		jmp midlevel_handler

	 lowlevel_handler_236:
		push dword 0xdeadbeef
		push dword 236
		jmp midlevel_handler

	 lowlevel_handler_237:
		push dword 0xdeadbeef
		push dword 237
		jmp midlevel_handler

	 lowlevel_handler_238:
		push dword 0xdeadbeef
		push dword 238
		jmp midlevel_handler

	 lowlevel_handler_239:
		push dword 0xdeadbeef
		push dword 239
		jmp midlevel_handler

	 lowlevel_handler_240:
		push dword 0xdeadbeef
		push dword 240
		jmp midlevel_handler

	 lowlevel_handler_241:
		push dword 0xdeadbeef
		push dword 241
		jmp midlevel_handler

	 lowlevel_handler_242:
		push dword 0xdeadbeef
		push dword 242
		jmp midlevel_handler

	 lowlevel_handler_243:
		push dword 0xdeadbeef
		push dword 243
		jmp midlevel_handler

	 lowlevel_handler_244:
		push dword 0xdeadbeef
		push dword 244
		jmp midlevel_handler

	 lowlevel_handler_245:
		push dword 0xdeadbeef
		push dword 245
		jmp midlevel_handler

	 lowlevel_handler_246:
		push dword 0xdeadbeef
		push dword 246
		jmp midlevel_handler

	 lowlevel_handler_247:
		push dword 0xdeadbeef
		push dword 247
		jmp midlevel_handler

	 lowlevel_handler_248:
		push dword 0xdeadbeef
		push dword 248
		jmp midlevel_handler

	 lowlevel_handler_249:
		push dword 0xdeadbeef
		push dword 249
		jmp midlevel_handler

	 lowlevel_handler_250:
		push dword 0xdeadbeef
		push dword 250
		jmp midlevel_handler

	 lowlevel_handler_251:
		push dword 0xdeadbeef
		push dword 251
		jmp midlevel_handler

	 lowlevel_handler_252:
		push dword 0xdeadbeef
		push dword 252
		jmp midlevel_handler

	 lowlevel_handler_253:
		push dword 0xdeadbeef
		push dword 253
		jmp midlevel_handler

	 lowlevel_handler_254:
		push dword 0xdeadbeef
		push dword 254
		jmp midlevel_handler

	lowlevel_handler_255:
		push dword 0xdeadbeef
		push dword 255
		jmp midlevel_handler
	
	; initialize the interrupt table ;
	initIDT:
		mov ecx, interrupt_table
		mov eax, lowlevel_handler_0
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_1
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_2
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_3
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_4
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_5
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_6
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_7
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_8
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_9
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_10
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_11
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_12
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_13
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_14
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_15
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_16
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_17
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_18
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_19
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_20
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_21
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_22
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_23
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_24
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_25
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_26
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_27
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_28
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_29
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_30
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_31
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_32
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_33
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_34
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_35
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_36
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_37
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_38
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_39
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_40
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_41
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_42
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_43
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_44
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_45
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_46
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_47
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_48
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_49
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_50
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_51
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_52
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_53
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_54
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_55
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_56
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_57
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_58
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_59
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_60
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_61
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_62
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_63
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_64
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_65
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_66
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_67
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_68
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_69
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_70
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_71
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_72
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_73
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_74
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_75
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_76
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_77
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_78
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_79
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_80
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_81
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_82
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_83
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_84
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_85
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_86
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_87
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_88
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_89
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_90
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_91
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_92
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_93
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_94
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_95
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_96
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_97
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_98
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_99
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_100
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_101
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_102
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_103
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_104
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_105
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_106
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_107
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_108
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_109
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_110
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_111
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_112
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_113
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_114
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_115
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_116
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_117
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_118
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_119
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_120
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_121
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_122
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_123
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_124
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_125
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_126
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_127
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_128
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_129
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_130
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_131
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_132
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_133
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_134
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_135
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_136
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_137
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_138
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_139
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_140
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_141
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_142
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_143
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_144
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_145
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_146
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_147
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_148
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_149
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_150
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_151
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_152
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_153
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_154
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_155
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_156
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_157
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_158
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_159
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_160
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_161
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_162
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_163
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_164
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_165
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_166
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_167
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_168
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_169
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_170
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_171
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_172
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_173
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_174
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_175
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_176
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_177
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_178
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_179
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_180
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_181
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_182
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_183
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_184
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_185
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_186
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_187
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_188
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_189
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_190
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_191
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_192
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_193
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_194
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_195
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_196
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_197
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_198
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_199
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_200
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_201
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_202
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_203
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_204
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_205
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_206
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_207
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_208
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_209
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_210
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_211
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_212
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_213
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_214
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_215
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_216
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_217
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_218
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_219
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_220
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_221
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_222
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_223
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_224
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_225
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_226
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_227
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_228
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_229
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_230
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_231
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_232
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_233
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_234
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_235
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_236
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_237
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_238
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_239
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_240
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_241
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_242
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_243
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_244
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_245
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_246
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_247
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_248
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_249
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_250
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_251
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_252
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_253
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_254
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov eax, lowlevel_handler_255
		mov [ecx], ax
		shr eax, 16
		mov [ecx+6], ax
		add ecx, 8
		
		mov dword [idtloc+2], interrupt_table
		mov eax, idtloc
		lidt [eax]
		ret
	
;///////////////////////////////////////////;