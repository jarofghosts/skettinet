#!/usr/bin/perl -w

package SkettiSCRIPT;
use sketdb;
use strict;
use sketboard;
use sketbase;


	skettiStartBoard("SMILIES!");

	my ($links_output,$link_info);
	my $db = skettiLoadDb();

	my $query = $db->prepare('SELECT * FROM SMILIES');
	$query->execute;
	my $count = 1;
	my $tr_class;
	print "<table>";
	while ( $link_info = $query->fetchrow_hashref() )
	{
		$tr_class = ($count % 2) == 0 ? "even_row" : "odd_row";
		print 
		qq|<tr class="$tr_class"><td>$$link_info{'KEYWORD'} = <img src="$$link_info{'IMAGE'}" alt="$$link_info{'KEYWORD'}"/></tr></td>\n\n|;
		$count++;
	}
	print "</table>";
	skettiEndBoard();
	exit;
