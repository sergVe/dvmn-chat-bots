import traceback


def get_error_msg(error_instance):
    tb_list = traceback.format_exception(None, error_instance, error_instance.__traceback__)

    error_title = ': '.join(tb_list[-1].split(':')[1:]).strip()
    error_body = ''.join(tb_list)
    return f'''\
    {error_title}
    {error_body}
    '''

