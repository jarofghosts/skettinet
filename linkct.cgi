#!/usr/bin/perl -w

package SkettiSCRIPT;
use strict;
use sketdb;
use sketusr;
use sketboard;
use CGI qw(param);

my $lid = param('lid');
my $db = skettiLoadDb();
my $q = new CGI;
my $query = $db->prepare("SELECT HITS,URL,TITLE FROM LINKS WHERE LID = $lid;");
$query->execute;
my ($hits,$url,$title) = $query->fetchrow_array;
$hits++;
skettiQuery ("UPDATE LINKS SET HITS = $hits WHERE LID = $lid;");

print $q->header(-location=>"$url");
exit;
