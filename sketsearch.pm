#!/usr/bin/perl -w

package SkettiSCRIPT;
use strict;
use sketdb;

sub skettiSearch
{
	my $type = shift;
	my $string = shift;
	my $key = $string;
	$key =~ s/ /%20/g;
	$key =~ s/\%/%25/g;
	my ($other, $body,$query,@pinfo,$mid,$topic,$msg,$nick,$pquote,$pquotee);
	my $db = skettiLoadDb();
	if ($type eq "post") { 
		$type="POSTS";
		$body="MSG";
		$other=qq|UPPER(QUOTE) LIKE UPPER("%$string%") OR UPPER(QUOTEE) LIKE UPPER("%$string%")|;
	}elsif ($type eq "poll"){
		$type="POLLS";
		$body="TXT";
		$other=qq|UPPER(OPT1) LIKE UPPER("%$string%") OR UPPER(OPT2) LIKE UPPER("%$string%") OR UPPER(OPT3) LIKE UPPER("%$string%") OR UPPER(OPT4) LIKE UPPER("%$string%") OR UPPER(OPT5) LIKE UPPER("%$string%")|;
	}else { $type="CHANS";
		$body="LOG";
		$other=qq|UPPER(NAME LIKE UPPER("%$string%") OR UPPER(LOG) LIKE UPPER("%$string%")|;
}
	$query = $db->prepare(qq|SELECT MID,TOPIC,NICK FROM $type WHERE VISIBLE = 1 AND (UPPER(TOPIC) LIKE UPPER("%$string%") OR UPPER($body) LIKE UPPER("%$string%") OR $other) ORDER BY MID DESC;|);
	$query->execute;
	my $ctr = 0;
while (@pinfo = $query->fetchrow_array)
{
	$ctr++;
($mid,$topic,$nick) = @pinfo;
print "<li> &quot;<a href=\"viewrp.cgi?id=$mid&key=$key\">$topic</a>&quot; ($nick)<br/>";
}
if ($type eq "POSTS"){
print "<h4>Replies:</h4><ol>";
my $query2 = $db->prepare(qq|SELECT MID,RID,NICK FROM REPLIES WHERE (UPPER(MSG) LIKE UPPER("%$string%") OR UPPER(QUOTE) LIKE UPPER("%$string%") OR UPPER(QUOTEE) LIKE UPPER("%$string%"))|);
$query2->execute;
my @pinfo2;
while (@pinfo2=$query2->fetchrow_array){
	$ctr++;
	my ($rmid,$rid,$rnick) = @pinfo2;
	print "<br/><li>&nbsp;($rmid)&nbsp;=>&quot;<a href=\"viewrp.cgi?id=$rmid&key=$key#$rid\">Re: #$rmid</a>&quot; ($rnick)";
}
}
print "</ol>";
return $ctr;
}
1;
