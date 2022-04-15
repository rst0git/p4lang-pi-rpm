Name: p4lang-pi
Version: 0.1.0
Release: 1%{?dist}
Summary: Protocol Independent API
License: ASL 2.0
URL: https://github.com/p4lang/PI

# Architectures supported by PI
ExclusiveArch: x86_64

%define submodule_googletest_version 1.8.0
%define submodule_gnmi_version 9c8d9e965b3e854107ea02c12ab11b70717456f2
%define submodule_public_version 1040d11c089c74084c64c234bee3691ec70e8a9f
%define submodule_p4runtime_version 1.3.0
%define submodule_uthash_version bf15263081be6229be31addd48566df93921cb46

Source0: https://github.com/p4lang/PI/archive/refs/tags/v%{version}.tar.gz
Source1: https://github.com/google/googletest/archive/refs/tags/release-%{submodule_googletest_version}.tar.gz
Source2: https://github.com/openconfig/gnmi/archive/%{submodule_gnmi_version}.tar.gz
Source3: https://github.com/openconfig/public/archive/%{submodule_public_version}.tar.gz
Source4: https://github.com/p4lang/p4runtime/archive/refs/tags/v%{submodule_p4runtime_version}.tar.gz
Source5: https://github.com/troydhanson/uthash/archive/%{submodule_uthash_version}.tar.gz

BuildRequires: valgrind
BuildRequires: automake
BuildRequires: libtool
BuildRequires: python3-devel
BuildRequires: glibc-devel gcc gcc-c++
BuildRequires: boost-devel boost-system boost-thread
BuildRequires: grpc-devel grpc-plugins
BuildRequires: protobuf-devel

%description
Protocol Independent API (PI or P4 Runtime) defines a set of APIs that allow
interacting with entities defined in a P4 program, such as tables, counters,
meters.

%package devel
Summary: Header files and libraries for %{name}
Requires: %{name} = %{version}-%{release}

%description devel
This package contains header files and libraries for %{name}.

%package libs
Summary: Libraries for %{name}
Requires: %{name} = %{version}-%{release}

%description libs
This package contains the libraries for %{name}

%prep
%setup -q -c -n p4lang-pi-%{version}

%setup -q -T -D -a 1 -n p4lang-pi-%{version}
cp -r googletest-release-%{submodule_googletest_version}/* PI-%{version}/third_party/googletest/

%setup -q -T -D -a 2 -n p4lang-pi-%{version}
cp -r gnmi-%{submodule_gnmi_version}/* PI-%{version}/proto/openconfig/gnmi/

%setup -q -T -D -a 3 -n p4lang-pi-%{version}
cp -r public-%{submodule_public_version}/* PI-%{version}/proto/openconfig/public/

%setup -q -T -D -a 4 -n p4lang-pi-%{version}
cp -r p4runtime-%{submodule_p4runtime_version}/* PI-%{version}/proto/p4runtime/

%setup -q -T -D -a 5 -n p4lang-pi-%{version}
cp -r uthash-%{submodule_uthash_version}/* PI-%{version}/third_party/uthash/


%build
cd PI-%{version}
./autogen.sh
mkdir build
cd build

# --with-cli and --with-internal-rpc are mostly deprecated.
# The internal RPC mechanism predates P4Runtime, and the CLI
# (very incomplete) should ideally be replaced by one built
# over P4Runtime.
#
# --with-sysrepo is to enable supporting gNMI and OpenConfig
# YANG models as part of the P4 Runtime server.

../configure \
    --prefix=%{_prefix} \
    --libdir=%{_libdir} \
    --without-bmv2 \
    --without-sysrepo \
    --without-internal-rpc \
    --without-cli \
    --with-proto

make %{?_smp_mflags}

%install
cd PI-%{version}
# license
%{__mkdir_p} %{buildroot}%{_datadir}/p4lang-pi
%{__cp} LICENSE %{buildroot}%{_datadir}/p4lang-pi/LICENSE
cd build
make install prefix=%{buildroot}%{_prefix} libdir=%{buildroot}/%{_libdir}

# remove static libs
rm -f %{buildroot}/%{_libdir}/*.a %{buildroot}/%{_libdir}/*.la

%files
%license %{_datadir}/p4lang-pi/LICENSE
%{_bindir}/pi_convert_p4info
%{_bindir}/pi_gen_fe_defines
%{_bindir}/pi_gen_native_json
%{python3_sitelib}/gnmi/*
%{python3_sitelib}/google/*
%{python3_sitelib}/p4/*

%files devel
%{_includedir}/gnmi/*
%{_includedir}/google/rpc/*
%{_includedir}/p4/*
%{_includedir}/PI/*
%{_libdir}/libpi*.so

%files libs
%{_libdir}/libpi*.so.*

%changelog
* Sun Mar 27 2022 <rstoyanov@fedoraproject.org> - 0.1.0
- Initial release