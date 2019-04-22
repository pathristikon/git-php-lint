from . import console
from . import string_processing as sp
from . import process as p
import sys, os


class Base:

    def __init__(self):
        self.Processes = p.Process()
        self.pwd = self.Processes.get_pwd()

    def do_php_lint(self, code):
        lint_output = self.Processes.execute_lint(code)

        if 'Errors parsing' in lint_output or 'Parse error' in lint_output:
            message = self.errors_encountered(lint_output)
            if hasattr(self, 'debug_on') and self.debug_on:
                message += self.debug(code)
        else:
            message = self.success_message("OK")

        return message

    def check_argv_before_script(self):
        """
        Getting the argv
        Before script executes, this gets executed
        :return:
        """
        if not os.path.exists(self.pwd + "/.git"):
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
        return "\n".join(list(sp.add_line_numbers(code))) + "\n"


    @console.output("notice", "Starting linting for")
    def notice_checking_file(self, s):
        return s

    @console.output("error", "Errors encountered")
    def errors_encountered(self, output):
        return output

    @console.output("success", "")
    def success_message(self, output):
        return output
