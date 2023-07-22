import pygame
from pygame.locals import *

pygame.init()

scale = 4
width = 64
height = 32
screen = pygame.Surface((width, height))
window = pygame.display.set_mode((scale*width, scale*height))
pygame.display.set_caption("")

memory = [0 for i in range(0x1000)]
v = [0 for i in range (16)]
pc = 0x200
idx = 0x0000
stack = [0 for i in range(24)]
stackPointer = 0
keys = [0 for i in range(16)]

font = [ 
	0x60, 0xa0, 0xa0, 0xa0, 0xc0,
	0x40, 0xc0, 0x40, 0x40, 0xe0,
	0xc0, 0x20, 0x40, 0x80, 0xe0,
	0xc0, 0x20, 0x40, 0x20, 0xc0,
	0x20, 0xa0, 0xe0, 0x20, 0x20,
	0xe0, 0x80, 0xc0, 0x20, 0xc0,
	0x40, 0x80, 0xc0, 0xa0, 0x40,
	0xe0, 0x20, 0x60, 0x40, 0x40,
	0x40, 0xa0, 0x40, 0xa0, 0x40,
	0x40, 0xa0, 0x60, 0x20, 0x40,
	0x40, 0xa0, 0xe0, 0xa0, 0xa0,
	0xc0, 0xa0, 0xc0, 0xa0, 0xc0,
	0x60, 0x80, 0x80, 0x80, 0x60,
	0xc0, 0xa0, 0xa0, 0xa0, 0xc0,
	0xe0, 0x80, 0xc0, 0x80, 0xe0,
	0xe0, 0x80, 0xc0, 0x80, 0x80
]

for i in range(80):
    memory[i] = font[i]

def avanzarEmulacion():
    global pc
    global memory
    global idx
    global v
    global stack
    global stackPointer
    global keys

    opcode = (memory[pc] << 8) | memory[pc+1]
    pc = pc + 2
    # decode
    nibble1 = opcode >> 12
    nibble2 = (opcode >> 8) & 0xF
    nibble3 = (opcode >> 4) & 0xF
    nibble4 = opcode & 0xF

    address = opcode & 0xFFF

    byte2 = opcode & 0xFF

    if (nibble1 == 0x00):
        
        if (address == 0x0EE):
            pc = pop()

        if (address == 0x0E0):
            
            for x in range(width):
                for y in range(height):
                    screen.set_at((x, y), (0, 0, 0))

    if (nibble1 == 0x6):
        v[nibble2] = byte2

    if (nibble1 == 0x7):
        v[nibble2] = v[nibble2] + byte2

    if (nibble1 == 0xA):
        idx = address

    if (nibble1 == 0xD):
        v[0xF] = 0
        
        for y in range(nibble4):
            actual = memory[idx + y]
            for x in range(8):
                if (actual & (0x80)) != 0 and x + v[nibble2] < 64 and y + v[nibble3] < 32:
                    if screen.get_at((x + v[nibble2], y + v[nibble3])) != 0:
                        screen.set_at((x + v[nibble2], y + v[nibble3]), (255, 255, 0))
                        v[0xF] = 1
                    else:
                        screen.set_at((x + v[nibble2], y + v[nibble3]), (255, 255, 255))
                actual = actual << 1

    if (nibble1 == 0x1):
        pc = address

def push(valor): 
    stack[stackPointer] = valor
    stackPointer = stackPointer + 1 

def pop(valor):
    stackPointer = stackPointer - 1
    return stack[stackPointer]

delayTimer = 0
soundTimer = 0

with open("3-corax+.ch8", "rb") as file:
    buffer = bytearray(0xE00)
    file.readinto(buffer)

    for i in range(0xE00):
        memory[i+0x200] = buffer[i]

quit = False
while quit == False:
    for event in pygame.event.get():
        if event.type == QUIT:
            quit = True

    pressed = pygame.key.get_pressed()

    keys[0] = 1 if pressed[K_x] else 0
    keys[1] = 1 if pressed[K_1] else 0
    keys[2] = 1 if pressed[K_2] else 0
    keys[3] = 1 if pressed[K_3] else 0
    keys[4] = 1 if pressed[K_q] else 0
    keys[5] = 1 if pressed[K_w] else 0
    keys[6] = 1 if pressed[K_e] else 0
    keys[7] = 1 if pressed[K_a] else 0
    keys[8] = 1 if pressed[K_s] else 0
    keys[9] = 1 if pressed[K_d] else 0
    keys[10] = 1 if pressed[K_z] else 0
    keys[11] = 1 if pressed[K_c] else 0
    keys[12] = 1 if pressed[K_4] else 0
    keys[13] = 1 if pressed[K_r] else 0
    keys[14] = 1 if pressed[K_f] else 0
    keys[15] = 1 if pressed[K_v] else 0
    
    if delayTimer > 0:
        delayTimer = delayTimer - 1

    if soundTimer > 0:
        soundTimer = soundTimer - 1

    for i in range(8):
        avanzarEmulacion()

    window.blit(pygame.transform.scale(screen, (scale*width, scale*height)), (0, 0))

    pygame.display.flip()

pygame.quit()

##  > <