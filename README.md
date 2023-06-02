# Adaptive Median Filter

The Adaptive Median Filter (AMF) is a digital image processing technique used to remove impulse noise, specifically salt and pepper noise, from images. Salt and pepper noise appears as randomly occurring white and black pixels scattered throughout the image, resembling grains of salt and pepper.

## Project Description
This project implements an Adaptive Median Filter with a graphical user interface (GUI). The algorithm dynamically adjusts the filter's size based on the noise level present in different regions of the image.

## Features
- Load an image file for processing.
- Add salt and pepper noise to the image with increasing probability.
- Apply the Adaptive Median Filter to remove noise.
- View the original image, noisy image, and filtered image side by side.
- Adjust filter parameters, such as filter size and noise detection threshold.


## Contributing
Contributions to this project are welcome. If you find any issues or have suggestions for improvement, please open an issue on the project repository. Additionally, you can fork the repository, make your changes, and submit a pull request.

## License
This project is licensed under the MIT License.

Make sure you have the following packages installed:
- PyQt5
- numpy
- OpenCV

If any of these packages are missing, you can install them using pip:

