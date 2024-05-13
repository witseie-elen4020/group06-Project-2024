# ELEN4020 Project - PDF data extraction from the EGRI database 
This repository contains python scripts and tests results from an investigation into the suitability and scalability of two parallelisation implementations (scatter and worker) for information extraction from the Wits Economic Geology Research Institute (EGRI) reports and stored as searchable PDFs.

## Dependencies
This system uses [mpi4pi](https://mpi4py.readthedocs.io/en/stable/) for parallelisation. [PyMuPDF](https://pymupdf.readthedocs.io/en/latest/index.html) and [Pillow](https://pypi.org/project/pillow/) are used for PDF data extraction and image saving.
A python virtual environment (called `venv`) containing these dependencies can be created using the following command: 

```shell
bash make_venv.sh
```
All scripts should be run with this environment activated.
To activate the virtual environment on Linux or MacOS use:
```shell
source venv/bin/activate
```
To activate the environment on Windows use:
```shell
source venv/Scripts/activate
```
## Frontend Interface
The ‘frontend’ terminal interface offers a convenient means of interacting with the extraction system and viewing extracted data. This system uses the worker-manager implementation with four processes. To run the frontend, use the following terminal command:
```shell
python app.py
```
ℹ️ Note: This does not need to be run with MPI. `mpiexec` is used when the frontend calls the extraction process.
## Run Tests
There are three test configurations which can be used to benchmark an implementation on different systems. Each set of tests will generate a `.txt` file containing script outputs, and a `.csv` file containing the documents' information and execution times. These files are stored in the `results/` folder.
Three subdirectories will also be created in `results/` to store information extracted from the PDFs using each implementation: `scatter_out/`, `worker _out/` and `serial_out/`. These directories are deleted each time a benchmarking (speed) test is run to ensure that file creation time is also recorded.
### Speed Tests
General benchmarking tests can be run with `mpiexec` using the command:
```shell
bash speed_tests.sh <data-directory>
```
`<data-directory>` is a folder that must contain a selection of EGRI PDFs that can be used as inputs to benchmark data extraction times.
This (general) test configuration is designed for performance benchmarking on a single node and will time each extraction using 2, 4, 8, and 16 processes for both scatter and worker implementations. The serial process is also timed to serve as a reference. Program outputs and extraction times are saved in `results/times.txt` and `results/times.csv`.
### Speed Tests on Dica10
A second single-node speed test script is created to run tests on the Dica10 node with 2, 4, 6, 8 and 12 process counts. This should be run to test extraction scalability on a single node that has more than four cores.
```shell
bash speed_tests_dica10.sh <data-directory>
```
Results and extraction times are stored in `results/times_dica10.txt` and `results/times_dica10.csv`.
### Speed tests with slurm
Tests can be run on multiple cluster nodes with the slurm batch scheduler using the following terminal command:
```shell
sbatch srun_speed_tests.sh <data-directory>
```
As with `speed_tests.sh`, PDF extraction is timed using 2, 4, 8 and 16 process.
Outputs from the process will be stored in the `results/slurm/` directory. 

ℹ️ Note: Serial implementation is not tested using slum.

## General Usage
Each of the three implementations can be used to extract PDF information with the terminal commands listed below. `<pdf-files>` is a list of input EGRI PDFs for data extraction, ` <output-directory>` is the folder in which the extracted information should be saved and `<process-count>` is the number of processes used (if applicable).
### Serial
```shell
Python src/main_serial.py <pdf-file> <output-directory>
```
### Scatter 
```shell
mpiexec -n <process-count> python src/main_scatter.py <pdf-files> <output-directory>
```  
### Worker-Manager
```shell
mpiexec -n <process-count> python src/main_str.py <pdf-files> <output-directory>
```  
## Repository Structure 
###  `src/`
The `src/` directory contains python code for all three implementations as well as auxiliary scripts used to aid information extraction. This directory can be seen as the latest interation of the PDF information extraction system.
### `results/`
The `results/` directory contains benchmark time data and extraction outputs.

### `initial_results/`
The `initial_results/` folder contains a set of scripts used to ascertain various extraction task execution times during the early development stages of the project. These tests can be run from the terminal as follows: 
```shell
bash initial_results/serial_time.sh data
```
### `misc/`
The `misc/` folder contains experimental scripts used to trail ideas before integrating them in the final system.




