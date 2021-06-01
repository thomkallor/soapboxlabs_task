# soapboxlabs_task
The algorithm does a speed based check on the given data points.

Change the `dataset_path` to give a new csv_file rather than the one given for the task.
Change the `speed_limit` variable to change the valid speed limit.
The `speed_limit` should be in kmph.

The **solution.py** contains the main solution for the task.
The unit test cases are written using pytest and are inside the ./tests folder

## Environment
The solution is written in python 3.9.5
The requirements for the solution are given in the `requirements.txt` file.

Run `pip install -r requirements.txt` to run the dependencies.

I have also provide a `Dockerfile` in case if it is the preferred method of running the solution.

## Commands

Run `python solution.py` to run the solution from the root folder.

Run `pytest ./tests/tests.py` to run the test cases from the root folder.
