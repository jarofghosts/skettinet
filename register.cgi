#!/usr/bin/perl -w

package SkettiSCRIPT;
use strict;
use CGI qw(param);
use sketboard;
use sketusr;
use sketdb;

skettiStartBoard("Register User");

my $ip = $ENV{'REMOTE_ADDR'};

my $mode = param('mode');

if ($mode eq "save")
{
my $nick = param('nick');
my $pass = param('pass');
my $pass2 = param('pass2');
my $rname = param('rname');
my $sb = param('sb');
my $sex = param('sex');
my $loc = param('loc');
my $hob = param('hob');
my $email = param('email');
my $url = param('url');
my $ava = param('ava');
my $wow = param('wow');
my $fontc = param('fontc');
my $age = param('age');
my $uin = param('uin');

$uin =~ s/'/\\'/g;
$nick =~ s/'/\\'/g;
$nick =~ s/&/&amp;/g;
$nick =~ s/</&lt;/g;
$pass =~ s/'/\\'/g;
$pass2 =~ s/'/\\'/g;
$rname =~ s/'/\\'/g;
$sb =~ s/'/\\'/g;
$loc =~ s/'/\\'/g;
$hob =~ s/'/\\'/g;
$email =~ s/'/\\'/g;
$url =~ s/'/\\'/g;
$wow =~ s/'/\\'/g;
$ava =~ s/'/\\'/g;
$fontc =~ s/'/\\'/g;
$age =~ s/'/\\'/g;

$wow =~ s/\r\n/<br\/>/gi;

my $db = skettiLoadDb();
my $query = $db->prepare("SELECT UID FROM USERS ORDER BY UID DESC;");
$query->execute;
my $uid;
if ($query->rows == 0) { $uid = 0; } else { $uid = $query->fetchrow_array; $uid++; }
$query = $db->prepare("SELECT UID FROM USERS WHERE NICK = '$nick';");
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
Those two passwords didn't match, try <a href="register.cgi?mode=get">going back</a> and trying a different one.

END

skettiEndBoard();
}

if ($nick =~ m/^\%/) {

	print <<END;
Your username cannot begin with a '%' as it is reserved for clans. <a href="register.cgi?mode=get">Go back</a> and take that thing out of there

END

skettiEndBoard();
}

if ($nick =~ m/http:\/\//) {
	
	print "Fuck you..";

skettiEndBoard();
}
my $nstat;
if (skettiCount("USERS",undef) == 0) { $nstat = "SkettiOP"; }else{ $nstat = "SkettiVISITOR"; }

$nick =~ s/"/&quot;/g;

if (skettiCount("REGISTER",qq|SESSION = "| . $ip . $0 . qq|"|) == 0) {
	print "Fuck you.";
	skettiEndBoard();
}
$query = $db->prepare ("INSERT INTO USERS (UID,NICK,PASS,STATUS,URL,FONTC,EMAIL,AVATAR,RNAME,UIN,LOCATION,AGE,SOAPBOX,HOBBIES,WORDSOFWIS,SEX,EXP,TITLE,LVL,THEME,BAN,ZIGGY,VIEWR,CLANS,BKMRKS,PMD,LN,MPP,TRUNC,CHATBOX,IP) VALUES ($uid,'$nick','$pass','$nstat','$url','$fontc','$email','$ava','$rname','$uin','$loc','$age','$sb','$hob','$wow','$sex',0,'Peon',1,'moderno',0,1,1,\"\",\"\",10,5,10,500,20,'$ip');");
$query->execute;
skettiQuery("DELETE FROM REGISTER WHERE SESSION = '" . $ip . $0 . "'");
print <<END;

Your profile has been added, click <a href="sbase.cgi">here</a> to begin posting!

END

open (MAIL, "|/usr/lib/sendmail $email") || print "<br/>..On second thought.. maybe that email won't be arriving";
print MAIL "Sender: SkettiSCRIPT\@sketti.net\n";
print MAIL "Subject: You are now a skettivisitor!\n";
print MAIL "\nThis message auto-sent by SkettiSCRIPT v1.5\n\n\nWell, you're officially a poster to the SkettiBASE, $rname.\nYour info is as follows:\nnickname: $nick\npassword: $pass\n\nuse them wisely.\n\n-The SkettiNet team.\n ";
print MAIL ".";
close(MAIL);
skettiEndBoard();
}

if ($mode eq "get" || $mode eq "")
{
	skettiQuery("INSERT INTO REGISTER (SESSION) VALUES ('" . $ip . $0 . "')");
	print <<END;

<form method="POST" action="register.cgi">
<input type="hidden" name="mode" value="save">
Fields with a <sup>*</sup> are required.<p>
<table border="0" cellspacing="0" cellpadding="10">
<tr><td><strong><sup>*</sup>Nickname:</strong></td><td><input type="text" name="nick" class="text" maxlength="30"/></td></tr>
<tr><td><strong><sup>*</sup>Password:</strong> </td><td><input type="password" name="pass" class="text"/></td></tr>
<tr><td><strong><sup>*</sup>Re-enter:</strong> </td><td><input type="password" name="pass2" class="text"/></td></tr>
<tr><td><strong><sup>*</sup>Gender:</strong> </td><td><select name="sex"><option value="Male">Male</option><option selected value="Female">Female</option></select></td></tr>
<tr><td><strong>URL:</strong> </td><td><input type="text" name="url" class="text"/></td></tr>
<tr><td><strong><sup>*</sup>Email:</strong> </td><td><input type="text" name="email" class="text"/></td></tr>
<tr><td><strong><sup>*</sup>Real name:</strong> </td><td><input type="text" name="rname" class="text"/></td></tr>
<tr><td><strong>UIN:</strong></td><td> <input type="text" name="uin" class="text"/></td></tr>
<tr><td><strong>Avatar:</strong></td><td> <input type="text" name="ava" class="text"/></td></tr>
<tr><td><strong>Location:</strong></td><td> <input type="text" name="loc" class="text"/></td></tr>
<tr><td><strong>Font color:</strong></td><td> <input type="text" name="fontc" class="text"/></td></tr>
<tr><td><strong>Hobbies:</strong> </td><td><input type="text" name="hob" class="text"/></td></tr>
<tr><td><strong>Age:</strong> </td><td><input type="text" name="age" class="text"/></td></tr>
<tr><td><strong>Soapbox:</strong></td><td><input type="text" name="sb" class="text"/></td></tr>
<tr><td><strong>Words of wisdom:</strong></td><td><textarea name="wow" cols="30" rows="10" class="textarea"></textarea></td></tr></table>
<br/><center><input type="submit" value="save profile" class="submit"/></center></form>

END
skettiEndBoard();
}
