# Made by Y. Pavlov <ympavlov@gmail.com>
# Based on spec file by Alexander Kazantcev <kazancas@mail.ru> from EduMandriva <edumandriva.ru>

Summary:	Dictionary Shell on Qt4
Name:		lightlang
Version:	0.8.6
Release:	rev927
License:	GPL
Group:		Applications/Office
URL:		http://lightlang.org.ru/

Packager:	Yuri Pavlov <ympavlov@gmail.com>
Vendor:		LightLang Team

Source:		lightlang-%{version}.tar.bz2
Patch:		lightlang.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
BuildRequires:	python-qt4 python-sip python-xlib vorbis-tools update-desktop-files
%if 0%{?suse_version} > 1020
BuildRequires:  fdupes
%endif
Requires:	python-qt4 python-sip python-xlib vorbis-tools

%description
LightLang is a small and powerfull dictionary shell, writed on qt4 and has a many dictionary (ru-en and en-ru).
LightLang это маленькая и быстрая словарная оболочка на Qt4 которая содержит в комплекте множество словарей (ru-en и en-ru).

%prep
%setup
%patch -p0

%build
%configure \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--datadir=%{_datadir} \
	--docdir=%{_docdir}

%{__make} %{?_smp_mflags}

%install
mkdir %{buildroot}%{_prefix}
mkdir -p %{buildroot}%{_libdir}/xsl/pyqt4
mkdir %{buildroot}%{_datadir}
mkdir -p %{buildroot}%{_mandir}/en/man1
mkdir -p %{buildroot}%{_mandir}/ru/man1

%makeinstall

mkdir -p %{buildroot}%{_datadir}/icons/hicolor/64x64
mv %{buildroot}%{_datadir}/icons/xsl.png %{buildroot}%{_datadir}/icons/hicolor/64x64/xsl.png
%suse_update_desktop_file -r xsl Office Utility Dictionary

%if 0%{?suse_version} > 1020
%fdupes %{buildroot}%{docdir}
%fdupes -s %{buildroot}
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(-, root, root)

%{_bindir}/lightlang
%{_bindir}/llrepo
%{_bindir}/sl
%{_bindir}/xsl
%dir %{_libdir}/llrepo
%{_libdir}/llrepo/*
%dir %{_libdir}/xsl
%{_libdir}/xsl/*
%{_libdir}/pkgconfig/lightlang.pc
%{_datadir}/applications/*.desktop
%dir %{_datadir}/icons/hicolor
%dir %{_datadir}/icons/hicolor/64x64
%{_datadir}/icons/hicolor/64x64/xsl.png
%dir %{_datadir}/xsl
%{_datadir}/xsl/*
%dir %{_mandir}/en
%dir %{_mandir}/en/man1
%{_mandir}/en/man1/*.1.gz
%dir %{_mandir}/ru
%dir %{_mandir}/ru/man1
%{_mandir}/ru/man1/*.1.gz
%doc %{_docdir}/lightlang

%changelog
* Thu Mar 19 2010 Yuri Pavlov <ymapvlov@gmail.com>
- Initial release for version 0.8.6