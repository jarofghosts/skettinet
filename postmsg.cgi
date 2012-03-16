#!/usr/bin/perl -w

package SkettiSCRIPT;
use strict;
use CGI qw(param);
use DBI;
use Date::Calc qw(Delta_DHMS);
use sd;

print "Content-type: text/html\n\n";
my $theme = getTheme();

open (TOP, "themes/$theme.tf") || skettiError ("Cannot open top file");
open (BOTTOM, "themes/$theme.bf") || skettiError ("Cannot open bottem file");
while (<TOP>) { print $_; }
close(TOP);

my $db = loadDb();

my $mode = param('mode');
my $bg = "";
our $query;

my $nickn = grabLogin();
if ($nickn != -2 && $nickn != -1) { 
	updateLa($nickn);
	$query = $db->prepare("SELECT FONTC FROM USERS WHERE NICK = '$nickn';");
	$query->execute;
	$bg = $query->fetchrow_array;
}

if ($mode eq "get" || $mode eq "")
{
	print <<END;

<form method="POST" action="powst.cgi">
<input type="hidden" name="mode" value="save">
<table border=0 cellspacing=0 cellpadding=10>
END
if ($nickn == -2)
{
	print <<END;
	<tr><td><strong><u>Nickname:</u></strong></td><td><input type="text" name="nick"></td></tr>
	<tr><td><strong><u>Password:</u></strong></td><td><input type="password" name="pass"></td></tr>
END
}else{
	my $query = $db->prepare("SELECT PASS FROM USERS WHERE NICK = '$nickn';");
	$query->execute;
	my $npass = $query->fetchrow_array;
	print <<END;
	<tr><td bgcolor="$bg"><strong><u>Nickname:</u></strong></td><td>$nickn</td></tr>
	<input type="hidden" name="nick" value="$nickn">
	<input type="hidden" name="pass" value="$npass">
END
}
print <<END;

<tr><td bgcolor="$bg"><b><u>Subject:</u></b></td><td><select name="subject">

END

system("ls subjects/*.JPG > .picindex");
open (PICS, ".picindex");
while (<PICS>)
{
	chomp ($_);
	$_ =~ s/subjects\///gi;
	my ($subname, $ext) = split(/\./,$_);
	print "<option>$subname</option>\n";
}
close(PICS);

print <<END;
</select></td></tr>
<tr><td bgcolor="$bg"><strong><u>Topic:</u></strong></td><td><input type="text" name="topic"></td></tr>
<tr><td bgcolor="$bg"><strong><u>Message:</u></strong></td><td><textarea name="msg" rows="25" cols="80">
</textarea></td></tr>
<tr><td bgcolor="$bg"><strong><u>Quote:</u></strong></td><td><em>&quot;</em><input type="text" name="quote"><em>&quot;</em></td></tr>
<tr><td bgcolor="$bg"><strong><u>Quotee:</u></strong></td><td>-<input type="text" name="quotee"></td></tr></table>
<center><input type="submit" value="post"></form>

END

	EndSBoard();
}elsif ($mode eq "save")
{

	our $nick = param('nick');
	our $pass = param('pass');
	our $subj = param('subject');
	our $topic = param('topic');
	our $msg = param('msg');
	$msg =~ s/'/\\'/gi;
	$topic =~ s/'/\\'/gi;
	our $quote = param('quote');
	our $quotee = param('quotee');
	$topic =~ s/'/\\'/gi;
	$topic =~ s/'/\\'/gi;
	if ($nick eq "" || $pass eq "" || $subj eq "" || $topic eq "" || $msg eq "")
	{
		print <<END;

Umm.. you are missing some stuff in your post there.. you should probably <a href="powst.cgi?mode=get">go back</a> and fill it in.

END
EndSBoard();
}
	$query = $db->prepare("SELECT MSG FROM POSTS WHERE NICK = '$nick' AND VISIBLE = 1 ORDER BY MID DESC;");
	$query->execute;
		{
			my $tmsg = $query->fetchrow_array;
			if ($msg eq $tmsg) {
			print <<END;

Whoa, whoa, whoa!<br>
Simmer down now, there's really no need to post the same thing twice is there?<br>
Why don't you sit back and <a href="sbase.cgi">relax</a>?

END
EndSBoard();
}
}
	$query = $db->prepare("SELECT UID,NICK,PASS,STATUS,URL,FONTC,BAN FROM USERS WHERE NICK = '$nick';");
	$query->execute;
	my $test = $query->rows;
	if ($test == 0)
	{
		print <<END;

Appy polly loggies!<br><br>You must <a href="join.cgi?mode=get">register</a> first.

END
EndSBoard();
}
	my @info = $query->fetchrow_array;
	my ($uid,$unick,$upass,$ustat,$url,$ufontc,$ban) = @info;
	if ($ban == 1) {
		print "You have been BANISHED!  Do not attempt to return here.\n";
		EndSBoard();
	}
	if ($upass ne $pass)
	{
		print <<END;
All right, poseur, don't pretend to be something you are not, why don't you find out the RIGHT password and <a href="powst.cgi?mode=get">try again</a>

END
EndSBoard();
}
	$quote =~ s/'/\\'/gi;
	$quotee =~ s/'/\\'/gi;
	$topic =~ s/'/\\'/gi;

	$query = $db->prepare("SELECT * FROM POSTS;");
	$query->execute;
	my $pid = $query->rows;
	$pid--;
	my $time = localtime;
	$query = $db->prepare("SELECT LASTR FROM POSTS ORDER BY LASTR DESC;");
	$query->execute;
	my $lastr = $query->fetchrow_array;
	$lastr++;
	my $ip = $ENV{REMOTE_ADDR};
	$time =~ s/  / /gi;
	$query = $db->prepare("UPDATE USERS SET EXP = EXP + 1 WHERE NICK = '$nick';");
	$query->execute;
	$query = $db->prepare("INSERT INTO POSTS (MID,NICK,SUBJECT,TOPIC,TIME,QUOTE,QUOTEE,REPLIES,VISIBLE,MSG,LASTR,SCORE,IP) VALUES ($pid, '$nick', '$subj', '$topic', '$time', '$quote', '$quotee', 0, 1, '$msg',$lastr,0,'$ip');");
	$query->execute;
	system ("./updaterdf.pl");
	print "Thank you, $nick.  Click <a href=\"viewrp.cgi?id=$pid\">here</a> to view your thread.";
EndSBoard();
}
