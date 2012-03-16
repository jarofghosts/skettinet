#!/usr/bin/perl -w

use strict;

package SkettiSCRIPT;
use sd;
use DBI;
use Date::Calc qw(Delta_DHMS);
use CGI qw(param);

print "Content-type: text/html\n\n";

my $theme = getTheme();
open (TOP, "themes/$theme.tf") || skettiError "Cannot open topfile.";
open (BOTTOM, "themes/$theme.bf") || skettiError "Cannot open bottomfile.";

print "<center><img src=\"ffej/quotes.gif\" alt=\"quotes\"></center><p><table border=1 bordercolor=\"#000000\" cellspacing=1 cellpadding=2>";
my $nick = grabLogin();
updateLa($nick);

my $db = loadDb();
my (@pquo,@rquo,$mid,$pq,$pqe,$rq,$rqe);

my $query = $db->prepare("SELECT MID,QUOTE,QUOTEE FROM POSTS WHERE QUOTE != '' ORDER BY QUOTEE;");
$query->execute;
while (@pquo = $query->fetchrow_array)
{
	($mid,$pq,$pqe) = @pquo;
	print "<tr><td bgcolor=\"#f8f8f8\"><em>&quot;$pq&quot;</em><br>-$pqe\n";
	my $q = $db->prepare("SELECT QUOTE,QUOTEE FROM REPLIES WHERE MID = $mid AND QUOTE != '' ORDER BY QUOTEE;");
	$q->execute;
	while (@rquo = $q->fetchrow_array)
	{
		($rq,$rqe) = @rquo;
		print "<br>&nbsp;&nbsp;&nbsp;<em>&quot;$rq&quot;</em><br>&nbsp;&nbsp;&nbsp;-$rqe\n";
	}
	print "</td></tr>";
}
print "</table></p>";
EndSBoard();
exit;
