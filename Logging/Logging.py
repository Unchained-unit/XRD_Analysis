import logging
import os

logging.basicConfig(level=logging.DEBUG, filename="py_log.log",
                    filemode="w", format="[%(levelname)s] --> %(message)s")


def counter(fu):
    def inner(*a, **kw):
        inner.count += 1
        return fu(*a, **kw)

    inner.count = 0
    return inner
@counter
def debug(msg):
    logging.debug(msg)
@counter
def info(msg):
    logging.info(msg)
@counter
def warn(msg):
    logging.warning(msg)
@counter
def error(msg):
    logging.error(msg)
@counter
def critical(msg):
    logging.critical(msg)

def summary_logging(warn, error, critical, module_name, filename='log_summary.log'):
    with open(filename, 'a+') as file:
        file.write(f'module [{module_name}] finished\n'
                f'{critical.count} - critical errors occurs\n'
                f'{error.count} - errors occurs\n'
                f'{warn.count} - warnings occurs\n\n')
    warn.count = 0
    error.count = 0
    critical.count = 0

def clear_summary_log(filename = 'log_summary.log'):
    open(filename, 'w').close()

def logging_main_func():
    clear_summary_log()



if __name__ == "__main__":
    logging.info("I AM")