#!/usr/bin/env bash
#xrandr --output HDMI-1-2 --rotate left
#xrandr --output HDMI-1-2 --rotate normal
cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
python3 src/neuron.py
