%define major %(echo %{version}|cut -d. -f1-2)
%define libname %mklibname xerces-c
%define oldlibname %mklibname xerces-c %{major}
%define develname %mklibname xerces-c -d

Summary:	Xerces-C++ validating XML parser
Name:		xerces-c
Version:	3.3.0
Release:	2
License:	Apache
Group:		System/Libraries
URL:		https://xml.apache.org/xerces-c/
Source0:	https://github.com/apache/xerces-c/archive/refs/tags/v%{version}.tar.gz
BuildRequires:	pkgconfig(libcurl)
BuildRequires:	pkgconfig(zlib)
BuildRequires:	pkgconfig(icu-uc)
BuildRequires:	icu
BuildRequires:	slibtool

%patchlist
xerces-c-3.3-fix-build.patch

%description
Xerces-C++ is a validating XML parser written in a portable subset of C++.
Xerces-C++ makes it easy to give your application the ability to read and
write XML data. A shared library is provided for parsing, generating,
manipulating, and validating XML documents.

The parser provides high performance, modularity, and scalability. Source
code, samples and API documentation are provided with the parser. For
portability, care has been taken to make minimal use of templates, no RTTI,
and minimal use of #ifdefs.

%package -n	%{libname}
Summary:	Xerces-c library
Group:		System/Libraries
%rename %{oldlibname}

%description -n %{libname}
Xerces-C++ is a validating XML parser written in a portable subset of C++.
Xerces-C++ makes it easy to give your application the ability to read and
write XML data. A shared library is provided for parsing, generating,
manipulating, and validating XML documents.

This package contains the shared xerces-c library.

%package -n	%{develname}
Summary:	Header files for Xerces-C++ validating XML parser
Group:		Development/C++
Requires:	%{libname} >= %{EVRD}
Provides:	xerces-c-devel = %{EVRD}
Provides:	libxerces-c-devel = %{EVRD}
Conflicts:	%{mklibname xerces-c 0 -d}
Conflicts:	%{mklibname xerces-c 28 -d}

%description -n	%{develname}
Xerces-C++ is a validating XML parser written in a portable subset of C++.
Xerces-C++ makes it easy to give your application the ability to read and
write XML data. A shared library is provided for parsing, generating,
manipulating, and validating XML documents.

This package contains development files such as header files you can use to
develop XML applications with Xerces-C++.

%package	doc
Summary:	Documentation for Xerces-C++ validating XML parser
Group:		Books/Other
Obsoletes:	xerces-c-manual

%description	doc
Xerces-C++ is a validating XML parser written in a portable subset of C++.
Xerces-C++ makes it easy to give your application the ability to read and
write XML data. A shared library is provided for parsing, generating,
manipulating, and validating XML documents.

This package contains the documentation for Xerces-C++.

%prep
%autosetup -p1
# Looks like they forgot to remove svn control files when building the
# tarball...
# And they do get copied into the -doc package, so let's get rid of them
find . -name .svn |xargs rm -rf
sed -i -e 's,libtoolize,slibtoolize,g' reconf
./reconf

%conf
%configure \
    --enable-netaccessor-curl \
    --enable-transcoder-icu \
%ifarch %{ix86}
    --disable-sse2 \
%endif
    --enable-msgloader-icu

%build
%make_build

#Disable tests for now
#check
#make check

%install
%make_install

%files
%{_bindir}/*

%files -n %{libname}
%{_libdir}/libxerces-c-%{major}.so

%files -n %{develname}
%{_includedir}/xercesc
%{_libdir}/libxerces-c.so
%{_libdir}/pkgconfig/xerces-c.pc

%files doc
%doc CREDITS LICENSE doc/*
