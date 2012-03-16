#!/usr/bin/perl -w
use strict;

package SkettiSCRIPT;
use sketdb;
use sketboard;
use sketusr;
use sketziggy;
use CGI qw(param);
use Date::Calc qw(Delta_DHMS);
use DBI;

my ($lbl,$status);
skettiStartBoard();

my $db = skettiLoadDb();

my $nick = skettiGrabLogin();
my $query = $db->prepare_cached("SELECT LVL,STATUS FROM USERS WHERE NICK = '$nick';");
$query->execute;
($lbl,$status) = $query->fetchrow_array;
if ($nick == -1 || $nick == -2 || ($lbl < 8 && $status ne "SkettiOP"))
{
	print "You must be logged in and a <em>God</em> in order to cast spells. Please <a href=\"sbase.cgi\">leave</a> this holy ground.";
	skettiEndBoard();
}
my $spell = param('spell');
my $doit = param('doit');

if ($spell eq "" || $spell eq " ")
{
print <<END;

<strong><font size=+1>Welcome, <em>God</em>, choose your weapon:</font></strong>

<form method="POST" action="castspell.cgi">
<p><select name="spell">
<option>Enchant</option><option>Arcane Knowledge</option><option>Revive</option><option> </option><option>Amnesia</option><option>Ignorance</option><option>Implosion</option><option>Jester</option><option>Mouthsoap</option></select>
<p>
<input type="submit" value="choose your target" class="submit"/></form>

END
skettiEndBoard();
}
if (($spell eq "Enchant" || $spell eq "Amnesia" || $spell eq "Ignorance" || $spell eq "Jester" || $spell eq "Mouthsoap") && $doit != 1)
{
	print "<strong><font size=+1>Welcome, <em>God</em>, choose your target:</strong></em><br>\n";
	print "<form method=\"POST\" action=\"castspell.cgi\"><input type=\"hidden\" name=\"doit\" value=1>\n";
	print "<select name=\"victim\">";
	$query = $db->prepare_cached("SELECT NICK FROM USERS ORDER BY UID ASC;");
	$query->execute;
	my $vic;
	while ($vic = $query->fetchrow_array) {	print "<option>$vic</option>"; }
	print "</select><p><input type=\"hidden\" name=\"spell\" value=\"$spell\"><input type=\"submit\" value=\"let it be done\" class=\"submit\"/></form>";
	skettiEndBoard();
}
if ($spell eq "Arcane Knowledge" && $doit != 1)
{
	print <<END;
<strong><font size=+1>Welcome, <em>God</em>, please choose your target:</strong><br>
<form method="POST" action="castspell.cgi"><input type="hidden" name="doit" value="1">
<select name="victim">
END
$query = $db->prepare_cached("SELECT NICK FROM USERS ORDER BY UID ASC;");
$query->execute;
my $vic;
while ($vic = $query->fetchrow_array) {	print "<option>$vic</option>"; }
print <<END;
</select><br>
<strong>Please choose the amount of EXP to grant to your target:</strong><br/>
<input type="text" name="exp" value="5" class="text"/>
<input type="hidden" name="spell" value="$spell">
<br>
<input type="submit" value="let it be done" class="submit"/></form>
END
skettiEndBoard();
}
if ($doit == 1 && $spell eq "Arcane Knowledge")
{
	my $target = param('victim');
	my $expi = param('exp');
	$query = $db->prepare_cached("UPDATE USERS SET EXP = EXP + $expi WHERE NICK = '$target';");
	$query->execute;

	$query = $db->prepare_cached("SELECT EXP,LVL,SEX,TITLE FROM USERS WHERE NICK = '$target';");
	$query->execute;
	my ($exp,$lvl,$sex,$title) = $query->fetchrow_array;
	if ($exp >= 50 && $lvl == 1) {
		$lvl++;
		$title = 'Novice';
	}
	if ($exp >= 150 && $lvl == 2) {
		$lvl++;
		$title = 'Apprentice';
	}
	if ($exp >= 300 && $lvl == 3) {
		$lvl++;
		if ($sex eq "Female") { $title = "Queen"; }else{ $title = "King"; }
	}
	if ($exp >= 450 && $lvl == 4) {
		$lvl++;
		if ($sex eq "Female") { $title = "Lady"; }else{ $title = "Lord"; }
	}
	if ($exp >= 550 && $lvl == 5) {
		$lvl++;
		$title = 'Messiah';
	}
	if ($exp >= 750 && $lvl == 6) {
		$lvl++;
		$title = 'Deity';
	}
	if ($exp >= 1000 && $lvl == 7) {
		$lvl++;
		$title = 'God';
	}
	print "It is done.  $target has been schooled in the mysterious <a href=\"sbase.cgi\">arcane arts</a> and has gained $expi EXP.";
	if ($expi > 0) { skettiSendZiggyMsg $target, "$nick has granted you $expi EXP!"; }
	skettiEndBoard();
}
if ($doit == 1 && $spell eq "Amnesia")
{
	my $target = param('victim');
	$query = $db->prepare("UPDATE USERS SET EXP = 0, LVL = 1, TITLE='Peon' WHERE NICK = '$target';");
	$query->execute;
	print "It is done. $target has been struck with amnesia.  Go <a href=\"sbase.cgi\">here</a> to recover.";
	skettiEndBoard();
}
