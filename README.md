# Build Instructions

Please run the following scripts to set up the Python virtual environment, antlr4 and generate the grammar tokens.

    ./setup.sh
    ./generate_antlr_files.sh

# Common Errors

In case you find an error with imports, run the following command

    export PYTHONPATH="<Absolute PATH OF Group4Project1 (root dir) on your computer>"

# Run Instructions

To run the DSL:

1. Run: `./setup.sh` to install all dependencies
2. `source activate` to set the Python virtual environment
3. `./generate_antlr_files.sh` to generate the ANTLR files
4. `python3 frontend/main.py` to run the GUI. Currently, the game is hardcoded to run the `input.txt` file stored in `src/tests/`
    1. We suggest that you use `input.txt` as a playground to experiment with different features of our DSL.

Note: On Windows machines, you may need to run variations of the commands in `./setup.sh` and `activate` to activate the Python virtual environment.
