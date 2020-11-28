# image-to-audio-chords
Inputs an image, and outputs a wav file containing a song composed of 3-note chords, where each chord is determined from one pixel.

Current the project uses a linear mapping from RGB value to note frequency, with no quantization into any tonal scale.  As a result, the song is intentionally displeasing.  This could easily be changed by rounding each note to the nearest frequency on a particular scale.

## Requirement
This project has successfully been tested for Python >= 3.8.

## Install dependencies
wave  
numpy  
tqdm  
PIL
