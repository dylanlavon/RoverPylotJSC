# RoverPylotJSC
This program allows users to control the Brookstone Rover 2.0 from their PC.

![rover](https://user-images.githubusercontent.com/44561221/169404097-fadc85a7-acec-4d48-b8c7-b232264bc758.jpg)

# Start the program with the ps3rover20.py script.


### Interpreter
Since the base repo for this project is quite old and out of use, Python 2.7 must be used.
[Python 2.7](https://www.python.org/download/releases/2.7/)


### Requisite Plug-Ins
RoverPylot requires pygame, numpy, and opencv-python. 
I would recommend following this tutorial here for installing Python2.7 and <a href="https://www.youtube.com/watch?v=lpKJHUPTjmk">pip:<a> 
Additionally, to install opencv, you will need to run the following command: python -m pip install opencv-python==4.2.0.32

Then install pip in the folder in the Python 2.7 path: `Python27\Scripts\`.

Use "pip i" to install 'pygame,' 'numpy,' and 'opencv-python' using PyPi.

### Running the Application
<ol>
<li>Once the plugins are all situated, begin by connecting to the rover's ad hoc network created after turning on the rover. 
<li>Next, open the <b>ps3rover.py</b> script, and verify or edit your control settings.
<li>You can launch the application and begin controlling your rover by running the <b>ps3rover.py</b> script.
</ol>

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

 
<h2>Credits</h2>
<b>Original Author -</b> <a href="https://github.com/simondlevy/RoverPylot/">simondlevy</a>

<b>Modification and Further Development -</b> JSC Spring 2022 Interns <a href="https://www.linkedin.com/in/dylan-britain-962046167/">Dylan Britain</a> and <a href="https://www.linkedin.com/in/mugdha-bhagavatula/">Mugdha Bhagavatula</a>

 <h3>Copyright and Licensing</h3>

Copyright and licensing information can be found in the header of each source file. 
