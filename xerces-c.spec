%define major 3.1
%define libname %mklibname xerces-c %{major}
%define develname %mklibname xerces-c -d

Summary:	Xerces-C++ validating XML parser
Name:		xerces-c
Version:	3.1.0
Release:	%mkrel 1
License:	Apache
Group:		System/Libraries
URL:		http://xml.apache.org/xerces-c/
Source0:	http://apache.dataphone.se/xerces/c/3/sources/%{name}-%{version}.tar.gz
Patch0:		xerces-c-3.0.1-include.patch
BuildRequires:	curl-devel
BuildRequires:	zlib-devel
BuildRequires:	libicu-devel icu
Epoch:		1
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

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
%setup -q -n %{name}-%{version}
#patch0 -p0

%build
#rm -f config.cache
#libtoolize --copy --force; aclocal -I m4; autoheader; automake -a -c -f; autoconf

%configure2_5x \
    --disable-static \
    --enable-netaccessor-curl \
    --enable-transcoder-icu \
    --enable-msgloader-icu

%make

%check
make check

%install
rm -rf %{buildroot}

%makeinstall_std

# cleanup
rm -f  %{buildroot}%{_libdir}/libxerces-c.*a

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_bindir}/*

%files -n %{libname}
%defattr(-,root,root,-)
%{_libdir}/libxerces-c-%{major}.so

%files -n %{develname}
%defattr(-,root,root,-)
%{_includedir}/xercesc
%{_libdir}/libxerces-c.so
%{_libdir}/pkgconfig/xerces-c.pc

%files doc
%defattr(-,root,root,-)
%doc CREDITS LICENSE doc/*
