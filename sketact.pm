#!/usr/bin/perl -w

#### SkettiSCRIPT v1.5                    ####
#### Auth: Jesse Keane                     ####

package SkettiSCRIPT;
use strict;
use sketdb;

sub skettiGetTA
{
	my $ta = localtime;
	$ta =~ s/  / /gi;
	return $ta;
}
sub skettiUpdateLa
{
	my $db = skettiLoadDb;
	my $nick = shift;
	my $ta = skettiGetTA;
	my $query = $db->prepare("UPDATE LOGGEDIN SET LA = '$ta' WHERE NICK = '$nick';");
	$query->execute;
}
sub skettiModTime
{
	my $time = localtime;
	$time =~ s/  / /gi;
	my ($q,$month,$date,$stime,$year) = split(/ /,$time);
	if ($month eq "Jan") { $month = 1; }elsif ($month eq "Feb") { $month = 2; }elsif ($month eq "Mar") { $month = 3; }elsif ($month eq "Apr") { $month = 4; }elsif ($month eq "May"){ $month = 5; }elsif ($month eq "Jun"){ $month = 6; }elsif ($month eq "Jul"){ $month = 7;}elsif ($month eq "Aug") { $month = 8; }elsif ($month eq "Sep"){ $month = 9;}elsif ($month eq "Oct") { $month = 10; }elsif ($month eq "Nov"){ $month = 11;}else{ $month = 12; }
	$stime =~ s/://gi;
	$stime =~ s/^00/24/gi;
	if ($date < 10) { $date = "0" . $date; }
	my $logtime = $month . $date . $stime . $year;
	return $logtime;
}
1;