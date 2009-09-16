#
%bcond_without  dist_kernel     # without distribution kernel
%bcond_without  kernel          # don't build kernel module
%bcond_without  userspace       # don't build userspace package
%bcond_with     verbose 	# verbose kernel mod build

# disable debug - no symbols here
%define		_enable_debug_packages	0
%define		rel	1
%ifarch %{x8664}
%define		arch	amd64
%define		prev	52130
%else
%define		arch	x86
%define		prev	52128
%endif

%define		pname	VirtualBox
Summary:	VirtualBox - x86 hardware virtualizer
Summary(pl.UTF-8):	VirtualBox - wirtualizator sprzętu x86
Name:		%{pname}-bin
Version:	3.0.6
Release:	%{rel}
License:	Free for non-commercial use, non-distributable
Group:		Applications/Emulators
#Source0:	http://download.virtualbox.org/virtualbox/%{version}/%{pname}-%{version}-%{prev}-Linux_%{arch}.run
Source0:	%{pname}-%{version}-%{prev}-Linux_%{arch}.run
NoSource:	0
#Source1:	http://download.virtualbox.org/virtualbox/%{version}/UserManual.pdf
Source1:	UserManual.pdf
# Source1-md5:	7b9dcaa2339f122db12228c6501c2176
Source3:        %{pname}-vboxdrv.init
Source4:        %{pname}-vboxadd.init
Source5:        %{pname}-vboxnetadp.init
Source6:        %{pname}-vboxnetflt.init
Source7:        %{pname}-vboxvfs.init
Source8:        %{pname}.desktop
Source9:        %{pname}.sh
URL:		http://www.virtualbox.org/
%{?with_userspace:BuildRequires:	ffmpeg-libs}
BuildRequires:	rpmbuild(macros) >= 1.379
Requires(post,preun):	/sbin/chkconfig
Requires(postun):	/usr/sbin/groupdel
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Suggests:	gxmessage
Provides:	group(vbox)
Conflicts:	%{pname}
ExclusiveArch:	%{ix86} %{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define	_noautoreq	libavcodec.so.51 libavformat.so.51

%description
Sun VirtualBox is a general-purpose full virtualizer for x86 hardware.
Targeted at server, desktop and embedded use.

Some of the features of VirtualBox are:

Modularity: VirtualBox has an extremely modular design with
well-defined internal programming interfaces and a client/server
design. This makes it easy to control it from several interfaces at
once: for example, you can start a virtual machine in a typical
virtual machine GUI and then control that machine from the command
line.

Virtual machine descriptions in XML: the configuration settings of
virtual machines are stored entirely in XML and are independent of the
local machines. Virtual machine definitions can therefore easily be
ported to other computers.

%description -l pl.UTF-8
Sun VirtualBox jest emulatorem sprzętu x86. Kierowany do zastosowań
serwerowych, desktopowych oraz wbudowanych.

Przykładowe cechy VirtualBoksa:

Modularność: VirtualBox jest wysoce zmodularyzowanym produktem z
dobrze zaprojektowanym wewnętrznym interfejsem programowym typu
klient/serwer. Dzięki temu można łatwo kontrolować go za pomocą
różnych interfejsów. Można na przykład uruchomić maszynę wirtualną z
poziomu interfejsu graficznego, a później kontrolować ją z linii
poleceń. VirtualBox dostarcza również pełny pakiet deweloperski, co
pozwala stworzyć dowolny inny interfejs zarządzania maszyną wirtualną.

Opisy maszyn wirtualnych w XML-u: konfiguracje poszczególnych maszyn
wirtualnych są w całości przechowywane w XML-u i są niezależne od
lokalnej maszyny. Dzięki temu można szybko i łatwo przenieść
konfigurację maszyny wirtualnej na inny komputer.

%package udev
Summary:	udev rules for VirtualBox kernel modules
Summary(pl.UTF-8):	Reguły udev dla modułów jądra Linuksa dla VirtualBoksa
Release:	%{rel}
Group:		Base/Kernel
Requires:	udev-core

%description udev
udev rules for VirtualBox kernel modules.

%description udev -l pl.UTF-8
Reguły udev dla modułów jądra Linuksa dla VirtualBoksa.

%package -n kernel%{_alt_kernel}-misc-vboxadd
Summary:	VirtualBox Guest Additions for Linux Module
Summary(pl.UTF-8):	Moduł jądra Linuksa dla VirtualBoksa
Release:	%{rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
Requires:	dev >= 2.9.0-7
%if %{with dist_kernel}
%requires_releq_kernel
Requires(postun):	%releq_kernel
%endif
Provides:	kernel(vboxadd) = %{version}-%{rel}

%description -n kernel%{_alt_kernel}-misc-vboxadd
VirtualBox Guest Additions for Linux Module.

%description -n kernel%{_alt_kernel}-misc-vboxadd -l pl.UTF-8
Moduł jądra Linuksa vboxadd dla VirtualBoksa - dodatki dla
systemu gościa.

%package -n kernel%{_alt_kernel}-misc-vboxdrv
Summary:	VirtualBox Support Driver
Summary(pl.UTF-8):	Moduł jądra Linuksa dla VirtualBoksa
Release:	%{rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
Requires:	dev >= 2.9.0-7
%if %{with dist_kernel}
%requires_releq_kernel
Requires(postun):	%releq_kernel
%endif
Provides:	kernel(vboxdrv) = %{version}-%{rel}

%description -n kernel%{_alt_kernel}-misc-vboxdrv
VirtualBox Support Driver.

%description -n kernel%{_alt_kernel}-misc-vboxdrv -l pl.UTF-8
Moduł jądra Linuksa dla VirtualBoksa - sterownik wsparcia dla
systemu głównego.

%package -n kernel%{_alt_kernel}-misc-vboxnetadp
Summary:	VirtualBox Linux Host Virtual Network Adapter Driver
Release:	%{rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
Requires:	dev >= 2.9.0-7
Requires:	kernel%{_alt_kernel}-misc-vboxdrv
%if %{with dist_kernel}
%requires_releq_kernel
Requires(postun):	%releq_kernel
%endif
Provides:	kernel(vboxnetadp) = %{version}-%{rel}

%description -n kernel%{_alt_kernel}-misc-vboxnetadp
This is a kernel module that creates a virtual interface that
can be attached to an internal network.

%package -n kernel%{_alt_kernel}-misc-vboxnetflt
Summary:	VirtualBox Linux Host Network Filter Driver
Summary(pl.UTF-8):	Moduł jądra Linuksa dla VirtualBoksa
Release:	%{rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
Requires:	dev >= 2.9.0-7
Requires:	kernel%{_alt_kernel}-misc-vboxdrv
%if %{with dist_kernel}
%requires_releq_kernel
Requires(postun):	%releq_kernel
%endif
Provides:	kernel(vboxnetflt) = %{version}-%{rel}

%description -n kernel%{_alt_kernel}-misc-vboxnetflt
This is a kernel module that attaches to a real interface on the
host and filters and injects packets.

%description -n kernel%{_alt_kernel}-misc-vboxnetflt -l pl.UTF-8
Moduł jądra Linuksa dla VirtualBoksa - sterownik filtrowania
sieci dla systemu głównego.

%package -n kernel%{_alt_kernel}-misc-vboxvfs
Summary:	Host file system access VFS for VirtualBox
Summary(pl.UTF-8):	Moduł jądra Linuksa dla VirtualBoksa
Release:	%{rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
Requires:	dev >= 2.9.0-7
Requires:	kernel%{_alt_kernel}-misc-vboxadd
%if %{with dist_kernel}
%requires_releq_kernel
Requires(postun):	%releq_kernel
%endif
Provides:	kernel(vboxvfs) = %{version}-%{rel}

%description -n kernel%{_alt_kernel}-misc-vboxvfs
Host file system access VFS for VirtualBox.

%description -n kernel%{_alt_kernel}-misc-vboxvfs -l pl.UTF-8
Moduł jądra Linuksa dla VirtualBoksa - dostęp do plików
systemu głównego z poziomu systemu gościa.

%package -n xorg-driver-input-vboxmouse
Summary:	X.org mouse driver for VirtualBox guest OS
Summary(pl.UTF-8):	Sterownik myszy dla systemu gościa w VirtualBoksie
Release:	%{rel}
Group:		X11/Applications
Requires:	xorg-xserver-server >= 1.0.99.901

%description -n xorg-driver-input-vboxmouse
X.org mouse driver for VirtualBox guest OS.

%description -n xorg-driver-input-vboxmouse  -l pl.UTF-8
Sterownik myszy dla systemu gościa w VirtualBoksie.

%package -n xorg-driver-video-vboxvideo
Summary:	X.org video driver for VirtualBox guest OS
Summary(pl.UTF-8):	Sterownik grafiki dla systemu gościa w VirtualBoksie
Release:	%{rel}
Group:		X11/Applications
Requires:	xorg-xserver-server >= 1.0.99.901

%description -n xorg-driver-video-vboxvideo
X.org video driver for VirtualBox guest OS.

%description -n xorg-driver-video-vboxvideo -l pl.UTF-8
Sterownik grafiki dla systemu gościa w VirtualBoksie.

%prep
%setup -qcT
%{__sh} %{SOURCE0} --noexec --keep
%{__tar} -jxf install/VirtualBox.tar.bz2

cat <<'EOF' > udev.conf
KERNEL=="vboxdrv", NAME="%k", GROUP="vbox", MODE="0660"
KERNEL=="vboxadd", NAME="%k", GROUP="vbox", MODE="0660"
KERNEL=="vboxnetctl", NAME="%k", GROUP="vbox", MODE="0660"
EOF

install %{SOURCE1} .
sed 's#@LIBDIR@#%{_libdir}#' < %{SOURCE9} > VirtualBox-wrapper.sh

rm -rf PLD-MODULE-BUILD && mkdir PLD-MODULE-BUILD && cd PLD-MODULE-BUILD
cp -rdf ../src/* ./
sed -i -e 's/-DVBOX_WITH_HARDENING//g' vboxdrv/Makefile
sed -i -e 's/-DVBOX_WITH_HARDENING//g' vboxnetadp/Makefile
sed -i -e 's/-DVBOX_WITH_HARDENING//g' vboxnetflt/Makefile

%build
%if %{with kernel}
cd PLD-MODULE-BUILD
%build_kernel_modules -m vboxdrv -C vboxdrv
cp -a vboxdrv/Module.symvers vboxnetadp/
%build_kernel_modules -m vboxnetadp -C vboxnetadp
cp -a vboxdrv/Module.symvers vboxnetflt/
%build_kernel_modules -m vboxnetflt -C vboxnetflt
cd ..
%endif


%install
rm -rf $RPM_BUILD_ROOT

%if %{with userspace}
install -d \
	$RPM_BUILD_ROOT{%{_bindir},%{_pixmapsdir},%{_desktopdir}} \
	$RPM_BUILD_ROOT%{_libdir}/VirtualBox/components

install VirtualBox-wrapper.sh $RPM_BUILD_ROOT%{_libdir}/VirtualBox
for f in {VBox{Headless,Manage,Net{AdpCtl,DHCP},SDL,SysInfo.sh,SVC,TestOGL,Tunctl,XPCOMIPCD,.sh},VirtualBox,rdesktop-vrdp,vboxwebsrv,webtest}; do
	install $f $RPM_BUILD_ROOT%{_libdir}/VirtualBox/$f
done

for f in {VBox{Headless,Manage,SDL,VRDP},VirtualBox,rdesktop-vrdp,vboxwebsrv}; do
	ln -s %{_libdir}/VirtualBox/VirtualBox-wrapper.sh $RPM_BUILD_ROOT%{_bindir}/$f
done

install libQt*.so.* VBox*.so VirtualBox.so VRDPAuth.so \
	$RPM_BUILD_ROOT%{_libdir}/VirtualBox
install VBox{DD,DD2}{GC.gc,R0.r0} VMM{GC.gc,R0.r0} \
	$RPM_BUILD_ROOT%{_libdir}/VirtualBox

for f in VBox{DDU,REM,RT,VMM,XPCOM}.so; do
	ln -s %{_libdir}/VirtualBox/$f $RPM_BUILD_ROOT%{_libdir}/VirtualBox/components/$f
done

cp -a accessible additions components nls rdesktop-vrdp-keymaps $RPM_BUILD_ROOT%{_libdir}/VirtualBox
install License-7.html $RPM_BUILD_ROOT%{_libdir}/VirtualBox

install VBox.png $RPM_BUILD_ROOT%{_pixmapsdir}/VBox.png
install %{SOURCE8} $RPM_BUILD_ROOT%{_desktopdir}/%{pname}.desktop

install VirtualBox.chm $RPM_BUILD_ROOT%{_libdir}/VirtualBox

# required by VBoxFFmpegFB.so
ln -s %{_libdir}/libavcodec.so.5? $RPM_BUILD_ROOT%{_libdir}/VirtualBox/libavcodec.so.51
ln -s %{_libdir}/libavformat.so.5? $RPM_BUILD_ROOT%{_libdir}/VirtualBox/libavformat.so.51

install -d $RPM_BUILD_ROOT/etc/udev/rules.d
install udev.conf $RPM_BUILD_ROOT/etc/udev/rules.d/virtualbox.rules
%endif

%if %{with kernel}
install -d $RPM_BUILD_ROOT/etc/rc.d/init.d
install %{SOURCE3} $RPM_BUILD_ROOT/etc/rc.d/init.d/vboxdrv
install %{SOURCE5} $RPM_BUILD_ROOT/etc/rc.d/init.d/vboxnetadp
install %{SOURCE6} $RPM_BUILD_ROOT/etc/rc.d/init.d/vboxnetflt
%install_kernel_modules -m PLD-MODULE-BUILD/vboxdrv/vboxdrv -d misc
%install_kernel_modules -m PLD-MODULE-BUILD/vboxnetadp/vboxnetadp -d misc
%install_kernel_modules -m PLD-MODULE-BUILD/vboxnetflt/vboxnetflt -d misc
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -g 221 -r -f vbox

%post
cat << 'EOF'
NOTE: You must also install kernel module for this software to work
  kernel-misc-vboxdrv-%{version}-%{rel}@%{_kernel_ver_str}
  kernel-desktop-misc-vboxdrv-%{version}-%{rel}@%{_kernel_ver_str}
  kernel-laptop-misc-vboxdrv-%{version}-%{rel}@%{_kernel_ver_str}
  kernel-vanilla-misc-vboxdrv-%{version}-%{rel}@%{_kernel_ver_str}
  etc.

Depending on which kernel brand You use.

EOF

%postun
if [ "$1" = "0" ]; then
	%groupremove vbox
fi

%post	-n kernel%{_alt_kernel}-misc-vboxdrv
%depmod %{_kernel_ver}
/sbin/chkconfig --add vboxdrv
%service vboxdrv restart "VirtualBox driver"

%postun	-n kernel%{_alt_kernel}-misc-vboxdrv
%depmod %{_kernel_ver}

%preun -n kernel%{_alt_kernel}-misc-vboxdrv
if [ "$1" = "0" ]; then
	%service vboxdrv stop
	/sbin/chkconfig --del vboxdrv
fi

%post	-n kernel%{_alt_kernel}-misc-vboxnetadp
%depmod %{_kernel_ver}
/sbin/chkconfig --add vboxnetadp
%service vboxnetadp restart "VirtualBox Network Adapter driver"

%postun	-n kernel%{_alt_kernel}-misc-vboxnetadp
%depmod %{_kernel_ver}

%preun -n kernel%{_alt_kernel}-misc-vboxnetadp
if [ "$1" = "0" ]; then
	%service vboxnetadp stop
	/sbin/chkconfig --del vboxnetadp
fi

%post	-n kernel%{_alt_kernel}-misc-vboxnetflt
%depmod %{_kernel_ver}
/sbin/chkconfig --add vboxnetflt
%service vboxnetflt restart "VirtualBox Network Filter driver"

%postun	-n kernel%{_alt_kernel}-misc-vboxnetflt
%depmod %{_kernel_ver}

%preun -n kernel%{_alt_kernel}-misc-vboxnetflt
if [ "$1" = "0" ]; then
	%service vboxnetflt stop
	/sbin/chkconfig --del vboxnetflt
fi

%if %{with userspace}
%files
%defattr(644,root,root,755)
%doc UserManual.pdf
%dir %{_libdir}/VirtualBox
%dir %{_libdir}/VirtualBox/accessible
%dir %{_libdir}/VirtualBox/additions
%dir %{_libdir}/VirtualBox/components
%dir %{_libdir}/VirtualBox/nls
%attr(755,root,root) %{_bindir}/VBoxHeadless
%attr(755,root,root) %{_bindir}/VBoxManage
%attr(755,root,root) %{_bindir}/VBoxSDL
%attr(755,root,root) %{_bindir}/VBoxVRDP
%attr(755,root,root) %{_bindir}/VirtualBox
%attr(755,root,root) %{_bindir}/rdesktop-vrdp
%attr(755,root,root) %{_bindir}/vboxwebsrv
%attr(755,root,root) %{_libdir}/VirtualBox/VBoxSVC
%attr(4755,root,root) %{_libdir}/VirtualBox/VBoxHeadless
%attr(755,root,root) %{_libdir}/VirtualBox/VBoxManage
%attr(4755,root,root) %{_libdir}/VirtualBox/VBoxNetAdpCtl
%attr(4755,root,root) %{_libdir}/VirtualBox/VBoxNetDHCP
%attr(4755,root,root) %{_libdir}/VirtualBox/VBoxSDL
%attr(755,root,root) %{_libdir}/VirtualBox/VBoxTestOGL
%attr(755,root,root) %{_libdir}/VirtualBox/VBoxTunctl
%attr(755,root,root) %{_libdir}/VirtualBox/VBoxXPCOMIPCD
%attr(755,root,root) %{_libdir}/VirtualBox/VBoxDbg.so
%attr(755,root,root) %{_libdir}/VirtualBox/VBoxDD2.so
%attr(755,root,root) %{_libdir}/VirtualBox/VBoxDD.so
%attr(755,root,root) %{_libdir}/VirtualBox/VBoxDDU.so
%attr(755,root,root) %{_libdir}/VirtualBox/VBoxGuestPropSvc.so
%attr(755,root,root) %{_libdir}/VirtualBox/VBoxHeadless.so
%attr(755,root,root) %{_libdir}/VirtualBox/VBoxKeyboard.so
%attr(755,root,root) %{_libdir}/VirtualBox/VBoxNetDHCP.so
%attr(755,root,root) %{_libdir}/VirtualBox/VBoxOGLhostcrutil.so
%attr(755,root,root) %{_libdir}/VirtualBox/VBoxOGLhosterrorspu.so
%attr(755,root,root) %{_libdir}/VirtualBox/VBoxOGLrenderspu.so
%attr(755,root,root) %{_libdir}/VirtualBox/VBoxPython2_6.so
%attr(755,root,root) %{_libdir}/VirtualBox/VBoxPython.so
%attr(755,root,root) %{_libdir}/VirtualBox/VBoxREM.so
%ifarch %{ix86}
%attr(755,root,root) %{_libdir}/VirtualBox/VBoxREM32.so
%attr(755,root,root) %{_libdir}/VirtualBox/VBoxREM64.so
%endif
%attr(755,root,root) %{_libdir}/VirtualBox/VBoxRT.so
%attr(755,root,root) %{_libdir}/VirtualBox/VBoxSDL.so
%attr(755,root,root) %{_libdir}/VirtualBox/VBoxSettings.so
%attr(755,root,root) %{_libdir}/VirtualBox/VBoxSharedClipboard.so
%attr(755,root,root) %{_libdir}/VirtualBox/VBoxSharedCrOpenGL.so
%attr(755,root,root) %{_libdir}/VirtualBox/VBoxSharedFolders.so
%attr(755,root,root) %{_libdir}/VirtualBox/VBoxVMM.so
%attr(755,root,root) %{_libdir}/VirtualBox/VBoxVRDP.so
%attr(755,root,root) %{_libdir}/VirtualBox/VBoxXPCOMC.so
%attr(755,root,root) %{_libdir}/VirtualBox/VBoxXPCOM.so
%attr(755,root,root) %{_libdir}/VirtualBox/libQtCoreVBox.so.4
%attr(755,root,root) %{_libdir}/VirtualBox/libQtGuiVBox.so.4
%attr(755,root,root) %{_libdir}/VirtualBox/libQtNetworkVBox.so.4
%attr(755,root,root) %{_libdir}/VirtualBox/VRDPAuth.so
%attr(4755,root,root) %{_libdir}/VirtualBox/VirtualBox
%attr(755,root,root) %{_libdir}/VirtualBox/VirtualBox.so
%attr(755,root,root) %{_libdir}/VirtualBox/VirtualBox-wrapper.sh
%attr(755,root,root) %{_libdir}/VirtualBox/VBox.sh
%attr(755,root,root) %{_libdir}/VirtualBox/VBoxSysInfo.sh
%attr(755,root,root) %{_libdir}/VirtualBox/libavcodec.so.51
%attr(755,root,root) %{_libdir}/VirtualBox/libavformat.so.51
%attr(755,root,root) %{_libdir}/VirtualBox/rdesktop-vrdp
%attr(755,root,root) %{_libdir}/VirtualBox/vboxwebsrv
%attr(755,root,root) %{_libdir}/VirtualBox/webtest
# isn't it already packaged somewhere in the system?
%attr(755,root,root) %{_libdir}/VirtualBox/accessible/libqtaccessiblewidgets.so
%{_libdir}/VirtualBox/VBoxDD2GC.gc
%{_libdir}/VirtualBox/VBoxDDGC.gc
%{_libdir}/VirtualBox/VMMGC.gc
%{_libdir}/VirtualBox/VBoxDD2R0.r0
%{_libdir}/VirtualBox/VBoxDDR0.r0
%{_libdir}/VirtualBox/VMMR0.r0
%{_libdir}/VirtualBox/additions/VBoxGuestAdditions.iso
%{_libdir}/VirtualBox/components/VBoxC.so
%{_libdir}/VirtualBox/components/VBoxDDU.so
%{_libdir}/VirtualBox/components/VBoxREM.so
%{_libdir}/VirtualBox/components/VBoxRT.so
%{_libdir}/VirtualBox/components/VBoxSVCM.so
%{_libdir}/VirtualBox/components/VBoxVMM.so
%{_libdir}/VirtualBox/components/VBoxXPCOMBase.xpt
%{_libdir}/VirtualBox/components/VBoxXPCOMIPCC.so
%{_libdir}/VirtualBox/components/VBoxXPCOM.so
%{_libdir}/VirtualBox/components/VirtualBox_XPCOM.xpt
%{_libdir}/VirtualBox/rdesktop-vrdp-keymaps
%{_libdir}/VirtualBox/License-7.html
%{_libdir}/VirtualBox/VirtualBox.chm
%lang(bg) %{_libdir}/VirtualBox/nls/*_bg.qm
%lang(ca) %{_libdir}/VirtualBox/nls/*_ca.qm
%lang(cs) %{_libdir}/VirtualBox/nls/*_cs.qm
%lang(de) %{_libdir}/VirtualBox/nls/*_de.qm
%lang(es) %{_libdir}/VirtualBox/nls/*_es.qm
%lang(eu) %{_libdir}/VirtualBox/nls/*_eu.qm
%lang(fi) %{_libdir}/VirtualBox/nls/*_fi.qm
%lang(fr) %{_libdir}/VirtualBox/nls/*_fr.qm
%lang(hu) %{_libdir}/VirtualBox/nls/*_hu.qm
%lang(id) %{_libdir}/VirtualBox/nls/*_id.qm
%lang(it) %{_libdir}/VirtualBox/nls/*_it.qm
%lang(ja) %{_libdir}/VirtualBox/nls/*_ja.qm
%lang(km_KH) %{_libdir}/VirtualBox/nls/*_km_KH.qm
%lang(ko) %{_libdir}/VirtualBox/nls/*_ko.qm
%lang(pl) %{_libdir}/VirtualBox/nls/*_pl.qm
%lang(pt) %{_libdir}/VirtualBox/nls/*_pt.qm
%lang(pt_BR) %{_libdir}/VirtualBox/nls/*_pt_BR.qm
%lang(ro) %{_libdir}/VirtualBox/nls/*_ro.qm
%lang(ru) %{_libdir}/VirtualBox/nls/*_ru.qm
%lang(sk) %{_libdir}/VirtualBox/nls/*_sk.qm
%lang(sr) %{_libdir}/VirtualBox/nls/*_sr.qm
%lang(sv) %{_libdir}/VirtualBox/nls/*_sv.qm
%lang(tr) %{_libdir}/VirtualBox/nls/*_tr.qm
%lang(uk) %{_libdir}/VirtualBox/nls/*_uk.qm
%lang(zh_CN) %{_libdir}/VirtualBox/nls/*_zh_CN.qm
%lang(zh_TW) %{_libdir}/VirtualBox/nls/*_zh_TW.qm
%{_pixmapsdir}/VBox.png
%{_desktopdir}/%{pname}.desktop

%files udev
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) /etc/udev/rules.d/virtualbox.rules
%endif

%if %{with kernel}
%files -n kernel%{_alt_kernel}-misc-vboxdrv
%defattr(644,root,root,755)
%attr(754,root,root) /etc/rc.d/init.d/vboxdrv
/lib/modules/%{_kernel_ver}/misc/vboxdrv.ko*

%files -n kernel%{_alt_kernel}-misc-vboxnetadp
%defattr(644,root,root,755)
%attr(754,root,root) /etc/rc.d/init.d/vboxnetadp
/lib/modules/%{_kernel_ver}/misc/vboxnetadp.ko*

%files -n kernel%{_alt_kernel}-misc-vboxnetflt
%defattr(644,root,root,755)
%attr(754,root,root) /etc/rc.d/init.d/vboxnetflt
/lib/modules/%{_kernel_ver}/misc/vboxnetflt.ko*
%endif
