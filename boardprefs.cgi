#!/usr/bin/perl -w

package SkettiSCRIPT;
use strict;
use CGI qw(param);
use DBI;
use sketdb;
use sketusr;
use sketact;
use sketboard;

skettiStartBoard("Board Prefs");

my $theme = skettiGrabTheme();
my $db = skettiLoadDb();

my $act = param('act');
my $ln = param('ln');
my $pmd = param('pmd');
my $zig = param('ziggy');
my $xt = param('xtra');
my $ppp = param('ppp');
my $trunc = param('trunc');
my $sb = param('sort');
my $disptype = param('dtype');
my $themea = param('theme');
my $saucedef = param('sauce');
my @exclusions = param('exclude');
my $chatbox = param('chatbox');
my $nickn;

if ($zig eq "on" || !defined $zig) { $zig = 1; } else { $zig = 0; }
if ($xt eq "yes" || !defined $xt) { $xt = 1; } else { $xt = 0; }
if (!defined $ppp) { $ppp = 10; }
if (!defined $trunc) { $ppp = 400; }
if (!defined $pmd) { $pmd = 10; }
if (!defined $chatbox) { $chatbox = 20; }

sub upPrefs()
{
	my ($ex_e,$excludez);
	foreach $ex_e(@exclusions)
	{
		$excludez .= "#$ex_e#";
	}
	my $query = $db->prepare( qq|UPDATE USERS SET SB="$sb", PMD = $pmd, DT = "$disptype", MPP = "$ppp", TRUNC = $trunc, LN = "$ln",THEME = "$themea",ZIGGY = $zig, VIEWR = $xt, EXCLUDE = "$excludez", SAUCEDEF = "$saucedef", CHATBOX = $chatbox WHERE NICK="$nickn"| );
	$query->execute;
	print "Your prefs have been updated, $nickn.  Please <a href=\"sbase.cgi\">return to the base<\/a>.";
	skettiEndBoard();
}
$nickn = skettiGrabLogin();
if ($nickn == -1)
{
	print "It appears you are not logged in, click <a href=\"login.cgi\">here</a> to login or <a href=\"register.cgi?mode=get\">here</a> to register.";
	skettiEndBoard();
}
skettiUpdateLa($nickn);
if ($act eq "update") { upPrefs(); }
my $query = $db->prepare("SELECT * FROM USERS WHERE NICK = '$nickn';");
$query->execute;
my @pinfo = $query->fetchrow_array;
my ($uid,$nick,$pass,$status,$url,$fontc,$email,$rname,$uin,$loc,$age,$soap,$hobbies,$wow,$sort,$pppg,$dispt,$ava,$trn,$x,$y,$z,$l,$g,$nl,$th,$ziggy,$xtra,$blah,$blahb,$pmd,$lli,$rpp,$exclud,$sauced,$chatter)=@pinfo;
print <<END;

<h2><strong>User preferences for $nickn</h2></strong><br/>

<form method="POST" action="boardprefs.cgi">
<table border=0 cellspacing=0 cellpadding=10>
<tr><td bgcolor="$fontc"><strong><u>Posts to Display:</u></strong></td><td><input type="text" name="ppp" value="$pppg" width="100" class="text"/></td></tr>
<tr><td bgcolor="$fontc"><strong><u>Links to Display:</u></strong></td><td><input type="text" name="ln" value="$nl" width="100" class="text"/></td></tr>
<tr><td bgcolor="$fontc"><strong><u>Private Messages to Display:</u></strong></td><td><input type="text" name="pmd" value="$pmd" width="100" class="text"/></td></tr>
<input type="hidden" name="act" value="update">
<tr><td bgcolor="$fontc"><strong><u>Theme:</u></strong></td><td><select name="theme">
END

$query = $db->prepare("SELECT TITLE,AUTHOR FROM THEMES;");
$query->execute;
my @themea;
while (@themea = $query->fetchrow_array) {
my ($themet,$themen) = @themea;
if ($themet eq $theme) { print "<option  selected value=\"$themet\">$themet ($themen)<\/option>"; }
print "<option value=\"$themet\">$themet ($themen)<\/option>";
}
print <<END;
</select></td></tr>
<tr><td bgcolor="$fontc"><strong><u>Sort Posts By:</u></strong></td><td><select name="sort">
<option selected>last replied</option><option>Post Number Desc</option>
<option>Post Number Asc</option><option>Score Asc</option><option>Score Desc</option></select></td></tr>
<tr><td bgcolor="$fontc"><strong><u>Display Format:</u></strong></td><td><select name="dtype">
<option>classic</option><option>long</option></select></td></tr>
<tr><td bgcolor="$fontc"><strong><u>Truncate Posts \@</u></strong></td><td><input type="text" name="trunc" value="$trn" width="100" class="text"/> <strong><u>Characters</u></strong></td></tr>
<tr><td bgcolor="$fontc"><strong><u>Chatbox Messages:</u></strong></td><td><input type="text" name="chatbox" value="$chatter"></td></tr>
<tr><td bgcolor="$fontc"><strong><u>Ziggy:</u></strong></td><td><select name="ziggy">
END

if ($ziggy == 1)
{
	print "<option selected>on</option><option>off</option>"; }else{
		print "<option>on</option><option selected>off</option>"; }
		print <<END;
</select></td></tr>
<tr><td bgcolor="$fontc"><strong><u>Saucedef Links:</u></strong></td><td><select name="sauce">
END
if ($sauced eq "short")
{
	print qq|<option selected value="short">New Window</option><option value="long">Regular Link</option>|; } else {
	print qq|<option value="short">New Window</option><option selected value="long">Regular Link</option>|; }
	
print <<END;
</select></td></tr>
<tr><td bgcolor="$fontc"><strong><u>View xtras:</u></strong></td><td><select name="xtra">
END

if ($xtra == 1)
{
	print "<option selected>yes</option><option>no</option>"; }else {
		print "<option>yes</option><option selected>no</option>"; }
		print <<END;
</select></td></tr>
<tr><td bgcolor="$fontc"><strong><u>Exclude Subject:</u></strong></td><td>

END
$query = $db->prepare("SELECT NAME FROM SUBJECTS");
$query->execute;
my $subj;
while ($subj = $query->fetchrow_array)
{
	my $query2 = $db->prepare(qq|SELECT UID FROM USERS WHERE NICK = "$nick" AND EXCLUDE REGEXP "#$subj#"|);
	$query2->execute;
	if ($query2->rows == 0) { print "<input type=\"checkbox\" name=\"exclude\" value=\"$subj\"> $subj<br/>"; }else {
	print "<input type=\"checkbox\" checked name=\"exclude\" value=\"$subj\"> $subj<br/>"; }
}
print <<END;
</table>
<br/><center><input type="submit" value="update prefs" class="submit"/></center>
</form>

END

skettiEndBoard();
