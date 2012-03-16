#!/usr/bin/perl -w

package SkettiSCRIPT;
use strict;
use sketdb;
use sketsauce;
use CGI qw(param);

my $def = param('def');
$def =~ s/&#040;/\(/g;
$def =~ s/&#041;/\)/g;

my $db = skettiLoadDb();
$def =~ s/'/\\'/g;
my $query = $db->prepare("SELECT * FROM SAUCE WHERE KW='$def';");
$query->execute;
if ($query->rows == 0)
{
	print <<END;
Content-type: text/html

<html>
<head>
<title>No Such Def '$def'</title>
</head>
<body>
No definition exists for '$def.' Sorry.
<hr noshade><center>
<a href="javascript:window.close()">close window</a></center>
</body></html>

END
	$db->disconnect;
	exit;
}
my ($id, $kw, $defi, $nick, $time, $type, $rating) = $query->fetchrow_array;
$defi = saucify $defi,"short";
$defi =~ s/\r\n/<br\/>/g;

print <<END;
Content-type: text/html

<html>
<head>
<title>SkettiSAUCE : $kw</title>
</head>
<body>
<strong>$kw</strong> ($type) <em>By $nick</em>:
<hr noshade>
$defi<hr noshade>
<center><a href="javascript:window.close()">close window</a></center>
</body></html>

END
$db->disconnect;
exit;
