from Unpack import package
from Origin import origin_session

if __name__ == '__main__':
    pack = package()
    pack.to_much()
    pack.sort_by()
    pack.unpack()
    print(pack.unpacked_files[0])


