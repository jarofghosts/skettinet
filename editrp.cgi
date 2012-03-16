#!/usr/bin/perl -w

package SkettiSCRIPT;
use strict;
use sketboard;
use sketdb;
use sketact;
use sketusr;
use skettime;
use CGI qw(param);

skettiStartBoard("Edit Reply");

my $mode = param('mode');
my $id = param('id');
my $pid = param('mid');
my $db = skettiLoadDb();

my $query = $db->prepare("SELECT * FROM REPLIES WHERE RID = '$id' AND MID = '$pid';");
$query->execute;

if ($query->rows == 0)
{
	print "Well, that reply doesn't exist, sorry..<br/>you should probably just try to follow links instead of putting in your own values unless you know what you're doing.. you should also <a href=\".\">leave</a>.";
	skettiEndBoard();
}
my ($nick,$pass,$bg);
$nick = skettiGrabLogin();
if ($nick != -1)
{
	my $q = $db->prepare("SELECT PASS,FONTC FROM USERS WHERE NICK = \"$nick\";");
	$q->execute;
	($pass,$bg) = $q->fetchrow_array;
	skettiUpdateLa($nick);
	if ($mode ne "save") { $mode = "edit";}
}
	if (($mode eq "auth" || $mode eq "") && $nick == -1)
{
	print <<END;

<form method="POST" action="editrp.cgi">
<input type="hidden" name="mode" value="edit">
<input type="hidden" name="id" value="$id">
<input type="hidden" name="mid" value="$pid">
<table border="0">
<tr><td><strong>Nickname:</strong></td><td><input type="text" name="nick" class="text"/></td></tr>
<tr><td><strong>Password:</strong></td><td><input type="password" name="pass" class="text"/></td></tr>
<tr><td colspan="2"><center><input type="submit" value="edit $id" class="submit"/></center></td></tr>
</table></form>

END
skettiEndBoard();
}
if ($nick == -1)
{
	$nick = param('nick');
	$pass = param('pass');
}
	my @pinfo = $query->fetchrow_array;
	my ($mid,$pnick,$quote,$quotee,$time,$msg,$oid,$ip,$rate,$rid,$score,$quote_rep,$smile) = @pinfo;
	my $selected = "";
	if ($smile == 0) { $selected="selected"; } 
	$query = $db->prepare("SELECT PASS,STATUS,LVL FROM USERS WHERE NICK = '$nick';");
	$query->execute;
	our @uinfo = $query->fetchrow_array;
	our ($upass,$stat,$lvl) = @uinfo;
	$query = $db->prepare("SELECT NICK FROM POSTS WHERE MID = $pid;");
	$query->execute;
	my $tnick = $query->fetchrow_array;
	if ($upass ne $pass) { print "Sorry, your password is in another castle.<br><a href=\"sbase.cgi\">flock off</a>.";
	skettiEndBoard(); }
	if ($nick ne $pnick && $stat ne "SkettiOP" && ($lvl < 3 || $nick ne $tnick) && $lvl < 4 && !(skettiIsOp($nick,skettiForum($pid))))
	{
		print <<END;

Ummm.. what are you trying to do?  Either you edit your OWN message or become an OP or a <em>King/Queen</em>.. as an <em>Apprentice</em>, you can edit replies to your OWN thread.  Otherwise, <a href="sbase.cgi">leave me alone</a>.

END

	skettiEndBoard();
}
	if ($mid == -2)
	{
		print "That message isn't even viewable.. what's the point of editing it?<br/>maybe you need to take a <a href=\"sbase.cgi\">break</a>.";
	skettiEndBoard(); }
if ($mode eq "edit")
{
	print <<END;

<form method="POST" action="editrp.cgi">
<input type="hidden" name="nick" value="$nick">
<input type="hidden" name="pass" value="$pass">
<input type="hidden" name="id" value="$id">
<input type="hidden" name="mid" value="$pid">
<input type="hidden" name="mode" value="save">
<table border="0" cellspacing="0" cellpadding="10">
<tr><td bgcolor="$bg"><strong><u>Message:</u></strong></td><td><textarea name="msg" rows="25" cols="80" class="textarea">$msg</textarea></td></tr>
<tr><td bgcolor="$bg"><strong><u>Quote:</strong></u></td><td><input type="text" name="quote" value="$quote" class="text"/></td></tr>
<tr><td bgcolor="$bg"><strong><u>Quotee:</u></strong></td><td><input type="text" name="quotee" value="$quotee" class="text"/></td></tr>
<tr><td bgcolor="$bg"><strong><u>Smilies:</u></strong></td><td><select name="smilies"><option value="1">Enabled</option>
<option $selected value="0">Disabled</option></select></td></tr>
</table>
<br/><center><input type="submit" value="save reply" class="submit"/></center>
</form>

END

skettiEndBoard();
}
if ($mode eq "save")
{
	my $nquote = param('quote');
	my $nquotee = param('quotee');
	my $ntopic = param('topic');
	my $nmsg = param('msg');

$nmsg =~ s/'/\\'/gi;
$nquote =~ s/'/\\'/gi;
$nquotee =~ s/'/\\'/gi;

	skettiQuery ("UPDATE REPLIES SET QUOTE = '$nquote', QUOTEE = '$nquotee', MSG = '$nmsg' WHERE RID = '$id' AND MID = '$pid';");
	print <<END;

Thank you, $nick, the reply has been updated.
<br/>go <a href="viewrp.cgi?id=$mid#$id">here</a> to view it, or click <a href=".">here</a> to return to the forum..

END
skettiEndBoard();
}
