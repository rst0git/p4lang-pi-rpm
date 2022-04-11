srpm:
	dnf -y install rpmdevtools fedpkg fedora-review valgrind automake libtool python3-devel glibc-devel g++ boost-devel boost-system boost-thread grpc-devel grpc-plugins protobuf-devel
	spectool -g p4lang-pi.spec
	fedpkg local
