import wave             # Helps save audio as .wav
import struct           # Helps save audio as .wav
import numpy as np      # Gives sine functions and pi
from PIL import Image   # Helps extract pixel information from images
from tqdm import tqdm   # Progress bar


def receive_image_give_freqs (image_name):
    # This function inputs an image file, then outputs frequency triplets to be used with write_3_note_chords.

    # [v] Get pixel information as an ordinary sequence.
    im = Image.open(image_name)
    im_pixels = list(im.getdata())  # im_pixels is an ordinary sequence containing pixel data, including alpha values.
    #im_pixels = im.getdata(band=None)
    #print(len(im_pixels))  # Just a debugging flag.

    # [v] Convert the ordinary sequence of pixel information to a format that can be input into write_3_note_chords.
    freq_triplets_list = []
    print("\nTurning list of list of subpixels into list of list of frequencies (Hz).")
    for pixel in im_pixels:
        freq_triplets_list.append([27.3725*pixel[0] + 20, 27.3725*pixel[1] + 20, 27.3725*pixel[2] + 20])
    return freq_triplets_list


def write_3_note_chords(freq_triplets_list, decay_flag):
    # This function inputs all frequencies for the entire image, then outputs a single wav made from the entire image.
    # decay_flag indicates how each chord should decay (grow quieter) over time.

    sampling_rate = 48000
    samples_per_chord = 2400
    amp = 20000

    x = np.arange(samples_per_chord)
    y = []

    # [v] Write the whole song into y
    print("\nWriting waveform with Numpy")
    for freq_triplet in freq_triplets_list:
        if decay_flag == "no_decay":
            y.extend((1)*(amp*(np.sin(2*np.pi*freq_triplet[0]*x/sampling_rate)+np.sin(2*np.pi*freq_triplet[1]*x/sampling_rate)+np.sin(2*np.pi*freq_triplet[2]*x/sampling_rate))))
        elif decay_flag == "linear_decay":
            y.extend((1 - x/samples_per_chord)*(amp*(np.sin(2*np.pi*freq_triplet[0]*x/sampling_rate)+np.sin(2*np.pi*freq_triplet[1]*x/sampling_rate)+np.sin(2*np.pi*freq_triplet[2]*x/sampling_rate))))
        else:
            print("Invalid input for decay_flag")
            return

    # [v] Plotting the wave to make sure it's correct.
    #plt.plot(np.arange(len(y)), y)
    #plt.show()  # Looks beautiful.

    # [v] Convert to .wav.
    test_wave = wave.open("newwave.wav", "wb")
    nchannels = 1
    sampwidth = 2
    framerate = int(sampling_rate)
    nframes = samples_per_chord
    comptype = "NONE"
    compname = "not compressed"
    test_wave.setparams((nchannels, sampwidth, framerate, nframes, comptype, compname))
    #test_wave.writeframes(y)       # Doesn't work.  Why?

    counter = 0
    y_length = len(y)
    print("\nExporting to .wav")
    for ii in tqdm(y):
        test_wave.writeframes(struct.pack('h', int(ii/2)))

    test_wave.close()



freqs_from_image = receive_image_give_freqs("1_cropped.png")
write_3_note_chords(freqs_from_image, "linear_decay")
