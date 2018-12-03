# **pxlTextGenerator**  *v0.0.1 - Alpha*
-----------------------------------
### **A PyQt Text to Handwriting Generator.**

Writen with Python 2.7 and PyQt 4

This tool is designed to allow users to gather hand written characters,
  (Or I guess, any connected mass)
  In photos and export them to an image library.
A database is built so later iterations of this tool can take the exported
  characters and use them to convert typed text into an image that is seemingly hand written.
Currently, You can save out hand written characters into individual PNG files with options
   to modify the alpha fall off from the dynamically built mask of the ink.
Since I have an intended purpose for this, it is expecting white/tan/beige paper and dark ink.
Being that, the color threshold will tell the script to select only neighboring pixels of color
   darker than the designated magnitude of brightness set.
   
The long term goal is to adapt this to be more of an OCR for many books I've written that other's have failed on.
To actually train the system, where it builds vectors and quadratic curves to make assumptions
  for what characters are what.
It is slow right now, but hoping to expand this out toward OpenGL or C++ in the future.
Python and PyQt was just the easy route to start with.

______________________________

### Thanks for checking out pxlTextGenerator!

