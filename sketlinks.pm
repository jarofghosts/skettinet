#!/usr/bin/perl -w

#### SkettiSCRIPT v1.04                                      ####
#### Auth: Jesse Keane                                       ####
#### sketlinks.pm::                                           ####
#### linkbase module                                     ####
####     provides:                                           ####
#### skettiBuildLinks (arg1) :builds arg1 number of links ####

package SkettiSCRIPT;
use sketdb;
use strict;

sub skettiBuildLinks
{
	my $link_count = shift;
	my ($links_output,$link_info,$hit_text);
	my $db = skettiLoadDb();

	my $query = $db->prepare('SELECT LID,NICK,TITLE,HITS,URL FROM LINKS ORDER BY LID DESC LIMIT ' . $link_count);
	$query->execute;
	my $count = 1;
	my $tr_class;
	while ( $link_info = $query->fetchrow_hashref() )
	{
		$tr_class = ($count % 2) == 0 ? "even_row" : "odd_row";
		$hit_text = "hits";
		if ($$link_info{'HITS'} == 1) { $hit_text = "hit"; }
		$links_output .= 
		qq|<tr class="$tr_class"><td>$$link_info{'LID'}. <a title="URL: $$link_info{'URL'}" href="linkct.cgi?lid=$$link_info{'LID'}">$$link_info{'TITLE'}</a> <strong>\[$$link_info{'HITS'} $hit_text\]</strong> ($$link_info{'NICK'})</tr></td>\n\n|;
		$count++;
	}
return $links_output;
}
1;
