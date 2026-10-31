# Release stays below 1 so a Fedora package, should one appear, replaces this.
Name:           cclip
Version:        3.3.1
Release:        0.1%{?dist}
Summary:        Clipboard manager for wayland
License:        GPL-3.0-or-later
URL:            https://github.com/heather7283/cclip
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz

BuildRequires:  gcc
# meson.build runs git for the commit and tag, and a missing program fails the
# build even though a failing one falls back to the version.
BuildRequires:  git-core
BuildRequires:  meson
BuildRequires:  pkgconfig(libxxhash)
BuildRequires:  pkgconfig(sqlite3)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-scanner)

%description
A clipboard manager for wayland compositors that support the
wlr-data-control protocol. cclipd stores the clipboard history in an SQLite
database, and cclip lists, retrieves, tags and deletes its entries.

%prep
%autosetup

%build
%meson
%meson_build

%install
%meson_install

%files
%license COPYING
%doc README.md examples
%{_bindir}/cclip
%{_bindir}/cclipd
%{_mandir}/man1/cclip.1*
%{_mandir}/man1/cclipd.1*

%changelog
* Sat Oct 31 2026 seeweedx <git.atlas138@passmail.com> - 3.3.1-0.1
- Package upstream 3.3.1
