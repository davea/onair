CC=clang
CFLAGS=-framework Foundation -framework AVFoundation -framework CoreMediaIO

onair_helper: onair_helper.m
	$(CC) $(CFLAGS) onair_helper.m -o onair_helper

.PHONY: clean

clean:
	rm onair_helper
