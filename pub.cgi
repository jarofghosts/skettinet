#!/usr/bin/perl -w

package SkettiSCRIPT;
use strict;
use CGI qw(param);
use CGI;
use sketdb;
use sketact;
use sketusr;
use sketboard;
use sketziggy;
use sketlog;
use URI::Escape;

my $cgi = new CGI;
print $cgi->header();
skettiStartBoardNoHead("Pub");

my $db = skettiLoadDb();

my $mode = $cgi->param('mode');
my ($nick,$pass,$f6,$f5,$f4,$f3,$f2,$f1,$upload_dir,$file1,$file2,$file3,$file4,$file5,$file6);

if ($mode eq "upload") {
	$nick = $cgi->param('nick');
	$pass = $cgi->param('pass');
	$f6 = $cgi->param('f6');
	$f5 = $cgi->param('f5');
	$f4 = $cgi->param('f4');
	$f3 = $cgi->param('f3');
	$f2 = $cgi->param('f2');
	$f1 = $cgi->param('f1');

	$upload_dir = "/sketti/pub/$nick";
	$f1 =~ s/.*[\/\\](.*)/$1/gi;
	$f2 =~ s/.*[\/\\](.*)/$1/gi;
	$f3 =~ s/.*[\/\\](.*)/$1/gi;
	$f4 =~ s/.*[\/\\](.*)/$1/gi;
	$f5 =~ s/.*[\/\\](.*)/$1/gi;
	$f6 =~ s/.*[\/\\](.*)/$1/gi;

	$file1 = $cgi->upload("f1");
	$file2 = $cgi->upload("f2");
	$file3 = $cgi->upload("f3");
	$file4 = $cgi->upload("f4");
	$file5 = $cgi->upload("f5");
	$file6 = $cgi->upload("f6");
}
my $bg = "";
my ($query,$nickn);

my $session = defined $cgi->cookie('session') ? $cgi->cookie('session') : "POOP";
skettiUpdateLITable(skettiGetTA());
$query = $db->prepare(qq|SELECT NICK FROM LOGGEDIN WHERE SID = "$session";|);
$query->execute;
if ($query->rows == 0) { $nickn = -1; }else{
$nickn = $query->fetchrow_array; }

if ($nickn != -1) { 
	skettiUpdateLa($nickn);
	$query = $db->prepare(qq|SELECT FONTC FROM USERS WHERE NICK = '$nickn'|);
	$query->execute;
	$bg = $query->fetchrow_array;
}
if (!defined $mode || $mode eq "get" || $mode eq "")
{
print qq|<form method="POST" action="pub.cgi" enctype="multipart/form-data">\n<table border="0" cellpadding="5" cellspacing="0">|;
if ($nickn == -1)
{
	print <<END;
	<tr><td><strong><u>Nickname:</u></strong></td><td><input type="text" name="nick" class="text"/></td></tr>
	<tr><td><strong><u>Password:</u></strong></td><td><input type="password" name="pass" class="text"/></td></tr>
END
}else{
	my $npass = skettiGrabPass($nickn);
	print <<END;
	<tr><td bgcolor="$bg"><strong><u>Nickname:</u></strong></td><td>$nickn</td></tr>
	<input type="hidden" name="nick" value="$nickn">
	<input type="hidden" name="pass" value="$npass">
END
}

print <<END;
<input type="hidden" name="mode" value="upload">
<tr><td bgcolor="$bg"><strong><u>File #1:</u></strong></td><td><input type="file" name="f1"/></td></tr>
<tr><td bgcolor="$bg"><strong><u>File #2:</u></strong></td><td><input type="file" name="f2"/></td></tr>
<tr><td bgcolor="$bg"><strong><u>File #3:</u></strong></td><td><input type="file" name="f3"/></td></tr>
<tr><td bgcolor="$bg"><strong><u>File #4:</u></strong></td><td><input type="file" name="f4"/></td></tr>
<tr><td bgcolor="$bg"><strong><u>File #5:</u></strong></td><td><input type="file" name="f5"/></td></tr>
<tr><td bgcolor="$bg"><strong><u>File #6:</u></strong></td><td><input type="file" name="f6"/></td></tr>
<tr><td colspan="2"><input type="submit" value="upload" class="submit"/></td></tr></table></form>
END

	skettiEndBoard();
}else
{
	if ($nick eq "" || $pass eq "")
	{
		print <<END;

Umm.. you are missing some stuff for your stuff there.. you should probably <a href="pub.cgi?mode=get">go back</a> and fill it in.

END
	skettiEndBoard();
}
	$query = $db->prepare("SELECT PASS,BAN FROM USERS WHERE NICK = '$nick';");
	$query->execute;
	my $test = $query->rows;
	if ($test == 0)
	{
		print <<END;

SRRY!<br/><br/>You must <a href="join.cgi?mode=get">register</a> first.

END
	skettiEndBoard(); }
	my ($upass,$ban) = $query->fetchrow_array;
	if ($ban == 1) {
		print "You have been BANISHED!  Do not attempt to return here.\n";
		skettiEndBoard(); }
	if ($upass ne $pass)
	{
		print <<END;
All right, dude, don't pretend to be something you are not, why don't you find out the RIGHT password and <a href="pub.cgi?mode=get">try again</a>

END
	skettiEndBoard();
}
umask(000);
mkdir("$upload_dir", 0777) unless (-d "$upload_dir");
if (defined $f1 && $f1 ne "")
{
	open (FILE, ">$upload_dir/$f1");
	
	binmode FILE;
	
	while ( <$file1> )
	{
		print FILE;
		
	}
	close (FILE);
}
if (defined $f2 && $f2 ne "")
{
	open (F2, ">$upload_dir/$f2");
	
	binmode F2;
	
	while ( <$file2> )
	{
		print F2 $_;
	}
	close (F2);
}
if (defined $f3 && $f3 ne "")
{
	open (F3, ">$upload_dir/$f3");

	binmode F3;
	
	while ( <$file3> )
	{
		print F3 $_;
	}
	close (F3);
}
if (defined $f4 && $f4 ne "")
{
	open (F4, ">$upload_dir/$f4");

	binmode F4;
	
	while ( <$file4> )
	{
		print F4 $_;
	}
	close (F4);
}
if (defined $f5 && $f5 ne "")
{
	open (F5, ">$upload_dir/$f5");

	binmode F5;
	
	while ( <$file5> )
	{
		print F5 $_;
	}
	close (F5);
}
if ( defined $f6 && $f6 ne "")
{
	open (F6, ">$upload_dir/$f6");

	binmode F6;
	
	while ( <$file6> )
	{
		print F6 $_;
	}
	close (F6);
}
	my $ip = $ENV{'REMOTE_ADDR'};
	my $nick_link = uri_escape($nick);
	print "Thank you, $nick.  Click <a href=\"/\">here</a> to return to the forum. Or <a href=\"/~$nick_link\">here</a> to goto your pub.";
	skettiLog ("$nick ($ip) uploads files: $f1 $f2 $f3 $f4 $f5 $f6");

skettiEndBoard(); }
