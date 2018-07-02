# OMV is missing stuff for tests
%bcond_with tests

%define major 0
%define libname %mklibname repo %{major}
%define devname %mklibname repo -d

Summary:	Repodata downloading library
Name:		librepo
Version:	1.9.0
Release:	1
Group:		System/Libraries
License:	LGPLv2+
URL:		https://github.com/rpm-software-management/librepo
Source0:	https://github.com/rpm-software-management/librepo/archive/%{name}-%{version}.tar.gz
Patch0:		librepo-1.7.18-no--Llib64.patch

BuildRequires:	pkgconfig(check)
BuildRequires:	cmake
BuildRequires:	doxygen
BuildRequires:	pkgconfig(expat)
BuildRequires:	pkgconfig(glib-2.0) >= 2.26.0
BuildRequires:	gpgme-devel
BuildRequires:	libassuan-devel
BuildRequires:	attr-devel
BuildRequires:	pkgconfig(gpg-error)
BuildRequires:	pkgconfig(libcurl) >= 7.19.0
BuildRequires:	pkgconfig(openssl)

# prevent provides from nonstandard paths:
%define __noautoprovfiles %{python2_sitearch}/.*\\.so\\|%{python3_sitearch}/.*\\.so

%description
A library providing C and Python (libcURL like) API to downloading repository
metadata.

%package -n %{libname}
Summary:	Libraries for %{name}
Group:		System/Libraries

%description -n %{libname}
Libraries for %{name}.

%package -n %{devname}
Summary:	Repodata downloading library
Group:		Development/C
Provides:	%{name}-devel = %{EVRD}
Requires:	%{libname}%{?_isa} = %{EVRD}

%description -n %{devname}
Development files for %{name}.

%package -n python2-librepo
Summary:	Python 2 bindings for the librepo library
Group:		Development/Python
BuildRequires:	python2-gpgme
BuildRequires:	pkgconfig(python2)
%if %{with tests}
BuildRequires:	python2-flask
BuildRequires:	python2-nose
%endif
BuildRequires:	python2-xattr
Requires:	%{libname}%{?_isa} = %{EVRD}

%description -n python2-librepo
Python 2 bindings for the librepo library.

%package -n python-librepo
Summary:	Python 3 bindings for the librepo library
Group:		Development/Python
Provides:	python3-%{name} = %{EVRD}
BuildRequires:python-gpgme
BuildRequires:	pkgconfig(python3)
%if %{with tests}
BuildRequires:	python-flask
BuildRequires:	python-nose
%endif
BuildRequires:	python-sphinx
BuildRequires:	python-xattr
Requires:	%{libname}%{?_isa} = %{EVRD}

%description -n python-librepo
Python 3 bindings for the librepo library.

%prep
%setup -q -n %{name}-%{name}-%{version}
%apply_patches

rm -rf py2
mkdir py2

%build
%cmake -DCMAKE_BUILD_TYPE=RelWithDebInfo -DPYTHON_DESIRED:str=3
%make

cd ../py2
%cmake -DCMAKE_BUILD_TYPE=RelWithDebInfo ../../ -DENABLE_DOCS:BOOL=OFF
%make
cd ..

%if %{with tests}
%check
cd ./build
make ARGS="-V" test
make clean
cd ..

cd ./py2/build
make ARGS="-V" test
cd ..
%endif

%install
cd ./build
%makeinstall_std
cd ..

cd ./py2/build
%makeinstall_std
cd ..

%files -n %{libname}
%{_libdir}/librepo.so.%{major}

%files -n %{devname}
%doc COPYING README.md
%{_libdir}/librepo.so
%{_libdir}/pkgconfig/librepo.pc
%{_includedir}/librepo/

%files -n python2-librepo
%{python2_sitearch}/librepo

%files -n python-librepo
%{python3_sitearch}/librepo
