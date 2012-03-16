#!/usr/bin/perl -w

package SkettiSCRIPT;
use strict;
use sketdb;
use sketact;
use sketboard;
use sketusr;
use CGI qw(param);

skettiStartBoard("Userlist");
my $lonick = skettiGrabLogin();

if ($lonick != -1) { skettiUpdateLa($lonick); }

my $start = param('s');
my $end = param('e');

if ($start eq "") { $start = 0; }
if ($end eq "") { $end = 10; }

my $db = skettiLoadDb();
my $query = $db->prepare("SELECT UID,NICK,STATUS,URL,AVATAR FROM USERS WHERE UID >= $start AND UID <= $end ORDER BY UID ASC;");
$query->execute;
if ($query->rows == 0)
{
	print <<END;
It appears there aren't that many members yet :(.  Try a lower number.

END
}
my $dif = $end-$start;
my $rend = $end;
$end++;
my $next = $end + $dif;
my $nhtml;
my @info;
print "</center><p align=\"left\">\n";
my ($uid,$nick,$status,$url,$avatar);
while (@info = $query->fetchrow_array)
{
	($uid,$nick,$status,$url,$avatar) = @info;
	$avatar = defined $avatar && $avatar ne "" ? $avatar : "ava_ernest.gif";
	print "&nbsp;<div style=\"position:relative\">$uid. <a href=\"users.cgi?id=$uid\"><img src=\"$avatar\" width=\"30\" height=\"35\" alt=\"$nick\" border=\"0\" style=\"vertical-align:middle\"/></a><span style=\"vertical-align:middle\">&nbsp;&nbsp;<a href=\"$url\" title=\"URL: $url\">$nick</a> [$status] (<a href=\"users.cgi?id=$uid\">info</a>)</span></div><br/><br/>";
}
if ($uid < $rend) { $nhtml = ""; } else{ $nhtml = "<a href='userlist.cgi?s=$end&e=$next'>next&gt;&gt;</a>"; }
print "<center>$nhtml</center>\n";
skettiEndBoard();
