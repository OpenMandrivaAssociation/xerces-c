%define tarversion 2_7_0

%define major 27
%define minor 0

%define libname %mklibname xerces-c %minor

Name:	xerces-c
Version:	2.7.0
Release:	%mkrel 4
Epoch: 1
URL:	http://xml.apache.org/xerces-c/
License:	Apache
Source0: %{name}-src_%{tarversion}.tar.gz
Patch0: xerces-c-lib64.patch
# Most of apps 
Patch1: xerces-c-pvtheader.patch
Summary:	Xerces-C++ validating XML parser
Group: System/Libraries
BuildRoot: %{_tmppath}/%{name}-root
BuildRequires: zlib-devel
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

%files
%defattr(-,root,root,-)
%_prefix/bin/*

#----------------------------------------------------------------------

%package -n %libname
Group: System/Libraries
Summary: xerces-c library

%description -n %libname
xerces-c library

%post -n %libname -p /sbin/ldconfig
%postun -n %libname -p /sbin/ldconfig

%files -n %libname
%defattr(-,root,root,-)
%_libdir/libxerces-*.so.*

#----------------------------------------------------------------------

%package -n %libname-devel
Requires: %libname = %epoch:%version-%release
Group: Books/Other
Summary:	Header files for Xerces-C++ validating XML parser
Provides: xerces-c-devel
Provides: libxerces-c-devel
Obsoletes: %{_lib}xerces-c26-devel

%description -n %libname-devel
Header files you can use to develop XML applications with Xerces-C++.

Xerces-C++ is a validating XML parser written in a portable subset of C++.
Xerces-C++ makes it easy to give your application the ability to read and
write XML data. A shared library is provided for parsing, generating,
manipulating, and validating XML documents.

%files -n %libname-devel
%defattr(-,root,root,-)
%_libdir/libxerces-c.so
%_libdir/libxerces-depdom.so
%_includedir/xercesc
%_datadir/%{name}/samples

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
	-P%_prefix 

make

cd $XERCESCROOT/samples
./runConfigure \
	-plinux \
	-cgcc \
	-xg++

%make


%install
rm -rf %buildroot

export XERCESCROOT=%_builddir/%name-src_%{tarversion}
cd $XERCESCROOT/src/xercesc
%makeinstall_std

mkdir -p %buildroot%_bindir
#we don't want obj directory
install `find $XERCESCROOT/bin -type f -maxdepth 1` %buildroot%_bindir
mkdir -p %buildroot%_datadir/%name
cp -a $XERCESCROOT/samples %buildroot%_datadir/%name

%clean
rm -rf %buildroot



