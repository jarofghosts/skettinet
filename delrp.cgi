#!/usr/bin/perl -w

package SkettiSCRIPT;
use strict;
use sketact;
use CGI qw(param);
use sketdb;
use sketusr;
use sketboard;
use sketmsgs;
use sketlog;
use sketziggy;

skettiStartBoard("Delete Reply");

my $mode = param('mode');
my $id = param('id');
my $pid = param('mid');

my $db = skettiLoadDb();

my $query = $db->prepare("SELECT NICK,MSG FROM REPLIES WHERE RID = $id AND MID = $pid;");
$query->execute;

if ($query->rows == 0)
{
	print <<END;

Well, that reply doesn't exist, sorry.. you should probably just try to follow links instead of putting in your own values unless you know what you're doing.. you should also <a href="sbase.cgi">leave</a>.

END
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

<form method="POST" action="delrp.cgi">
<input type="hidden" name="mode" value="del">
<input type="hidden" name="id" value="$id">
<input type="hidden" name="mid" value="$pid">
<table border="0">
<tr><td><strong>Nickname:</strong></td><td><input type="text" name="nick" class="text"/></td></tr>
<tr><td><strong>Password:</strong></td><td><input type="password" name="pass" class="text"/></td></tr>
<tr><td colspan="2"><center><input type="submit" value="check reply" class="submit"/></td></tr>
</table></form>

END
	skettiEndBoard(); }
if ($nick == -1)
{
	$nick = param('nick');
	$pass = param('pass');
}
	my @pinfo = $query->fetchrow_array;
	my ($pnick,$msg) = @pinfo;
	$query = $db->prepare("SELECT PASS,STATUS,LVL FROM USERS WHERE NICK = '$nick';");
	$query->execute;
	my @uinfo = $query->fetchrow_array;
	my ($upass,$stat,$ulvl) = @uinfo;
	if ($upass ne $pass) { print "That password appears to be completely wrong.. <a href=\".\">go away.</a>";
	skettiEndBoard(); }
	if ($nick ne $pnick && $stat ne "SkettiOP" && $ulvl < 7 && !(skettiIsOp($nick,skettiForum($pid))))
	{
		print "Ummm.. what are you trying to do?  Either you delete your OWN message or become an OP or <em>Deity</em>, otherwise, <a href=\".\">go away.</a>";
		skettiEndBoard(); }

	if ($pid == -2)
	{
		print "It appears that message has ALREADY been deleted..dumbass.<p><a href=\".\">leave me alone</a>";
		skettiEndBoard(); }
if ($mode eq "del")
{
	$msg =~ s/\r\n/<br\/>/g;
		print skettiBuildReply($pid,$id,undef,1);
	print <<END;
<br/><hr noshade><br/>
<form method="POST" action="delrp.cgi">
<input type="hidden" name="id" value="$id">
<input type="hidden" name="mid" value="$pid">
<input type="hidden" name="mode" value="rm">
<input type="hidden" name="nick" value="$nick">
<input type="hidden" name="pass" value="$pass">
<input type="hidden" name="pnick" value="$pnick">
Would you like to deduct 2 EXP from $pnick? 
<select name="punish"><option value="1">yes</option><option value="0">no</option></select><br/>
<center><input type="submit" value="delete reply" class="submit"/>
</form>

END

	skettiEndBoard(); }

if ($mode eq "rm")
{

	my $panick = param('pnick');
	my $punish = param('punish');
	skettiQuery ("UPDATE REPLIES SET OID = MID, MID = -2 WHERE RID = $id AND MID = $pid;");
	if ($punish == 1) { 
		skettiQuery ("UPDATE USERS SET EXP = EXP - 2 WHERE NICK = '$panick';");
		skettiSendZiggyMsg ($panick, "A reply of yours has been deleted- unfortunately it will cost you 2 EXP."); }
		skettiLog ("$nick deletes $panick\'s reply (rid $id) to mid $pid");
print <<END;

Thank you, $nick, the reply has been deleted
<br/>go <a href="sbase.cgi">back</a> to the base.

END
	skettiEndBoard();
}
