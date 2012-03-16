#!/usr/bin/perl -w

package SkettiSCRIPT;
use strict;
use sketdb;
use sketusr;
use sketboard;
#use sketxml;
use sketact;
use CGI qw(param);

my $mode = param('mode');
skettiStartBoard("Create a Channel");

my ($query,$status,$lvl);
my $bg = "";
my $db = skettiLoadDb();

my $nickn = skettiGrabLogin();
if ($nickn != -1) {
	skettiUpdateLa($nickn);
	$query = $db->prepare("SELECT FONTC,STATUS,LVL FROM USERS WHERE NICK = '$nickn';");
	$query->execute;
	($bg,$status,$lvl) = $query->fetchrow_array;
}
if ($nickn == -1 || ($status ne "SkettiOP" && $lvl < 4))
{
	print "I'm sorry, you must be logged in and a SkettiOP or AT LEAST level 3.  Try <a href=\"sbase.cgi\">posting and whatnot</a>.";
	skettiEndBoard(); }

if ($mode eq "get" || $mode eq "")
{
	print <<END;
<form method="POST" action="channel.cgi">
<input type="hidden" name="mode" value="save">
<table border=0 cellspacing=0 cellpadding=10>
<tr><td bgcolor="$bg"><strong><u>Nickname:</u></strong></td><td>$nickn</td></tr>
<tr><td bgcolor="$bg"><strong><u>Subject</u></strong></td><td><select name="subject">
END

my $query = $db->prepare("SELECT NAME FROM SUBJECTS ORDER BY NAME ASC;");
$query->execute;
my $subname;
while ($subname = $query->fetchrow_array) { print "<option>$subname</option>"; }

print <<END;
</select></td></tr>
<tr><td bgcolor="$bg"><strong><u>Name:</u></strong></td><td><input type="text" name="name"></td></tr>
<tr><td bgcolor="$bg"><strong><u>Topic:</u></strong></td><td><input type="text" name="topic"></td></tr>
<tr><td bgcolor="$bg"><strong><u>Clear<sup>*</sup>:</u></strong></td><td><select name="clr"><option>yes</option><option>no</option></select>
</table>
<center><input type="submit" value="create"></form><br><sup>*</sup>This function will clear the channel every 30 minutes.

END
	skettiEndBoard();
}elsif ($mode eq "save")
{
	my $subj = param('subject');
	my $topic = param('topic');
	my $name = param('name');
	my $clear = param('clr');
	if ($clear eq "yes") { $clear = 1; }else{ $clear = 0; }
	$name =~ s/'/\\'/gi;
	$topic =~ s/'/\\'/gi;
	if ($topic eq "" || $name eq "")
	{
		print <<END;

You need some more stuff in your post.. go <a href="channel.cgi">back</a> and fill the rest out.

END
	skettiEndBoard(); }

	if ( skettiIsBanned("$nickn") == 1 )
	{
		print "You have been BANISHED!  You shall not pass!";
		skettiEndBoard();
	}
	$query = $db->prepare("SELECT NAME FROM CHANS WHERE NAME = '$name';");
	$query->execute;
	if ($query->rows > 0)
	{
		print "Sorry, a channel of that name already exists.  You could <a href=\"channel.cgi\">try again</a>, though.";
		EndSBoard();
	}
	$query = $db->prepare("SELECT MID,LASTR FROM BASE ORDER BY LASTR DESC;");
	$query->execute;
	my $pid = $query->rows;
	$pid--;
	my $time = localtime;
	my ($zz, $lastr) = $query->fetchrow_array;
	$lastr++;
	my $ip = $ENV{'REMOTE_ADDR'};
	$time =~ s/  / /gi;
	skettiUpdateLvl($nickn,1);
	skettiSendZiggyMsg ($nickn, "Creation of #$name has gained you 1 EXP!");
	$query = $db->prepare ("INSERT INTO CHANS (MID,NICK,SUBJECT,TOPIC,TIME,VISIBLE,NAME,IP,LOG,CLEAR) VALUES ($pid,'$nickn','$subj','$topic','$time',1,'$name','$ip','',$clear);");
	$query->execute;
	$query = $db->prepare ("INSERT INTO BASE (MID,TYPE,LASTR,SCORE,VISIBLE) VALUES ($pid,'chan',$lastr,0,1);");
	$query->execute;
	print "Thank you, $nickn, your channel #$name has been created, Click <a href=\"sbase.cgi\">here</a> to return to the base.";
	#skettiUpXML();
	skettiEndBoard();
}
