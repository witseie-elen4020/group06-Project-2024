# ELEN4020 Project - PFD data extraction from EGRI database 
This repository contains python scripts and tests results from an investigation into the suitability and scalability of two parallelisation techniques for information extraction from Wits Economic Geology Research Institute (EGRI) reports stored as searchable PDFs.

## Dependacies
Dependencies 
This system uses [mpi4pi](https://mpi4py.readthedocs.io/en/stable/) for pareleisation. [PyMuPDF](https://pymupdf.readthedocs.io/en/latest/index.html) and [Pillow](https://pypi.org/project/pillow/) are used for PDF data extraction and image saving.
A python virtual environment (called `venv`) containing these dependencies can be create using the following command. 

```shell
bash make_venv.sh
```
All scripts should be run with this environment activated.
To activate the virtual environment on Linux or MacOs use:
```shell
source venv/bin/activate
```
To activate the environment on Windows use:
```shell
source venv/Scripts/activate
```
