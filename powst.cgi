#!/usr/bin/perl -w

package SkettiSCRIPT;
use strict;
use CGI qw(param);
use sketdb;
use sketusr;
#use sketxml;
use sketact;
use sketboard;
use sketziggy;


skettiStartBoard("Post a Message");
my ($subj_name,$subj_image);
my $db = skettiLoadDb();
my $cgi = new CGI;
my $forum = defined $cgi->cookie('forum') ? $cgi->cookie('forum') : "*";
print qq|<script language="javascript">\nfunction changeSubj () {|;
my $query;
if (!defined $forum || $forum eq ""){ 
$forum = "*"; }
$query = $db->prepare("SELECT NAME,IMG FROM SUBJECTS ORDER BY NAME DESC;");
$query->execute;
my $disp_select = $forum =~ (m/^\%/) ? "selected" : "";
while (($subj_name,$subj_image) = $query->fetchrow_array) { print <<END;

if (document.post_form.subject.options[document.post_form.subject.selectedIndex].value == '$subj_name') { document['subject_icon'].src = '$subj_image'
END
if ($subj_name =~ m/^\%/) {
	print <<END;
document.post_form.display.options[1].selected = 1
}
END
}else{
	print <<END;
document.post_form.display.options[0].selected = 1
}
END
}
}
print "} </script>";

my $mode = param('mode');
my $bg = "";
our $query;

