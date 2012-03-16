#!/usr/bin/perl -w
use strict;

package SkettiSCRIPT;
use sketboard;
use sketdb;
use sketusr;
use DBI;
use CGI qw(param);

my $theme = skettiGrabTheme();
my $query;

my $nick = skettiGrabLogin();
if ($nick == -1 || $nick == -2)
{
	print "Content-type: text/html\n\n";
	skettiStartBoard("Delete Private Messages");
	print "You must be <a href=\"login.cgi\">logged in</a> to delete private messages..";
	skettiEndBoard();
}else{
	skettiUpdateLa($nick);
	my $db = skettiLoadDb();
	my $nick = param('nick');
	$query = $db->prepare("DELETE FROM PRIVMSG WHERE NICK = '$nick';");
	$query->execute;
	my $q = new CGI;
	print $q->header(-location=>"sbase.cgi");
	$db->disconnect;
}
