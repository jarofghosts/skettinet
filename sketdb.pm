#!/usr/bin/perl -w

#### SkettiSCRIPT v1.04                    ####
#### Auth: Jesse Keane                     ####
#### sketdb.pm::                           ####
#### database loading module               ####
####     provides:                         ####
#### skettiLoadDb :loads database          ####
#### skettiQuery arg :queries db w/ arg    ####

package SkettiSCRIPT;
use strict;
use DBI;

sub skettiLoadDb
{
	my $db = DBI->connect("DBI:mysql:sketti:localhost","root","") || die "can't access database:" . DBI->errstr;
	return $db;
}
sub skettiQuery
{
	my $db = skettiLoadDb();
	my $qtext = shift;
	my $query = $db->prepare($qtext);
	$query->execute;
	return $query->fetchrow_array;
}
1;
