#!/usr/bin/perl -w

#### SkettiSCRIPT v1.04                    ####
#### Auth: Jesse Keane                     ####
#### sketusr.pm::                          ####
#### user settings module                  ####
####     provides:                         ####
#### skettiGrabLogin :grabs login name     ####
#### skettiGrabTheme :grabs user's theme   ####
#### skettiUpdateLITable :updates loggedin ####
#### skettiGrabPass (arg) :gets arg's pass ####

package SkettiSCRIPT;
use strict;
use sketdb;
use CGI;
use sketact;
use sketziggy;
use Date::Calc qw(Delta_DHMS);

sub skettiUserLevel
{
	my $nick = shift;
	my $db = skettiLoadDb();
	my $query = $db->prepare(qq|SELECT LVL FROM USERS WHERE NICK = "$nick"|);
	$query->execute;
	return $query->fetchrow_array;
}
sub skettiGrabLogin
{
	my $db = skettiLoadDb;
	my $q = new CGI;
	my $session = defined $q->cookie('session') ? $q->cookie('session') : "POOP";
	skettiUpdateLITable(skettiGetTA());
	my $query = $db->prepare(qq|SELECT NICK FROM LOGGEDIN WHERE SID = "$session";|);
	$query->execute;
	if ($query->rows == 0) { return -1; }
	return $query->fetchrow_array;
}
sub skettiUpdateLITable
{
	my $db = skettiLoadDb;
	my @time = split(/ /,skettiGetTA());
	my ($hour1,$min1,$sec1) = split(/:/,$time[3]);
	
	my $query = $db->prepare("SELECT LA,NICK FROM LOGGEDIN;");
	$query->execute;
	while (my ($la,$nick) = $query->fetchrow_array){
		$la =~ s/  / /gi;
		my @time2 = split(/ /,$la);
		my ($hour2,$min2,$sec2) = split(/:/,$time2[3]);
	
		my ($Dd,$Dh,$Dm,$Ds) = Delta_DHMS(102,1,2,$hour1,$min1,$sec1,102,1,2,$hour2,$min2,$sec2);
		
		if ($Dm < -30){
			my $q = $db->prepare(qq|DELETE FROM LOGGEDIN WHERE NICK = "$nick"|);
			$q->execute;
			my $time = time;
			$q = $db->prepare(qq|UPDATE USERS SET LLI = $time WHERE NICK = "$nick"|);
			$q->execute;
		}
		
	}
}
sub skettiGrabTheme
{
	my ($query,$theme);
	my $db = skettiLoadDb();
	my $nick = skettiGrabLogin();
	
	if ($nick != -1){
		$query = $db->prepare(qq|SELECT THEME FROM USERS WHERE NICK = "$nick"|);
		$query->execute;
		$theme = $query->fetchrow_array;
	}else{ $theme = "moderno"; }
	
	return $theme;
}
sub skettiGrabLLI
{
	my $nick = shift;
	my $db = skettiLoadDb();
	my $query = $db->prepare(qq|SELECT LLI FROM USERS WHERE NICK="$nick"|);
	$query->execute;
	return $query->fetchrow_array;
}
sub skettiGrabPass
{
	my $nick = shift;
	my $db = skettiLoadDb();
	my $query = $db->prepare("SELECT PASS FROM USERS WHERE NICK = \"$nick\";");
	$query->execute;
	return $query->fetchrow_array;
}
sub skettiIsBanned
{
	my $nick = shift;
	my $db = skettiLoadDb();
	my $query = $db->prepare(qq|SELECT BAN FROM USERS WHERE NICK = "$nick"|);
	$query->execute;
	return $query->fetchrow_array;
}
sub skettiDeleteBMarks
{
	my $pid = shift;
	my $nick = shift;
	if ($nick ne "") { $nick = " AND NICK = \"$nick\""; }
	my @pids = split(/##/,$pid);
	my $db = skettiLoadDb();
	my ($bmd,@bkms);
	foreach $bmd(@pids)
	{
		$bmd =~ s/#//g;
		my $query = $db->prepare("SELECT NICK,BKMRKS FROM USERS WHERE BKMRKS REGEXP \"$bmd\";");
		$query->execute;
		while (@bkms = $query->fetchrow_array)
		{
			my ($nick,$bkm) = @bkms;
			$bkm =~ s/#$bmd#//g;
			my $q = $db->prepare ("UPDATE USERS SET BKMRKS = \"$bkm\" WHERE NICK = \"$nick\";");
			$q->execute;
		}
	}
}
sub skettiUpdateLvl
{
	my $nick = shift;
	my $rating = shift;
	my $db = skettiLoadDb();
	my $query = $db->prepare(qq|SELECT EXP,LVL,TITLE,SEX FROM USERS WHERE NICK = "$nick"|);
	$query->execute;
	my ($exp,$lvl,$title,$sex) = $query->fetchrow_array;
	my $olvl = $lvl;
	$exp += $rating;
	if ($exp >= 50 && $lvl == 1) {
		$lvl++;
		$title = 'Novice';
	}
	if ($exp >= 150 && $lvl == 2) {
		$lvl++;
		$title = 'Apprentice';
	}
	if ($exp >= 300 && $lvl == 3) {
		$lvl++;
		if ($sex eq "Female") { $title = "Queen"; }else{ $title = "King"; }
	}
	if ($exp >= 450 && $lvl == 4) {
		$lvl++;
		if ($sex eq "Female") { $title = "Lady"; }else{ $title = "Lord"; }
	}
	if ($exp >= 550 && $lvl == 5) {
		$lvl++;
		$title = 'Messiah';
	}
	if ($exp >= 750 && $lvl == 6) {
		$lvl++;
		$title = 'Deity';
	}
	if ($exp >= 1000 && $lvl == 7) {
		$lvl++;
		$title = 'God';
	}
	if ($olvl < $lvl) { skettiSendZiggyMsg ($nick, qq|Huzzah, you've acheived the rank of "$title"!|); }
	$query = $db->prepare (qq|UPDATE USERS SET EXP = $exp, LVL = $lvl, TITLE = "$title" WHERE NICK = "$nick"|);
	$query->execute;
}
sub skettiIsOp
{
	my $nick = shift;
	my $forum = shift;
	if (!($forum =~ m/^%/)) { return 0; }
	my $db = skettiLoadDb();
	my $query = $db->prepare(qq|SELECT CID FROM CLANS WHERE NAME = "$forum" AND LEADER = "$nick"|);
	$query->execute;
	if ($query->rows == 0) { return 0; } else { return 1; }
}
sub skettiForum
{
	my $id = shift;
	return skettiQuery("SELECT FORUM FROM BASE WHERE MID = $id");
}
1;
