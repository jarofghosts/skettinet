#!/usr/bin/perl -w

package SkettiSCRIPT;
use strict;
use sketdb;
use sketact;
use sketusr;
use sketboard;
use CGI qw(param);

skettiStartBoard("Rate Post");

my $query;
my $db = skettiLoadDb();
my $id = param('id');
my $mode = param('mode');

my $anick = skettiGrabLogin();

$query = $db->prepare("SELECT STATUS,LVL FROM USERS WHERE NICK='$anick';");
$query->execute;
my ($astat,$alvl) = $query->fetchrow_array;
if (($anick == -1) || ($astat ne "SkettiOP" && $alvl < 7))
{
	print "I'm afraid that you must be logged in (and an <strong>OP</strong> or <em>Deity</em> for that matter) to add a rating to a post.. so <a href=\"sbase.cgi\">away with you</a>.";
	skettiEndBoard(); }
skettiUpdateLa($anick);
$query = $db->prepare("SELECT NICK, SUBJECT, TOPIC, MSG, SCORE, RAT FROM POSTS WHERE MID = $id;");
$query->execute;
my ($nick,$subj,$topic,$msg,$score,$ratan) = $query->fetchrow_array;
if ($anick eq $nick)
{
	print "What kind of a loser are you.. trying to rate your OWN post?  Geesh.. get <a href=\"sbase.cgi\">outta my face</a>.";
	skettiEndBoard(); }

$msg =~ s/\r\n/<br>/gi;

if ($mode eq "view" || $mode eq "")
{
	print <<END;
<p align = left>
<strong>$nick</strong> writes (subject: $subj) on the topic of &quot;$topic&quot;<p>
&quot;$msg&quot;<br>
<font size=-1>(This message is currently scored: $score)</font><br>
</p>
<form method="POST" action="ratepost.cgi">
<strong>Score:</strong> <select name="score"><option>-5</option><option>-4</option><option>-3</option><option>-2</option><option>-1</option><option selected>0</option><option>1</option><option>2</option><option>3</option><option>4</option><option>5</option></select><p><strong>Rating:</strong><br>
END
if ($ratan ne "") { print "$ratan";
print "<input type=\"hidden\" name=\"rating\" value=\"$ratan\">\n";
print "<input type=\"hidden\" name=\"prate\" value=1>\n";
}else{
print <<END;
<input type="hidden" name="prate" value=0>
<textarea name="rating" cols=30 rows=3></textarea><br>
END
}
print <<END;

<input type="hidden" name="mode" value="update">
<input type="hidden" name="id" value=$id>
<input type="submit" value="rate"></form>

END
	skettiEndBoard();
}
if ($mode eq "update")
{
	my $rating = param('rating');
	my $scoring = param('score');
	my $prate = param('prate');
	$rating =~ s/'/\\'/gi;
	if ($prate == 0 && $rating ne "") { $rating = $rating . "<br>-$anick"; }
	$rating =~ s/\r\n/<br>/gi;
	$query = $db->prepare("SELECT NICK,SCORE FROM POSTS WHERE MID = $id;");
	$query->execute;
	my ($mnick, $mscore) = $query->fetchrow_array;
	$mscore += $scoring;
	if ($scoring > 0) { skettiSendZiggyMsg $mnick, "Congrats, <a href=\"viewrp.cgi?id=$id\">your post</a> has gained you $scoring EXP!"; }else{
		my $soo = abs($scoring);
		skettiSendZiggyMsg ($mnick, "Hmm.. <a href=\"viewrp.cgi?id=$id\">your post</a> just lost you $soo EXP.. maybe you should <a href=\"editmsg.cgi?id=$id\">work on it</a>.");
	}
	skettiUpdateLvl ($mnick,$scoring);
	skettiQuery ("UPDATE POSTS SET RAT = '$rating', SCORE = $mscore WHERE MID = $id;");
	skettiQuery ("UPDATE BASE SET SCORE = $mscore WHERE MID = $id;");
	print "Thank you, $anick.  Please <a href=\"sbase.cgi\">return<\/a> to the base.\n";
	skettiEndBoard();
}
