#include <Windows.h>

#include "pixels.h"

size_t pixel_start = 0;
size_t old_jmps[WIDTH][HEIGHT] = { 0 };

int frame_no = 0;

void init_image() {

	image();

	DWORD dummy;
	VirtualProtect((LPVOID)pixel_start, IMAGE_SIZE, PAGE_EXECUTE_READWRITE, &dummy);
	size_t loc = pixel_start + LONG_INST_SIZE + BLOCK_SIZE + 1;

	for (int j = 0; j < WIDTH; j++) {
		for (int i = 0; i < HEIGHT; i++) {
			old_jmps[j][i] = *(size_t*)loc;
			loc += PIXEL_SIZE;
		}
	}
}

void change_pixel(unsigned int x, unsigned int y, unsigned char val) {

	size_t loc = pixel_start + PIXEL_SIZE * (x * HEIGHT + y) + LONG_INST_SIZE;

	for (int j = 0; j < PIXEL_SIZE - LONG_INST_SIZE; ++j)
		((char*)(loc + j))[0] = 0xCC;
	for (int j = 0; j < val; ++j)
		((char*)(loc + j))[0] = 0x90;

	int addr = old_jmps[x][y];
	((char*)loc + val)[0] = 0xE9;
	((size_t*)(loc + val + 1))[0] = addr + BLOCK_SIZE - val;

	/* Both approaches requires IDA to refresh graph. Above is cleaner
	
	size_t loc = pixel_start + PIXEL_SIZE * (x * HEIGHT + y);
	val = BLOCK_SIZE - val - 1;

	for (int j=0; j < LONG_INST_SIZE + BLOCK_SIZE; ++j)
		((char*)(loc + j))[0] = 0xCC;
	for (int j = val; j < val + LONG_INST_SIZE; ++j)
		((char*)(loc + j))[0] = ((char*)(pixel_start + j - val))[0];
	for (int j=LONG_INST_SIZE + val; j < LONG_INST_SIZE + BLOCK_SIZE; ++j)
		((char*)(loc + j))[0] = 0x90;

	loc -= 5;
	((size_t*)loc)[0] = old_jmps[x][y-1] + val;
	*/
}

void next_frame() {
	FRAME* f = &movie[frame_no];
	char* diff = f->diffs;

	for (int j = 0; j < f->n_diff; ++j)
		change_pixel(diff[3 * j], diff[3 * j + 1], diff[3 * j + 2]);

	frame_no += 1;
}