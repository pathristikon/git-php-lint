from . import base as b, string_processing as sp
from . import process as p
from concurrent.futures import ThreadPoolExecutor, thread
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
        files = self.Processes.get_files(self.pwd, (self.filelint if hasattr(self, 'filelint') else False))

        with ThreadPoolExecutor() as executor:
            make_files = {executor.submit(self.lint_file, f): f for f in files}
            try:
                for future in as_completed(make_files):
                    try:
                        print(future.result())
                    except Exception as e:
                        print('An exception encountered: %s' % (e))
            except KeyboardInterrupt:
                executor._threads.clear()
                thread._threads_queues.clear()
                print('\nShutdown complete.')

        if not hasattr(self, 'filelint'):
            print("Omitting git untracked files. See help for details.")

    def split_output(self, filename):
        """
        Split the git diff and return list of parts
        :return:
        """
        branch = self.compare_to_branch \
            if hasattr(self, 'compare_to_branch') \
               and self.compare_to_branch \
            else 'origin/master'

        output = self.Processes.get_diff(filename, branch, self.pwd)
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
        return sp.remove_lines_from_string(str, 5)

    def lint_file(self, f):
        content = self.split_output(f)
        sourcecode = self.source_code(content)
        return self.notice_checking_file(f) + self.do_php_lint(sourcecode, f)
