#!/usr/bin/perl -w

package SkettiSCRIPT;
use strict;
use sketdb;
use sketusr;
use sketact;
use sketziggy;
use sketboard;
use sketlog;
use CGI qw(param);

my $db = skettiLoadDb();
my ($id, $nickn, $query, $nstat, $bnick, $sure, $nlvl);
$nickn = skettiGrabLogin();
if ($nickn != -1) {
skettiUpdateLa($nickn);
$query = $db->prepare("SELECT STATUS,LVL FROM USERS WHERE NICK = '$nickn';");
$query->execute;
($nstat,$nlvl) = $query->fetchrow_array;
}

skettiStartBoard("Ban User");

if ($nickn eq "" || $nstat ne "SkettiOP" || ($nstat ne "SkettiOP" && $nlvl < 5))
{
	print "You must be logged in AND a SkettiOP or <em>Lord/Lady</em> in order to banish- <a href=\"sbase.cgi\">sorry</a>.";
	skettiEndBoard(); }
	
	$id = param('id');
	$query = $db->prepare("SELECT BAN FROM USERS WHERE UID = $id;");
	$query->execute;
if ($query->fetchrow_array == 1)
{
	print "It seems user #$id has already been run and banished from <a href=\"sbase.cgi\">this land</a>.";
	skettiEndBoard(); }
$sure = param('sure');
my $bnick = param('bnick');
if ($sure == 1) {
	skettiQuery ("UPDATE USERS SET BAN = 1 WHERE UID = $id;");
	print "So it is done; user #$id has been banished from this land.";

	skettiSendZiggyMsg ($bnick, "I'm not sure what you did, but $nickn has banned you from this realm.");
	skettiLog ("$nickn bans $bnick from this realm.");
	skettiEndBoard(); }
$query = $db->prepare("SELECT NICK FROM USERS WHERE UID = $id;");
$query->execute;
$bnick = $query->fetchrow_array;
print <<END;
<form method="POST" action="banuser.cgi">
<input type="hidden" name="id" value="$id"><input type="hidden" value="1" name="sure">
Are you sure you wish to banish $bnick from your realm?<p align="center">
<table border=0><tr><td><input type=\"hidden\" name=\"bnick\" value=\"$bnick\"><input type="submit" value="ban" class="submit"></form></td><td><form method="POST" action="sbase.cgi"><input type="submit" value="don't" class="submit"></p></form></table>
END

skettiEndBoard();
