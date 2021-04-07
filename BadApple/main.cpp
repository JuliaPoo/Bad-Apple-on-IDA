#include "pixels.h"

int main() {

	init_image();

	for (int j = 0; j < n_frames; ++j) {
		next_frame();
		image();
	}
}