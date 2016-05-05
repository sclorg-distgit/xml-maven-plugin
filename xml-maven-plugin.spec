%global pkg_name xml-maven-plugin
%{?scl:%scl_package %{pkg_name}}
%{?maven_find_provides_and_requires}

Name:          %{?scl_prefix}%{pkg_name}
Version:       1.0
Release:       10.5%{?dist}
Summary:       Maven XML Plugin
Group:         Development/Libraries
License:       ASL 2.0
Url:           http://mojo.codehaus.org/xml-maven-plugin/
Source0:       http://repo2.maven.org/maven2/org/codehaus/mojo/xml-maven-plugin/1.0/xml-maven-plugin-1.0-source-release.zip

BuildRequires: %{?scl_prefix}mojo-parent

BuildRequires: %{?scl_prefix}apache-rat-plugin
BuildRequires: %{?scl_prefix}maven-local
BuildRequires: %{?scl_prefix}maven-changes-plugin
BuildRequires: %{?scl_prefix}maven-clean-plugin
BuildRequires: %{?scl_prefix}maven-compiler-plugin
BuildRequires: %{?scl_prefix}maven-enforcer-plugin
BuildRequires: %{?scl_prefix}maven-install-plugin
BuildRequires: %{?scl_prefix}maven-invoker-plugin
BuildRequires: %{?scl_prefix}maven-jar-plugin
BuildRequires: %{?scl_prefix}maven-javadoc-plugin
BuildRequires: %{?scl_prefix}maven-plugin-testing-harness

BuildRequires: %{?scl_prefix}plexus-component-api
BuildRequires: %{?scl_prefix}plexus-io
BuildRequires: %{?scl_prefix}plexus-resources
BuildRequires: %{?scl_prefix}plexus-utils
BuildRequires: %{?scl_prefix}saxon
BuildRequires: %{?scl_prefix_java_common}xerces-j2
BuildRequires: %{?scl_prefix_java_common}xml-commons-apis
BuildRequires: %{?scl_prefix_java_common}xml-commons-resolver

BuildArch:     noarch

%description
A plugin for various XML related tasks like validation and transformation.

%package javadoc
Summary:       Javadocs for %{pkg_name}

%description javadoc
This package contains the API documentation for %{pkg_name}.

%prep
%setup -q -n %{pkg_name}-%{version}
%{?scl:scl enable %{scl} - <<"EOF"}
set -e -x

for d in LICENSE NOTICE ; do
  iconv -f iso8859-1 -t utf-8 $d.txt > $d.txt.conv && mv -f $d.txt.conv $d.txt
  sed -i 's/\r//' $d.txt
done

rm -rf src/it/mojo-1438-validate

# Add the version
sed -i 's|stylesheet |stylesheet version="1.0" |'  src/it/it8/src/main/xsl/it8.xsl

# In maven 3, the functionality we need has been moved to maven-core
%pom_remove_dep org.apache.maven:maven-project
%pom_add_dep org.apache.maven:maven-core
%{?scl:EOF}

%build
%{?scl:scl enable %{scl} - <<"EOF"}
set -e -x
%mvn_build -f -- install
%{?scl:EOF}

%install
%{?scl:scl enable %{scl} - <<"EOF"}
set -e -x
%mvn_install
%{?scl:EOF}

%files -f .mfiles
%dir %{_javadir}/%{pkg_name}
%dir %{_mavenpomdir}/%{pkg_name}
%doc LICENSE.txt NOTICE.txt

%files javadoc -f .mfiles-javadoc
%doc LICENSE.txt NOTICE.txt

%changelog
* Thu Apr 14 2016 Michal Srb <msrb@redhat.com> - 1.0-10.5
- Fix directory ownership (Resolves: rhbz#1325866)

* Mon Feb 08 2016 Michal Srb <msrb@redhat.com> - 1.0-10.4
- Fix BR on maven-local & co.

* Mon Jan 11 2016 Michal Srb <msrb@redhat.com> - 1.0-10.3
- maven33 rebuild #2

* Sat Jan 09 2016 Michal Srb <msrb@redhat.com> - 1.0-10.2
- maven33 rebuild

* Mon Jun 08 2015 Michal Srb <msrb@redhat.com> - 1.0-10.1
- SCL-ize spec

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Sep 12 2013 Marek Goldmann <mgoldman@redhat.com> - 1.0-9
- Use xmvn
- Make the integration tests build

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Mar 02 2013 Mat Booth <fedora@matbooth.co.uk> - 1.0-7
- Fix FTBFS rhbz #914586

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 1.0-5
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Feb 21 2012 David Nalley <david@gnsa.us> - 1.0-3
- patched to remove offending integration tests

* Thu Feb 16 2012 David Nalley <david@gnsa.us> - 1.0-2
- removed needless arguments for setup
- reduced description line to less than 80 chars
- added license to -javadoc
- removed unused source file
- removed all update_maven_depmap references

* Mon Jan 16 2012 David Nalley <david@gnsa.us> - 1.0-1 
- Initial rpm build - spec modified from mageia's version of same
