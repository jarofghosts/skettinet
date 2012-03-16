#!/usr/bin/perl -w

package SkettiSCRIPT;
use strict;
use sketdb;
use CGI qw(param);
use sketact;
use sketusr;
use sketboard;

skettiStartBoard("Edit Theme");

my $mode = param('mode');
my $id = param('id');

my $db = skettiLoadDb;

if ($id eq "" || $mode eq "")
{
	print "	<form method=\"POST\" action=\"edittheme.cgi\">\n<p align=\"center\"><select name=\"id\">";
	my $query = $db->prepare("SELECT TID, TITLE, AUTHOR FROM THEMES WHERE LUP != 1;");
	$query->execute;
	my @themeinfo;
	while (@themeinfo = $query->fetchrow_array)
	{
		my ($tid,$title,$author) = @themeinfo;
		print "<option value=$tid>$title ($author)</option>";
	}
	print "</select><br/><br/><input type=\"hidden\" name=\"mode\" value=\"auth\">\n<input type=\"submit\" value=\"edit\" class=\"submit\"/></form>";
	skettiEndBoard(); }

my $query = $db->prepare("SELECT TITLE,AUTHOR,MAIN,TOP,BOTTOM,POST,REPLY,POLL,CHANNEL,POLLIMAGE FROM THEMES WHERE TID = $id;");
$query->execute;

if ($query->rows == 0)
{
	print <<END;

Well, that theme doesn't exist, sorry.. you should probably just try to follow links instead of putting in your own values unless you know what you're doing.. you should also <a href="sbase.cgi">leave</a>.

END
	skettiEndBoard(); }

my ($nickn,$pass,$nick);
$nickn = skettiGrabLogin();
if ($nickn != -1) { 
	$pass = skettiGrabPass($nickn);
	skettiUpdateLa($nickn);
	if ($mode ne "save") { $mode = "edit"; }
}
if (($mode eq "auth") && $nickn == -1 )
{
	print <<END;

<form method="POST" action="edittheme.cgi">
<input type="hidden" name="mode" value="edit">
<input type="hidden" name="id" value="$id">
<strong>Nickname:</strong> <input type="text" name="nick" class="text"/><br/>
<strong>Password:</strong> <input type="password" name="pass" class="text"/><br/>
<br/><center><input type="submit" value="edit $id" class="submit"/></form>

END
	skettiEndBoard();
}
if ($nickn == -1)
{
	$nick = param('nick');
	$pass = param('pass');
}else{ $nick = $nickn; }
	my ($title,$author,$main,$top,$bottom,$post,$reply,$poll,$channel,$pollimage) = $query->fetchrow_array;
	my $query = $db->prepare("SELECT PASS,STATUS,LVL FROM USERS WHERE NICK = '$nick';");
	$query->execute;
	my ($upass,$stat,$ulvl) = $query->fetchrow_array;
	if ($upass ne $pass && $nickn == -1) { print "Umm.. shouldn't you know your password?? <a href=\"sbase.cgi\">get out of my sight!</a>";
	skettiEndBoard(); }
		if ($nick ne $author && $stat ne "SkettiOP" && $ulvl < 7)
	{
		print "Ummm.. what are you trying to do?  Either you edit your OWN theme or become a SkettiOP or <em>Deity</em>, otherwise, <a href=\"sbase.cgi\">leave me alone</a>.";
		skettiEndBoard(); }
if ($mode eq "edit")
{
	my $query = $db->prepare("SELECT LUP FROM THEMES WHERE TID=$id;");
	$query->execute;
	if ($query->fetchrow_array == 1)
	{
		print "That theme is currently being edited by another user.<br/><a href=\"sbase.cgi\">Back to the forum</a>";
		skettiEndBoard(); }
	my $bg = "";
	if ($nickn != -1) {
		$query = $db->prepare("SELECT FONTC FROM USERS WHERE NICK = '$nickn';");
		$query->execute;
		$bg = $query->fetchrow_array;
	}
	skettiQuery ("UPDATE THEMES SET LUP = 1 WHERE TID=$id;");
	print <<END;

<form method="POST" action="edittheme.cgi">
<input type="hidden" name="nick" value="$nick">
<input type="hidden" name="pass" value="$pass">
<input type="hidden" name="id" value="$id">
<input type="hidden" name="mode" value="save">
<table border="0" cellspacing="0" cellpadding="10">
<tr><td bgcolor="$bg"><strong><u>Main:</u></strong></td><td><textarea name="main" rows="25" cols="80" class="textarea">$main</textarea></td></tr>
<tr><td bgcolor="$bg"><strong><u>Top:</u></strong></td><td><textarea name="top" rows="25" cols="80" class="textarea">$top</textarea></td></tr>
<tr><td bgcolor="$bg"><strong><u>Bottom:</u></strong></td><td><textarea rows="25" cols="80" class="textarea"  name="bottom">$bottom</textarea></td></tr>
<tr><td bgcolor="$bg"><strong><u>Post:</strong></u></td><td><textarea rows="25" cols="80" class="textarea" name="post">$post</textarea></td></tr>
<tr><td bgcolor="$bg"><strong><u>Reply:</strong></u></td><td><textarea rows="25" cols="80" class="textarea" name="reply">$reply</textarea></td></tr>
<tr><td bgcolor="$bg"><strong><u>Poll:</strong></u></td><td><textarea rows="25" cols="80" class="textarea" name="poll">$poll</textarea></td></tr>
<tr><td bgcolor="$bg"><strong><u>Poll Image:</strong></u></td><td><input type="text" name="pollimage" value="$pollimage" class="text"/></td></tr>
</table><br>
<center><input type="submit" value="save theme $id" class="submit"/></center>
</form>

END

skettiEndBoard();
}
if ($mode eq "save")
{
	my $main = param('main');
	my $top = param('top');
	my $bottom = param('bottom');
	my $post = param('post');
	my $reply = param('reply');
	my $poll = param("poll");
	my $channel = param("channel");
	my $pollimg = param("pollimage");

$main =~ s/'/\\'/g;
$top =~ s/'/\\'/g;
$bottom =~ s/'/\\'/g;
$post =~ s/'/\\'/g;
$reply =~ s/'/\\'/g;
$poll =~ s/'/\\'/g;
$channel =~ s/'/\\'/g;
$pollimg =~ s/'/\\'/g;

	$query = $db->prepare ("UPDATE THEMES SET MAIN = '$main', TOP = '$top', BOTTOM = '$bottom', POST = '$post', REPLY = '$reply', POLL = '$poll', POLLIMAGE='$pollimg',LUP=0 WHERE TID = $id;");
	$query->execute;
	print <<END;

Thank you, $nick, the theme (tid $id) has been updated.
<br/>go <a href="sbase.cgi">back to the base</a>.

END
	skettiEndBoard(); }
