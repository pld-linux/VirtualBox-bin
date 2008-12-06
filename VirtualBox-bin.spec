#

# disable debug - no symbols here
%define		_enable_debug_packages	0

%ifarch %{x8664}
%define		arch	amd64
%else
%define		arch	x86
%endif

%define		prev	39760
%define		pname	VirtualBox
Summary:	VirtualBox - x86 hardware virtualizer
Summary(pl.UTF-8):	VirtualBox - wirtualizator sprzętu x86
Name:		%{pname}-bin
Version:	2.0.6
Release:	0.9
License:	Free for non-commercial use, non-distributable
Group:		Applications/Emulators
#Source0:	http://download.virtualbox.org/virtualbox/%{version}/%{pname}-%{version}-%{prev}-Linux_%{arch}.run
Source0:	%{pname}-%{version}-%{prev}-Linux_%{arch}.run
NoSource:	0
# NoSource0-md5:	dfb62b048a58a14691b93356a5824bec
#Source1:	http://download.virtualbox.org/virtualbox/%{version}/UserManual.pdf
Source1:	UserManual.pdf
# Source1-md5:	691682f681a8289cac7f9b1f550b94a0
Source2:	%{pname}.desktop
Source3:	%{pname}.sh
URL:		http://www.virtualbox.org/
BuildRequires:	ffmpeg-libs
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

%prep
%setup -qcT
%{__sh} %{SOURCE0} --noexec --keep
%{__tar} -jxf install/VirtualBox.tar.bz2

install %{SOURCE1} .
sed 's#@LIBDIR@#%{_libdir}#' < %{SOURCE3} > VirtualBox-wrapper.sh

%install
rm -rf $RPM_BUILD_ROOT

install -d \
	$RPM_BUILD_ROOT{%{_bindir},%{_pixmapsdir},%{_desktopdir}} \
	$RPM_BUILD_ROOT%{_libdir}/VirtualBox

install VirtualBox-wrapper.sh $RPM_BUILD_ROOT%{_libdir}/VirtualBox
for f in {VBox{Headless,Manage,SDL,SVC,Tunctl,XPCOMIPCD},VirtualBox}; do
	install $f $RPM_BUILD_ROOT%{_libdir}/VirtualBox/$f
	ln -s %{_libdir}/VirtualBox/VirtualBox-wrapper.sh $RPM_BUILD_ROOT%{_bindir}/$f
done

%ifarch %{x8664}
install VBox*.rel \
        $RPM_BUILD_ROOT%{_libdir}/VirtualBox
%endif

install libVBoxQt*.so.* VBox*.so VirtualBox.so \
	$RPM_BUILD_ROOT%{_libdir}/VirtualBox
install VBox{DD,DD2}{GC.gc,R0.r0} VMM{GC.gc,R0.r0} \
	$RPM_BUILD_ROOT%{_libdir}/VirtualBox

cp -a additions components nls $RPM_BUILD_ROOT%{_libdir}/VirtualBox
install License-7.html $RPM_BUILD_ROOT%{_libdir}/VirtualBox

install VBox.png $RPM_BUILD_ROOT%{_pixmapsdir}/VBox.png
install %{SOURCE2} $RPM_BUILD_ROOT%{_desktopdir}/%{pname}.desktop

# required by VBoxFFmpegFB.so
ln -s %{_libdir}/libavcodec.so.5? $RPM_BUILD_ROOT%{_libdir}/VirtualBox/libavcodec.so.51
ln -s %{_libdir}/libavformat.so.5? $RPM_BUILD_ROOT%{_libdir}/VirtualBox/libavformat.so.51

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -g 221 -r -f vbox

%postun
if [ "$1" = "0" ]; then
	%groupremove vbox
fi

%files
%defattr(644,root,root,755)
%doc UserManual.pdf
%dir %{_libdir}/VirtualBox
%dir %{_libdir}/VirtualBox/additions
%dir %{_libdir}/VirtualBox/components
%dir %{_libdir}/VirtualBox/nls
%attr(755,root,root) %{_bindir}/VBox*
%attr(755,root,root) %{_bindir}/VirtualBox
%attr(755,root,root) %{_libdir}/VirtualBox/VBoxSVC
%attr(4755,root,root) %{_libdir}/VirtualBox/VBoxHeadless
%attr(755,root,root) %{_libdir}/VirtualBox/VBoxManage
%attr(4755,root,root) %{_libdir}/VirtualBox/VBoxSDL
%attr(755,root,root) %{_libdir}/VirtualBox/VBoxTunctl
%attr(755,root,root) %{_libdir}/VirtualBox/VBoxXPCOMIPCD
%attr(755,root,root) %{_libdir}/VirtualBox/VBox*.so
%attr(755,root,root) %{_libdir}/VirtualBox/libVBox*.so.*
%ifarch %{x8664}
%attr(755,root,root) %{_libdir}/VirtualBox/VBox*.rel
%endif
%attr(4755,root,root) %{_libdir}/VirtualBox/VirtualBox
%attr(755,root,root) %{_libdir}/VirtualBox/VirtualBox.so
%attr(755,root,root) %{_libdir}/VirtualBox/VirtualBox-wrapper.sh
%attr(755,root,root) %{_libdir}/VirtualBox/libav*.so.*
%{_libdir}/VirtualBox/*.gc
%{_libdir}/VirtualBox/*.r0
%{_libdir}/VirtualBox/additions/*
%{_libdir}/VirtualBox/components/*
%{_libdir}/VirtualBox/License-7.html
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
%lang(zh_CN) %{_libdir}/VirtualBox/nls/*_zh_CN.qm
%lang(zh_TW) %{_libdir}/VirtualBox/nls/*_zh_TW.qm
%{_pixmapsdir}/VBox.png
%{_desktopdir}/%{pname}.desktop
