# Star Light

Star Light is a task management software designed to support students and family by tracking events and information for 
their school. 

This project was built for the 2023 FBLA Mobile Application Development.

Check out the ongoing project at https://github.com/DatBirbDude/App-Hopefully for releases and latest builds

# Getting Started

To get started with our app, we recommend that you install the newest version to your device from our releases page. 
Go to https://github.com/DatBirbDude/App-Hopefully/releases, and select the top and latest build. Send the file to your
android or IOS device and start the sideloading process accordingly.

==================== BUILDING FROM SOURCE ====================

If you wish to build from source due to any unforeseen compatibility issues, please clone our repo to your local 
computer. We have provided a configured 'buildozer.spec' file, which you should only alter if absolutely necessary.

We only offer build instructions for Android devices, IOS may be buildable but remains undocumented.

*Remember to clone shallowly if you only intend to build the app, not contribute to it*

Now create a virtual environment for the project: https://docs.python.org/3/library/venv.html

You will need to install >=python3.8 as well as the latest version of buildozer. 

Buildozer instructions: https://buildozer.readthedocs.io/en/latest/installation.html

Python instructions: https://wiki.python.org/moin/BeginnersGuide/Download

You will need all dependencies that both python and buildozer run on, including the pip package manager.

With pip, install certifi, Pillow, tqdm, typing-extensions, decorator, pycryptodomex, filelock, idna, requests, 
Pygments, platformdirs, imageio, charset-normalizer, pydantic, PySocks, kivymd, kivy, instagrapi, pybase62, docutils, 
requests-toolbelt, distlib, moviepy, Kivy-Garden, urllib3, numpy, kivy-deps.sdl2, distlib, kivy-deps.angle, 
kivy-deps.glew

Some packages may already be on your system.

run 'buildozer android debug'

**Warning: This may take a very long time depending on the speed of your system, do not halt the process**

**Warning: This will require the download of the majority of the Android development software, please set aside
sufficient storage before starting the build process**

If no errors arise, you can go the /bin directory of the project to retrieve your apk and send it to your device.
Buildozer also provides extensional commands to send it to your device directly after building.

# Support

If you find an internal issue or oversight within the app, please use the provided bug report system so that 
administrators can review it.

If you find a major bug or for any reason find yourself unable to use the reporting system, you can email us directly at
support@glitchtech.top

Due to the scale of our operation, we may be unable to provide additional instructions to building our app from source,
but we promise to try our best.

# License

Star Light is licensed under the MIT license.

Copyright © 2022-2023 Glitch Technologies (Vincent Barilaro and Samuel Tibbs).

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.