from . import base as b
from . import process as p
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed


class Linting(b.Base):

    def __init__(self):
        super().__init__()

    def main(self):
        """
        Start the main console program
        :return:
        """
        # checking before_script
        self.check_argv_before_script()

        # get the list of files
        files = self.get_files()[:100]

        with ThreadPoolExecutor() as executor:
            make_files = {executor.submit(self.lint_file, f): f for f in files}
            for future in as_completed(make_files):
                try:
                    res = future.result()
                    print(res)
                except Exception as e:
                    print('An exception encountered: %s' % (e))

    def split_output(self, filename):
        """
        Split the git diff and return list of parts
        :return:
        """
        output = self.get_diff(filename)
        return output

    def source_code(self, str):
        """
        Return clean source code from the string
        Only PHP code will be output

        It removes the first 5 lines from each string
        and cleans any unwanted comments from git
        :param str:
        :return:
        """
        return b.Base.remove_lines_from_string(str, 5)

    def get_files(self):
        files = p.Process.run_process("git diff --name-only")
        return list(filter(lambda x: ".php" in x, files.split("\n")))

    def lint_file(self, f):
        content = self.split_output(f)
        sourcecode = self.source_code(content)
        return self.notice_checking_file(f) + self.do_php_lint(sourcecode)
