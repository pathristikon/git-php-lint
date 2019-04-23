import subprocess, os


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
    def get_files(pwd, file_lint):
        """
        Get a file list of PHP files
        :return:
        """
        files = Process.run_process("git diff --name-only")
        names = list(filter(lambda x: ".php" in x, files.split("\n")))

        if file_lint:
            # add untracked git files, prepared for linting
            untracked = Process.get_untracked_files("/work/ejobs-live/")
            [names.append(file) for file in untracked.split("\n")]

        return names

    @staticmethod
    def get_diff(filename, origin, pwd):
        """
        Get the git diff for added in the current directory
        :return:
        """
        return Process.run_process("cd " + str(pwd) + " && "
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
    def get_untracked_files(pwd):
        return Process.run_process("cd " + str(pwd) + " && "
                                                      "git ls-files "
                                                      "--others "
                                                      "--exclude-standard "
                                                      "*.php")

    @staticmethod
    def execute_lint(code):
        """
        Execute the php lint
        for a part of the code
        :param code:
        :return:
        """
        return Process.run_process("echo '<?php %s' | php -l" % code)

    @staticmethod
    def execute_file_fint(filename):
        """
        Execute lint for entire file
        :param filename:
        :return:
        """
        return Process.run_process("php -l %s" % filename)
