from . import process as p
from . import console
import sys, os

class Base:

    def __init__(self):
        pass

    def get_pwd(self):
        """
        Return the current path of the project
        :return:
        """
        return p.Process.run_process("pwd")

    def get_diff(self, filename, origin):
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
                                     "--no-prefix " +
                                     origin + " " + filename)

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
            message = self.errors_encountered(lint_output)
            if hasattr(self, 'debug_on') and self.debug_on:
                message += self.debug(code)
        else:
            message = self.success_message("OK")

        return message

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
            print(self.errors_encountered("- Missing .git folder"))
            sys.exit()

        if len(sys.argv) > 1:
            # get help
            if '-h' in sys.argv or '--help' in sys.argv:
                print("Usage: git-php-lint [options]\n \n"
                      "Options: \n"
                      "  --debug                            outputs the added php for debug purposes \n\n"
                      "  --with-branch=[origin/master]      compare the files with specified origin or \n"
                      "                                     branch. Default: origin/master \n\n"
                      "  -h || --help                       get help \n\n")

                sys.exit()

            # debug mode
            if '--debug' in sys.argv:
                self.debug_on = True

            # compare with origin/branch
            is_branch_set = [i for i in sys.argv if '--with-branch=' in i]
            if is_branch_set:
                get_branch = is_branch_set[0].split("=")[1]
                self.compare_to_branch = get_branch



    def debug(self, code):
        return "\n".join(list(self.add_line_numbers(code))) + "\n"

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
        return s

    @console.output("error", "Errors encountered")
    def errors_encountered(self, output):
        return output

    @console.output("success", "")
    def success_message(self, output):
        return output
