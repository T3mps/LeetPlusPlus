#!/bin/bash
# Build PDCurses for Linux
cd PDCurses/x11
./configure
make clean
make
echo "PDCurses for Linux built successfully!"