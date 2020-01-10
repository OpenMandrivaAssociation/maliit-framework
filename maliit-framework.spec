%define Werror_cflags %nil
%define _fortify_cflags %nil

%define major	0
%define minor	94
%define libname	%mklibname maliit %{major}
%define devname	%mklibname -d maliit

%define libconn	%mklibname maliit-connection %{major}
%define libglib	%mklibname maliit-glib %{major}
%define libquick %mklibname maliit-plugins-quick %{major}
%define libsett %mklibname maliit-settings %{major}
%define libplug %mklibname maliit-plugins %{major}

Name:           maliit-framework
Version:        0.94.2
Release:	4
Summary:        Input method framework

Group:          System/Libraries
License:        LGPLv2
URL:            http://maliit.org/
Source0:        http://maliit.org/releases/%{name}/%{name}-%{version}.tar.bz2
Patch0:		xfixes-maliit-framework.patch
Patch1:		hide-qt-input.patch

BuildRequires:	doxygen
BuildRequires:	graphviz
BuildRequires:	gtk-doc
BuildRequires:	qt4-devel
BuildRequires:	pkgconfig(dbus-1)
BuildRequires:	pkgconfig(dbus-glib-1)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gobject-introspection-1.0)
BuildRequires:	pkgconfig(gtk+-2.0)
BuildRequires:	pkgconfig(gtk+-3.0)
BuildRequires:	pkgconfig(hunspell)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xcomposite)
BuildRequires:	pkgconfig(xdamage)
BuildRequires:	pkgconfig(xext)	
BuildRequires:	pkgconfig(xfixes)
BuildRequires:	pkgconfig(udev)

%description
Maliit provides a flexible and cross-platform input method framework. It has a
plugin-based client-server architecture where applications act as clients and
communicate with the Maliit server via input context plugins. The communication
link currently uses D-Bus.

%package -n	%{libname}
Summary:	Input method module for Qt 4 based on Maliit framework
Group:		System/Libraries

%description -n %{libname}
Libraries for Maliit framework.

%package -n	%{libconn}
Summary:	Input method module for Qt 4 based on Maliit framework
Group:		System/Libraries

%description -n %{libconn}
Libraries for Maliit framework.

%package -n	%{libquick}
Summary:	Input method module for Qt 4 based on Maliit framework
Group:		System/Libraries

%description -n %{libquick}
Libraries for Maliit framework.

%package -n	%{libglib}
Summary:	Input method module for Qt 4 based on Maliit framework
Group:		System/Libraries

%description -n %{libglib}
Libraries for Maliit framework.

%package -n	%{libsett}
Summary:	Input method module for Qt 4 based on Maliit framework
Group:		System/Libraries

%description -n %{libsett}
Libraries for Maliit framework.

%package -n	%{libplug}
Summary:	Input method module for Qt 4 based on Maliit framework
Group:		System/Libraries

%description -n %{libplug}
Libraries for Maliit framework.

%package	qt4
Summary:	Input method module for Qt 4 based on Maliit framework
Group:		System/Libraries
Requires:	%{libname} = %{EVRD}

%description	 qt4
Input method module for Qt 4 based on Maliit framework.

%package	gtk2
Summary:	Input method module for GTK+ 2 based on Maliit framework
Group:		System/Libraries
Requires:	%{libname} = %{EVRD}

%description	gtk2
Input method module for GTK+ 2 based on Maliit framework.

%package	gtk3
Summary:	Input method module for GTK+ 3 based on Maliit framework
Group:		System/Libraries
Requires:	%{libname} = %{EVRD}

%description	gtk3
Input method module for GTK+ 3 based on Maliit framework.

%package -n	%{devname}
Summary:	Development files for %{name}
Group:		Development/C
Requires:	%{libname} = %{EVRD}
Requires:	%{libconn} = %{EVRD}
Requires:	%{libglib} = %{EVRD}
Requires:	%{libquick} = %{EVRD}
Requires:	%{libsett} = %{EVRD}
Requires:	%{libplug} = %{EVRD}

%description -n %{devname}
Files for development with %{name}.

%package	docs
Summary:	Documentation files for %{name}
Group:		Documentation
BuildArch:	noarch

%description	docs
This package contains developer documentation for %{name}.

%package	examples
Summary:	Tests and examples for %{name}
Group:		System/Libraries

%description	examples
This package contains tests and examples for %{name}.

%prep
%setup -q
%autopatch -p1

%build
%qmake_qt4 -r MALIIT_VERSION=%{version} PREFIX=%{_prefix} \
             BINDIR=%{_bindir} LIBDIR=%{_libdir} INCLUDEDIR=%{_includedir} \
             QMAKE_CC=gcc QMAKE_CXX=g++ \
             MALIIT_ENABLE_MULTITOUCH=true \
             CONFIG+=disable-gtk-cache-update CONFIG+=disable-preedit \
             CONFIG+=enable-hunspell CONFIG+=enable-dbus-activation \
	     CONFIG+=disable-background-translucency \
	     CONFIG+=notests

%make

%install
%makeinstall INSTALL="install -p" INSTALL_ROOT=%{buildroot} DESTDIR=%{buildroot}

find %{buildroot} -name '.moc' -exec rm -rf {} ';'
find %{buildroot} -name '.gitignore' -exec rm -rf {} ';'

# e.g. maliit-plugins package stores files in there
mkdir -p %{buildroot}%{_datadir}/maliit

# move installed docs to include them in subpackage via %%doc magic
rm -rf __tmp_doc ; mkdir __tmp_doc
mv %{buildroot}%{_docdir}/%{name}/* __tmp_doc

%files
%doc LICENSE.LGPL README NEWS
%{_bindir}/maliit-server
%dir %{_libdir}/maliit
%dir %{_libdir}/maliit/plugins
%dir %{_libdir}/maliit/plugins/factories
%{_libdir}/maliit/plugins/factories/libmaliit-plugins-quick-factory.so
%{_libdir}/girepository-1.0/Maliit-1.0.typelib
%{_datadir}/maliit/
%{_datadir}/dbus-1/services/org.maliit.server.service

%files -n %{libname}
%{_libdir}/libmaliit.so.%{major}*

%files -n %{libconn}
%{_libdir}/libmaliit-connection.so.%{major}*

%files -n %{libglib}
%{_libdir}/libmaliit-glib.so.%{major}*

%files -n %{libquick}
%{_libdir}/libmaliit-plugins-quick.so.%{major}*

%files -n %{libsett}
%{_libdir}/libmaliit-settings.so.%{major}*

%files -n %{libplug}
%{_libdir}/libmaliit-plugins.so.%{major}*

%files qt4
%{_libdir}/qt4/plugins/inputmethods/libmaliit*

%files gtk2
%{_libdir}/gtk-2.0/2.10.0/immodules/libim-maliit.so

%files gtk3
%{_libdir}/gtk-3.0/3.0.0/immodules/libim-maliit.so

%files -n %{devname}
%{_includedir}/maliit/
%{_libdir}/libmaliit*.so
%{_libdir}/pkgconfig/maliit*.pc
%{qt4dir}/mkspecs/features/maliit*
%dir %{_datadir}/gir-1.0
%{_datadir}/gir-1.0/Maliit-1.0.gir

%files docs
%doc __tmp_doc/*
%dir %{_datadir}/gtk-doc
%dir %{_datadir}/gtk-doc/html
%{_datadir}/gtk-doc/html/maliit/

%files examples
%{_bindir}/maliit-example*
%{_libdir}/maliit-framework-tests
