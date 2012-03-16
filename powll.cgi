#!/usr/bin/perl -w
use strict;

package SkettiSCRIPT;
use CGI qw(param);
use sketdb;
use sketziggy;
use sketact;
use sketusr;
#use sketxml;
use sketboard;

my $mode = param('mode');

skettiStartBoard("Post a Poll");

my ($query,$status,$lvl);
my $bg = "";
my $db = skettiLoadDb();
my ($subj_name,$subj_image,$subname,$subimage);
my $db = skettiLoadDb();
print qq|<script language="javascript">\nfunction changeSubj () {|;
my $query = $db->prepare("SELECT NAME,IMG FROM SUBJECTS ORDER BY NAME ASC;");
$query->execute;
my $i = 0;
while (($subj_name,$subj_image) = $query->fetchrow_array) {
if ($i == 0) { $subname = $subj_name; $subimage = $subj_image; }
print <<END;

if (document.post_form.subject.options[document.post_form.subject.selectedIndex].value == '$subj_name') { document['subject_icon'].src = '$subj_image' }

END
$i++;
}
print "} </script>";


my $nickn = skettiGrabLogin();
if ($nickn != -1) {
	skettiUpdateLa($nickn);
	$query = $db->prepare("SELECT FONTC,STATUS,LVL FROM USERS WHERE NICK = '$nickn';");
	$query->execute;
	($bg,$status,$lvl) = $query->fetchrow_array;
}
if ($nickn == -1 || ($status ne "SkettiOP" && $lvl < 2))
{
	print "I'm sorry, you must be logged in and a SkettiOP or AT LEAST level 2.  Try <a href=\"sbase.cgi\">posting and whatnot</a>.";
	skettiEndBoard();
}

if ($mode eq "get" || $mode eq "")
{
	print <<END;
<form method="POST" action="powll.cgi" name="post_form">
<input type="hidden" name="mode" value="save">
<table border=0 cellspacing=0 cellpadding=10>
<tr><td bgcolor="$bg"><img src="$subimage" name="subject_icon" alt="Subject" width="120" height="140"/></td></tr>
<tr><td bgcolor="$bg"><strong><u>Nickname:</u></strong></td><td>$nickn</td></tr>
<tr><td bgcolor="$bg"><strong><u>Subject:</u></strong></td><td><select name="subject" onChange="changeSubj()">
END

my $query = $db->prepare("SELECT NAME FROM SUBJECTS ORDER BY NAME ASC;");
$query->execute;
while ($subj_name = $query->fetchrow_array) { 
if ($subname eq $subj_name) { print "<option selected value=\"$subj_name\">$subj_name</option>"; }
print "<option value=\"$subj_name\">$subj_name</option>"; }

print<<END;
</select></td></tr>
<tr><td bgcolor="$bg"><strong><u>Option #1:</u></strong></td><td><input type="text" name="opt1"></td></tr>
<tr><td bgcolor="$bg"><strong><u>Option #2:</u></strong></td><td><input type="text" name="opt2"></td></tr>
<tr><td bgcolor="$bg"><strong><u>Option #3:</u></strong></td><td><input type="text" name="opt3"></td></tr>
<tr><td bgcolor="$bg"><strong><u>Option #4:</u></strong></td><td><input type="text" name="opt4"></td></tr>
<tr><td bgcolor="$bg"><strong><u>Option #5:</u></strong></td><td><input type="text" name="opt5"></td></tr>
<tr><td bgcolor="$bg"><strong><u>Topic:</u></strong></td><td><input type="text" name="topic"></td></tr>
<tr><td bgcolor="$bg"><strong><u>Poll Text:</u></strong></td><td><textarea name="txt" rows="25" cols="80">
</textarea></td></tr></table>
<center><input type="submit" value="post"></form>

END
	skettiEndBoard();
}elsif($mode eq "save")
{
	my $subj = param('subject');
	my $topic = param('topic');
	my $txt = param('txt');
	my $opt1 = param('opt1');
	my $opt2 = param('opt2');
	my $opt3 = param('opt3');
	my $opt4 = param('opt4');
	my $opt5 = param('opt5');
	if ($topic eq "" || $txt eq "")
	{
		print "You need to fill some crap out on there, so go <a href=\"powll.cgi\">back</a> and fill it out.";
		skettiEndBoard(); }
	if (skettiIsBanned($nickn) == 1) {
		print "You have been BANISHED!  Do not attempt to return here.\n";
		skettiEndBoard(); }
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
	$query->execute;
	skettiSendZiggyMsg $nickn, "Creation of the &quot;$topic&quot poll has gained you 1 EXP!";
	$query = $db->prepare(qq|INSERT INTO POLLS (MID,NICK,SUBJECT,TOPIC,TIME,VISIBLE,TXT,OPT1,OPT2,OPT3,OPT4,OPT5,OPT1N,OPT2N,OPT3N,OPT4N,OPT5N,IP,TOTAL,VOTERS,VIEWS) VALUES ($pid,"$nickn","$subj","$topic","$time",1,"$txt","$opt1","$opt2","$opt3","$opt4","$opt5",0,0,0,0,0,"$ip",0,"",0)|);
	$query->execute;
	$query = $db->prepare(qq|INSERT INTO BASE (MID,TYPE,LASTR,SCORE,VISIBLE,FORUM) VALUES ($pid,"poll",$lastr,0,1,"$subj");|);
	$query->execute;
	#skettiUpXML();
	print "Thank you, $nickn, your poll has been added.  Click <a href=\"sbase.cgi\">here</a> to return to the base.";
	skettiEndBoard();
}
