from Lib_config import install_reader
from Unpack import package, unpack_main_func
from XRD import xrd_main_func
from Origin import origin_session

def main():
    pack = unpack_main_func()
    xrd_main_func(pack.unpacked_files, names=pack.s_file_names)


if __name__ == '__main__':
    main()


if __name__ != '__main__':
    install_reader()
    #b = origin_session()