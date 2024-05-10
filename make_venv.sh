#! /usr/bin/env bash

# This script was oringnally made by Joshua Jandrell for the ELEN4022 porject. 
# It is being reused here.

python -m venv venv


if [[ "$OSTYPE" == "cygwin" ]] || [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    # Running on windows
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

python -m pip PyMuPDF Pillow
python -m pip install mpi4py