#!/usr/bin/env bash

apt update
apt -y upgrade
apt install -y build-essential libssl-dev libffi-dev
apt install -y python3-dev python3-pip python3-venv python3-wheel
apt install -y libsndfile1-dev
apt install -y unzip

python3 -V
pip3 -V

reboot
