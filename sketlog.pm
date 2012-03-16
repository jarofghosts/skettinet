#!/usr/bin/perl -w

#### SkettiSCRIPT v1.5                    ####
#### Auth: Jesse Keane                     ####


package SkettiSCRIPT;
use strict;

sub skettiError
{
	my $arg = shift;
	my $etime = localtime;
	print "Error in SkettiSystem, the error was reported as follows:<br/>\n";
	print "&nbsp;&nbsp;&nbsp;<strong>@_</strong>";
	open (LOG, ">>sketti.log") || die "Cannot open sketti.log for writing.\n";
	print LOG "err: $arg ($etime)\n";
	close(LOG);
	return;
}
sub skettiLog
{
	my $arg = shift;
	my $etime = localtime;
	open (LOG, ">>sketti.log") || die "Cannot open sketti.log for writing.\n";
	print LOG "$arg ($etime)\n";
	close(LOG);
	return;
}
1;
