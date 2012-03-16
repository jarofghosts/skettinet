#!/usr/bin/perl -w

#### SkettiSCRIPT v1.5                                      ####
#### Auth: Jesse Keane                                       ####

package SkettiSCRIPT;
use strict;
use sketdb;
use sketact;

## skettiBuildUsers () 
##    accepts no arguments
##    returns a zebra-stripe formatted list of current users logged in

sub skettiBuildUsers
{
	my $db = skettiLoadDb();
	my ($logged_in_text, $ban, $tr_class) = "";
	skettiUpdateLITable(); # make sure we get the FRESHNESS
	
	my $query = $db->prepare("SELECT NICK FROM LOGGEDIN ORDER BY NICK ASC;");
	$query->execute;
	my $logged_in_users = $query->fetchall_arrayref(); # let's go ahead and get a big ole arrayref of all the logged in peoples' nicknames
	
	my $count = 1; # for zebra striping
	
	for my $logged_in_user (@{$logged_in_users})
	{
		my $nick = $logged_in_user->[0];
		$tr_class = ($count % 2) == 0 ? "even_row" : "odd_row"; # if the number is even, it's class is even_row.. odd .. odd_row yeah..
		$query = $db->prepare(qq|SELECT UID,TITLE,BAN FROM USERS WHERE NICK = "$nick"|); #man, this whole working with nicknames thing was a bad idea.
		# if i wouldve made the db when i was say.. older than 16 or whatever it wouldve been based on uid. maybe some auto_increment action.. ANYWAY
		$query->execute;
		my $user = $query->fetchrow_hashref; # get a nice hashref of the user's info.
		
		$ban = $$user{'BAN'} == 0 ? "" : " <strong>{BANNED}</strong>"; # if they're banned, let em know
		$logged_in_text .= qq|<tr class="$tr_class"><td><a href="users.cgi?id=$$user{'UID'}" title="View $nick\'s Profile">$nick (<em>$$user{'TITLE'}</em>)</a>$ban</td></tr>\n|; # format Nickname (title) {banned?}
		$count++; # increment for striping
	}
	if ($logged_in_text eq "") { $logged_in_text = qq|<tr class="odd_row"><td><em>No one</em></td></tr>|; } #no people? NOT A PROBLEM!!@##$$
	return $logged_in_text; # return all that junk for addition to the base
}
1;