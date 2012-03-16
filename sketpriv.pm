#!/usr/bin/perl -w

#### SkettiSCRIPT v1.5                                      ####
#### Auth: Jesse Keane                                       ####

package SkettiSCRIPT;
use strict;
use sketdb;
use sketsauce;

## skettiBuildPrivs
##     accepts a username and a message count as arguments
##     returns a zebra-striped list of (message count) private messages for (username)
sub skettiBuildPrivs
{
	my ($username,$pmessage_count) = @_;

	my ($privs_output,$priv_info,@priv_time,$query,$tr_class,
	$real_name,$output_name,$cgi_file,$color_query);
	
	my $db = skettiLoadDb();
	
	$query = $db->prepare(qq|SELECT SENDER,MSG,MID,TIME FROM PRIVMSG WHERE NICK = "$username" ORDER BY MID DESC LIMIT $pmessage_count|);
	$query->execute;

	my $count = 1;
	
	while ( $priv_info = $query->fetchrow_hashref() )
	{
		$$priv_info{'MSG'} =~ s/\r\n/<br\/>/g; # convert returns to <br/>'s for displaying
		$$priv_info{'MSG'} = saucify $$priv_info{'MSG'}; # EVERYTHING GETS SAUCIFIED! OW!
		$$priv_info{'TIME'} =~ s/  / /g;
		@priv_time = split(/ /,$$priv_info{'TIME'}); # as of right now, im not using this for anything
		
		# here's the bit where we get the font color of the message, define what script will handle the user/clan info link
		if ($$priv_info{'SENDER'} =~ /^%/) {
			$color_query = $db->prepare(qq|SELECT CID,COLOR FROM CLANS WHERE NAME = "$$priv_info{SENDER}"|);
			$cgi_file = "viewgrp.cgi";
		} else {
			$color_query = $db->prepare(qq|SELECT UID,FONTC FROM USERS WHERE NICK = "$$priv_info{SENDER}"|);
			$cgi_file = "users.cgi";
		}
		
		$color_query->execute;
		my ($sender_id,$font_color) = $color_query->fetchrow_array;
		
		$tr_class = ($count % 2) == 0 ? "even_row" : "odd_row"; # for striping
		
		$privs_output .= qq( <tr class="$tr_class"><td><a href="delpriv.cgi?id=$$priv_info{'MID'}" title="Delete message $$priv_info{'MID'}">x</a>  &lt;<a href="$cgi_file?id=$sender_id" title="View $$priv_info{'SENDER'}'s Information">$$priv_info{'SENDER'}</a>&gt; <span style="color:$font_color">$$priv_info{'MSG'}</span></td></tr>);
		
		$count++; # again with the stripes
	}

	if (length($privs_output) > 0){ # if there were some, let em choose to delete all of them...
		$tr_class = $tr_class eq "odd_row" ? "even_row" : "odd_row";
		$privs_output .= qq(<tr class="$tr_class"><td><a href="delpriv.cgi?id=all" title="Delete All of Your Private Messages"><p align="center">x all</a></td></tr>);
	}
	$tr_class = $tr_class eq "odd_row" ? "even_row" : "odd_row";
	$privs_output .= qq(<tr class="$tr_class"><td><form method="post" action="sendmsg.cgi"><p align="center">
	/msg <select name="to">);
	$query = $db->prepare("SELECT NAME FROM CLANS WHERE ACTIVE = 1;"); # let's make a list of clans to message!
	$query->execute;
	
	while ($output_name = $query->fetchrow_array)
	{
		$real_name = $output_name;
		if (length($output_name) > 20) { $output_name = substr($output_name,0,20) . ".."; } #make sure we don't go out of bounds
		$privs_output .= qq(<option value="$real_name">$output_name</option>\n);
	}
	
	$query = $db->prepare("SELECT NICK FROM USERS WHERE BAN = 0 ORDER BY UID ASC;"); # now let's break it on down for the users
	$query->execute;
	
	while ($output_name = $query->fetchrow_array)
	{
		$real_name = $output_name;
		if (length($output_name) > 20) { $output_name = substr($output_name,0,20) . ".."; }
		$privs_output .= qq(<option value="$real_name">$output_name</option>\n);
	}
	
	$privs_output .= qq(</select><br/><br/><input type="text" name="msg" class="text"/><br/><br/><input type="submit" value="send" class="submit"/></p></form></td></tr>);
	
	return $privs_output;
}
1;
