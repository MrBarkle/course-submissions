#include "helpers.h"
#include "math.h"
#include "stdio.h"
#include "string.h"

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    double red;
    double blue;
    double green;
    int average;
    
    // Loop through each pixel
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // Get RGB values
            red = image[i][j].rgbtRed;
            blue = image[i][j].rgbtBlue;
            green = image[i][j].rgbtGreen;

            // Average RGB values
            average = (int)round((red + blue + green) / 3.0);
            
            // Set new greyscaled RGB values
            image[i][j].rgbtRed = average;
            image[i][j].rgbtBlue = average;
            image[i][j].rgbtGreen = average;
        }
    }
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    // Loop through each pixel
    for (int i = 0; i < height; i ++)
    {
        RGBTRIPLE temp;
        int j = 0;
        int k = width - 1;

        // Reflect pixels horizontally by reversing the array values on each row
        while (j < k)
        {
            temp = image[i][j];
            image[i][j] = image[i][k];
            image[i][k] = temp;
            j ++;
            k --;
        }
    }
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    // Create temporary 2D pixel array
    RGBTRIPLE temp[height][width];
    // Copy image to temp. Changes will be made to image based off temp
    memcpy(temp, image, sizeof(temp));

    // Loop through each pixel
    for (int i = 0; i < height; i ++)
    {
        for (int j = 0; j < width; j ++)
        {
            int sumR = 0;
            int sumB = 0;
            int sumG = 0;
            int averageR;
            int averageB;
            int averageG;
            double counter = 1.0;

            // Look at main pixel (i, j)
            sumR += temp[i][j].rgbtRed;
            sumB += temp[i][j].rgbtBlue;
            sumG += temp[i][j].rgbtGreen;

            // Look for (i - 1, j - 1) if it exists
            if (i - 1 >= 0 && j - 1 >= 0)
            {
                sumR += temp[i - 1][j - 1].rgbtRed;
                sumB += temp[i - 1][j - 1].rgbtBlue;
                sumG += temp[i - 1][j - 1].rgbtGreen;
                counter ++;
            }
            // Look for (i + 1, j + 1) if it exists
            if (i + 1 < height && j + 1 < width)
            {
                sumR += temp[i + 1][j + 1].rgbtRed;
                sumB += temp[i + 1][j + 1].rgbtBlue;
                sumG += temp[i + 1][j + 1].rgbtGreen;
                counter ++;
            }
            // Look for (i + 1, j - 1) if it exists
            if (i + 1 < height && j - 1 >= 0)
            {
                sumR += temp[i + 1][j - 1].rgbtRed;
                sumB += temp[i + 1][j - 1].rgbtBlue;
                sumG += temp[i + 1][j - 1].rgbtGreen;
                counter ++;
            }
            // Look for (i - 1, j + 1) if it exists
            if (i - 1 >= 0 && j + 1 < width)
            {
                sumR += temp[i - 1][j + 1].rgbtRed;
                sumB += temp[i - 1][j + 1].rgbtBlue;
                sumG += temp[i - 1][j + 1].rgbtGreen;
                counter ++;
            }
            // Look for (i - 1, j) if it exists
            if (i - 1 >= 0)
            {
                sumR += temp[i - 1][j].rgbtRed;
                sumB += temp[i - 1][j].rgbtBlue;
                sumG += temp[i - 1][j].rgbtGreen;
                counter ++;
            }
            // Look for (i + 1, j) if it exists
            if (i + 1 < height)
            {
                sumR += temp[i + 1][j].rgbtRed;
                sumB += temp[i + 1][j].rgbtBlue;
                sumG += temp[i + 1][j].rgbtGreen;
                counter ++;
            }
            // Look for (i, j - 1) if it exists
            if (j - 1 >= 0)
            {
                sumR += temp[i][j - 1].rgbtRed;
                sumB += temp[i][j - 1].rgbtBlue;
                sumG += temp[i][j - 1].rgbtGreen;
                counter ++;
            }
            // Look for (i, j + 1) if it exists
            if (j + 1 < width)
            {
                sumR += temp[i][j + 1].rgbtRed;
                sumB += temp[i][j + 1].rgbtBlue;
                sumG += temp[i][j + 1].rgbtGreen;
                counter ++;
            }

            // Calculate averages for each color value
            averageR = (int)round(sumR / counter);
            averageB = (int)round(sumB / counter);
            averageG = (int)round(sumG / counter);

            // Set new color values in original image
            image[i][j].rgbtRed = averageR;
            image[i][j].rgbtBlue = averageB;
            image[i][j].rgbtGreen = averageG;
        }
    }
}

