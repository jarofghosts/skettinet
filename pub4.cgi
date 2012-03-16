#!/usr/bin/perl -w

package SkettiSCRIPT;
use CGI;
use CGI qw(param);
use sketdb;
use sketact;
use sketusr;
use sketboard;
use sketziggy;
use sketlog;

skettiStartBoard("Contribute");

my $db = skettiLoadDb();

my $mode = param('mode');
my $bg = "";
my $query;

my $nickn = skettiGrabLogin();
if ($nickn != -1) { 
	skettiUpdateLa($nickn);
	$query = $db->prepare("SELECT FONTC FROM USERS WHERE NICK = '$nickn';");
	$query->execute;
	$bg = $query->fetchrow_array;
}

if ($mode eq "get" || $mode eq "")
{
	print <<END;

<form action="pub4.cgi" method="POST" enctype="multipart/form-data" >
<input type="hidden" name="mode" value="save" />
<table border=0 cellspacing=0 cellpadding=10>
END
if ($nickn == -1)
{
	print <<END;
	<tr><td><strong><u>Nickname:</u></strong></td><td><input type="text" name="nick"></td></tr>
	<tr><td><strong><u>Password:</u></strong></td><td><input type="password" name="pass"></td></tr>
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
<tr><td bgcolor="$bg"><strong><u>File #1:</u></strong></td><td><input type="file" name="f1"></td></tr>
<tr><td bgcolor="$bg"><strong><u>File #2:</u></strong></td><td><input type="file" name="f2"></td></tr>
<tr><td bgcolor="$bg"><strong><u>File #3:</u></strong></td><td><input type="file" name="f3"></td></tr>
<tr><td bgcolor="$bg"><strong><u>File #4:</u></strong></td><td><input type="file" name="f4"></td></tr>
<tr><td bgcolor="$bg"><strong><u>File #5:</u></strong></td><td><input type="file" name="f5"></td></tr>
<tr><td bgcolor="$bg"><strong><u>File #6:</u></strong></td><td><input type="file" name="f6"></td></tr>
</table>
<center><input type="submit" value="upload"></form> <font size=-1><br>All files will be uploaded to the <a href="pub/">pub directory</a>.</font>

END

	skettiEndBoard();
}elsif ($mode eq "save")
{
	my $upload_dir = "/sketti/pub";
	my $upld = new CGI;

	our $nick = param('nick');
	our $pass = param('pass');
	our $f6 = param('f6');
	our $f5 = param('f5');
	our $f4 = param('f4');
	our $f3 = param('f3');
	our $f2 = param('f2');
	my $f1 = param('f1');

	$f1 =~ s/.*[\/\\](.*)/$1/gi;
	$f2 =~ s/.*[\/\\](.*)/$1/gi;
	$f3 =~ s/.*[\/\\](.*)/$1/gi;
	$f4 =~ s/.*[\/\\](.*)/$1/gi;
	$f5 =~ s/.*[\/\\](.*)/$1/gi;
	$f6 =~ s/.*[\/\\](.*)/$1/gi;

	my $file1 = $upld->upload("f1");
	my $file2 = $upld->upload("f2");
	my $file3 = $upld->upload("f3");
	my $file4 = $upld->upload("f4");
	my $file5 = $upld->upload("f5");
	my $file6 = $upld->upload("f6");

	if ($nick eq "" || $pass eq "")
	{
		print <<END;

Umm.. you are missing some stuff for your theme there.. you should probably <a href="pub.cgi?mode=get">go back</a> and fill it in.

END
	skettiEndBoard();
}
	$query = $db->prepare("SELECT PASS,BAN FROM USERS WHERE NICK = '$nick';");
	$query->execute;
	my $test = $query->rows;
	if ($test == 0)
	{
		print <<END;

Appy polly loggies!<br><br>You must <a href="join.cgi?mode=get">register</a> first.

END
	skettiEndBoard(); }
	my ($upass,$ban) = $query->fetchrow_array;
	if ($ban == 1) {
		print "You have been BANISHED!  Do not attempt to return here.\n";
		skettiEndBoard(); }
	if ($upass ne $pass)
	{
		print <<END;
All right, poseur, don't pretend to be something you are not, why don't you find out the RIGHT password and <a href="themef.cgi?mode=get">try again</a>

END
	skettiEndBoard();
}
if ($f1 ne "")
{
	open (F1, ">pub/$f1");
	
	binmode F1;
	
	while ( <$file1> )
	{
		print F1;
		
	}
	close (F1);
}

print "yah";
exit;

if ($f2 ne "")
{
	open (F2, ">$upload_dir/$f2");
	
	binmode F2;
	
	while ( <$file2> )
	{
		print F2 $_;
	}
	close (F2);
}
if ($f3 ne "")
{
	open (F3, ">$upload_dir/$f3");

	binmode F3;
	
	while ( <$file3> )
	{
		print F3 $_;
	}
	close (F3);
}
if ($f4 ne "")
{
	open (F4, ">$upload_dir/$f4");

	binmode F4;
	
	while ( <$file4> )
	{
		print F4 $_;
	}
	close (F4);
}
if ($f5 ne "")
{
	open (F5, ">$upload_dir/$f5");

	binmode F5;
	
	while ( <$file5> )
	{
		print F5 $_;
	}
	close (F5);
}
if ($f6 ne "")
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
	print "Thank you, $nick.  Click <a href=\"sbase.cgi\">here</a> to return to the base. Or <a href=\"pub/\">here</a> to goto the pub.";
	skettiLog ("$nick ($ip) uploads files: $f1 $f2 $f3 $f4 $f5 $f6");

skettiEndBoard(); }
