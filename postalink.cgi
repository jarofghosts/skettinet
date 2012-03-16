#!/usr/bin/perl -w

package SkettiSCRIPT;
use strict;
use sketdb;
use sketact;
use sketboard;
use sketusr;
use CGI qw(param);

skettiStartBoard("Post a Link");

my $db = skettiLoadDb();
my $query;
my $nickn = skettiGrabLogin();
if ($nickn == -1) {
	print "You must be logged in to post a link to the linkbase, sorry.  <a href=\"sbase.cgi\">return</a>";
	skettiEndBoard(); }
$query = $db->prepare("SELECT FONTC FROM USERS WHERE NICK='$nickn';");
$query->execute;
my $bg = $query->fetchrow_array;

skettiUpdateLa($nickn);
my $link = param('link');
my $title = param('title');
if ($link eq "")
{
print <<END;
<form method="POST" action="postalink.cgi">
<table border="0" cellspacing="0" cellpadding="5">
<tr><td bgcolor="$bg"><strong>URL:</strong></td><td><input type="text" name="link" value="http://" class="text"/></td></tr>
<tr><td bgcolor="$bg"><strong>Title:</strong></td><td><input type="text" name="title" class="text"/></td></tr></table>
<center><input type="submit" value="+link" class="submit"/></form>

END

skettiEndBoard(); }
$query = $db->prepare("SELECT NICK,TITLE FROM LINKS WHERE URL = '$link';");
$query->execute;
if ($query->rows != 0)
{
	my ($anick,$atitle) = $query->fetchrow_array;
	print <<END;
I'm sorry, $anick has already linked that under &quot;$atitle&quot;, please <a href="sbase.cgi">return to the forum</a>

END

	skettiEndBoard(); }
$query = $db->prepare("SELECT * FROM LINKS;");
$query->execute;
my $id = $query->rows;
$title =~ s/'/\\'/g;
$query = $db->prepare ("INSERT INTO LINKS (TITLE, URL, NICK, LID, HITS) VALUES ('$title','$link','$nickn',$id,0);");
$query->execute;
print "Thank you, $nickn, your link, &quot;$title&quot, has been added to the <a href=\"sbase.cgi\">forum</a>.";
skettiUpdateLvl ($nickn,1);
skettiEndBoard();
