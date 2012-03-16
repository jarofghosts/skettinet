#!/usr/bin/perl -w

package SkettiSCRIPT;
use strict;
use sketsauce;
use sketusr;
use skettime;
use sketboard;
use sketmsgs;
use sketact;
use sketdb;
use CGI qw(param);

skettiStartBoard("View Replies");

my $id = param('id');
my $key = param('key');
my $ptext;
my $query3;

my $db = skettiLoadDb();
my ($query,$replies,$query2);

my $li = 0;
my $lonick = skettiGrabLogin();
if ($lonick != -1) { skettiUpdateLa($lonick); $li = 1;}

$query = $db->prepare("SELECT VISIBLE,TYPE FROM BASE WHERE MID = $id;");
$query->execute;
my ($vis,$type) = $query->fetchrow_array;
my (@pinfo,$m,$time1,$time2,$time3,$time4,$time5,$time6,$stopic,$score,$rating,$lr);
if ($query->rows < 1) {
	$query = $db->prepare("SELECT MID FROM BASE ORDER BY MID DESC;");
	$query->execute;
	my $current = $query->fetchrow_array;
	my $morep = $id - $current;
	print "That message doesn't exist.  You could post $morep more messages to the <a href=\"sbase.cgi\">base</a> to get that number if you so desire, though :)";
	skettiEndBoard();
}
my ($outp,$views);
if ($type eq "post") { $outp = skettiBuildPost ($id,$vis,999999999,undef,$key);
skettiQuery ("UPDATE POSTS SET VIEWS = VIEWS + 1 WHERE MID = $id");
 }elsif ($type eq "poll"){ $outp = skettiBuildPoll ($id,$vis);
skettiQuery ("UPDATE POLLS SET VIEWS = VIEWS + 1 WHERE MID = $id");
 }
print "$outp<br/><hr noshade/><br/>";
my $id_column = $vis == 0 ? "OID" : "MID";

if (skettiCount("REPLIES",qq|$id_column = $id|) == 0)
{
	print "That message apparently has no replies.. if you would like, you could <a href=\"replym.cgi?id=$id\">reply to it<\/a> or <a href=\".\">return to the forum</a>.";
	skettiEndBoard();
}
$query = $db->prepare("SELECT RID FROM REPLIES WHERE $id_column = $id");
$query->execute;
my $replies = $query->fetchall_arrayref();

for my $reply (@{$replies}){
    
	print skettiBuildReply($id,$reply->[0],$key,$li);
	
}

print "<p align=\"center\"><hr noshade></p>";
print "<p align=\"center\"><a href='replym.cgi?id=$id'>add reply</a> + <a href='sbase.cgi'>back to the forum</a></p>\n";
skettiEndBoard();
