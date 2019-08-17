`Python-Auto-Srcipt` is a series of automation scripts I build to deal with routine works. All the scripts are based on a simple console application framework to unify their structure. You may visit the `utility` package for more details.

# How to Run
 
Each package, except for `config` and `utility`, represents an automation task and can be executed by either:

1. Run as Python script: execute `run.py` of the package.

2. Run as module: execute `python -m pakcageName` from console.

If you find some scripts are frequently used, you may register (1) or (2) as bash command.

Some scripts contain confirm process, which is meant to let user understand the consequence of running.
You can use `-nc` option, such as `python -m pakcageName -nc`, to skip it.

# Configuring Scripts

Config template of each script can be found in the `config` directory. For the purpose of version control, you have to trim the suffix `_example` of the config file to let packages load the correct file.

# Package Description

* porter

Collect content of multiple directories and export compressed files to designated path.

* ss_cleaner

Collect all screenshots files in the desktop, or any other designated directory, to another directory.