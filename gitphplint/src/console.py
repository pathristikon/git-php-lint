normal = "\033[0;37;40m"
success_text = "\033[0;30;42m"
notice_text = "\033[0;37;44m"
error_text = "\033[0;37;41m"

def output(type, message):
    def wrap(func):
        def wrapped_f(*args):
            if type == 'notice':
                call_var = notice_text
            elif type == 'error':
                call_var = error_text
            elif type == 'success':
                call_var = success_text
            else:
                call_var = normal

            print(format_text("%s %s" % (message, args[1]), call_var))
        return wrapped_f
    return wrap


def format_text(str, func):
    return "{} {} {} \n".format(func, str, normal)

