#!/usr/bin/perl -w

package SkettiSCRIPT;
use strict;
use sketdb;
use sketusr;
use sketboard;
use CGI qw(param);

my $nick = param('nick');
my $pass = param('pass');
my $db = skettiLoadDb();
my $theme = skettiGrabTheme();

if ($nick eq "" || $pass eq "")
{
	my $nickname = skettiGrabLogin();
	if ($nickname == -1) { $nickname = ""; }
	skettiStartBoard();
	print <<END;
<form method="GET" action="login.cgi">
<strong>Nickname:</strong> <input type="text" name="nick" value="$nickname"><br>
<strong>Password:</strong> <input type="password" name="pass"><br>
<center><input type="submit" value="login"></center>
</form>

END

	skettiEndBoard();
}else{
	my $query = $db->prepare("SELECT PASS FROM USERS WHERE NICK = '$nick';");
	$query->execute;
	if ($query->rows == 0)
	{
		skettiStartBoard();
		print "That user does not seem to exist.. why dont you <a href=\"register.cgi?mode=get\">register</a>?";
		skettiEndBoard();
	}
	if ($query->fetchrow_array ne $pass)
	{
		skettiStartBoard();
		print "That is the incorrect password for that account, why don't you <a href=\"register.cgi\">register</a> yourself..?";
		skettiEndBoard();
	}
	my $q = new CGI;
	my $co = $q->cookie(-name=>'nick',
	-value=>"$nick");
	my $lt = localtime;
	$lt =~ s/  / /gi;
	my $ses = $ENV{REMOTE_ADDR} . "=" . $lt;
	my $cses = $q->cookie(-name=>'session',
	-value=>"$ses");
	my $la = skettiGetTA();
	print $q->header(-cookie=>$co,-cookie=>$cses,-location=>"sbase.cgi");
	$query=$db->prepare ("DELETE FROM LOGGEDIN WHERE NICK = '$nick';");
	$query->execute;
	$query=$db->prepare ("INSERT INTO LOGGEDIN (NICK,SID,LA) VALUES ('$nick','$ses','$la');");
	$query->execute;
	skettiUpdateLITable();
	exit;
}
