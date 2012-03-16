#!/usr/bin/perl -w

package SkettiSCRIPT;
use strict;
use sketdb;
use CGI qw(param);
use sketact;
use sketusr;
use sketboard;

skettiStartBoard("Edit Message");

my $mode = param('mode');
my $id = param('id');

my $db = skettiLoadDb;

my $query = $db->prepare("SELECT NICK,SUBJECT,TOPIC,QUOTE,QUOTEE,VISIBLE,MSG,SMILIE FROM POSTS WHERE MID = $id;");
$query->execute;

if ($query->rows == 0)
{
	print <<END;

Well, that message doesn't exist, sorry.. you should probably just try to follow links instead of putting in your own values unless you know what you're doing.. you should also <a href="sbase.cgi">leave</a>.

END
	skettiEndBoard(); }

my ($nickn,$pass,$nick);
$nickn = skettiGrabLogin();
if ($nickn != -1) { 
	$pass = skettiGrabPass($nickn);
	skettiUpdateLa($nickn);
	if ($mode ne "save") { $mode = "edit"; }
}
if (($mode eq "auth" || $mode eq "" || !defined $mode) && $nickn == -1 )
{
	print <<END;

<form method="POST" action="editmsg.cgi">
<input type="hidden" name="mode" value="edit">
<input type="hidden" name="id" value="$id">
<strong>Nickname:</strong> <input type="text" name="nick" class="text"/><br/>
<strong>Password:</strong> <input type="password" name="pass" cass="text"/><br/>
<br/><center><input type="submit" value="edit $id" class="submit"/></form>

END
	skettiEndBoard();
}
if ($nickn == -1)
{
	$nick = param('nick');
	$pass = param('pass');
}else{ $nick = $nickn; }
	my @pinfo = $query->fetchrow_array;
	my ($pnick,$subject,$topic,$quote,$quotee,$visible,$msg,$smile) = @pinfo;
	$query = $db->prepare("SELECT PASS,STATUS,LVL FROM USERS WHERE NICK = '$nick';");
	my $selected= "";
	if ($smile == 0) { $selected="selected"; }
	$query->execute;
	my ($upass,$stat,$ulvl) = $query->fetchrow_array;
	if ($upass ne $pass && $nickn == -1) { print "Umm.. shouldn't you know your password?? <a href=\"sbase.cgi\">get out of my sight!</a>";
	skettiEndBoard(); }
		if ($nick ne $pnick && $stat ne "SkettiOP" && $ulvl < 4 && !(skettiIsOp($nick,skettiForum($id))))
	{
		print "Ummm.. what are you trying to do?  Either you edit your OWN message or become an OP, otherwise, <a href=\"sbase.cgi\">leave me alone</a>.";
		skettiEndBoard(); }
		
if ($mode eq "edit")
{
	my $bg = "";
	my ($subj_name,$subj_image);
	if ($nickn != -1) {
		$bg = skettiQuery("SELECT FONTC FROM USERS WHERE NICK = '$nickn';");
	}
	print qq|<script language="javascript">\nfunction changeSubj () {|;
my $query = $db->prepare("SELECT NAME,IMG FROM SUBJECTS ORDER BY NAME ASC;");
$query->execute;
my ($subname,$subimage);
while (($subj_name,$subj_image) = $query->fetchrow_array) { 
if ($subj_name eq $subject) { $subimage = $subj_image; }
print <<END;

if (document.post_form.subject.options[document.post_form.subject.selectedIndex].value == '$subj_name') { document['subject_icon'].src = '$subj_image';
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
	print <<END;

<form method="POST" action="editmsg.cgi" name="post_form">
<input type="hidden" name="nick" value="$nick">
<input type="hidden" name="pass" value="$pass">
<input type="hidden" name="id" value="$id">
<input type="hidden" name="mode" value="save">
<table border="0" cellspacing="0" cellpadding="10">
<tr><td bgcolor="$bg"><img name="subject_icon" src="$subimage" alt="Subject" width="120" height="140"/></td></tr>
<tr><td bgcolor="$bg"><strong><u>Subject:</u></strong></td><td><select name="subject" onChange="changeSubj()">

END
	$query = $db->prepare("SELECT NAME FROM SUBJECTS ORDER BY NAME ASC;");
	$query->execute;
	while ($subname = $query->fetchrow_array)
	{
		if ($subname eq $subject) { print "<option selected value=\"$subname\">$subname</option>"; }else{
			print "<option value=\"$subname\">$subname</option>";
		}
	}
print <<END;
</select></td></tr>
<tr><td bgcolor="$bg"><strong><u>Topic:</u></strong></td><td><input type="text" name="topic" value="$topic" class="text"/></td></tr>
<tr><td bgcolor="$bg"><strong><u>Message:</u></strong></td><td><textarea name="msg" rows="25" cols="80" class="textarea">$msg</textarea></td></tr>
<tr><td bgcolor="$bg"><strong><u>Quote:</u></strong></td><td><input type="text" name="quote" value="$quote" class="text"/></td></tr>
<tr><td bgcolor="$bg"><strong><u>Quotee:</strong></u></td><td><input type="text" name="quotee" value="$quotee" class="text"/></td></tr>
<tr><td bgcolor="$bg"><strong><u>Smilies:</u></strong></td><td><select name="smilies"><option value="1">Enabled</option>
<option $selected value="0">Disabled</option></select></td></tr>
<tr><td bgcolor="$bg"><strong><u>Display:</u></strong></td><td><select name="display">
END
if ($visible == 1) { print qq|<option selected value="1">Public</option><option value="2">Private</option>|; } else {
	print qq|<option value="1">Public</option><option selected value="2">Private</option>|; }
	
print <<END;
</select></td></tr>
</table><br/>
<center><input type="submit" value="save post $id" class="submit"/></center>
</form>

END

skettiEndBoard();
}
if ($mode eq "save")
{
	my $nquote = param('quote');
	my $nquotee = param('quotee');
	my $ntopic = param('topic');
	my $subject = param('subject');
	my $nmsg = param('msg');
	my $smilie = param('smilies');
	my $display = param('display');

$nmsg =~ s/'/\\'/g;
$ntopic =~ s/'/\\'/g;
$nquote =~ s/'/\\'/g;
$nquotee =~ s/'/\\'/g;
$subject =~ s/'/\\'/g;

	$query=$db->prepare ("UPDATE POSTS SET QUOTE = '$nquote', QUOTEE = '$nquotee', TOPIC = '$ntopic', MSG = '$nmsg',SUBJECT = '$subject', SMILIE=$smilie, VISIBLE = $display WHERE MID = $id;");
	$query->execute;
	$query = $db->prepare("UPDATE BASE SET FORUM = '$subject', VISIBLE = $display WHERE MID = $id;");
	$query->execute;
	print <<END;

Thank you, $nick, the post <a href="viewrp.cgi?id=$id">(pid $id)</a> has been updated.
<br/>go <a href="sbase.cgi">back to the base</a>.

END
	skettiEndBoard();
}
