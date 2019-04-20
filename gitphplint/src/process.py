import subprocess, sys
from . import console

class Process:

    def __init__(self):
        pass

    @staticmethod
    def run_process(command):
        try:
            process = subprocess.Popen(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE)

        except subprocess.CalledProcessError as err:
            print("Status : FAIL", err.returncode, err.output)

        else:
            stdout, stderr = process.communicate()

            if stderr:
                return stderr.decode("utf-8").strip()
            else:
                return stdout.decode("utf-8").strip()

