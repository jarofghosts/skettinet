#!/usr/bin/perl -w

package SkettiSCRIPT;
use strict;
use sketdb;
use sketact;
use sketboard;
use sketusr;
use CGI qw(param);

skettiStartBoard("Create a Subject");

my $db = skettiLoadDb();
my $query;
my $nickn = skettiGrabLogin();
$query = $db->prepare("SELECT LVL,STATUS,FONTC FROM USERS WHERE NICK = '$nickn';");
$query->execute;
my ($lvl,$stat,$bg) = $query->fetchrow_array;
if ($nickn == -1 || ($stat ne "SkettiOP" && $lvl < 4)) {
	print "You must be logged in (and a SkettiOP or <em>Lord/Lady</em> to create a subject icon, sorry.  <a href=\"sbase.cgi\">return</a>";
	skettiEndBoard();
	exit;
}
skettiUpdateLa($nickn);
my $subname = param('subname');
my $sublink = param('sublink');

if ($subname eq "" || $sublink eq "")
{
print <<END;
<form method="POST" action="createsub.cgi">
<table border=0 cellspacing=0 cellpadding=5>
<tr><td bgcolor="$bg"><strong>Subject Name:</strong></td><td><input type="text" name="subname" value="$subname" class="text"/></td></tr>
<tr><td bgcolor="$bg"><strong>Image Location:</strong></td><td><input type="text" name="sublink" value="http://" class="text"/></td></tr>
</table>
<center><input type="submit" value="+subject" class="submit"/><br/><br/><font size=-1>If you wish to upload an image, please do so <a href="pub.cgi">here</a>.
</form>

END

skettiEndBoard();
exit;
}
if ($subname =~ m/^\%/) {
	print "Sorry, % is reserved for Clans<br/><a href=\"sbase.cgi\">Back to the BASE!</a>";
	skettiEndBoard();
	exit
}
my $subname2 = $subname;
$subname =~ s/'/\\'/g;
$query = $db->prepare("SELECT NAME FROM SUBJECTS WHERE NAME = '$subname';");
$query->execute;
if ($query->rows != 0)
{
	my ($name) = $query->fetchrow_array;
	print <<END;
I'm sorry, $name is already a subject, <a href="sbase.cgi">BACK TO THE BASE!</a>

END

	skettiEndBoard();
	exit;
}
$sublink =~ s/'/\\'/g;
skettiQuery ("INSERT INTO SUBJECTS (NAME, IMG) VALUES ('$subname','$sublink');");
print "Thank you, $nickn, your subject, &quot;$subname2&quot, has been added to the <a href=\"sbase.cgi\">forum</a>.";
skettiUpdateLvl ($nickn,3);
skettiEndBoard();
