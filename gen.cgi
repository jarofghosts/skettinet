#!/usr/bin/perl -w

use strict;
use HTML::Prototype;
use CGI;

my $cgi = new CGI;
my $proto = new HTML::Prototype;

print $cgi->header();

print $proto->submit_to_remote("post","say", { update => 'chatter', url=> 'chatter.cgi', with=>'message'});

print "<br/><br/>" . $proto->periodically_call_remote( { update => 'chatter', frequency => 5, url => 'chatter.cgi'});
