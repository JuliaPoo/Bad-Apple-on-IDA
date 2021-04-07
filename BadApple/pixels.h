#include "gen/image.h"

void init_image(void);
void image(void);
void change_pixel(unsigned int x, unsigned int y, unsigned char val);
void next_frame(void);

extern size_t pixel_start;

#define _n _asm nop

#define HEADER \
	_asm xor edi,edi	\
	_asm xor esi,esi	\
	_asm xor eax,eax	\
	_asm int 3			\

#define TAIL \
	_asm xor edi,edi \
	;return

#define LONG_INST _asm vfmaddsub132ps xmm0, xmm1, xmmword ptr cs:[edi+esi*4+image]
#define LONG_INST_SIZE 11

#define BLOCK_SIZE 23
#define BLOCK \
	_n _n _n _n _n _n _n _n _n _n _n _n _n _n _n _n _n _n _n _n _n _n _n //_n _n _n

#define PIXEL_LABEL(x,y) pixel_##x##_##y##_
#define PIXEL(dest) LONG_INST \
	BLOCK \
	__asm jmp dword ptr dest \
	__asm int 3
#define PIXEL_SIZE (LONG_INST_SIZE+BLOCK_SIZE+5+1)

#define IMAGE_SIZE (PIXEL_SIZE*HEIGHT*WIDTH)

typedef struct {
	int n_diff;
	char* diffs;
}FRAME;

extern int n_frames;
extern FRAME movie[];