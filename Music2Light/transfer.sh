#!/bin/bash

ssh pi@192.168.0.2 "rm -r brain"
scp -r ../Music2Light pi@192.168.0.2:/home/pi/brain/
