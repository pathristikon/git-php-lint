from . import process as p
from . import console
import sys, os

class Base:

    def get_pwd(self):
        """
        Return the current path of the project
        :return:
        """
        return p.Process.run_process("pwd")

    def get_diff(self):
        """
        Get the git diff for added in the current directory
        :return:
        """
        return p.Process.run_process("cd " + str(self.get_pwd()) + " && "
                                     "git diff "
                                     "--diff-filter=cdruxb "
                                     "--word-diff=color "
                                     "--no-color "
                                     "--ignore-blank-lines "
                                     "--unified=0 "
                                     "--exit-code "
                                     "--no-prefix")

    def get_base_name(self, s):
        """
        Get the base name of file from string
        :param s:
        :return:
        """
        line = s.splitlines()[0]
        return list(filter(None, line.split(" ")))[0]

    @staticmethod
    def remove_lines_from_string(s, remove_num):
        """
        Remove lines from string and filter the output
        to get only the source code written
        :param s:
        :param remove_num:
        :return:
        """
        str = s.splitlines()
        filtered_list = list(filter(lambda x: "@@" not in x, str[remove_num:]))
        remove_empty = list(filter(None, filtered_list))

        return '\n'.join(remove_empty)

    def do_php_lint(self, code):
        lint_output = self._execute_lint(code)

        if 'Errors parsing' in lint_output or 'Parse error' in lint_output:
            self.debug(code)
            self.errors_encountered(lint_output)
        else:
            self.success_message("OK")

    def _execute_lint(self, code):
        """
        Execute the php lint
        :param code:
        :return:
        """
        return p.Process.run_process("echo '<?php %s' | php -l" % code)

    def check_argv_before_script(self):
        """
        Getting the argv
        Before script executes, this gets executed
        :return:
        """
        if not os.path.exists(self.get_pwd() + "/.git"):
            self.errors_encountered("- Missing .git folder")
            sys.exit()

        if len(sys.argv) > 1:
            if sys.argv[1] == '-h' or sys.argv[1] == '--help':
                print("Usage: git-php-lint [options]\n \n"
                      "Options: \n"
                      "  --debug         outputs the added php for debug purposes \n"
                      "  -h              get help \n"
                      "  --help          get help \n")
                sys.exit()

    def debug(self, code):
        if len(sys.argv) > 1:
            if sys.argv[1] == '--debug':
                print("\n".join(list(self.add_line_numbers(code))))
                print("\n")

    def add_line_numbers(self, code):
        """
        For debug purposes, add line number to each
        line of code
        :param code:
        :return:
        """
        sourceCode = code.splitlines()
        num = 0
        for line in sourceCode:
            yield "\033[1;30;40m{}\033[0;37;40m {}".format(num, line)
            num += 1

    @console.output("notice", "Starting linting for")
    def notice_checking_file(self, s):
        return self.get_base_name(s)

    @console.output("error", "Errors encountered")
    def errors_encountered(self, output):
        print(output)

    @console.output("success", "")
    def success_message(self, output):
        print(output)
