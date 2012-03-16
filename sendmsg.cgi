#!/usr/bin/perl -w

package SkettiSCRIPT;
use sketact;
use sketdb;
use sketboard;
use sketusr;
use sketziggy;
use CGI qw(param);
use strict;

skettiStartBoard("Send a Private Message");
my $db = skettiLoadDb();
my $query;

my $nick = skettiGrabLogin();
if ($nick == -1)
{
	print "Sorry, you must be <a href=\"login.cgi\">logged in</a> to send a private message.";
	skettiEndBoard();
}else{
	skettiUpdateLa($nick);
	my $rec = param('to');
	my $msg = param('msg');
	my $mid;
	my $time = localtime;
	$msg =~ s/'/\\'/gi;
	$msg =~ s/"/\\"/g;
	$rec =~ s/'/\\'/gi;
	$nick =~ s/'/\\'/gi;
	$query = $db->prepare("SELECT MID FROM PRIVMSG ORDER BY MID DESC;");
	$query->execute;
	if ($query->rows == 0) { $mid = 0; }else{ $mid = $query->fetchrow_array; $mid++; }
	if ($rec =~ /^%/ || $rec eq "Ziggy") { sendGrp($rec,$nick,$msg,$time,$mid); }
	$query = $db->prepare ("INSERT INTO PRIVMSG (NICK,SENDER,MSG,TIME,MID) VALUES ('$rec', '$nick', '$msg', '$time', $mid);");
	$query->execute;
	print "Thank you, $nick, your message to $rec has been sent.  Please <a href=\"sbase.cgi\">return to the base</a>.";
	skettiEndBoard();
}
sub sendGrp
{
	my $rec = shift; my $nick = shift; my $msg = shift; my $time = shift; my $mid = shift;
	if ($rec eq "Ziggy")
	{
		my $query2 = $db->prepare("SELECT NICK FROM USERS WHERE BAN = 0 AND ZIGGY = 1;");
		$query2->execute;
		my $lnick = $nick;
		$lnick =~ s/ /%20/g;
		$msg = "(<a href=\"users.cgi?nick=$lnick\">$nick</a>) " . $msg;
		my $users;
		while ($users = $query2->fetchrow_array)
		{
			if ($users ne "Ziggy") { skettiSendZiggyMsg($users, $msg); }
		}
		print "Message sent to Ziggy (and thus to EVERYONE)<br/><a href=\"sbase.cgi\">Back to the forum</a>";
		skettiEndBoard();
	}
	$query = $db->prepare("SELECT CID FROM CLANS WHERE NAME=\"$rec\";");
	$query->execute;
	my $cid = $query->fetchrow_array;
	$query = $db->prepare("SELECT NICK FROM USERS WHERE (CLANS REGEXP \",$cid,\" OR CLANS REGEXP \"^$cid,\" OR CLANS REGEXP \",$cid\$\" OR CLANS = \"$cid\");");
	$query->execute;
	my $lnick = $nick;
	$lnick =~ s/ /%20/gi;
	$msg = "(<a href=\"users.cgi?nick=$lnick\">$nick</a>) " . $msg;
	my $ginfo;
	while ($ginfo = $query->fetchrow_array)	{	my $query2=$db->prepare ("INSERT INTO PRIVMSG (NICK,SENDER,MSG,TIME,MID) VALUES ('$ginfo', '$rec', '$msg', '$time', $mid);");$query2->execute;	}
	print "Message sent to group $rec.<br/><a href=\"sbase.cgi\">Back to the forum</a>.";
	skettiEndBoard();
	exit;
}
