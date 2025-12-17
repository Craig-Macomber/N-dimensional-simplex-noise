This project is a collection of scraps of code related to simplex noise. It was made for my own educational purposes, and is not packaged up for general reuse.

Kenneth Perlin, of Perlin Noise fame, filed a patent that seems related to this, US6867776 B2, which is now expired. While it was unclear how this code was impacted by the patent, it it no longer relevant and this codebase is now under the MIT license.

This project contains a few new ideas, modifications and extensions to previous works. Part of the generalization to N dimensions was by own design, and my gradient vector selection is very different. I derived the derivative math myself, but I assume it's identical. It is not a port of any existing code: it was simply inspired by a few different versions (none of which were n-dimensional).

The `simplex.py` file contain a SimplexNoise class with a simplexNoise function. It samples n-dimensional simplex noise!

`texMaker` is an example of its use to make 3D smooth noise textures, and save them as images.

`noisetest` does some performance testing of various dimensions.

`ray.py` is a ray marching based renderer of surfaces made from 3D simplex noise on the GPU. It may fail to run on most computers due to shader compatibility issues.
