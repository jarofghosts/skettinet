#!/usr/bin/perl -w

package SkettiSCRIPT;
use strict;
use sketdb;
use sketact;
use sketusr;
use sketboard;
use CGI qw(param);

my $mid = param('id');
my $nick = skettiGrabLogin();
if ($nick == -1)
{
	skettiStartBoard("Bookmark Post");
	print "You must be logged in, sorry. Go <a href=\"sbase.cgi\">back</a>";
	skettiEndBoard(); }
skettiUpdateLa($nick);
if (skettiGrabType($mid) eq "NULL")
{
	skettiStartBoard("Bookmark Post");
	print "That post does not exist, please <a href=\"sbase.cgi\">return to the base</a>.";
	skettiEndBoard(); }
my $db = skettiLoadDb();
my $query = $db->prepare("SELECT UID FROM USERS WHERE NICK='$nick' AND BKMRKS REGEXP '#$mid#';");
$query->execute;
if ($query->rows != 0)
{
	skettiStartBoard("Bookmark Post");
	print "You have already bookmarked that post!<br/>Go <a href=\"sbase.cgi\">find a different one</a>.";
	skettiEndBoard(); }
$query = $db->prepare("SELECT BKMRKS FROM USERS WHERE NICK = '$nick';");
$query->execute;
if ($query->fetchrow_array ne "") { $query=$db->prepare ("UPDATE USERS SET BKMRKS = CONCAT('#$mid#',BKMRKS) WHERE NICK='$nick';"); } else {
	$query=$db->prepare ("UPDATE USERS SET BKMRKS = '#$mid#' WHERE NICK='$nick';"); }
	$query->execute;
	my $q = new CGI;
	print $q->header(-location=>"viewrp.cgi?id=$mid");
skettiEndBoard();
