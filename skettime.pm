#!/usr/bin/perl -w

#### SkettiSCRIPT v1.04                    ####
#### Auth: Jesse Keane                     ####
#### skettime.pm::                         ####
#### time manipulation module              ####
####     provides:                         ####
#### skettiTimeForm :formats time          ####

package SkettiSCRIPT;
use strict;

sub skettiTimeForm
{
	my $m;
	my $time = shift;
	my $timef = shift;
	my ($day,$month,$date,$ltime,$year) = split(/ /,$time);
	my ($day2,$month2,$month3,$hour2);
	if ($day eq "Sun") { $day2 = "Sunday"; }elsif ($day eq "Mon") { $day2 = "Monday"; }elsif ($day eq "Tue") { $day2 = "Tuesday"; }
	elsif ($day eq "Wed") { $day2 = "Wednesday"; }elsif ($day eq "Thu") { $day2 = "Thursday"; }elsif ($day eq "Fri") { $day2 = "Friday"; }
	elsif ($day eq "Sat") { $day2 = "Saturday"; }else { $day2 = "Skettiday"; }
	if ($month eq "Jan") { $month2 = "January" }elsif ($month eq "Feb") { $month2 = "February"; }elsif ($month eq "Mar") { $month2 = "March"; }
	elsif ($month eq "Apr") { $month2 = "April"; }elsif ($month eq "May") { $month2 = "May"; }elsif ($month eq "Jun") { $month2 = "June"; }
	elsif ($month eq "Jul") { $month2 = "July"; }elsif ($month eq "Aug") { $month2 = "August"; }elsif ($month eq "Sep") { $month2 = "September"; }
	elsif ($month eq "Oct") { $month2 = "October"; }elsif ($month eq "Nov") { $month2 = "November"; }elsif ($month eq "Dec") { $month2 = "December"; }
	else{ $month2 = "Smarch"; }
	my ($hour,$min,$sec) = split(/:/,$ltime);
	if ($hour > 12) { $m = "PM"; }else{ $m = "AM"; }
	if ($hour == 13) { $hour2 = "01"; }elsif ($hour == 14) { $hour2 = "02"; }elsif ($hour == 15) { $hour2 = "03"; }elsif ($hour == 16) { $hour2 = "04"; }
	elsif ($hour == 17) { $hour2 = "05"; }elsif ($hour == 18) { $hour2 = "06"; }elsif ($hour == 19) { $hour2 = "07"; }elsif ($hour == 20) { $hour2 = "08"; }
	elsif ($hour == 21) { $hour2 = "09"; }elsif ($hour == 22) { $hour2 = 10; }elsif ($hour == 23) { $hour2 = 11; }elsif ($hour == 24 || $hour == 0) { $hour2 = 12; }
	else{ $hour2 = $hour; }
	if ($month eq "Jan") { $month3 = 1; }elsif ($month eq "Feb") { $month3 = 2; }elsif ($month eq "Mar") { $month3 = 3; }elsif ($month eq "Apr") { $month3 = 4; }
	elsif ($month eq "May") { $month3 = 5; }elsif ($month eq "Jun") { $month3 = 6; }elsif ($month eq "Jul") { $month3 = 7; }elsif ($month eq "Aug") { $month3 = 8; }
	elsif ($month eq "Sep") { $month3 = 9; }elsif ($month eq "Oct") { $month3 = 10; }elsif ($month eq "Nov") { $month3 = 11; }elsif ($month eq "Dec") { $month3 = 12; }
	else{ $month3 = 27; }

my $time1 = "$day2, $month2 $year ($hour2:$min $m)";
my $time2 = "$hour:$min:$sec ($month3/$date/$year)";
my $time3 = "$day2, $month $date \@$hour2:$min $m";
my $time4 = "$day2, $month $date \@$hour:$min:$sec";
my $time5 = "$month\/$date\/$year \@$hour:$min:$sec";
my $time6 = "$month\/$date\/$year \@$hour2:$min $m";

	if ($timef eq "time1") { return $time1; }
	if ($timef eq "time2") { return $time2; }
	if ($timef eq "time3") { return $time3; }
	if ($timef eq "time4") { return $time4; }
	if ($timef eq "time5") { return $time5; }
	if ($timef eq "time6") { return $time6; }
	else { return $time; }
}
1;