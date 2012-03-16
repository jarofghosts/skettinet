#!/usr/bin/perl -w

package SkettiSCRIPT;
use strict;
use CGI qw(param);
use sketboard;
use sketusr;
use sketdb;

skettiStartBoard("Register User");

my $mode = param('mode');

if ($mode eq "save")
{
our $nick = param('nick');
our $pass = param('pass');
our $pass2 = param('pass2');
our $rname = param('rname');
our $sb = param('sb');
our $sex = param('sex');
our $loc = param('loc');
our $hob = param('hob');
our $email = param('email');
our $url = param('url');
our $ava = param('ava');
our $wow = param('wow');
our $fontc = param('fontc');
our $age = param('age');
our $uin = param('uin');

$uin =~ s/'/\\'/gi;
$nick =~ s/'/\\'/gi;
$nick =~ s/&/&amp;/gi;
$nick =~ s/</&lt;/gi;
$pass =~ s/'/\\'/gi;
$pass2 =~ s/'/\\'/gi;
$rname =~ s/'/\\'/gi;
$sb =~ s/'/\\'/gi;
$loc =~ s/'/\\'/gi;
$hob =~ s/'/\\'/gi;
$email =~ s/'/\\'/gi;
$url =~ s/'/\\'/gi;
$wow =~ s/'/\\'/gi;
$ava =~ s/'/\\'/gi;
$fontc =~ s/'/\\'/gi;
$age =~ s/'/\\'/gi;

my $test = substr($url,0,7);
if ($test ne "http://" && $url ne "") { $url = "http://" . $url; }
$wow =~ s/\r\n/<br>/gi;
$wow =~ s/\r\n\r\n/<p>/gi;

my $db = skettiLoadDb();
my $query = $db->prepare("SELECT UID FROM USERS ORDER BY UID DESC;");
$query->execute;
my $uid;
if ($query->rows == 0) { $uid = 0; } else { $uid = $query->fetchrow_array; $uid++; }
$query = $db->prepare("SELECT * FROM USERS WHERE NICK = '$nick';");
$query->execute;
if ($query->rows == 1)
{
	print <<END;
Sorry, that nickname has been taken, please <a href="register.cgi?mode=get">try a different one</a>

END

skettiEndBoard();
}
if ($pass ne $pass2)
{
	print <<END;
Those to passwords didn't match, try <a href="register.cgi?mode=get">going back</a> and trying a different one.

END

skettiEndBoard();
}
$query = $db->prepare("SELECT * FROM USERS;");
$query->execute;
my $nstat;
if ($query->rows == 0) { $nstat = "SkettiOP"; }else{ $nstat = "SkettiVISITOR"; }

skettiQuery "INSERT INTO USERS (UID,NICK,PASS,STATUS,URL,FONTC,EMAIL,AVATAR,RNAME,UIN,LOCATION,AGE,SOAPBOX,HOBBIES,WORDSOFWIS,SEX,EXP,TITLE,LVL,THEME,BAN,ZIGGY,VIEWR,CLANS,BKMRKS) VALUES ($uid,'$nick','$pass','$nstat','$url','$fontc','$email','$ava','$rname','$uin','$loc','$age','$sb','$hob','$wow','$sex',0,'Peon',1,'default',0,1,1,"","");";

print <<END;

Your profile has been added, click <a href="sbase.cgi">here</a> to begin posting!
<p>An email will be sent soon to $email.

END

open (MAIL, "|/usr/lib/sendmail $email") || print "<br>..On second thought.. maybe that email won't be arriving";
print MAIL "Sender: SkettiSCRIPT\@sketti.net\n";
print MAIL "Subject: You are now a skettivisitor!\n";
print MAIL "\nThis message auto-sent by SkettiSCRIPT v1.04\n\n\nWell, you're officially a poster to the SkettiBASE, $rname.\nYour info is as follows:\nnickname: $nick\npassword: $pass\n\nuse them wisely.\n\n-The SkettiNet team.\n ";
print MAIL " ";
close(MAIL);
skettiEndBoard();
}

if ($mode eq "get" || $mode eq "")
{
	print <<END;

<form method="POST" action="register.cgi">
<input type="hidden" name="mode" value="save">
Fields with a <sup>*</sup> are required.<p>
<table border=0 cellspacing=0 cellpadding=10>
<tr><td><b><sup>*</sup>Nickname:</b></td><td><input type="text" name="nick"><br></td></tr>
<tr><td><b><sup>*</sup>Password:</b> </td><td><input type="password" name="pass"><br></td></tr>
<tr><td><b><sup>*</sup>Re-enter:</b> </td><td><input type="password" name="pass2"><br></td></tr>
<tr><td><b><sup>*</sup>Gender:</b> </td><td><select name="sex"><option>Male</option><option>Female</option></select></td></tr>
<tr><td><b>URL:</b> </td><td><input type="text" name="url"><br></td></tr>
<tr><td><b><sup>*</sup>Email:</b> </td><td><input type="text" name="email">&lt;-- an email will be sent here!<br></td></tr>
<tr><td><b><sup>*</sup>Real name:</b> </td><td><input type="text" name="rname"><br></td></tr>
<tr><td><b>UIN:</b></td><td> <input type="text" name="uin"><br></td></tr>
<tr><td><b>Avatar:</b></td><td> <input type="text" name="ava"><br></td></tr>
<tr><td><b>Location:</b></td><td> <input type="text" name="loc"><br></td></tr>
<tr><td><b>Font color:</b></td><td> <input type="text" name="fontc"><br></td></tr>
<tr><td><b>Hobbies:</b> </td><td><input type="text" name="hob"><br></td></tr>
<tr><td><b>Age:</b> </td><td><input type="text" name="age"><br></td></tr>
<tr><td><b>Soapbox:</b></td><td><input type="text" name="sb"><br></td></tr>
<tr><td><b>Words of wisdom:</b></td><td><textarea name="wow" cols="30" rows="10"></textarea></td></tr></table>
<br><center><input type="submit" value="save profile"></center></form>

END
skettiEndBoard();
}
