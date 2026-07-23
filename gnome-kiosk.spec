Summary:	GNOME Kiosk - Mutter based compositor for kiosks
Summary(pl.UTF-8):	GNOME Kiosk - oparty na Mutter zarządca składania dla punktów sprzedaży
Name:		gnome-kiosk
Version:	50.1
Release:	1
License:	GPL v2+
Group:		X11/Applications
Source0:	https://download.gnome.org/sources/gnome-kiosk/50/%{name}-%{version}.tar.xz
# Source0-md5:	6ae6e1f4b47721cee83b0ccad09ed453
URL:		https://gitlab.gnome.org/GNOME/gnome-kiosk
BuildRequires:	gettext-tools
BuildRequires:	glib2-devel >= 2.0
BuildRequires:	gnome-desktop4-devel >= 42
BuildRequires:	gtk4-devel >= 4.0
BuildRequires:	ibus-devel >= 1.0
BuildRequires:	meson >= 0.59
BuildRequires:	mutter-devel >= 50
BuildRequires:	ninja >= 1.5
BuildRequires:	rpmbuild(macros) >= 2.042
BuildRequires:	systemd-devel
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	dbus
Requires:	gdm
Requires:	gnome-desktop4 >= 42
Requires:	gnome-session
Requires:	gnome-settings-daemon
Requires:	ibus >= 1.0
Requires:	mutter >= 50
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

%{__sed} -i -e '1s,/usr/bin/sh,/bin/sh,' \
	kiosk-script/gnome-kiosk-script

%{__sed} -i -e '1s,/usr/bin/env python3,%{__python3},' \
	accessibility-panel/accessibility-panel.py.in \
	notification-daemon/gnome-kiosk-notification-send.py.in \
	notification-daemon/notification-daemon.py.in

%build
%meson \
	-Daccessibility-panel=true \
	-Dinput-selector=true \
	-Dnotification-daemon=true

%meson_build

%install
rm -rf $RPM_BUILD_ROOT

%meson_install

# no translations yet (as of 43)
#find_lang %{name}.lang

%clean
rm -rf $RPM_BUILD_ROOT

%files
# -f %{name}.lang
%defattr(644,root,root,755)
%doc NEWS README.md
%attr(755,root,root) %{_bindir}/gnome-kiosk
%attr(755,root,root) %{_bindir}/gnome-kiosk-accessibility-panel
%attr(755,root,root) %{_bindir}/gnome-kiosk-notification-send
%attr(755,root,root) %{_bindir}/gnome-kiosk-script
%attr(755,root,root) %{_libexecdir}/gnome-kiosk-notification-daemon
%{systemduserunitdir}/gnome-kiosk-notification-daemon.service
%dir %{systemduserunitdir}/gnome-session@gnome-kiosk-script.target.d
%{systemduserunitdir}/gnome-session@gnome-kiosk-script.target.d/session.conf
%dir %{systemduserunitdir}/gnome-session@org.gnome.Kiosk.SearchApp.target.d
%{systemduserunitdir}/gnome-session@org.gnome.Kiosk.SearchApp.target.d/session.conf
%{systemduserunitdir}/org.gnome.Kiosk.Script.service
%{systemduserunitdir}/org.gnome.Kiosk.SearchApp.service
%{systemduserunitdir}/org.gnome.Kiosk.target
%{systemduserunitdir}/org.gnome.Kiosk@wayland.service
%{_datadir}/dbus-1/services/org.freedesktop.Notifications.service
%{_datadir}/dbus-1/services/org.gtk.Notifications.service
%{_datadir}/dconf/profile/gnomekiosk
%{_datadir}/gnome-kiosk
%{_datadir}/gnome-session/sessions/gnome-kiosk-script.session
%{_datadir}/gnome-session/sessions/org.gnome.Kiosk.SearchApp.session
%{_datadir}/wayland-sessions/gnome-kiosk-script-wayland.desktop
%{_datadir}/wayland-sessions/org.gnome.Kiosk.SearchApp.Session.desktop
%{_desktopdir}/org.gnome.Kiosk.desktop
%{_desktopdir}/org.gnome.Kiosk.AccessibilityPanel.desktop
%{_desktopdir}/org.gnome.Kiosk.Script.desktop
%{_desktopdir}/org.gnome.Kiosk.SearchApp.desktop
