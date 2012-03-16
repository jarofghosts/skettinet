#!/usr/bin/perl

use strict;
use CGI qw(param);

print "Content-type: text/html\n\n";

my $var = param('pic');
if ($var eq "") { $var = 1; }
my $next = $var +1;
my $prev = $var -1;

print <<END;
<html>
<head>
<title>The Legend of SkettiISLAND</title>
<body bgcolor="#000000" text="#FFFFFF">
<center><strong><font size=+5>SkettiISLAND</font></strong>
<table border=0 width=75%>
<tr><td align=center><img src="PIC$var" alt="PIC$var"></td></tr>
<tr><td align=center>PIC$var</td></tr>
<tr><td align=center>

END
if ($prev > 0) { print "<a href=\"index.cgi?pic=$prev\">&lt;Previous</a>";
if ($prev > 0 && $next < 98) { print "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;";
if ($next < 98) { print "<a href=\"index.cgi?pic=$next\">Next&gt;</a>";
print "</td></tr></table>";
exit;
