#!/usr/bin/perl -w

use strict;
use CGI qw(debug);

my $cgi = new CGI;

my $file = $cgi->param('section');

print $cgi->header();

open(SECTION, "/sketti/pub/Decapitron/sections/$file\.ds") || die "Can't open $file\.ds";

while (<SECTION>){
	
	print $_;
	
}
close(SECTION);

exit;