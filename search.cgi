#!/usr/bin/perl -w

package SkettiSCRIPT;
use sketusr;
use sketact;
use sketsearch;
use sketboard;
use sketbase;
use sketdb;
use URI::Escape;
use strict;
use CGI qw(param);

skettiStartBoard("Search");
my $theme = skettiGrabTheme();
my $login = skettiGrabLogin();
my $db = skettiLoadDb();
my $gy =0;
my ($uid,$handle,$pass,$status,$url,$fontc,$email,$rname,$uin,$loc,$age,$soap,$hobbies,$words,$sb,$ppp,$dt,$avaa,$trunc,$exp,$title,$lvl,$ban,$sex,$ln,$thm,$zig,$viw,$cln,$bkmr,$pmd) = "";
if ($login != -1) { skettiUpdateLa($login);
	my $query = $db->prepare("SELECT * FROM USERS WHERE NICK = '$login';");
	$query->execute;
	($uid,$handle,$pass,$status,$url,$fontc,$email,$rname,$uin,$loc,$age,$soap,$hobbies,$words,$sb,$ppp,$dt,$avaa,$trunc,$exp,$title,$lvl,$ban,$sex,$ln,$thm,$zig,$viw,$cln,$bkmr,$pmd) = $query->fetchrow_array;
 } else { $dt = "classic"; $ppp = 15; $sb = "default"; }
my $search = param('query');
my $key = param('query');
$key =~ s/ /%20/gi;
my $ctr = 0;

print "</center>";
if ($search =~ /^subj:/gi) {
my ($t,$ns) = split(/:/,$search);
my $query = $db->prepare(qq|SELECT IMG FROM SUBJECTS WHERE NAME="$ns"|);
$query->execute;
my $subjecti = $query->fetchrow_array;
print "<center><table border=\"0\"><tr><td><img src=\"$subjecti\" alt=\"$ns\" width=\"120\" height=\"140\"/></td><td valign=\"center\"><h1>$ns</h1></td></tr></table>";
my $subposts = skettiBuildBase($dt,$ppp,$sb,$trunc,$gy,$ns);
print $subposts . "</center>";
skettiEndBoard;
exit; }
if ($search =~ /^nick:/gi) { listByNick(); }

if ($search eq "") { skipIt();}

my (@pinfo,$mid,$topic,$msg,$nick,$pquote,$pquotee);
print "<h2>Results for query <em>&quot;$search&quot;</em></h2><br/>";
print "<h3>Posts:</h3><ol><br/>";
$ctr += skettiSearch ("post",$search);
print "</ol><br/><h3>Polls:</h3><br/><ol>";
$ctr += skettiSearch ("poll",$search);
skipIt();
sub skipIt()
{
print "</ol><center>Results: $ctr<br/>\n";
print "<br/><a href=\"sbase.cgi\">back to the forum</a> &nbsp; &nbsp; <form method=\"POST\" action=\"search.cgi\"><input type=\"text\" name=\"query\" value=\"$search\" class=\"text\"/> <input type=\"submit\" value=\"try again\" class=\"submit\"/></form></center>";
skettiEndBoard();
}
sub listByNick()
{
	my ($t,$ns) = split(/:/,$search);
	my $query = $db->prepare(qq|SELECT MID,TIME,TOPIC,SUBJECT FROM POSTS WHERE NICK = "$ns" AND VISIBLE != 0 ORDER BY MID DESC;|);
	$query->execute;
	my @pinfo;
	my $forum_link;
	my $query2 = $db->prepare("SELECT AVATAR FROM USERS WHERE NICK=\"$ns\";");
	$query2->execute;
	my $ava = $query2->fetchrow_array;
	print "<table border=\"0\" cellspacing=\"5\" cellpadding=\"5\"><tr><td><img src=\"$ava\" width=\"120\" height=\"140\"></td><td><h2><strong>Results for Author: <em>$ns</em>\n</h2></strong></td></tr></table><p>Posts:<br/><ol>";
	while (@pinfo=$query->fetchrow_array)
	{
		my ($mid,$time,$topic,$searchubject) = @pinfo;
		if ($searchubject =~ m/^\%/){
			$forum_link = "/clans/" . uri_escape(substr($searchubject,1,length($searchubject))) . "/forum/"; }
		else {
			$forum_link = "/forums/" . uri_escape($searchubject) . "/";
		}
		print "<li>$ns: <a href=\"viewrp.cgi?id=$mid\">$topic</a> (<a href=\"$forum_link\">$searchubject</a>) ($time)<br/>\n";
	}
	$t = $query->rows;
	print "</ol></p><p>Polls:<br/><ol>";
	$query = $db->prepare(qq|SELECT MID,TIME,TOPIC,SUBJECT FROM POLLS WHERE NICK="$ns" AND VISIBLE != 0 ORDER BY MID DESC;|);
	$query->execute;
	while (@pinfo=$query->fetchrow_array)
	{
		my ($mid,$time,$topic,$searchubject) = @pinfo;
		if ($searchubject =~ m/^\%/){
			$forum_link = "/clans/" . uri_escape(substr($searchubject,1,length($searchubject))) . "/forum/"; }
		else {
			$forum_link = "/forums/" . uri_escape($searchubject) . "/";
		}
		print "<li>$ns: <a href=\"viewrp.cgi?id=$mid\">$topic</a> (<a href=\"$forum_link\">$searchubject</a>) ($time)<br/>\n";
	}
	$t += $query->rows;
	print "</ol><center>Results: $t<br/><br/><a href=\"sbase.cgi\">back to the forum</a>";
	print "<form method=\"POST\" action=\"search.cgi\"><br/><input type=\"text\" name=\"query\" value=\"$search\" class=\"text\"/> &nbsp; <input type=\"submit\" value=\"try again\" class=\"submit\"/>";
	skettiEndBoard();
}
