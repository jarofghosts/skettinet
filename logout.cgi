#!/usr/bin/perl -w
use strict;

package SkettiSCRIPT;
use sketdb;
use sketusr;
use sketboard;
use CGI;

my $nick = skettiGrabLogin();

if ($nick == -1) {
	skettiStartBoard();
	print "You are already logged out, genius.  <a href=\"sbase.cgi\">Flee this place</a>";
	skettiEndBoard();
}
my $db = skettiLoadDb();
my $query = $db->prepare ("DELETE FROM LOGGEDIN WHERE NICK = \"$nick\";");
$query->execute;
skettiUpdateLITable(skettiGetTA());

my $q = new CGI;
print $q->header(-location=>"sbase.cgi");
skettiEndBoard();
exit;
