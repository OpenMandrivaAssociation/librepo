%define major 0
%define libname %mklibname repo %{major}
%define devname %mklibname repo -d

# prevent provides from nonstandard paths:
%define __provides_exclude_from %{python_sitearch}/.*\\.so

Summary:	Repodata downloading library
Name:		librepo
Version:	1.16.0
Release:	2
Group:		System/Libraries
License:	LGPLv2+
URL:		https://github.com/rpm-software-management/librepo
Source0:	https://github.com/rpm-software-management/librepo/archive/%{version}/%{name}-%{version}.tar.gz
Patch0:		librepo-1.7.18-no--Llib64.patch
BuildRequires:	cmake
BuildRequires:	doxygen
BuildRequires:	pkgconfig(check)
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(glib-2.0) >= 2.26.0
BuildRequires:	pkgconfig(libcurl) >= 7.52.0
BuildRequires:	pkgconfig(openssl)
BuildRequires:	pkgconfig(zck) >= 0.9.11
BuildRequires:	pkgconfig(rpm) >= 4.18.0
Obsoletes:	python2-librepo < 1.13.0

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

%package -n python-librepo
Summary:	Python 3 bindings for the librepo library
Group:		Development/Python
Provides:	python3-%{name} = %{EVRD}
BuildRequires:	python-gpg
BuildRequires:	pkgconfig(python)
BuildRequires:	python-requests
BuildRequires:	python-sphinx
BuildRequires:	python-pyxattr
Requires:	%{libname}%{?_isa} = %{EVRD}

%description -n python-librepo
Python bindings for the librepo library.

%prep
%autosetup -p1

%build
%cmake \
	-DWITH_ZCHUNK=ON \
	-DUSE_GPGME=OFF

%make_build

%install
%make_install -C build

%files -n %{libname}
%{_libdir}/librepo.so.%{major}

%files -n %{devname}
%doc COPYING README.md
%{_libdir}/librepo.so
%{_libdir}/pkgconfig/librepo.pc
%{_includedir}/librepo/

%files -n python-librepo
%{python_sitearch}/librepo
