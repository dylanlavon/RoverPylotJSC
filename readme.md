# RoverPylotJSC
This program allows users to control the Brookstone Rover 2.0 from their PC.

![rover](https://user-images.githubusercontent.com/44561221/169404097-fadc85a7-acec-4d48-b8c7-b232264bc758.jpg)

# Start the program with the ps3rover20.py script.


### Interpreter
Since the base repo for this project is quite old and out of use, Python 2.7 must be used.
[Python 2.7](https://www.python.org/download/releases/2.7/)


### Requisite Plug-Ins
RoverPylot requires pygame, numpy, and opencv-python. 
I would recommend following this tutorial here for installing Python2.7 and pip: https://www.youtube.com/watch?v=lpKJHUPTjmk
Additionally, to install opencv, you will need to run the following command: python -m pip install opencv-python==4.2.0.32

Then install pip in the folder in the Python 2.7 path: `Python27\Scripts\`.

Use "pip i" to install 'pygame,' 'numpy,' and 'opencv-python' using PyPi.
 

RoverPylot
==========

Pilot the Brookstone Rover 2.0 from Python

<h2>Instructions</h2>

This repository contains a Python API and demo
program allowing you to control the Brookstone 
<a href="http://www.amazon.com/Rover-2-0-App-Controlled-Wireless-Tank/dp/B0093285XK">
Rover 2.0 spy tank</a> from your laptop or PC. To get started, you should
get hold of a 
Rover 2.0 and install the repository
(<b>sudo python setup.py install</b> for Linux users), as well as
<a href="http://pygame.org/news.html">PyGame</a> and <a href="http://opencv.org/">OpenCV</a> for Python
Join the Rover's ad-hoc wifi network from your computer.
Then run the <b>ps3rover20.py</b> script from the repository.  This script will
allow you to drive the Rover around and watch its streaming video, as shown
<a href="http://www.youtube.com/watch?v=AsRleC1ediU">here</a>.  


Once you're up and running with the <b>ps3rover.py</b> script, look at its 
source code (and run pydoc on <b>rover.py</b>) to see how RoverPylot works and
how you can modify it to do other interesting things.
<a href="http://isgroupblog.blogspot.com/2013/09/how-i-hacked-brookstone-rover-20.html">
This blog post</a> explains how I hacked the Rover 2.0, and 
<a href="http://mas802.wordpress.com/2014/04/01/brookstone-rover-2-0-skype-client/">
this blog post</a> shows a clever application using Skype.


<h2>Known issues</h2>

<ol>

<li> The  <b>ps3rover20.py</b> script will report a harmless error about extraneous bytes in the JPEG image.
<p>
<li> The  <b>ps3revolution.py</b> script will often show a blurred/smudged image. This happens because, whereas
the Rover 2.0 sends JPEG images, the Revolution sends <a href="http://en.wikipedia.org/wiki/H.264/MPEG-4_AVC">H.264 video</a>.
I couldn't find a Python package for decoding and displaying H.264 on the fly, so I wrote little workaround that 
saves the video to a temporary file, which
from which the script then reads.  You can tweak the performance of this setup by playing with the <tt>FRAMERATE</tt>
and <tt>DELAY_SEC</tt> parameters at the top of the script.
<li> The camera tends to get stuck when trying to pan up, likely just due to old hardware.
<li> If you are having issues with dropped connection or cannot find the ad hoc network after turning on the rover, try replacing the batteries.
<li> As of now, the rover is still quite sluggish in terms of response time. Don't be suprised if the rover doesn't move consistently. 
</ol>



<h2>Copyright and licensing</h2>

Copyright and licensing information can be found in the header of each source file. 
Please <a href="mailto:simon.d.levy@gmail.com">contact</a> the original author with any questions or 
suggestions."# RoverPylotJSC" 
 
<h3>Credits</h3>
Original Author - <a href="https://github.com/simondlevy/RoverPylot/">simondlevy</a>

Modification and Further Development - JSC Spring Interns <a href="https://www.linkedin.com/in/dylan-britain-962046167/">Dylan Britain</a> and <a href="https://www.linkedin.com/in/mugdha-bhagavatula/">Mugdha Bhagavatula</a>