// Detect edges
void edges(int height, int width, RGBTRIPLE image[height][width])
{

    // Create temporary 2D pixel array
    RGBTRIPLE temp[height][width];
    // Copy image to temp. Changes will be made to image based off temp
    memcpy(temp, image, sizeof(temp));

    // Loop through each pixel
    for (int i = 0; i < height; i ++)
    {
        for (int j = 0; j < width; j ++)
        {
            int Gx_sumR = 0;
            int Gx_sumB = 0;
            int Gx_sumG = 0;
            
            int Gy_sumR = 0;
            int Gy_sumB = 0;
            int Gy_sumG = 0;

            int r;
            int b;
            int g;
            
            // Look for (i - 1, j - 1) if it exists
            if (i - 1 >= 0 && j - 1 >= 0)
            {
                Gx_sumR = Gx_sumR - temp[i - 1][j - 1].rgbtRed;
                Gx_sumB = Gx_sumB - temp[i - 1][j - 1].rgbtBlue;
                Gx_sumG = Gx_sumG - temp[i - 1][j - 1].rgbtGreen;
                Gy_sumR = Gy_sumR - temp[i - 1][j - 1].rgbtRed;
                Gy_sumB = Gy_sumB - temp[i - 1][j - 1].rgbtBlue;
                Gy_sumG = Gy_sumG - temp[i - 1][j - 1].rgbtGreen;
            }
            // Look for (i + 1, j + 1) if it exists
            if (i + 1 < height && j + 1 < width)
            {
                Gx_sumR = Gx_sumR + temp[i + 1][j + 1].rgbtRed;
                Gx_sumB = Gx_sumB + temp[i + 1][j + 1].rgbtBlue;
                Gx_sumG = Gx_sumG + temp[i + 1][j + 1].rgbtGreen;
                Gy_sumR = Gy_sumR + temp[i + 1][j + 1].rgbtRed;
                Gy_sumB = Gy_sumB + temp[i + 1][j + 1].rgbtBlue;
                Gy_sumG = Gy_sumG + temp[i + 1][j + 1].rgbtGreen;
            }
            // Look for (i + 1, j - 1) if it exists
            if (i + 1 < height && j - 1 >= 0)
            {
                Gx_sumR = Gx_sumR - temp[i + 1][j - 1].rgbtRed;
                Gx_sumB = Gx_sumB - temp[i + 1][j - 1].rgbtBlue;
                Gx_sumG = Gx_sumG - temp[i + 1][j - 1].rgbtGreen;
                Gy_sumR = Gy_sumR + temp[i + 1][j - 1].rgbtRed;
                Gy_sumB = Gy_sumB + temp[i + 1][j - 1].rgbtBlue;
                Gy_sumG = Gy_sumG + temp[i + 1][j - 1].rgbtGreen;
            }
            // Look for (i - 1, j + 1) if it exists
            if (i - 1 >= 0 && j + 1 < width)
            {
                Gx_sumR = Gx_sumR + temp[i - 1][j + 1].rgbtRed;
                Gx_sumB = Gx_sumB + temp[i - 1][j + 1].rgbtBlue;
                Gx_sumG = Gx_sumG + temp[i - 1][j + 1].rgbtGreen;
                Gy_sumR = Gy_sumR - temp[i - 1][j + 1].rgbtRed;
                Gy_sumB = Gy_sumB - temp[i - 1][j + 1].rgbtBlue;
                Gy_sumG = Gy_sumG - temp[i - 1][j + 1].rgbtGreen;
            }
            // Look for (i - 1, j) if it exists
            if (i - 1 >= 0)
            {
                Gy_sumR = Gy_sumR - (2 * (temp[i - 1][j].rgbtRed));
                Gy_sumB = Gy_sumB - (2 * (temp[i - 1][j].rgbtBlue));
                Gy_sumG = Gy_sumG - (2 * (temp[i - 1][j].rgbtGreen));
            }
            // Look for (i + 1, j) if it exists
            if (i + 1 < height)
            {
                Gy_sumR = Gy_sumR + (2 * (temp[i + 1][j].rgbtRed));
                Gy_sumB = Gy_sumB + (2 * (temp[i + 1][j].rgbtBlue));
                Gy_sumG = Gy_sumG + (2 * (temp[i + 1][j].rgbtGreen));
            }
            // Look for (i, j - 1) if it exists
            if (j - 1 >= 0)
            {
                Gx_sumR = Gx_sumR - (2 * (temp[i][j - 1].rgbtRed));
                Gx_sumB = Gx_sumB - (2 * (temp[i][j - 1].rgbtBlue));
                Gx_sumG = Gx_sumG - (2 * (temp[i][j - 1].rgbtGreen));
            }
            // Look for (i, j + 1) if it exists
            if (j + 1 < width)
            {
                Gx_sumR = Gx_sumR + (2 * (temp[i][j + 1].rgbtRed));
                Gx_sumB = Gx_sumB + (2 * (temp[i][j + 1].rgbtBlue));
                Gx_sumG = Gx_sumG + (2 * (temp[i][j + 1].rgbtGreen));
            }
            
            // Calculate new values
            r = round(sqrt(pow(Gx_sumR, 2) + pow(Gy_sumR, 2)));
            b = round(sqrt(pow(Gx_sumB, 2) + pow(Gy_sumB, 2)));
            g = round(sqrt(pow(Gx_sumG, 2) + pow(Gy_sumG, 2)));

            // Set new color red values in original image
            if (r > 255)
            {
                image[i][j].rgbtRed = 255;
            }
            else 
            {
                image[i][j].rgbtRed = r;
            }
            // Set new color blue values in original image
            if (b > 255)
            {
                image[i][j].rgbtBlue = 255;
            }
            else 
            {
                image[i][j].rgbtBlue = b;
            }
            // Set new color green values in original image
            if (g > 255)
            {
                image[i][j].rgbtGreen = 255;
            }
            else 
            {
                image[i][j].rgbtGreen = g;
            }
        }
    }

}
