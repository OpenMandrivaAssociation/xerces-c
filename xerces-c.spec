%define major %(echo %{version}|cut -d. -f1-2)
%define libname %mklibname xerces-c
%define oldlibname %mklibname xerces-c %{major}
%define develname %mklibname xerces-c -d

Summary:	Xerces-C++ validating XML parser
Name:		xerces-c
Version:	3.2.5
Release:	1
License:	Apache
Group:		System/Libraries
URL:		http://xml.apache.org/xerces-c/
Source0:	http://mirrors.ukfast.co.uk/sites/ftp.apache.org/xerces/c/%(echo %{version}|cut -d. -f1)/sources/xerces-c-%{version}.tar.xz
BuildRequires:	curl-devel
BuildRequires:	zlib-devel
BuildRequires:	icu-devel
BuildRequires:	icu
Epoch:		1

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
Requires:	%{libname} >= %{epoch}:%{version}-%{release}
Provides:	xerces-c-devel = %{epoch}:%{version}-%{release}
Provides:	libxerces-c-devel = %{epoch}:%{version}-%{release}
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
%setup -q
# Looks like they forgot to remove svn control files when building the
# tarball...
# And they do get copied into the -doc package, so let's get rid of them
find . -name .svn |xargs rm -rf

%build
%configure \
    --enable-netaccessor-curl \
    --enable-transcoder-icu \
%ifarch %{ix86}
    --disable-sse2 \
%endif
    --enable-msgloader-icu
%make

#Disable tests for now
#check
#make check

%install
%makeinstall_std

# cleanup
rm -f  %{buildroot}%{_libdir}/libxerces-c.*a

%clean

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

