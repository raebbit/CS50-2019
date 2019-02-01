// resizes a BMP file

#include <stdio.h>
#include <stdlib.h>

#include "bmp.h"

int main(int argc, char *argv[])
{
    // ensure proper usage
    if (argc != 4)
    {
        fprintf(stderr, "Usage: f infile outfile\n");
        return 1;
    }

    //remember the factor
    float f = atof(argv[1]);

    // check the range of f
    if (f <= 0.0 || f > 100.0)
    {
        fprintf(stderr, "The factor must be a floating-point value in (0.0, 100.0].\n");
        return 2;
    }

    // remember filenames
    char *infile = argv[2];
    char *outfile = argv[3];

    // open input file
    FILE *inptr = fopen(infile, "r");
    if (inptr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", infile);
        return 3;
    }

    // open output file
    FILE *outptr = fopen(outfile, "w");
    if (outptr == NULL)
    {
        fclose(inptr);
        fprintf(stderr, "Could not create %s.\n", outfile);
        return 4;
    }

    // read infile's BITMAPFILEHEADER
    BITMAPFILEHEADER bf;
    fread(&bf, sizeof(BITMAPFILEHEADER), 1, inptr);

    // read infile's BITMAPINFOHEADER
    BITMAPINFOHEADER bi;
    fread(&bi, sizeof(BITMAPINFOHEADER), 1, inptr);

    // ensure infile is (likely) a 24-bit uncompressed BMP 4.0
    if (bf.bfType != 0x4d42 || bf.bfOffBits != 54 || bi.biSize != 40 ||
        bi.biBitCount != 24 || bi.biCompression != 0)
    {
        fclose(outptr);
        fclose(inptr);
        fprintf(stderr, "Unsupported file format.\n");
        return 5;
    }

    // initialize the new header file
    BITMAPFILEHEADER new_bf;
    BITMAPINFOHEADER new_bi;
    new_bf = bf;
    new_bi = bi;

    // set the new width and height
    new_bi.biWidth = bi.biWidth * f;
    new_bi.biHeight = bi.biHeight * f;

    // determine padding for scanlines
    int padding = (4 - (bi.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;
    int new_padding = (4 - (new_bi.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;

    // new image size
    new_bi.biSizeImage = ((sizeof(RGBTRIPLE) * new_bi.biWidth) + new_padding) * abs(new_bi.biHeight);
    new_bf.bfSize = new_bi.biSizeImage + sizeof(BITMAPFILEHEADER) + sizeof(BITMAPINFOHEADER);

    // write outfile's BITMAPFILEHEADER
    fwrite(&new_bf, sizeof(BITMAPFILEHEADER), 1, outptr);

    // write outfile's BITMAPINFOHEADER
    fwrite(&new_bi, sizeof(BITMAPINFOHEADER), 1, outptr);



    if (f >= 1.0) // if f is posstive int(same as resize/less)
    {
        // iterate over infile's scanlines
        for (int i = 0, biHeight = abs(bi.biHeight); i < biHeight; i++)
        {
            //re-copy method
            for (int k = 0; k < f; k++)
            {
                // iterate over pixels in scanline
                for (int j = 0; j < bi.biWidth; j++)
                {
                    // temporary storage
                    RGBTRIPLE triple;

                    // read RGB triple from infile
                    fread(&triple, sizeof(RGBTRIPLE), 1, inptr);

                    // write RGB triple to outfile
                    for (int r = 0; r < f; r++)
                    {
                        fwrite(&triple, sizeof(RGBTRIPLE), 1, outptr);
                    }
                }

                // skip over infile's padding
                fseek(inptr, padding, SEEK_CUR);

                // then add ourfile's padding
                for (int m = 0; m < new_padding; m++)
                {
                    fputc(0x00, outptr);
                }

                //send infile cursor back
                if (k < f - 1)
                {
                    long offset = (bi.biWidth * sizeof(RGBTRIPLE)) + padding;
                    fseek(inptr, - offset, SEEK_CUR);
                }
            }
        }
    }
    else if (f < 1.0) // f is 0.5, reduce the size , actually it only works when f is 0.5
    {
        // iterate over every other infile's scanlines
        for (int i = 0, new_biHeight = abs(new_bi.biHeight); i < new_biHeight; i++)
        {
            // iterate over every other pixels in scanline
            for (int j = 0; j < new_bi.biWidth; j++)
            {
                // temporary storage
                RGBTRIPLE triple;

                // read RGB triple from infile
                fread(&triple, sizeof(RGBTRIPLE), 1, inptr);

                // write RGB triple to outfile
                fwrite(&triple, sizeof(RGBTRIPLE), 1, outptr);

                // move cursor to every other pixel
                fseek(inptr, 3, SEEK_CUR);
            }
            // skip over infile's padding
            fseek(inptr, padding, SEEK_CUR);

            // then add ourfile's padding
            for (int m = 0; m < new_padding; m++)
            {
                fputc(0x00, outptr);
            }

            // send cursor to every other row
            long offset = (bi.biWidth * sizeof(RGBTRIPLE)) + padding;
            fseek(inptr, offset, SEEK_CUR);
        }
    }

    // close infile
    fclose(inptr);

    // close outfile
    fclose(outptr);

    // success
    return 0;
}
