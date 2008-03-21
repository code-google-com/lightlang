%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Name:           slog
Version:        0.9.1
Release:        1%{?dist}
Summary:        PyGTK based GUI for the LightLang SL
Group:          Applications/Desktops
License:        GPLv2
URL:            http://lightlang.org.ru
Source0:        ftp://ftp.lightlang.org.ru/apps/slog-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  desktop-file-utils
BuildRequires:  pygtk2-devel gtk2-devel
BuildRequires:  python-devel
BuildRequires:  gettext
Requires:       pygtk2 dbus-python 
%description
SLog is a lightweight PyGTK+ dictionary client for the LigthLang SL.
It aims to be efficient , user-friendly, and clean.

%prep
%setup -q
#workaround very odd cleaning at the end of setup.py

%build
CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT

%find_lang %{name}

desktop-file-install --vendor="fedora"                          \
        --dir=${RPM_BUILD_ROOT}%{_datadir}/applications         \
        --remove-category Application                           \
        --remove-key Version                                    \
        --delete-original                                       \
        ${RPM_BUILD_ROOT}%{_datadir}/applications/%{name}.desktop

rm -rf $RPM_BUILD_ROOT%{_datadir}/slog

%clean
rm -rf $RPM_BUILD_ROOT


%files -f %{name}.lang
%defattr(-,root,root,-)
%doc ChangeLog COPYING README 
%{python_sitearch}/*
%{_bindir}/%{name}
%{_datadir}/applications/*.desktop
%{_datadir}/pixmaps/%{name}*


%changelog
* Mon Jan 28 2007 Renat Nasyrov <renatn at gmail.com> - 0.9.1 - 1
- Initial release
