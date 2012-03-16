#!/usr/bin/perl -w

#### SkettiSCRIPT v1.04                    ####
#### Auth: Jesse Keane                     ####
#### sketziggy.pm::                        ####
#### ziggy module                          ####
####     provides:                         ####
#### skettiSendZiggyMsg :sends msg as ziggy####
#### skettiGlobalZiggy :sends global msg   ####

package SkettiSCRIPT;
use strict;
use sketdb;

sub skettiSendZiggyMsg
{
	my $rec = shift;
	my $msg = shift;
	$msg =~ s/'/\\'/gi;
	my $db = skettiLoadDb;
	my $mid;
	my $time = localtime;
	my $query = $db->prepare("SELECT ZIGGY FROM USERS WHERE NICK = '$rec';");
	$query->execute;
	if ($query->fetchrow_array == 0) { return; }
	$query = $db->prepare("SELECT MID FROM PRIVMSG ORDER BY MID DESC;");
	$query->execute;
	if ($query->rows == 0) { $mid = 0; } else { $mid = $query->fetchrow_array; $mid++; }
	$query = $db->prepare("INSERT INTO PRIVMSG (NICK,SENDER,MSG,TIME,MID) VALUES ('$rec', 'Ziggy', '$msg', '$time', $mid);");
	$query->execute;
	return;
}
sub skettiGlobalZiggy
{
	my $db = skettiLoadDb;
	my $sender = shift;
	my $msg = shift;
	my $nnick;
	my $urlsender = $sender;
	$urlsender =~ s/ /%20/gi;
	my $query = $db->prepare("SELECT NICK FROM USERS WHERE ZIGGY = 1;");
	$query->execute;
	while ($nnick = $query->fetchrow_array)
	{
		if ($nnick ne "Ziggy") { skettiSendZiggyMsg $nnick, "(<a href=\"users.cgi?nick=$urlsender\">$sender</a>) $msg"; }
	}
}
1;