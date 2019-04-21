import subprocess


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

    @staticmethod
    def get_files():
        """
        Get a file list of PHP files
        :return:
        """
        files = Process.run_process("git diff --name-only")
        return list(filter(lambda x: ".php" in x, files.split("\n")))

    @staticmethod
    def get_diff(filename, origin):
        """
        Get the git diff for added in the current directory
        :return:
        """
        return Process.run_process("cd " + str(Process.get_pwd()) + " && "
                                     "git diff "
                                     "--diff-filter=cdruxb "
                                     "--word-diff=color "
                                     "--no-color "
                                     "--ignore-blank-lines "
                                     "--unified=0 "
                                     "--exit-code "
                                     "--no-prefix " +
                                     origin + " " + filename)

    @staticmethod
    def get_pwd():
        """
        Return the current path of the project
        :return:
        """
        return Process.run_process("pwd")

    @staticmethod
    def execute_lint(code):
        """
        Execute the php lint
        :param code:
        :return:
        """
        return Process.run_process("echo '<?php %s' | php -l" % code)
