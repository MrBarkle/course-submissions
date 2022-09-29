// Modifies the volume of an audio file

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

// Number of bytes in .wav header
const int HEADER_SIZE = 44;
typedef int16_t SAMPLE;

int main(int argc, char *argv[])
{
    // Check command-line arguments
    if (argc != 4)
    {
        printf("Usage: ./volume input.wav output.wav factor\n");
        return 1;
    }

    // Open files and determine scaling factor
    FILE *input = fopen(argv[1], "r");
    if (input == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }

    FILE *output = fopen(argv[2], "w");
    if (output == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }

    float factor = atof(argv[3]);

    uint8_t header[HEADER_SIZE];
    // Read first 44 bytes of input file (the header)
    fread(header, sizeof(uint8_t), HEADER_SIZE, input);
    
    // Write first 44 bytes of input to output    
    fwrite(header, sizeof(uint8_t), HEADER_SIZE, output);
    
    
    SAMPLE buffer;
    // Read in samples and write them as multiples of factor
    while (fread(&buffer, sizeof(SAMPLE), 1, input))
    {
        buffer *= factor;
        fwrite(&buffer, sizeof(SAMPLE), 1, output);
    }

    // Close files
    fclose(input);
    fclose(output);
}
