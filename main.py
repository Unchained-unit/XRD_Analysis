from Unpack import package
from XRD.XRD import XRD_pack
from Origin import origin_session

if __name__ == '__main__':
    pack = package()
    pack.to_much()
    pack.sort_by()
    pack.unpack()
    pack.files_check()

    a = XRD_pack(pack.unpacked_files, names=pack.s_file_names)
    a.cross_peak()
    a.find_params()
    #a.imprint()