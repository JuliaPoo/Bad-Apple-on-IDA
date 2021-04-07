_cpp_template = """
#include "../pixels.h"

void image(void) {

	HEADER;
	unsigned int i;
	_asm mov i, eax;

	_asm pop ecx;
	_asm mov ecx, PIXEL_LABEL(1, 0);
	_asm mov pixel_start, ecx;

%s

%s

end:
	TAIL;
}
"""

_h_template = """
#define WIDTH %d
#define HEIGHT %d
"""

def _gen_switch_case(width:int):

	template = """
	switch (i) {\n%s
	}
	"""
	width += 1
	cases = []
	for i in range(width-1):
		cases.append("\tcase %d: _asm jmp dword ptr PIXEL_LABEL(%d, 0);"%(i, i))
	cases.append("\tdefault: _asm jmp dword ptr PIXEL_LABEL(%d, 0);"%(width-1))

	return template%"\n".join(cases)

def _gen_image_code(width:int, height:int):

	width += 1
	pixels = []
	for col_idx in range(width):
		for row_idx in range(height-1):
			pixels.append(
				"\tPIXEL_LABEL(%d, %d) : PIXEL(PIXEL_LABEL(%d, %d));"%(col_idx, row_idx, col_idx, row_idx+1)
			)
		pixels.append("\tPIXEL_LABEL(%d, %d) : PIXEL(end);\n"%(col_idx, height-1))
	
	return "\n".join(pixels)

def _gen_image(width:int, height:int):

	return _cpp_template%(
		_gen_switch_case(width),
		_gen_image_code(width, height)
	)

def gen(width:int, height:int):
	open("image.cpp", "w").write(_gen_image(width, height))
	open("image.h", "w").write(_h_template%(width, height))

if __name__ == "__main__":
	width, height = int(input("Width: ")), int(input("Height: "))
	gen(width, height)
	print("Wrote to `image.cpp` and `image.h`")
