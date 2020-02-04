#!/bin/sh
gst-launch-1.0 filesrc location=test.wav ! decodebin ! audioconvert ! audioresample ! autoaudiosink
