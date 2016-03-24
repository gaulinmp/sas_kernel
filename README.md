# SAS Jupyter Kernel

sas_kernel is a very bare bones SAS kernel for Jupyter. It is based on [bash_kernel](https://github.com/takluyver/bash_kernel), which uses [pexpect](http://pexpect.readthedocs.org/en/stable/) to wrap sas in -nodms mode.

## Install

    git clone https://github.com/gaulinmp/sas_kernel.git
    cd sas_kernel
    python install.py

## Run
    jupyter qtconsole --kernel bash
    jupyter console --kernel bash

Or run `jupyter notebook`, and select SAS under the New dropdown. To exit, use EOF or Ctrl-D. No SAS interrupts are implemented.

## TODO: in no particular order

1. Add line number stripping
1. Add interrupts
1. Add table recognition
1. Add HTML formatting to tables, potentially using SAS's built in ODS system.
1. Move away from pexpect if helpful
