from Lib_config import install_reader
from Logging import logging_main_func
from Unpack import package, unpack_main_func
from XRD import xrd_main_func
from Origin import origin_main_func

def main():
    logging_main_func()
    install_reader()
    pack = unpack_main_func()
    xrd_session = xrd_main_func(pack.unpacked_files, names=pack.s_file_names)
    #origin_main_func(xrd_session)



if __name__ == '__main__':
    main()


if __name__ != '__main__':
    install_reader()
