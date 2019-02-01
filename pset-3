#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

typedef uint8_t  BYTE;


int main(int argc, char *argv[])
{
    // ensure proper usage
    if (argc != 2)
    {
        fprintf(stderr, "Usage: ./recover image\n");
        return 1;
    }

    // open card file
    FILE *inptr = fopen(argv[1], "r");
    if (inptr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", argv[1]);
        return 2;
    }

    // making a new JPEG
    char filename[8];
    int filenumber = 0;  // to keep tracking the file

    FILE *img = NULL;

    BYTE buffer[512];

    // repeat until end of card
    while (fread(buffer, 512, 1, inptr) == 1)
    {
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0) // start of new JPEG? - yes
        {
            if (filenumber == 0 && img == NULL) //already found a JPEG? - no
            {
                sprintf(filename, "%03i.jpg", filenumber);
                img = fopen(filename, "w");
                fwrite(buffer, 512, 1, img);
            }
            else // already found a JPEG? - yes
            {
                fclose(img);
                filenumber++;
                sprintf(filename, "%03i.jpg", filenumber);
                img = fopen(filename, "w");
                fwrite(buffer, 512, 1, img);
            }
        }
        else // start of new JPEG? - no
        {
            if (filenumber > 0)
            {
                fwrite(buffer, 512, 1, img);
            }
            else if (filenumber == 0 && img != NULL)
            {
                fwrite(buffer, 512, 1, img);
            }
        }
    }

    // close infile
    fclose(inptr);

    // close outfile
    fclose(img);

    // success
    return 0;


}
