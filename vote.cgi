#!/usr/bin/perl -w

package SkettiSCRIPT;
use strict;
use sketdb;
use sketboard;
use sketusr;
use sketact;
use CGI qw(param);

skettiStartBoard("Vote");

my $db = skettiLoadDb();
my $choice = param('choice');
my $id = param('id');
my $nickn = skettiGrabLogin();

if ($nickn == -1)
{
	print "I'm afraid you must be <a href=\"login.cgi\">logged in</a> to vote in the poll.";
	skettiEndBoard();
	exit;
}
	skettiUpdateLa($nickn);
	my $qu = "SELECT OPT$choice" . "N FROM POLLS WHERE MID = $id;";
	my $query = $db->prepare($qu);
	$query->execute;
	if ($query->fetchrow_array eq "")
	{
		print "I'm sorry, that option ($choice) is invalid in this poll.  Please <a href=\"sbase.cgi\">return to the base</a>.";
		skettiEndBoard();
	}
	my $q = $db->prepare("SELECT VOTERS FROM POLLS WHERE MID = $id;");
	$q->execute;
	my $voters = $q->fetchrow_array;
	if ($voters =~ /\&$nickn\&/)
	{
		print "It appears you have already had a vote tallied- are you trying to stuff the ballot box?  Or are you just trying to make me work overtime?!  Geez.. go <a href=\"sbase.cgi\">away</a>";
		skettiEndBoard();
		exit;
	}
	$voters .= "\&$nickn\&";
	my $choice = "OPT$choice" . "N";
	$query = $db->prepare ("UPDATE POLLS SET VOTERS = '$voters', TOTAL = TOTAL + 1, $choice = $choice + 1 WHERE MID = $id;");
	$query->execute;
	print "Your vote has been added, click <a href=\"viewrp.cgi?id=$id\">here</a> to see the results.";
	skettiEndBoard();
