#!/usr/bin/perl -w
use strict;

package SkettiSCRIPT;
use sketdb;
use sketact;
use sketusr;
use sketboard;
use CGI qw(param);

my $nick = skettiGrabLogin();
if ($nick == -1)
{
	skettiStartBoard("Error");
	print "You must be <a href=\"login.cgi\">logged in</a> to delete private messages..";
	skettiEndBoard();
}else{
	skettiUpdateLa($nick);
	my $db = skettiLoadDb();
	my $id = param('id');
	if ($id eq "all")
	{
		my $query=$db->prepare ("DELETE FROM PRIVMSG WHERE NICK = '$nick';");
		$query->execute;
		my $q = new CGI;
		print $q->header(-location=>"sbase.cgi");
		exit;
	}
	my $query = $db->prepare("SELECT NICK FROM PRIVMSG WHERE MID = $id;");
	$query->execute;
	if ($query->fetchrow_array ne $nick)
	{
		skettiStartBoard("Error");
		print "That's not YOUR private message!!  <a href=\"sbase.cgi\">Away with you</a>!";
		skettiEndBoard();
		exit;
	}
	skettiQuery ("DELETE FROM PRIVMSG WHERE MID = $id;");
	my $q = new CGI;
	print $q->header(-location=>"sbase.cgi");
}
