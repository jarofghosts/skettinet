#!/usr/bin/perl -w

package SkettiSCRIPT;
use strict;
use sketdb;
use sketmsgs;
use sketact;
use sketusr;
use sketboard;
use CGI qw(param);
use sketsauce;

skettiStartBoard("Chat");

my $id = param('id');
my $txt = param('txt');
$txt =~ s/'/\\'/gi;

my ($query,$time,$m,$query3,$mid);
my $db = skettiLoadDb();

my $lonick = skettiGrabLogin();
if ($lonick != -1) { skettiUpdateLa($lonick); }else{
	print "You must be <a href=\"login.cgi\">logged in</a> to join a chat channel.";
	skettiEndBoard();
}
if ($txt ne "") {
	my $nickt;
	my $lonickl = $lonick;
	$lonickl =~ s/ /%20/gi;
	if ($txt =~ /^\/me/)
	{
		$nickt = "";
		$txt =~ s/^\/me/<em>* $lonick/gi;
	}else { $nickt=" \&lt;<a href=\"users.cgi?nick=$lonickl\">$lonick</a>\&gt; "; }
	$time = localtime;
	$time =~ s/  / /gi;
	$query = $db->prepare("SELECT FONTC FROM USERS WHERE NICK = '$lonick';");
	$query->execute;
	my $fontc = $query->fetchrow_array;
	$txt = "<tr><td>\&\#91;$time\&\#93;$nickt <font color=\"$fontc\">$txt</font></em></td></tr>\n";
	$query = $db->prepare("SELECT LOG FROM CHANS WHERE MID = $id;");
	$query->execute;
	my $otxt = $query->fetchrow_array;
	if ($otxt =~ /'/) { $otxt =~ s/'/\\'/gi; }
	my $ntxt = $otxt . $txt;
	$query = $db->prepare("UPDATE CHANS SET LOG = '$ntxt' WHERE MID = $id;");
	$query->execute;
	my ($x,$y,$cda,$ct,$cy) = split(/ /,$time);
	if ($y eq "Jan") { $y = 1; }elsif ($y eq "Feb") { $y = 2; }elsif ($y eq "Mar") { $y = 3; }elsif ($y eq "Apr") { $y = 4; }elsif ($y eq "May"){ $y = 5; }elsif ($y eq "Jun"){ $y = 6; }elsif ($y eq "Jul"){ $y = 7;}elsif ($y eq "Aug") { $y = 8; }elsif ($y eq "Sep"){ $y = 9;}elsif ($y eq "Oct") { $y = 10; }elsif ($y eq "Nov"){ $y = 11;}else{ $y = 12; }
	$ct =~ s/://gi;
	$ct =~ s/^00/24/gi;
	my $dvl = $y . $cda . $ct;
	$query = $db->prepare("UPDATE BASE SET LASTR = $dvl WHERE MID = $id;");
	$query->execute;
}

$query = $db->prepare("SELECT MID FROM CHANS WHERE VISIBLE != 0 AND MID = $id;");
$query->execute;
if ($query->rows == 0)
{
	print "Sorry, that channel does not exist.  Go <a href=\"sbase.cgi\">back</a>.";
	skettiEndBoard();
}
	my $chann = skettiBuildChannel($id,0,999999999999999999999);
print $chann;
print <<END;
<p><hr></p><p>
<form method="POST" action="joinchan.cgi"><input type="hidden" name="id" value="$id"><input type="text" name="txt" width=500> <input type="submit" value="say"></form>
 &nbsp;&nbsp; <form method="POST" action="joinchan.cgi"><input type="hidden" name="id" value="$id"><input type="submit" value="refresh"></form>
 </p>
END
	skettiEndBoard();
