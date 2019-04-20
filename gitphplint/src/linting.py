from . import base as b


class Linting(b.Base):

    def __init__(self):
        pass

    def main(self):
        """
        Start the main console program
        :return:
        """
        # checking before_script
        self.check_argv_before_script()

        # start linting
        splited_output = self.split_output()

        for part in splited_output:
            basename = self.get_base_name(part)
            if '.php' in basename:

                self.notice_checking_file(basename)

                sourcecode = self.source_code(part)
                self.do_php_lint(sourcecode)

    def split_output(self):
        """
        Split the git diff and return list of parts
        :return:
        """
        output = self.get_diff()
        return list(filter(None, output.split('diff --git')))

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
