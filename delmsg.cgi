#!/usr/bin/perl -w

package SkettiSCRIPT;
use strict;
use CGI qw(param);
use sketboard;
use sketdb;
use sketusr;
use sketact;
use sketmsgs;

my ($pnick,$visible,$type);

skettiStartBoard("Delete Message");

my $mode = param('mode');
my $id = param('id');

my $db = skettiLoadDb;

my $query = $db->prepare("SELECT VISIBLE,TYPE FROM BASE WHERE MID = $id;");
$query->execute;
my ($visible,$type) = $query->fetchrow_array;
if ($query->rows == 0)
{
	print "Well, that message doesn't exist, sorry.. you should probably just try to follow links instead of putting in your own values unless you know what you're doing.. you should also <a href=\".\">leave</a>.";
	skettiEndBoard(); }
my ($nick,$pass);
$nick = skettiGrabLogin();
if ($nick != -1)
{
	$pass = skettiGrabPass($nick);
	skettiUpdateLa($nick);
	if ($mode ne "rm") { $mode = "del"; }
}
if (($mode eq "auth" || $mode eq "") && $nick == -1)
{
	print <<END;

<form method="POST" action="delmsg.cgi">
<input type="hidden" name="mode" value="del">
<input type="hidden" name="id" value="$id">
<table border="0">
<tr><td><strong>Nickname:</strong></td><td><input type="text" name="nick" class="text"/></td></tr>
<tr><td><strong>Password:</strong></td><td><input type="password" name="pass" class="text"/></td></tr>
<tr><td colspan="2"><center><input type="submit" value="check $id" class="submit"/></center></td></tr>
</table></form>

END
skettiEndBoard();
}
	if ($nick == -1)
	{
		$nick = param('nick');
		$pass = param('pass');
	}
	$query = $db->prepare("SELECT PASS,STATUS,LVL FROM USERS WHERE NICK = '$nick';");
	$query->execute;
	my $tipe = $type;
	$tipe =~ tr/[a-z]/[A-Z]/;
	$tipe .= "S";
	my ($upass,$stat,$ulvl) = $query->fetchrow_array;
	$query = $db->prepare("SELECT NICK FROM $tipe WHERE MID = $id;");
	$query->execute;
	my $pnick = $query->fetchrow_array;
	if ($upass ne $pass) { print "Hmm.. you should probably know your password, eh?!<br/><a href=\".\">leave</a>";
	skettiEndBoard(); }
	if ($nick ne $pnick && $stat ne "SkettiOP" && $ulvl < 7 && !(skettiIsOp($nick,skettiForum($id))))
	{
		print <<END;

Ummm.. what are you trying to do?  Either you delete your OWN message or become an OP or a <em>Deity</em>, otherwise, <a href="sbase.cgi">leave me alone.</a>

END

	skettiEndBoard(); }
if ($mode eq "del")
{
	my $post_text;
	if ($type eq "poll") { $post_text = skettiBuildPoll($id,1,undef); } elsif ($type eq "post") { $post_text = skettiBuildPost($id,1,999999,undef,undef); }elsif ($type eq "chan") { $post_text = skettiBuildChannel($id,1,999,undef); }
	my $pun = "deduct 3 EXP from";
	if ($visible == 0) { $pun = "grant 3 EXP to"; }
	$query->execute;
	print <<END;
$post_text<br/><hr noshade><br/>
<form method="POST" action="delmsg.cgi">
<input type="hidden" name="id" value="$id">
<input type="hidden" name="mode" value="rm">
<input type="hidden" name="pnick" value="$pnick">
<input type="hidden" name="nick" value="$nick">
<input type="hidden" name="pass" value="$pass">
<br/>Would you like to $pun $pnick? <select name="punish">
<option value="1">yes</option>
<option value="0">no</option></select><br/>
<center><input type="submit" value="delete $id" class="submit"/>
</form>

END

	skettiEndBoard();
}

if ($mode eq "rm")
{
	my $panick = param('pnick');
	my $punish = param('punish');

	if ($type eq "post") { $type = "POSTS"; }elsif ($type eq "poll") { $type = "POLLS"; }elsif ($type eq "chan") { $type = "CHANS"; }
	my $pun = "- 2";
	my $st = 0;
	if ($visible == 0) { $pun = "+ 2"; $st = 1; }
skettiQuery ("UPDATE $type SET VISIBLE = $st WHERE MID = $id;");
skettiQuery ("UPDATE BASE SET VISIBLE = $st WHERE MID = $id;");
if ($punish == 1) {
	skettiQuery ("UPDATE USERS SET EXP = EXP $pun WHERE NICK = '$panick';");
	if ($visible == 1) { skettiSendZiggyMsg ($panick, "Your message #$id has been deleted, resulting in a 3 EXP penalty.  My deepest apologies."); }
	else { skettiSendZiggyMsg ($panick, "Looks like someone made a mistake and deleted your post, so it has been UNdeleted, and as a result, you have been REgranted 3 EXP."); } }

if ($visible == 1) { skettiQuery ("UPDATE REPLIES SET MID = -2, OID = $id WHERE MID = $id;"); } else {
skettiQuery ("UPDATE REPLIES SET MID = OID WHERE OID = $id;"); }

print <<END;

Thank you, $nick, the message (pid $id) has been deleted
<br/>go <a href=".">back</a> to the forum.

END
skettiEndBoard(); }