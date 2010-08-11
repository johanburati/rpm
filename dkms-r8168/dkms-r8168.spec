%define module r8168

Summary: Driver for RTL8111/RTL8168 PCI Express Gigabit Ethernet controllers
Name: dkms-%{module}
Version: 8.018.00
Release: 1
Vendor: Realtek
License: GPL+
Group: System Environment/Kernel
URL: http://www.realtek.com/
# the ftp access is password protected, download the file manually via the following url:
# http://www.realtek.com/downloads/downloadsView.aspx?Langid=1&PNid=13&PFid=5&Level=5&Conn=4&DownTypeID=3&GetDown=false#2
Source: ftp://207.232.93.28/cn/nic/%{module}-%{version}.tar.bz2
Patch1: %{module}-modversions.patch
Patch2: %{module}-makefile.patch
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch: noarch
Requires: gcc, make
Requires(post): dkms
Requires(preun): dkms

%description
Driver (Linux kernel module) for RTL8111B/RTL8168B/RTL8111/RTL8168/RTL8111C
PCI Express Gigabit Ethernet controllers.

%prep
%setup -n %{module}-%{version}
%patch1 -p1 -b .modversions
%patch2 -p1 -b .makefile

%build

%install
%{__rm} -rf %{buildroot}

%define dkms_name %{module}
%define dkms_vers %{version}-%{release}
%define quiet -q

# Kernel module sources install for dkms
%{__mkdir_p} %{buildroot}%{_usrsrc}/%{dkms_name}-%{dkms_vers}/
%{__cp} -a src/* %{buildroot}%{_usrsrc}/%{dkms_name}-%{dkms_vers}/

# Configuration for dkms
%{__cat} <<'EOF' >%{buildroot}%{_usrsrc}/%{dkms_name}-%{dkms_vers}/dkms.conf
PACKAGE_NAME=%{dkms_name}
PACKAGE_VERSION=%{dkms_vers}
MAKE[0]="make KVER=${kernelver}"
CLEAN[0]="make clean"
BUILT_MODULE_NAME[0]=%{dkms_name}
DEST_MODULE_LOCATION[0]=/kernel/drivers/net
AUTOINSTALL="YES"
EOF

%clean
%{__rm} -rf %{buildroot}

%post
dkms add -m %{dkms_name} -v %{dkms_vers} %{?quiet} || :
dkms build -m %{dkms_name} -v %{dkms_vers} %{?quiet} || :
dkms install -m %{dkms_name} -v %{dkms_vers} %{?quiet} --force || :

%preun
# Remove all versions from DKMS registry
dkms remove -m %{dkms_name} -v %{dkms_vers} %{?quiet} --all || :

%files
%defattr(-, root, root, -)
%doc README
%{_usrsrc}/%{dkms_name}-%{dkms_vers}/

%changelog
* Tue Aug 08 2010 Johan Burati <johan.burati@gmail.com> - 8.018.00-1
- Version update

* Wed Jan 07 2009 Manuel "lonely wolf" Wolfshant <wolfy@fedoraproject.org> - 8.010.00-1
- Version update

* Thu Nov 13 2008 Manuel "lonely wolf" Wolfshant <wolfy@fedoraproject.org> - 8.009.00-1
- Version update

* Mon Aug 18 2008 Manuel "lonely wolf" Wolfshant <wolfy@fedoraproject.org> - 8.008.00-1
- Version update

* Thu May 18 2008 Manuel "lonely wolf" Wolfshant <wolfy@fedoraproject.org> - 8.006.00-1
- Version update

* Tue Mar 18 2008 Manuel "lonely wolf" Wolfshant <wolfy@fedoraproject.org> - 8.005.00-1
- Version update

* Mon Feb 06 2008 Manuel "lonely wolf" Wolfshant <wolfy@fedoraproject.org> - 8.004.00-1
- Initial rpm version. Shamelessly copy from dkms-r1000 by Matthias Saou
