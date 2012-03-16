#!/usr/bin/perl -w

package SkettiSCRIPT;
use strict;
use sketdb;
use sketact;
use sketusr;
use sketboard;
use sketmsgs;
use CGI qw(param);

skettiStartBoard("Rate Reply");

my $query;
my $db = skettiLoadDb();
my $id = param('id');
my $mid = param('mid');
my $mode = param('mode');

my $anick = skettiGrabLogin();

$query = $db->prepare(qq|SELECT STATUS,LVL FROM USERS WHERE NICK="$anick";|);
$query->execute;
my ($astat,$alvl) = $query->fetchrow_array;
if (($anick == -1) || ($astat ne "SkettiOP" && $alvl < 5 && !(skettiIsOp($anick,skettiForum($mid)))))
{
	print "I'm afraid that you must be logged in (and an <strong>OP</strong> or <em>Lord/Lady</em> for that matter) to add a rating to a reply.. so <a href=\".\">away with you</a>.";
	skettiEndBoard(); }
skettiUpdateLa($anick);
$query = $db->prepare("SELECT NICK, MSG, RATE FROM REPLIES WHERE RID = $id AND MID = $mid;");
$query->execute;
my ($nick,$msg,$rating) = $query->fetchrow_array;
if ($anick eq $nick)
{
	print "What kind of a loser are you.. trying to rate your OWN reply?  Geesh.. get <a href=\"sbase.cgi\">outta my face</a>.";
	skettiEndBoard(); }

if ($mode eq "view" || $mode eq "")
{
	print skettiBuildReply($mid,$id,undef,1);
if ($rating ne "") { print "<font size=-1>(This message is currently rated: $rating)</font><br/>"; }
print "</p>";
if ($rating eq "")
{
print <<END;
<form method="POST" action="raterp.cgi">
<strong>Rating:</strong> <select name="rating">
<option>Troll</option>
<option>Insipid</option>
<option>Vapid</option>
<option>Worthless</option>
<option>Unnecessary</option>
<option selected>Slightly Interesting</option>
<option>Insightful</option>
<option>Enlightening</option>
<option>Hilarious</option>
<option>Life Altering</option></select>
<input type="hidden" name="mode" value="update">
<input type="hidden" name="id" value="$id">
<input type="hidden" name="mid" value="$mid">
<input type="submit" value="rate" class="submit"/></form>

END
}
	skettiEndBoard(); }
if ($mode eq "update")
{
	my $rate = param('rating');
	my $score;
	$query = $db->prepare("SELECT NICK FROM REPLIES WHERE RID = $id AND MID = $mid;");
	$query->execute;
	my $mnick = $query->fetchrow_array;
	if ($rate eq "Troll") { $score = -5; }
	elsif ($rate eq "Insipid") { $score = -4; }
	elsif ($rate eq "Vapid") { $score = -3; }
	elsif ($rate eq "Worthless") { $score = -2; }
	elsif ($rate eq "Unnecessary") { $score = -1; }
	elsif ($rate eq "Slightly Interesting") { $score = 1; }
	elsif ($rate eq "Insightful") { $score = 2; }
	elsif ($rate eq "Enlightening") { $score = 3; }
	elsif ($rate eq "Hilarious") { $score = 4; }
	else { $score = 5; }
	if ($score > 0) { skettiSendZiggyMsg ($mnick, "Congrats, <a href=\"viewrp.cgi?id=$mid#$id\">your reply</a> has gained you $score EXP!"); }else{
		my $soo = abs($score);
		skettiSendZiggyMsg ($mnick, "Hmm.. <a href=\"viewrp.cgi?id=$mid#$id\">your reply</a> just lost you $soo EXP.. maybe you should <a href=\"editrp.cgi?id=$id&mid=$mid\">work on it</a>."); }
	skettiUpdateLvl ($mnick,$score);
	my $query = $db->prepare ("UPDATE REPLIES SET RATE = \"$rate\", RATE_SCORE = $score WHERE RID = $id AND MID = $mid;");
	$query->execute;
	print "Thank you, $anick.  Please <a href=\".\">return<\/a> to the forum.\n";
	skettiEndBoard(); }
