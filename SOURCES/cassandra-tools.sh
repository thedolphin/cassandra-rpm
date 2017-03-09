#!/bin/sh

logdir=/tmp/cassandra-$USER
mkdir -p "${logdir}"

set -- "-Dcassandra.logdir=${logdir}" "$@"

. /etc/sysconfig/cassandra
. $0.sh
