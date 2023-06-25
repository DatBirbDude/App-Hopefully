# Star Light

Star Light is a task management software designed to support students and family by tracking events and information for 
their school. 

This project was built for the 2023 FBLA Mobile Application Development.

Check out the ongoing project at https://github.com/DatBirbDude/App-Hopefully for releases and latest builds

# Getting Started

To get our app, we recommend that you install the newest stable version to your device from our releases page. 
Go to https://github.com/DatBirbDude/App-Hopefully/releases, and select the top and latest build. You will be greeted
with two options, one with cmd and one without. For most users, we recommend the one without, unless you are using an 
unsupported Windows version. Download the zip file to your computer and unzip it wherever you would like. Next, start 
the app by entering the new folder and clicking on starlight.exe. It will begin automatically.

We currently support Windows Vista, 7, 10, 11. Support for the Windows phone is experimental at this time.

If you have any issues installing the app, please see the **Support** section of the README

**==================== BUILDING FROM SOURCE ====================**

If you wish to build from source due to any unforeseen compatibility issues, please clone our repo 
(https://github.com/DatBirbDude/App-Hopefully) to your computer. We have provided a configured 'starlight.spec' file, 
which you should only alter to our instructions.

We only offer build instructions for Windows devices, Windows Phone may be buildable but remains undocumented.

*Remember to clone shallowly(use **git clone --depth 1 <url>**) if you only intend to build the app, not contribute to 
it*

You will need to install >=python3.8.
Python instructions: https://wiki.python.org/moin/BeginnersGuide/Download

Now create a virtual environment for the project: https://docs.python.org/3/library/venv.html

You will need all dependencies that both python and pyinstaller run on, including the pip package manager.

Run `python -m pip install PyInstaller certifi Pillow tqdm typing-extensions decorator pycryptodomex filelock idna requests 
Pygments platformdirs imageio charset-normalizer pydantic PySocks kivymd kivy instagrapi pybase62 docutils
requests-toolbelt distlib moviepy Kivy-Garden urllib3 numpy pywin32 pypiwin32`

**Warning: This may take a some time depending on the speed of your system and connection rate**

Some packages may already be on your system.

Create a new directory for the exported build.

**Move** `starlight.spec` from the source directory into the newly created one and open it in your text editor of 
choice.

Replace all instances of `PATH\\TO\\THE\\PROJECT\\` with the path to your **source** directory.

If you would like to keep the build as light as possible, it is safe to delete the following files/folders:
```
server
Calendar.ics
Any folder or file starting with "."
```

Now return to the new directory.

run `python -m PyInstaller starlight.spec`

**Warning: This may take a very long time depending on the speed of your system, do not halt the process**

If no errors arise, you can go the /dists directory of the new folder and find the folder named starlight. This and all
files contained within are responsible for running the app, you can launch it with the newly created starlight.exe 
inside

Note: If you would like to toggle the command line visibility, use the console flag (default="console=True") in the 
starlight.spec file

# Support

If you find an internal issue or oversight within the app, please use the provided bug report system so that 
administrators and developers can review it.

If you find a major bug or for any reason find yourself unable to use the reporting system, you can email us directly at
support@glitchtech.top

Due to the scale of our operation, we may be unable to provide additional instructions to building our app from source,
but we promise to try our best.

# License

Please refer to the LICENSE.md for all copyrighted libraries and code used in Star Light. Further licenses 
generated from our compiler will be under their individual LICENSE files.

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