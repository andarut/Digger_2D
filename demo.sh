#!/bin/bash

python3.12 -m venv .venv && .venv/bin/python3 -m pip install pygame
.venv/bin/python3 main.py
