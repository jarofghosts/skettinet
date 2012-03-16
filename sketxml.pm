#!/usr/bin/perl -w

#### SkettiSCRIPT v1.04                    ####
#### Auth: Jesse Keane                     ####
#### sketxml.pm::                          ####
#### xml module                            ####
####     provides:                         ####
#### skettiUpXML :updates xml headline file ####

package SkettiSCRIPT;
use strict;
use sketdb;
use XML::RSS;

sub skettiUpXML
{
	my $db = skettiLoadDb();
	my $query = $db->prepare("SELECT NICK,SUBJECT,TOPIC,MID FROM POSTS ORDER BY MID DESC LIMIT 10");
	$query->execute;
	my (@info,$nick,$subject,$topic,$mid);
	my $rss = new XML::RSS (version => '1.0');
		$rss->channel(
			title			=>	"sketti.net",
			link			=>	"http://other.sketti.net",
			description		=>	"SkettiNet?"
		);
		$rss->image(
			title			=>	"other.sketti.net",
			url			=>	"http://other.sketti.net/snowy.gif",
			link			=>	"http://other.sketti.net"
		);
	while (@info = $query->fetchrow_array)
	{
		($nick,$subject,$topic,$mid) = @info;
		$rss->add_item(
			title			=>	"$subject: $topic ($nick)",
			link			=>	"http://other.sketti.net/viewrp.cgi?id=$mid"
		);
	}
	open (SKETXML, ">sketti.rdf");
	print SKETXML $rss->as_string;
	return 0;
}
1;
