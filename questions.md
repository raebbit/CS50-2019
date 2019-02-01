# Questions

## What's `stdint.h`?

The `stdint.h` include file declares sets of integer types that have specified widths and defines corresponding sets of macros. It also defines macros that specify limits of integer types corresponding to the types defined in other standard include files.

## What's the point of using `uint8_t`, `uint32_t`, `int32_t`, and `uint16_t` in a program?

It makes clear that you use data for specific purpose and size. 

## How many bytes is a `BYTE`, a `DWORD`, a `LONG`, and a `WORD`, respectively?

`BYTE` is 1 byte, `DWORD` is 4 bytes, `LONG` is 4 bytes and `WORD` is 2 bytes.

## What (in ASCII, decimal, or hexadecimal) must the first two bytes of any BMP file be? Leading bytes used to identify file formats (with high probability) are generally called "magic numbers."

The first 2 bytes of BMP file format are **BM** in ASCII and `0x42``0x4D` in hexadecimal.

## What's the difference between `bfSize` and `biSize`?

`bfSize` is contained in `BITMAPFILEHEADER` and `biSize` is contained in `BITMAPINFOHEADER`.

## What does it mean if `biHeight` is negative?

If `biHeight` is negative, the bitmap is top-down DIB and its origin is upper-left corner.

## What field in `BITMAPINFOHEADER` specifies the BMP's color depth (i.e., bits per pixel)?

`biBitCount`

## Why might `fopen` return `NULL` in lines 24 and 32 of `copy.c`?

There might be no argument value, in other word, the user might forget to prompt the arguments.

## Why is the third argument to `fread` always `1` in our code? (For example, see lines 40, 44, and 75.)

The third argument is the number of elements. Our code `fread`s one element.

## What value does line 63 of `copy.c` assign to `padding` if `bi.biWidth` is `3`?

3

## What does `fseek` do?

`fseek` function is used to move file position to a desired location within the file.

## What is `SEEK_CUR`?

`SEEK_CUR` indicates the current position of the file pointer.
