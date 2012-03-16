#!/usr/bin/perl -w

package SkettiSCRIPT;
use strict;
use sketdb;
use sketact;
use sketusr;
use sketboard;
use sketmsgs;
use CGI qw(param debug);

skettiStartBoard("Add Reply");
my $nickn = skettiGrabLogin();
my $theme = skettiGrabTheme();
my $db = skettiLoadDb();
my $passn="";
if ($nickn != -1) { $passn = skettiGrabPass ($nickn); }
my $mode = param('mode');
my $id = param('id');
my $rquote = param('rquote');
my $type = skettiGrabType($id);

my ($dbt,$mdb,$query);
if ($type eq "post") { $dbt = "POSTS";$mdb = "MSG"; }
elsif ($type eq "poll") { $dbt = "POLLS";$mdb = "TXT"; }
$query = $db->prepare("SELECT NICK,TOPIC,$mdb FROM $dbt WHERE MID = $id AND VISIBLE >= 1;");
$query->execute;
if ($query->rows == 0)
{
	print "That post either doesn't exist or has been killed.  It is not possible to reply to it.  You can <a href=\"sbase.cgi\">go back</a> to the forum, though.";
	skettiEndBoard(); }

if ($mode eq "" || $mode eq "get")
{
	my $bg = "";
	my ($repnick, $repmsg);
	if (defined $rquote) { 
		$query = $db->prepare("SELECT NICK,MSG FROM REPLIES WHERE MID = $id AND RID = $rquote");
		$query->execute;
		($repnick,$repmsg) = $query->fetchrow_array;
	}
	if ($nickn != -1) {$bg = skettiQuery "SELECT FONTC FROM USERS WHERE NICK =\"$nickn\";"}
	my $post;
	if ($type eq "post") { $post = skettiBuildPost($id,1,9999999,undef,undef); } elsif ($type eq "poll") {
		$post = skettiBuildPoll($id,1,undef); }
	print <<END;
	$post
<br/><hr noshade>
<br/><form method="POST" action="replym.cgi">
<table border=0 cellspacing=0 cellpadding=10>
<input type="hidden" name="id" value="$id">
<input type="hidden" name="mode" value="areply">
END
if ($nickn == -1)
{
	print <<END;
	<tr><td><strong><u>Nickname:</u></strong></td><td><input type="text" name="nick" class="text"/></td></tr>
	<tr><td><strong><u>Password:</u></strong></td><td><input type="password" name="pass" class="text"/></td></tr>

END
}else{

	print <<END;
	<tr><td bgcolor="$bg"><strong><u>Nickname:</u></strong></td><td>$nickn</td></tr>
	<input type="hidden" name="nick" value="$nickn">
	<input type="hidden" name="pass" value="$passn">
END
}
if (defined $rquote) { print qq|<input type="hidden" name="rep_quote" value="$repnick">\n|; }
print <<END;

<tr><td bgcolor="$bg"><strong><u>Message:</u></strong></td><td><textarea name="reply" rows="25" cols="80" class="textarea">
END
if (defined $rquote) { $repmsg =~ s/<pull_quote>(.*?)<\/pull_quote>(\r\n)*//gis; }
if (defined $rquote) { print qq|<pull_quote>$repmsg</pull_quote>\n\n| }
print <<END;
</textarea></td></tr>
<tr><td bgcolor="$bg"><strong><u>Quote:</u></strong></td><td><em>&quot;</em><input type="text" name="quote" class="text"/><em>&quot;</em></td></tr>
<tr><td bgcolor="$bg"><strong><u>Quotee:</u></strong></td><td>-<input type="text" name="quotee" class="text"/></td></tr>
<tr><td bgcolor="$bg"><strong><u>Smilies:</u></strong></td><td><select name="smilies"><option value="1">Enabled</option>
<option value="0">Disabled</option></select></td></tr>
</table>
<br/><center><input type="submit" value="reply" class="submit"/></center></form>

END

skettiEndBoard();
}
if ($mode eq "areply")
{

my $nick = param('nick');
my $pass = param('pass');
my $reply = param('reply');
my $quote = param('quote');
my $quotee = param('quotee');
my $rep_quote = param('rep_quote');
my $smile = param('smilies');

$query = $db->prepare("SELECT PASS, BAN FROM USERS WHERE NICK=\"$nick\";");
$query->execute;
if ($query->rows == 0)
{
	print "Sorry, you must <a href=\"register.cgi?mode=get\">register</a> before sharing your wisdom, $nick.";
	skettiEndBoard(); }
my ($rpass,$ban) = $query->fetchrow_array;
if ($ban == 1)
{
	print "You have been BANISHED you foul creature.  Leave this place and do not intend to invade our postspace.";
	skettiEndBoard(); }

if ($rpass ne $pass)
{
	print "Umm.. looks like you're not who you claim to be..<br/>you should probably <a href=\"sbase.cgi\">leave</a>.";
	skettiEndBoard(); }

if ($reply =~ m/<pull_quote>/ && !($reply =~ m/<\/pull_quote>/)) {
	print "Why did you delete the end tag on the quote? Think that's funny? <a href=\"sbase.cgi\">go away</a>";
	skettiEndBoard(); }

my $dvl = time;
my $time = skettiGetTA();

skettiQuery ("UPDATE POSTS SET LASTR = $dvl WHERE MID = $id;");
skettiQuery ("UPDATE BASE SET LASTR = $dvl WHERE MID = $id;");
skettiUpdateLvl ($nick,1);
$reply =~ s/"/\\"/g;
my $ip = $ENV{REMOTE_ADDR};
$query = $db->prepare("SELECT RID FROM REPLIES WHERE MID = $id ORDER BY RID DESC;");
$query->execute;
my $rid = $query->fetchrow_array;
$rid++;
$query = $db->prepare(qq|INSERT INTO REPLIES (RID,MID,NICK,MSG,QUOTE,QUOTEE,TIME,IP,SMILIES) VALUES ($rid,$id,"$nick","$reply","$quote","$quotee","$time","$ip",$smile)|);
$query->execute;
if (defined $rep_quote) {
	$query = $db->prepare(qq|UPDATE REPLIES SET QUOTE_REP = "$rep_quote" WHERE MID = $id AND RID = $rid|);
	$query->execute;
}
print <<END;

Thank you, $nick, your reply to message #$id has been added.
<br/><a href="viewrp.cgi?id=$id#$rid">click here</a> to view it or click <a href="sbase.cgi">here</a> to return to the base..

END

skettiEndBoard(); }
