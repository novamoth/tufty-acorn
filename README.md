# Acorn

Acorn is a premade MicroPython program for running on Tufty2040 Microcontrollers. It is intended to provide a semi-automatic badge setup for plural systems.

## How to Use

1. Download the entire repository as a ZIP file, and unzip
2. The program will come with placeholder data for a hypothetical system. Update system.json with information about your system, or export information from PluralKit (this does not include palette information)
3. Add your own JPG images that align with your own system. The program will check for the unique ID of the alter, and failing that, search for the name of the alter.
4. Push all files to the Tufty2040 via a program, such as Thonny. Refer to Pimoroni's "Getting Started" guide.
5. Start the Tufty2040. All necessary information should be obtained from system.json and loaded into the program.

## Q&A

> Can't it automatically obtain files from system.json?

The Tufty does not have internet access, and I don't want to do a whole desktop program.

> My images look "off".

The Tufty2040 uses a RGB332 color palette for JPEG rendering. Not all colors will be accessible. Where possible, it will attempt to "dither" the image, attempting to emulate the desired color from a distance. Up close, this may cause certain JPEG files to appear "speckled".

## License

[MIT](https://choosealicense.com/licenses/mit/)
