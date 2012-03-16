#!/usr/bin/perl -w

#### SkettiSCRIPT v1.5                    ####
#### Auth: Jesse Keane                     ####

package SkettiSCRIPT;
use strict;
use sketusr;
use sketdb;
use CGI;

sub skettiEndBoard
{
	my $ident = shift;
	if (!defined $ident) { $ident = ""; }
	my $theme = skettiGrabTheme();
	my $db = skettiLoadDb();
	my $query = $db->prepare(qq|SELECT BOTTOM FROM THEMES WHERE TITLE="$theme"|);
	$query->execute;
	my $bottom = $query->fetchrow_array;
	$bottom =~ s/!ident/$ident/gi;
	print $bottom;
	exit;
}
sub skettiStartBoardNoHead
{
	my $ident = shift;
	if (!defined $ident) { $ident = ""; }
	my $theme = skettiGrabTheme();
	my $db = skettiLoadDb();
	my $query = $db->prepare("SELECT TOP FROM THEMES WHERE TITLE=\"$theme\";");
	$query->execute;
	my $top = $query->fetchrow_array;
	$top =~ s/!ident/$ident/gi;
	print $top;
	return 0;
}
sub skettiStartBoard
{
	my $ident = shift;
	my $cgi = new CGI;
	print $cgi->header();
	if (!defined $ident) { $ident = ""; }
	my $theme = skettiGrabTheme();
	my $db = skettiLoadDb();
	my $query = $db->prepare("SELECT TOP FROM THEMES WHERE TITLE=\"$theme\";");
	$query->execute;
	my $top = $query->fetchrow_array;
	$top =~ s/!ident/$ident/gi;
	print $top;
	return 0;
}
sub skettiGrabType
{
	my $mid = shift;
	my $db = skettiLoadDb();
	my $query = $db->prepare("SELECT TYPE FROM BASE WHERE MID = $mid;");
	$query->execute;
	my $type = $query->fetchrow_array;
	if ($query->rows == 0) { $type = "NULL"; }
	return $type;
}
sub skettiCount
{
	my ($table_name,$args) = @_;
	my $where_statement = "";
	if (defined $args){
		$where_statement = "WHERE " . $args;
	}
	return skettiQuery ("SELECT COUNT(*) FROM $table_name $where_statement");
}
1;
