#!/usr/bin/sh

rm results.md
python SimHash.py >> results.md
pandoc results.md --pdf-engine=lualatex -o results.pdf
