#
# Conditional build:
# _without_dist_kernel	- without kernel from distribution
#
Summary:	Orinoco wireless cards driver
Summary(pl):	Sterownik kart bezprzewodowych Orinoco
Name:		kernel-pcmcia-orinoco-usb
Version:	0.0.8
%define	rel	0
Release:	%{rel}@%{_kernel_ver_str}
License:	GPL
Group:		Base/Kernel
URL:		http://ranty.ddts.net/~ranty/orinoco/
Source0:	http://ranty.ddts.net/~ranty/orinoco/driver/cvs-%{version}.tar.bz2
# Source0-md5:	f791ac19f39f9e3ba17a7a3f91221fab
%{!?_without_dist_kernel:BuildRequires:	kernel-source}
%{!?_without_dist_kernel:%requires_releq_kernel_up}
Requires(post,postun):	/sbin/depmod
ExclusiveArch:	%{ix86}
Buildroot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Orinoco wireless cards driver (including USB).

%description -l pl
Sterownik kart bezprzewodowych Orinoco (³±cznie z USB).

%package -n kernel-smp-pcmcia-orinoco-usb
Summary:	Orinoco wireless cards SMP driver
Summary(pl):	Sterownik SMP dla bezprzewodowych kart Orinoco
Release:	%{rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{!?_without_dist_kernel:%requires_releq_kernel_up}
Requires(post,postun):	/sbin/depmod

%description -n kernel-smp-pcmcia-orinoco-usb
Orinoco wireless cards driver (including USB). SMP version.

%description -n kernel-smp-pcmcia-orinoco-usb -l pl
Sterownik kart bezprzewodowych Orinoco (w³±czaj±c USB). Wersja dla
j±der wieloprocesorowych.

%prep
%setup -q -n cvs-%{version}

%build
%{__make} \
	CC="%{kgcc}" \
	KERNEL_SRC=%{_kernelsrcdir} \
	EXTRACFLAGS="-D__SMP__ -D_KERNEL_SMP=1"
mkdir smp
mv driver/*.o smp/
%{__make} clean
%{__make} \
	CC="%{kgcc}" \
	KERNEL_SRC=%{_kernelsrcdir} \
	EXTRACFLAGS=""

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}{,smp}/kernel/drivers/net/wireless/

install driver/*.o $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/kernel/drivers/net/wireless/
install smp/*.o $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/kernel/drivers/net/wireless/

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/depmod -a %{!?_without_dist_kernel:-F /boot/System.map-%{_kernel_ver} }%{_kernel_ver}

%postun
/sbin/depmod -a %{!?_without_dist_kernel:-F /boot/System.map-%{_kernel_ver} }%{_kernel_ver}

%post	-n kernel-smp-pcmcia-orinoco-usb
/sbin/depmod -a %{!?_without_dist_kernel:-F /boot/System.map-%{_kernel_ver}smp }%{_kernel_ver}smp

%postun	-n kernel-smp-pcmcia-orinoco-usb
/sbin/depmod -a %{!?_without_dist_kernel:-F /boot/System.map-%{_kernel_ver}smp }%{_kernel_ver}smp

%files
%defattr(644,root,root,755)
%doc firmware/Makefile README util/*.c
/lib/modules/%{_kernel_ver}/kernel/drivers/net/wireless/*

%files -n kernel-smp-pcmcia-orinoco-usb
%defattr(644,root,root,755)
%doc firmware/Makefile README util/*.c
/lib/modules/%{_kernel_ver}smp/kernel/drivers/net/wireless/*
