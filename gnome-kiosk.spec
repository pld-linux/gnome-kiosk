Summary:	GNOME Kiosk - Mutter based compositor for kiosks
Summary(pl.UTF-8):	GNOME Kiosk - oparty na Mutter zarządca składania dla punktów sprzedaży
Name:		gnome-kiosk
Version:	42.0
Release:	1
License:	GPL v2+
Group:		X11/Applications
Source0:	https://download.gnome.org/sources/gnome-kiosk/42/%{name}-%{version}.tar.xz
# Source0-md5:	1e31a9280f86273eeff2834c0b73bfdd
Patch0:		%{name}-meson.patch
URL:		https://gitlab.gnome.org/GNOME/gnome-kiosk
BuildRequires:	gettext-tools
BuildRequires:	glib2-devel >= 2.0
BuildRequires:	gnome-desktop-devel >= 3.0
BuildRequires:	gtk4-devel >= 4.0
BuildRequires:	ibus-devel >= 1.0
BuildRequires:	meson
BuildRequires:	mutter-devel >= 42
BuildRequires:	ninja >= 1.5
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	systemd-devel
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	dbus
Requires:	gdm
Requires:	gnome-desktop >= 3.0
Requires:	gnome-session
Requires:	gnome-settings-daemon
Requires:	ibus >= 1.0
Requires:	mutter >= 42
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
GNOME Kiosk provides a desktop environment suitable for fixed purpose,
or single application deployments like wall displays and point-of-sale
systems.

It provides a very minimal Wayland display server and compositor and
Xorg compositor and window manager. It automatically starts
applications fullscreen.

Notably, GNOME Kiosk features no panels, dashes, or docks that could
distract from the application using it as a platform.

%description -l pl.UTF-8
GNOME Kiosk dostarcza środowisko graficzne odpowiednie do ustalonego
zastosownia albo wdrożeń jednoaplikacyjnych, takich jak ekrany ścienne
czy systemy dla punktów sprzedaży.

Zapewnia bardzo minimalny serwer wyświetlania i zarządcę składania
Wayland oraz zarządcę składania i okien Xorg. Automatycznie uruchamia
aplikacje w trybie pełnoekranowym.

GNOME Kiosk w szczególności nie zawiera paneli, pasków czy doków,
mogących odrywać uwagę od aplikacji wykorzystującej go jako platformę.

%prep
%setup -q
%patch0 -p1

%{__sed} -E -i -e '1s,#!\s*/usr/bin/sh(\s|$),#!/bin/sh\\1,' \
	kiosk-script/gnome-kiosk-script

%build
%meson build

%ninja_build -C build

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

# no translations yet (as of 40.alpha)
#find_lang %{name}.lang

%clean
rm -rf $RPM_BUILD_ROOT

%files
# -f %{name}.lang
%defattr(644,root,root,755)
%doc NEWS README.md
%attr(755,root,root) %{_bindir}/gnome-kiosk
%attr(755,root,root) %{_bindir}/gnome-kiosk-script
%dir %{systemduserunitdir}/gnome-session@gnome-kiosk-script.target.d
%{systemduserunitdir}/gnome-session@gnome-kiosk-script.target.d/session.conf
%{systemduserunitdir}/org.gnome.Kiosk.Script.service
%{systemduserunitdir}/org.gnome.Kiosk.target
%{systemduserunitdir}/org.gnome.Kiosk@wayland.service
%{systemduserunitdir}/org.gnome.Kiosk@x11.service
%{_datadir}/gnome-session/sessions/gnome-kiosk-script.session
%{_datadir}/gnome-session/sessions/org.gnome.Kiosk.SearchApp.session
%{_datadir}/wayland-sessions/gnome-kiosk-script-wayland.desktop
%{_datadir}/wayland-sessions/org.gnome.Kiosk.SearchApp.Session.desktop
%{_datadir}/xsessions/gnome-kiosk-script-xorg.desktop
%{_datadir}/xsessions/org.gnome.Kiosk.SearchApp.Session.desktop
%{_desktopdir}/org.gnome.Kiosk.desktop
%{_desktopdir}/org.gnome.Kiosk.Script.desktop
%{_desktopdir}/org.gnome.Kiosk.SearchApp.desktop
