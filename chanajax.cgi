#!/usr/bin/perl -w
use strict;
use sketdb;
use CGI;

my $cgi = new CGI;
my $db = skettiLoadDb();

my $id = $cgi->param('id');
my $text = $cgi->param('text');
my $query;

if (!defined $text) {

	$query = $db->prepare_cached("SELECT LOG FROM CHANS WHERE MID = ?;");
	$query->execute($id);
	print $query->fetchrow_array;
	$db->disconnect;
	exit;
}else{
	my $nick = skettiGrabLogin();
	if ($nick == -1) { print "Must be logged in."; exit; } else {
			my $nickt;
	my $lonickl = $nick;
	$lonickl =~ s/ /%20/gi;
	if ($txt =~ /^\/me/)
	{
		$nickt = "";
		$txt =~ s/^\/me/<em>* $lonick/gi;
	}else { $nickt=" \&lt;<a href=\"users.cgi?nick=$nickl\">$nick</a>\&gt; "; }
	$time = localtime;
	$time =~ s/  / /gi;
	$query = $db->prepare("SELECT FONTC FROM USERS WHERE NICK = '$nick';");
	$query->execute;
	my $fontc = $query->fetchrow_array;
	$txt = "<tr><td>\&\#91;$time\&\#93;$nickt <font color=\"$fontc\">$txt</font></em></td></tr>\n";
	$query = $db->prepare("SELECT LOG FROM CHANS WHERE MID = $id;");
	$query->execute;
	my $otxt = $query->fetchrow_array;
	if ($otxt =~ /'/) { $otxt =~ s/'/\\'/gi; }
	my $ntxt = $otxt . $txt;
	$db->do("UPDATE CHANS SET LOG = '$ntxt' WHERE MID = $id;");
	my $dvl2 = time;
	$db->do("UPDATE BASE SET LASTR = $dvl2 WHERE MID = $id;");
	$query = $db->prepare_cached("SELECT LOG FROM CHANS WHERE MID = ?;");
	$query->execute($id);
	print $query->fetchrow_array;
	$db->disconnect;
	exit;
}