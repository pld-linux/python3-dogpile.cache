#
# Conditional build:
%bcond_with	doc	# Sphinx documentation (sdist contains prebuilt html)
%bcond_without	tests	# unit tests

Summary:	A caching front-end based on the Dogpile lock
Summary(pl.UTF-8):	Frontend z pamięcią podręczną oparty na blokadzie Dogpile
Name:		python3-dogpile.cache
Version:	1.5.0
Release:	1
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/dogpile.cache/
Source0:	https://files.pythonhosted.org/packages/source/d/dogpile.cache/dogpile_cache-%{version}.tar.gz
# Source0-md5:	a60ad9511e7bbf45417bd89d16d5b222
URL:		https://pypi.org/project/dogpile.cache/
BuildRequires:	python3-modules >= 1:3.10
BuildRequires:	python3-setuptools >= 1:77.0.3
%if %{with tests}
BuildRequires:	python3-Mako
BuildRequires:	python3-decorator >= 4.0.0
#BuildRequires:	python3-junitparser
BuildRequires:	python3-pytest >= 8
BuildRequires:	python3-stevedore >= 3.0.0
%if "%{py3_ver}" == "3.10"
BuildRequires:	python3-typing_extensions
%endif
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	python3-Mako
BuildRequires:	python3-changelog
BuildRequires:	python3-decorator
BuildRequires:	python3-sphinx-paramlinks
BuildRequires:	python3-sphinx_book_theme
BuildRequires:	python3-stevedore
BuildRequires:	sphinx-pdg-3
%endif
Requires:	python3-modules >= 1:3.10
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Dogpile consists of two subsystems, one building on top of the other.

dogpile provides the concept of a "dogpile lock", a control structure
which allows a single thread of execution to be selected as the
"creator" of some resource, while allowing other threads of execution
to refer to the previous version of this resource as the creation
proceeds; if there is no previous version, then those threads block
until the object is available.

dogpile.cache is a caching API which provides a generic interface to
caching backends of any variety, and additionally provides API hooks
which integrate these cache backends with the locking mechanism of
dogpile.

%description -l pl.UTF-8
Dogpile składa się z dwóch podsystemów, jeden jest zbudowany na
drugim.

dogpile udostępnia koncept "blokady dogpile" - struktury sterującej,
pozwalającej na wybór jednego z wątków jako "twórcy" jakiegoś zasobu,
podczas gdy pozostałe wątki odwołują się do poprzedniej wersji zasobu
w miarę procesu tworzenia; jeśli nie ma poprzedniej wersji, wątki te
blokują się do czasu dostępności obiektu.

dogpile.cache to API z pamięcią podręczną, zapewniające ogólny
interfejs do dowolnych backendów pamięci podręcznej oraz uchwyty API
integrujące te backendy z mechanizmem blokującym dogpile.

%package apidocs
Summary:	API documentation for Python dogpile.cache module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona dogpile.cache
Group:		Documentation

%description apidocs
API documentation for Python dogpile.cache module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona dogpile.cache.

%prep
%setup -q -n dogpile_cache-%{version}

%build
%py3_build

%if %{with tests}
# backend tests take long time
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
%{__python3} -m pytest tests -k 'not test_dbm_backend and not test_memcached_backend and not test_redis_backend'
%endif

%if %{with doc}
sphinx-build-3 -b html docs/build docs
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE README.rst
%{py3_sitescriptdir}/dogpile
%{py3_sitescriptdir}/dogpile.cache-%{version}-py*.egg-info

%files apidocs
%defattr(644,root,root,755)
%doc docs/{_static,*.html,*.js}
