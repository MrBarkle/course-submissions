#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

const int BLOCK_SIZE = 512;
typedef uint8_t BYTE;

int main(int argc, char *argv[])
{
    // Check command-line arguments
    if (argc != 2)
    {
        printf("Usage: ./recover image\n");
        return 1;
    }
    // Open file
    FILE *file = fopen(argv[1], "r");
    if (file == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }
    
    // Create buffer array of 512 Byte block sizes 
    BYTE buffer[BLOCK_SIZE];
    // Keep track of JPEG images found
    int count = 0;
    // Make buffer for filename
    char filename[8];
    // Define first JPEG file to write to later
    sprintf(filename, "%03i.jpg", count);
    // Open first new JPEG file
    FILE *img = fopen(filename, "w");
    
    // Keep reading from image file in 512 Byte blocks, store them in buffer:
    while (fread(buffer, sizeof(BYTE), BLOCK_SIZE, file) == BLOCK_SIZE)
    {
        // If this block is the start of a new JPEG
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            // If this is the first JPEG
            if (count == 0)
            {
                // Write header signature to first JPEG file
                fwrite(buffer, sizeof(BYTE), 4, img);
                
                // Increase count after writing to file
                count ++;
                
                // Write all non-header bytes to first JPEG file one at a time
                fwrite(&buffer[4], sizeof(BYTE), BLOCK_SIZE - 4, img);
            }
            // Not first JPEG
            else
            {
                // Close previous file before opening a new one
                fclose(img);
                // Define new JPEG file name with newly increased count
                sprintf(filename, "%03i.jpg", count);
                // Open the new JPEG file
                img = fopen(filename, "w");
                
                // Write header signature to new JPEG file
                fwrite(buffer, sizeof(BYTE), 4, img);
                
                // Increase count after writing to file
                count ++;
                
                // Write all non-header bytes to new JPEG file one at a time
                fwrite(&buffer[4], sizeof(BYTE), BLOCK_SIZE - 4, img);
            }
        }
        // If this isn't the start of a new JPEG
        else
        {
            // If the start of the first JPEG has been found
            if (count != 0)
            {
                // Write all to open file
                fwrite(buffer, sizeof(buffer), 1, img);
            }
        }
    }
    // Close remining files
    fclose(file);
}