my $nickn = skettiGrabLogin();
if ($nickn != -1) {
	skettiUpdateLa($nickn);
	$query = $db->prepare("SELECT FONTC FROM USERS WHERE NICK = '$nickn';");
	$query->execute;
	$bg = $query->fetchrow_array;
}
if ($mode eq "get" || $mode eq "")
{
if (!defined $forum || $forum eq "*" || $forum eq ""){ $query = $db->prepare("SELECT NAME,IMG FROM SUBJECTS ORDER BY NAME DESC;");
$forum = "*"; } else {
$query = $db->prepare(qq|SELECT NAME,IMG FROM SUBJECTS WHERE NAME="$forum"|); }
	$query->execute;
	($subj_name,$subj_image) = $query->fetchrow_array;

	print <<END;

<form method="POST" action="powst.cgi" name="post_form">
<input type="hidden" name="mode" value="save">
<table border=0 cellspacing=0 cellpadding=10>
<tr><td bgcolor="$bg"><img name="subject_icon" src="$subj_image" width="120" height="140" alt="Subject"/></td></tr>
END
if ($nickn == -1)
{
	print <<END;
	<tr><td><strong><u>Nickname:</u></strong></td><td><input type="text" name="nick" class="text"/></td></tr>
	<tr><td><strong><u>Password:</u></strong></td><td><input type="password" name="pass" class="text"/></td></tr>
END
}else{
	my $npass = skettiGrabPass($nickn);
	print <<END;
	<tr><td bgcolor="$bg"><strong><u>Nickname:</u></strong></td><td>$nickn</td></tr>
	<input type="hidden" name="nick" value="$nickn">
	<input type="hidden" name="pass" value="$npass">
END
}
print <<END;

<tr><td bgcolor="$bg"><strong><u>Subject:</u></strong></td><td><select name="subject" onChange="changeSubj()">

END

$query = $db->prepare("SELECT NAME,IMG FROM SUBJECTS ORDER BY NAME DESC;");
$query->execute;
my $i = 0;
while (($subj_name,$subj_image) = $query->fetchrow_array) { 
if ((!defined $forum || $forum eq "*") && $i == 0) { print "<option selected value=\"$subj_name\">$subj_name</option>"; } elsif ((!defined $forum || $forum eq "*") && $i != 0) {
print "<option value=\"$subj_name\">$subj_name</option>"; }elsif ((defined $forum) && $forum eq $subj_name) {
print "<option selected value=\"$subj_name\">$subj_name</option>"; }else{
print "<option value=\"$subj_name\">$subj_name</option>"; }
$i++;
}

print <<END;
</select></td></tr>
<tr><td bgcolor="$bg"><strong><u>Topic:</u></strong></td><td><input type="text" name="topic" class="text"/></td></tr>
<tr><td bgcolor="$bg"><strong><u>Message:</u></strong></td><td><textarea class="textarea" name="msg" rows="25" cols="80">
</textarea></td></tr>
<tr><td bgcolor="$bg"><strong><u>Quote:</u></strong></td><td><em>&quot;</em><input type="text" name="quote" class="text"/><em>&quot;</em></td></tr>
<tr><td bgcolor="$bg"><strong><u>Quotee:</u></strong></td><td>-<input type="text" name="quotee" class="text"/></td></tr>
<tr><td bgcolor="$bg"><strong><u>Smilies:</u></strong></td><td><select name="smilies"><option value="1">Enabled</option>
<option value="0">Disabled</option></select></td></tr>
<tr><td bgcolor="$bg"><strong><u>Display:</u></strong></td><td><select name="display"><option value="1">Public</option>
<option $disp_select value="2">Private</option></select></td></tr>
</table>
<center><input type="submit" value="post" class="submit"/></form>

END

	skettiEndBoard();
}elsif ($mode eq "save")
{

	my $nick = param('nick');
	my $pass = param('pass');
	my $subj = param('subject');
	my $topic = param('topic');
	my $msg = param('msg');
	my $smilies = param('smilies');
	my $display = param('display');
	
	$msg =~ s/'/\\'/g;
	$subj =~ s/'/\\'/g;
	$topic =~ s/'/\\'/g;
	my $quote = param('quote');
	my $quotee = param('quotee');
	$quote =~ s/'/\\'/g;
	$quotee =~ s/'/\\'/g;
	if ($nick eq "" || $pass eq "" || $subj eq "" || $topic eq "" || $msg eq "")
	{
		print "Umm.. you are missing some stuff in your post there.. you should probably <a href=\"powst.cgi?mode=get\">go back</a> and fill it in.";
	skettiEndBoard(); }
	$query = $db->prepare("SELECT MSG FROM POSTS WHERE NICK = '$nick' AND VISIBLE = 1 ORDER BY MID DESC;");
	$query->execute;
		{
			my $tmsg = $query->fetchrow_array;
			if ($msg eq $tmsg) {
			print <<END;

Whoa, whoa, whoa!<br/>
Simmer down now, there's really no need to post the same thing twice is there?<br>
Why don't you sit back and <a href="sbase.cgi">relax</a>?

END
skettiEndBoard();
}
}
	$query = $db->prepare("SELECT UID,NICK,PASS,STATUS,URL,FONTC,BAN FROM USERS WHERE NICK = '$nick';");
	$query->execute;
	my $test = $query->rows;
	if ($test == 0)
	{
		print "So sorry!<br/><br/>You must <a href=\"register.cgi?mode=get\">register</a> first.";
	skettiEndBoard(); }
	my @info = $query->fetchrow_array;
	my ($uid,$unick,$upass,$ustat,$url,$ufontc,$ban) = @info;
	if ($ban == 1) {
		print "You have been BANISHED!  Do not attempt to return here.\n";
		skettiEndBoard();
	}
	if ($upass ne $pass)
	{
		print "All right, poseur, don't pretend to be something you are not, why don't you find out the RIGHT password and <a href=\"powst.cgi?mode=get\">try again</a>";
skettiEndBoard(); }
	$query = $db->prepare("SELECT MID FROM BASE;");
	$query->execute;
	my $pid = $query->rows;
	$pid--;
	my $time = localtime;
	my $lastr = time;
	my $ip = $ENV{'REMOTE_ADDR'};
	$time =~ s/  / /gi;
	skettiUpdateLvl($nick,2);
	skettiSendZiggyMsg ($nick, "Since you posted &quot;$topic&quot;, you've gained 2 EXP!");
	$query=$db->prepare ("INSERT INTO POSTS (MID,NICK,SUBJECT,TOPIC,TIME,QUOTE,QUOTEE,REPLIES,VISIBLE,MSG,LASTR,SCORE,IP,VIEWS,SMILIE) VALUES ($pid, '$nick', '$subj', '$topic', '$time', '$quote', '$quotee', 0, $display, '$msg',$lastr,0,'$ip',0,$smilies);");
	$query->execute;
	$query = $db->prepare ("INSERT INTO BASE (MID,TYPE,SCORE,LASTR,VISIBLE,FORUM) VALUES ($pid, 'post', 0, $lastr, $display, '$subj');");
	$query->execute;
	print "Thank you, $nick.  Click <a href=\"viewrp.cgi?id=$pid\">here</a> to view your thread. Or <a href=\"/\">here</a> to return to the forum.";
	#skettiUpXML();
skettiEndBoard();
}
