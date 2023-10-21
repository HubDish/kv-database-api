# Instructions to run
 
To run the back-end api, ensure python3 is installed.
1. Clone the repository into the desired folder with "git clone --recurse-submodules" to clone with existing version of RocksDB.
2. Compile RocksDB using "make all" (Follow instructions in RocksDB INSTALL.md)
3. Create a python virtual environment using "python3 -m venv /path-to-venv" and invoke virtual environment (Optional)
4. Run "make fastapi" to install requirements and/or run back-end
