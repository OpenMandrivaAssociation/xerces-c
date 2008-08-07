%define tarversion 2_8_0

%define major 28

%define libname %mklibname xerces-c %major
%define libdev %mklibname -d xerces-c

%define enable_debug 0
%{?_enable_debug: %{expand: %%global enable_debug 1}}

Name: xerces-c
Version: 2.8.0
Release: %mkrel 2
Epoch: 1
URL: http://xml.apache.org/xerces-c/
License: Apache
Source0: %{name}-src_%{tarversion}.tar.gz
Patch0: xerces-c-lib64.patch
# Most of apps 
Patch1: xerces-c-pvtheader.patch
# XQilla patches
Patch2: xercesc_content_type.patch
Patch3: xercesc_regex.patch
Summary:	Xerces-C++ validating XML parser
Group: System/Libraries
BuildRoot: %{_tmppath}/%{name}-root
BuildRequires: zlib-devel
BuildRequires: libicu-devel
BuildConflicts: %{_lib}xerces-c26-devel

%description
Xerces-C++ is a validating XML parser written in a portable subset of C++.
Xerces-C++ makes it easy to give your application the ability to read and
write XML data. A shared library is provided for parsing, generating,
manipulating, and validating XML documents.

The parser provides high performance, modularity, and scalability. Source
code, samples and API documentation are provided with the parser. For
portability, care has been taken to make minimal use of templates, no RTTI,
and minimal use of #ifdefs.


#----------------------------------------------------------------------

%package -n %libname
Group: System/Libraries
Summary: Xerces-c library

%description -n %libname
xerces-c library

%if %mdkversion < 200900
%post -n %libname -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %libname -p /sbin/ldconfig
%endif

%files -n %libname
%defattr(-,root,root,-)
%_libdir/libxerces-*.so.*

#----------------------------------------------------------------------

%package -n %libdev
Requires: %libname = %epoch:%version-%release
Group: Development/C
Summary:	Header files for Xerces-C++ validating XML parser
Provides: xerces-c-devel
Provides: libxerces-c-devel
Obsoletes: %{_lib}xerces-c26-devel
Obsoletes: xerces-c
Obsoletes: %{_lib}xerces-c0-devel

%description -n %libdev
Header files you can use to develop XML applications with Xerces-C++.

Xerces-C++ is a validating XML parser written in a portable subset of C++.
Xerces-C++ makes it easy to give your application the ability to read and
write XML data. A shared library is provided for parsing, generating,
manipulating, and validating XML documents.

%files -n %libdev
%defattr(-,root,root,-)
%_libdir/libxerces-c.so
%_libdir/libxerces-depdom.so
%_includedir/xercesc

#----------------------------------------------------------------------

%package doc
Group: Books/Other
Summary:	Documentation for Xerces-C++ validating XML parser
Obsoletes: xerces-c-manual

%description doc
Documentation for Xerces-C++.

Xerces-C++ is a validating XML parser written in a portable subset of C++.
Xerces-C++ makes it easy to give your application the ability to read and
write XML data. A shared library is provided for parsing, generating,
manipulating, and validating XML documents.

%files doc
%defattr(-,root,root,-)
%doc LICENSE.txt STATUS credits.txt Readme.html doc/

#----------------------------------------------------------------------

%prep
%setup -q -n %{name}-src_%{tarversion}
%if "%{_lib}" != "lib"
%patch0 -p1 -b .orig
%endif
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
export XERCESCROOT=%_builddir/%name-src_%{tarversion}

cd $XERCESCROOT/src/xercesc
./runConfigure \
	-plinux \
	-cgcc \
	-xg++ \
	-minmem \
	-nsocket \
	-tnative \
	-rpthreads \
%if %{enable_debug}
	-d \
%endif
%if "%{_lib}" != "lib"
    -b "64" \
%else
    -b "32" \
%endif
    -P %_prefix \
	-C --libdir=%_libdir

make

%install
rm -rf %buildroot

export XERCESCROOT=%_builddir/%name-src_%{tarversion}
cd $XERCESCROOT/src/xercesc
%makeinstall_std

%clean
rm -rf %buildroot



