%define __os_install_post %{nil}

Name:           cassandra
Version:        3.10
Release:        9%{?dist}
Summary:        Cassandra

Group:          Applications/Databases
License:        ASL 2.0
URL:            http://cassandra.apache.org/
Source0:        http://apache-mirror.rbc.ru/pub/apache/cassandra/%{version}/apache-cassandra-%{version}-bin.tar.gz
Source1:        cassandra.sysconfig
Source2:        cassandra.service
Source3:        cassandra-tools.sh
Patch0:         cassandra-env.sh.patch
Patch1:         cassandra.yaml.patch
Patch2:         cassandra.patch

BuildRequires:  Cython
Requires:       java >= 1.8.0 jre >= 1.8.0 numactl jemalloc

%description
The Apache Cassandra database is the right choice when you need scalability
and high availability without compromising performance. Linear scalability
and proven fault-tolerance on commodity hardware or cloud infrastructure make it
the perfect platform for mission-critical data.Cassandra's support for replicating
across multiple datacenters is best-in-class, providing lower latency for your
users and the peace of mind of knowing that you can survive regional outages

%prep
%setup -q -n apache-cassandra-%{version}
%patch0
%patch1
%patch2

%build
cd pylib
%{__python} setup.py build

%install
%{__mkdir_p} %{buildroot}%{_bindir}
%{__mkdir_p} %{buildroot}%{_sbindir}
%{__mkdir_p} %{buildroot}%{_sysconfdir}/cassandra/triggers
%{__mkdir_p} %{buildroot}%{_sysconfdir}/sysconfig
%{__mkdir_p} %{buildroot}%{_sharedstatedir}/cassandra
%{__mkdir_p} %{buildroot}%{_datarootdir}/cassandra/lib/sigar-bin
%{__mkdir_p} %{buildroot}%{_unitdir}
%{__mkdir_p} %{buildroot}%{_localstatedir}/log/cassandra

%{__cp} bin/cassandra %{buildroot}%{_sbindir}/cassandra
%{__cp} bin/cassandra.in.sh %{buildroot}%{_sbindir}/cassandra.in.sh
%{__cp} bin/cqlsh %{buildroot}%{_bindir}/cqlsh
%{__cp} bin/cqlsh.py %{buildroot}%{_bindir}/cqlsh.py
%{__cp} bin/debug-cql %{buildroot}%{_bindir}/debug-cql.sh
%{__cp} bin/sstableloader %{buildroot}%{_bindir}/sstableloader.sh
%{__cp} bin/sstablescrub %{buildroot}%{_bindir}/sstablescrub.sh
%{__cp} bin/sstableupgrade %{buildroot}%{_bindir}/sstableupgrade.sh
%{__cp} bin/sstableutil %{buildroot}%{_bindir}/sstableutil.sh
%{__cp} bin/sstableverify %{buildroot}%{_bindir}/sstableverify.sh
%{__cp} bin/nodetool %{buildroot}%{_bindir}/nodetool.sh

%{__cp} %{SOURCE3} %{buildroot}%{_bindir}/cassandra-tools.sh
%{__ln_s} cassandra-tools.sh %{buildroot}%{_bindir}/debug-cql
%{__ln_s} cassandra-tools.sh %{buildroot}%{_bindir}/sstableloader
%{__ln_s} cassandra-tools.sh %{buildroot}%{_bindir}/sstablescrub
%{__ln_s} cassandra-tools.sh %{buildroot}%{_bindir}/sstableupgrade
%{__ln_s} cassandra-tools.sh %{buildroot}%{_bindir}/sstableutil
%{__ln_s} cassandra-tools.sh %{buildroot}%{_bindir}/sstableverify
%{__ln_s} cassandra-tools.sh %{buildroot}%{_bindir}/nodetool

%{__cp} conf/cassandra-env.sh %{buildroot}%{_sysconfdir}/cassandra/cassandra-env.sh
%{__cp} conf/cassandra.yaml %{buildroot}%{_sysconfdir}/cassandra/cassandra.yaml
%{__cp} conf/hotspot_compiler %{buildroot}%{_sysconfdir}/cassandra/hotspot_compiler
%{__cp} conf/jvm.options %{buildroot}%{_sysconfdir}/cassandra/jvm.options
%{__cp} conf/logback.xml %{buildroot}%{_sysconfdir}/cassandra/logback.xml

%{__cp} -pr interface %{buildroot}%{_datarootdir}/cassandra

%{__cp} lib/*.jar %{buildroot}%{_datarootdir}/cassandra/lib
%{__cp} lib/*.zip %{buildroot}%{_datarootdir}/cassandra/lib
%{__cp} -pr lib/sigar-bin/libsigar-amd64-linux.so %{buildroot}%{_datarootdir}/cassandra/lib/sigar-bin

%{__cp} %{SOURCE1} %{buildroot}%{_sysconfdir}/sysconfig/cassandra
%{__cp} %{SOURCE2} %{buildroot}%{_unitdir}/cassandra.service

cd pylib
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

%pre
getent passwd cassandra >/dev/null 2>&1 || useradd -M -r -s /sbin/nologin -c "Cassandra" -d %{_datarootdir}/cassandra cassandra >/dev/null 2>&1 || :

%post
%{__chown} cassandra:cassandra %{_localstatedir}/log/cassandra
%{__chown} cassandra:cassandra %{_sharedstatedir}/cassandra

%systemd_post cassandra.service

%preun
%systemd_preun cassandra.service

%postun
%systemd_postun cassandra.service

%files
%defattr(-,root,root,-)
%{_bindir}/*
%{_sbindir}/*
%{_datarootdir}/cassandra
%{_unitdir}/cassandra.service
%{python_sitearch}/cqlshlib
%{python_sitearch}/cassandra_pylib*
%dir %{_sysconfdir}/cassandra
%dir %{_sharedstatedir}/cassandra
%dir %{_localstatedir}/log/cassandra
%config(noreplace) %{_sysconfdir}/cassandra/*
%config(noreplace) %{_sysconfdir}/sysconfig/cassandra
%doc CHANGES.txt LICENSE.txt NEWS.txt NOTICE.txt doc javadoc conf lib/licenses

%changelog
* Thu Mar  2 2017 - alexander@rumyantsev.com - 3.10-9
- Initial packaging
