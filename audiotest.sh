#!/bin/sh
gst-launch-1.0 -v -m audiotestsrc ! audioconvert ! audioresample ! autoaudiosink
