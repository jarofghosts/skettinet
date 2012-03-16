#!/usr/bin/perl -w

package SkettiSCRIPT;
use strict;
use sketdb;
use sketusr;
use sketlog;
use sketboard;
use sketsauce;
use CGI qw(param);
use URI::Escape;

skettiStartBoard("User Info");

my $db = skettiLoadDb();
my $lonick = skettiGrabLogin();
if ($lonick != -1) { skettiUpdateLa($lonick); }

my $uid = param('id');
my $unick = param('nick');

my $query;
if ($unick eq "") { $query = $db->prepare("SELECT * FROM USERS WHERE UID = $uid;"); } elsif ($unick ne "") { $query = $db->prepare(qq|SELECT * FROM USERS WHERE NICK = "$unick";|); }
	else{ print "Error."; }
$query->execute;
if ($query->rows == 0)
{
	print <<END;

SORRY! that user doesn\'t seem to exist in THIS database..
<br/>just <a href="userlist.cgi?s=0&e=10">go here</a> and choose one.

END
skettiEndBoard();
}

my ($id,$nick,$pass,$status,$url,$fontc,$email,$rname,$uin,$location,$age,$soapbox,$hobbies,$wow,$r,$t,$y,$v,$b,$exp,$titl,$lvl,$ban,$sex) = $query->fetchrow_array;

my $postn = skettiCount("POSTS",qq|NICK = "$nick"|);

my $bantxt;

$wow = saucify $wow;
$rname = saucify $rname;
$location = saucify $location;
$soapbox = saucify $soapbox;
$hobbies = saucify $hobbies;

if ($ban == 1) { $bantxt = "-- banished!"; } else { $bantxt = ""; }
if ($v eq "") { $v = "ava_ernest.gif"; }

my $lnick = uri_escape($nick);

my $clantxt = "<bl>";

$query = $db->prepare(qq|SELECT CLANS FROM USERS WHERE NICK="$nick"|);
$query->execute;
my @clans = split(/##/,$query->fetchrow_array);
my $clan;
foreach $clan (@clans)
{
	$clan =~ s/#//g;
	if ($clan ne "" ) {
	my $query = $db->prepare("SELECT LEADER,NAME FROM CLANS WHERE CID=$clan;");
	$query->execute;
	my ($leader,$name) = $query->fetchrow_array;
	my $link_name = substr($name,1,length($name));
	if ($leader eq $nick)
	{
		$clantxt .= "<li><strong><a href=\"/clans/$link_name/\" title=\"$nick is Leader of Clan $name\">$name</a></strong><br/>";
	}else{
		$clantxt .= "<li><a href=\"/clans/$link_name\" title=\"Clan $name\">$name</a><br/>";
	}
}
}
$clantxt .= "</bl>";
my ($bmtxt,$bkm,$bkmrks);
$query = $db->prepare(qq|SELECT BKMRKS FROM USERS WHERE NICK="$nick"|);
$query->execute;
$bkmrks = $query->fetchrow_array;
if ($query->rows != 0 && $bkmrks ne "")
{
	my @bkmrk = split(/##/,$bkmrks);
	foreach $bkm(@bkmrk)
	{
		$bkm =~ s/#//g;
		my $type = skettiGrabType($bkm);
		$type =~ tr/[a-z]/[A-Z]/;
		$type .= "S";
		$query = $db->prepare("SELECT TOPIC FROM $type WHERE MID = $bkm;");
		$query->execute;
		my $topic = $query->fetchrow_array;
		$bmtxt .= "<li><a href=\"viewrp.cgi?id=$bkm\" title=\"Message #$bkm\">$topic</a><br>";
	}
}else{ $bmtxt = ""; }

print <<END;

<center><font size=+3><strong>$nick</strong></font>
</center>
<p align="left"><table cellpadding = "5" cellspacing = "0">
<tr><td bgcolor="$fontc"><center><img src="$v" alt="$v" width="120" height="140"/></td></tr>
<tr><td bgcolor="$fontc"><strong><u>PUB</strong></u></td><td><a href="/~$lnick">$nick\'s SkettiSpace</a></td></tr>
<tr><td bgcolor="$fontc"><strong><u>UID</strong></u></td><td>$id</td></tr>
<tr><td bgcolor="$fontc"><strong><u>EXP</strong></u></td><td>$exp</td></tr>
<tr><td bgcolor="$fontc"><strong><u>Title/Level</strong></u></td><td>$titl ($lvl)</td></tr>
<tr><td bgcolor="$fontc"><strong><u>Posts</strong></u></td><td><a href="search.cgi?query=nick:$lnick">$postn</a></td></tr>
<tr><td bgcolor="$fontc"><strong><u>Status</strong></u></td><td>$status$bantxt</td></tr>
<tr><td bgcolor="$fontc"><strong><u>Gender</strong></u></td><td>$sex</td></tr>
<tr><td bgcolor="$fontc"><strong><u>URL</strong></u></td><td><a href="$url" title="$nick's URL">$url</a></td></tr>
<tr><td bgcolor="$fontc"><strong><u>Real Name</strong></u></td><td>$rname</td></tr>
<tr><td bgcolor="$fontc"><strong><u>UIN</strong></u></td><td>$uin</td></tr>
<tr><td bgcolor="$fontc"><strong><u>Location</strong></u></td><td>$location</td></tr>
<tr><td bgcolor="$fontc"><strong><u>Clans</strong></u></td><td>$clantxt</td></tr>
<tr><td bgcolor="$fontc"><strong><u>Bookmarks</strong></u></td><td><bl>$bmtxt</bl></td></tr>
<tr><td bgcolor="$fontc"><strong><u>Age</strong></u></td><td>$age</td></tr>
<tr><td bgcolor="$fontc"><strong><u>Soapbox</strong></u></td><td>$soapbox</td></tr>
<tr><td bgcolor="$fontc"><strong><u>Hobbies</strong></u></td><td>$hobbies</td></tr>
<tr><td bgcolor="$fontc"><strong><u>Send a Message</strong></u></td><td><form method="POST" action="sendmsg.cgi"><input type="hidden" name="to" value="$nick"><input type="text" name="msg" class="text"/> &nbsp; <input type="submit" value="send" class="submit"/></form></td></tr>
</table>
END
$wow =~ s/\r\n/<br\/>/gi;
if (!defined $wow || $wow eq "") { $wow = "<em>N/A</em>"; }
print <<END;
<br/>
<fieldset class="words_of_wisdom"><legend><span class="words_of_wisdom_head">Words of Wisdom:</span></legend>
<span style="color:$fontc"><blockquote>
<p align="center">$wow</p>
</blockquote></span></fieldset><br/><br/><center>
<a href="banuser.cgi?id=$id">ban user</a> + <a href="editp.cgi?id=$id&mode=auth">edit this profile</a> + <a href="sbase.cgi">back to the forum</a> + <a href="userlist.cgi">user listing</a> + <a href="castspell.cgi">cast a spell</a> (<em>God</em>s only)
</p>
END
skettiEndBoard();
