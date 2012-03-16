#!/usr/bin/perl -w

package SkettiSCRIPT;
use strict;
use sketdb;
use sketact;
use sketusr;
use sketboard;
use CGI qw(param);

skettiStartBoard("Edit Profile");

my ($query,$nick,$pass,$bg);
my $db = skettiLoadDb();
my $id = param('id');
my $mode = param('mode');

my $nick = skettiGrabLogin();
if ($nick != -1)
	{
		skettiUpdateLa($nick);
		$query = $db->prepare("SELECT PASS,FONTC FROM USERS WHERE NICK = '$nick';");
		$query->execute;
		($pass,$bg) = $query->fetchrow_array;
	if ($mode eq "" || $mode eq "auth")
	{
		$mode = "disp";
	}
}

if ($mode eq "" || $mode eq "auth")
{
$query = $db->prepare("SELECT * FROM USERS WHERE UID = $id;");
$query->execute;
if ($query->rows == 0)
{
print <<END;

That user (uid $id) has stepped into the quantum leap accelerator and vanished!
<br/>click <a href="/">here</a> to awake to find yourself trapped in the past.

END
	skettiEndBoard();
}

print <<END;

<form method="POST" action="editp.cgi">
<input type="hidden" name="id" value="$id">
<input type="hidden" name="mode" value="disp">
<table border="0">
<tr><td><strong>Nickname:</strong></td><td><input type="text" name="nick" class="text"/></td></tr>
<tr><td><strong>Password:</strong></td><td><input type="password" name="pass" class="text"/></td></tr>
<tr><td colspan="2"><center><input type="submit" value="edit $id" class="submit"/></center></td></tr>
</table>
</form>

END
	skettiEndBoard();
}
if ($mode eq "disp")
{
if ($nick == -1)
{
	$nick = param('nick');
	$pass = param('pass');
}
$query = $db->prepare(qq|SELECT STATUS,PASS FROM USERS WHERE NICK = "$nick"|);
$query->execute;
if ($query->rows == 0)
{
	print <<END;

Umm.. you should <a href="register.cgi?mode=get">register</a> first, then become a SkettiOP.

END
	skettiEndBoard();
}
my @uinfo = $query->fetchrow_array;
my ($s,$p) = @uinfo;
if ($p ne $pass)
{
print <<END;
I don't think it's very nice to pretend to be someone else, why don't you <a href="sbase.cgi">leave</a>?

END
	skettiEndBoard();
}
$query = $db->prepare("SELECT NICK FROM USERS WHERE UID = $id;");
$query->execute;
my $rn = $query->fetchrow_array;
if ($rn ne $nick && $s ne "SkettiOP")
{
print <<END;
You either need to become a SkettiOP, or edit your own profile, jackass.<br/>
Click <a href="sbase.cgi">here</a> and get out of my sight.

END
skettiEndBoard();
}
$query = $db->prepare("SELECT * FROM USERS WHERE UID = $id;");
$query->execute;
my @info = $query->fetchrow_array;
my ($uid,$unick,$upass,$ustat,$uurl,$ufontc,$uemail,$urname,$uuin,$uloc,$uage,$usb,$uhob,$uwow,$x,$y,$z,$ava,$l,$t,$ex,$bb,$r,$sex,$ln,$theme,$ziggy,$viewr,$clans,$bkmrks) = @info;

print <<END;

<form method="POST" action="editp.cgi">
<input type="hidden" name="id" value="$id">
<input type="hidden" name="s" value="$s">
<input type="hidden" name="n" value="$unick">
<input type="hidden" name="mode" value="save">
<p align="left">
<table cellspacing="0" cellpadding="5">
<tr><td bgcolor="$bg"><strong>Nickname:</strong></td><td>$unick</td></tr>
<tr><td bgcolor="$bg"><strong>Password:</strong></td><td><input type="password" name="pass1" value="$upass" class="text"/></td></tr>
<tr><td bgcolor="$bg"><strong>Re-enter:</strong></td><td><input type="password" name="pass2" value="$upass" class="text"/></td></tr>
<tr><td bgcolor="$bg"><strong>Status:</strong></td><td>

END

if ($s eq "SkettiOP")
{
print "<select name=\"status\"><option";
if ($ustat eq "SkettiOP") { print " selected>"; }else{ print ">"; }
print "SkettiOP</option><option ";
if ($ustat eq "SkettiMEMBER") { print "selected>"; }else{ print ">"; }
print "SkettiMEMBER</option><option ";
if ($ustat eq "SkettiPHILE") { print "selected>"; }else{ print ">"; }
print "SkettiPHILE</option><option ";
if ($ustat eq "Ubergahnite") { print "selected>"; }else{ print ">"; }
print "Ubergahnite</option><option ";
if ($ustat eq "SkettiVISITOR") { print "selected>"; }else{ print ">"; }
print "SkettiVISITOR</option></select></td></tr>";
}else
{
print "<input type=\"hidden\" name=\"status\" value=\"$ustat\">";
print "$ustat</td></tr>\n";
}

print <<END;
<tr><td bgcolor="$bg"><strong>Real Name:</strong></td><td><input type="text" name="rname" value="$urname" class="text"/></td></tr>
<tr><td bgcolor="$bg"><strong>Avatar:</strong></td><td><input type="text" name="ava" value="$ava" class="text"/></td></tr>
<tr><td bgcolor="$bg"><strong>Font color:</strong></td><td><input type="text" name="fontc" value="$ufontc" class="text"/></td></tr>
<tr><td bgcolor="$bg"><strong>Gender:</strong></td><td><select name="sex">
END
if ($sex eq "Male") { print "<option selected>Male</option><option>Female</option>"; }
else {
	print "<option selected>Female</option><option>Male</option>"; }
print <<END;
	
</select></td></tr>
<tr><td bgcolor="$bg"><strong>URL:</strong></td><td><input type="text" name="url" value="$uurl" class="text"/></td></tr>
<tr><td bgcolor="$bg"><strong>Email:</strong></td><td><input type="text" name="email" value="$uemail" class="text"/></td></tr>
<tr><td bgcolor="$bg"><strong>Hobbies:</strong></td><td><input type="text" name="hobbies" value="$uhob" class="text"/></td></tr>
<tr><td bgcolor="$bg"><strong>Soapbox:</strong></td><td><input type="text" name="soapbox" value="$usb" class="text"/></td></tr>
<tr><td bgcolor="$bg"><strong>Location:</strong></td><td><input type="text" name="location" value="$uloc" class="text"/></td></tr>
<tr><td bgcolor="$bg"><strong>Clans:</strong></td><td><em>Delete:</em><br/>

END
my @clanz = split(/##/,$clans);
my $cln;
foreach $cln(@clanz)
{
	$cln =~ s/#//g;
	$query = $db->prepare("SELECT NAME FROM CLANS WHERE CID=$cln;");
	$query->execute;
	my $clan2 = $query->fetchrow_array;
	print "<input type=\"checkbox\" name=\"clans\" value=\"$cln\"> $clan2<br/>";
}
print "</td></tr>\n<tr><td bgcolor=\"$bg\"><strong>Bookmarks:</strong></td><td><em>Delete:</em><br/>\n";
my @bkms = split(/##/,$bkmrks);
my $bkm;
foreach $bkm(@bkms)
{
	$bkm =~ s/#//g;
	my $type = skettiGrabType($bkm);
	$type =~ tr/[a-z]/[A-Z]/;
	$type .= "S";
	$query = $db->prepare("SELECT TOPIC FROM $type WHERE MID = $bkm;");
	$query->execute;
	my $bkm2 = $query->fetchrow_array;
	print "<input type=\"checkbox\" name=\"bookmarks\" value=\"$bkm\"> $bkm2<br/>";
}

print <<END;
<tr><td bgcolor="$bg"><strong>Age:</strong></td><td><input type="text" name="age" value="$uage" class="text"/></td></tr>
<tr><td bgcolor="$bg"><strong>UIN:</strong></td><td><input type="text" name="uin" value="$uuin" class="text"/></td></tr>
<tr><td bgcolor="$bg"><strong>Words of Wisdom:</strong></td><td>
<textarea name="wow" rows="25" cols="70" class="textarea">$uwow</textarea></td></tr></table><br/>
<center><input type="submit" value="update profile $uid" class="submit"/></center>

END
skettiEndBoard();
}
if ($mode eq "save")
{
	my $nick = param('n');
	my $status = param('s');
	my $upass1 = param('pass1');
	my $upass2 = param('pass2');
	my $nstatus = param('status');
	my $rname = param('rname');
	my $fontc = param('fontc');
	my $url = param('url');
	my $email = param('email');
	my $hob = param('hobbies');
	my $loc = param('location');
	my $ava = param('ava');
	my $sex = param('sex');
	my $sb = param('soapbox');
	my $age = param('age');
	my $uin = param('uin');
	my $wow = param('wow');
if ($upass1 ne $upass2)
{
	print "Those passwords don't match, <a href=\"editp.cgi?id=$id&mode=auth\">go back</a> and try again.";
	skettiEndBoard();
}

$upass1 =~ s/'/\\'/gi;
$upass2 =~ s/'/\\'/gi;
$rname =~ s/'/\\'/gi;
$fontc =~ s/'/\\'/gi;
$url =~ s/'/\\'/gi;
$email =~ s/'/\\'/gi;
$hob =~ s/'/\\'/gi;
$loc =~ s/'/\\'/gi;
$ava =~ s/'/\\'/gi;
$sb =~ s/'/\\'/gi;
$age =~ s/'/\\'/gi;
$uin =~ s/'/\\'/gi;
$wow =~ s/'/\\'/gi;

my @bkmarks = param('bookmarks');
my @clan2 = param('clans');
my ($cl,$bm);
foreach $bm(@bkmarks)
{
	skettiDeleteBMarks("$bm","$nick");
}
$query = $db->prepare("SELECT CLANS FROM USERS WHERE NICK=\"$nick\";");
$query->execute;
my $clnz = $query->fetchrow_array;

if ($clnz ne "")
{
	foreach $cl(@clan2)
	{
		$clnz =~ s/#$cl#//g;
	}
}

$query = $db->prepare ("UPDATE USERS SET PASS='$upass1',WORDSOFWIS='$wow',AVATAR='$ava',STATUS='$nstatus',RNAME='$rname',FONTC='$fontc',URL='$url' WHERE UID=$id;");
$query->execute;
$query=$db->prepare ("UPDATE USERS SET EMAIL='$email',HOBBIES='$hob',LOCATION='$loc',SOAPBOX='$sb',SEX='$sex' WHERE UID=$id;");
$query->execute;
$query = $db->prepare ("UPDATE USERS SET AGE=$age,UIN=$uin,CLANS='$clnz' WHERE UID=$id;");
$query->execute;

print <<END;

The profile (uid $id) has been updated!<br/>
Click <a href="sbase.cgi">here</a> to return to the base or <a href="users.cgi?id=$id">here</a> to see the newly updated profile!

END
	skettiEndBoard();
}
