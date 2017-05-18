# Prerequisites

* Raspberry PI - but can be run on a local machine as well. This install guide was written using a new install of Raspbian Jessie (2017-04-10-raspbian-jessie.img). Make sure your system is up to date:

```
$ sudo apt-get update
```

* Python (http://www.python.org) - original code developed under  python 2.7.10. Python should already be installed on your PI.

* Git (http://www.gitscm.org) - you will probably have the `git` command installed, but if not install it by:

```
$ sudo apt-get install git
```

* WiringPi (http://wiringpi.com) - original code developed against version 2.44. Currently the `gpio` command is used from this package. The code will first check to see if this command can be found before accessing GPIO pins. If the command is not present, a log message will be printed to the server output indicating so along with what pins were intended to be accessed. This allows for local development that is not happening on the PI.

To install WiringPi:

```
$ git clone git://git.drogon.net/wiringPi
$ cd wiringPi
$ git checkout -b 2.44 2.44
$ ./build
```
  
Verify WiringPi installed to the expected location:

```
$ test -e /usr/local/bin/gpio || echo "not installed"
```

If you see "not installed", check your WiringPi installation. If the installation was completed properly, you can delete the WiringPi repository

```
$ cd .. ; rm -rf wiringPi
```

# Setup

Ensure this repo is cloned and `cd` into it:

```
$ git clone https://github.com/srqsoftware-hacknight/LEARN.git
$ cd LEARN
```

# Running locally / for development

You can run the provided script to launch the HTTP server:

```
$ ./bin/run.sh
```

or invoke the CGI server directly. This command must be run in the project root directory:

```
$ python -m CGIHTTPServer
```

Open `http://localhost:8000` in your browser. If you are accessing your PI remotely, you will need to replace "localhost" with the IP of your PI

# Setup for kiosk mode on PI

Install chromium and utilities on the PI:

```
$ sudo apt-get install chromium-browser x11-xserver-utils unclutter
```

Update config files to support booting into "kiosk mode":

```
$ sed -i '/xscreensaver/d' $HOME/.config/lxsession/LXDE-pi/autostart
$ cat << EOF >> $HOME/.config/lxsession/LXDE-pi/autostart
@/home/pi/LEARN/bin/run.sh
@xset s off
@xset -dpms
@xset s noblank
@sed -i "s/\"exited_cleanly\": false/\"exited_cleanly\": true/" ~/.config/chromium/Default/Preferences
@chromium-browser --noerrdialogs --kiosk http://127.0.0.1:8000 --incognito
EOF
$ sudo reboot
```

Within a few seconds of the window manager loaded you should see the browser display the main page in full screen mode

# Developing

The `cgi-bin` directory contains python scripts that get invoked. The `controller.py` file provides the main logic for determining which template to use and toggling GPIO pins. Given the small size of the functionality, its probably best to keep things here but feel free to refactor as needed.

The `css` directory contains CSS directives for the HTML files that live in the `templates` directory. To make changes to the UI, simply edit the appropriate CSS file or HTML template.

Edit the `controller.py` file if you are adding new functionality such as a new letter or button that renders a new page and so on. The index.html file serves as a convenience to automatically redirect requests made to the root URL to `controller.py`.

To change and re-generate the letter images:

```
./bin/generate-images.py /path/to/images/directory
```

NOTE: to use the image generation script you will need to have the Wand bindings installed:

`pip install Wand`
