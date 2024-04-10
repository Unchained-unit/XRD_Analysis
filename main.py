from Logging import logging_main_func
from Lib_config import main_installing_func
from Unpack import package, unpack_main_func
from XRD import xrd_main_func
from Origin import origin_main_func

def main():
    logging_main_func()
    main_installing_func()
    pack = unpack_main_func()
    xrd_session = xrd_main_func(pack.unpacked_files, names=pack.s_file_names)
    origin_main_func(xrd_session)



if __name__ == '__main__':
    main()

