def add_line_numbers(code):
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