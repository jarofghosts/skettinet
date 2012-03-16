#!/usr/bin/perl -w

#### SkettiSCRIPT v1.5                    ####
#### Auth: Jesse Keane                     ####

package SkettiSCRIPT;
use strict;
use skettime;
use sketdb;
use sketmsgs;
use sketusr;
use sketsauce;
use sketboard;

my ($query,$query2,$rating,$score,$lr,$query3,$limtxt,$ptext,$pimage,$basetxt,$replies)="";

sub skettiBuildBase
{
	my $db = skettiLoadDb();
	my ($disp,$ptd,$sort,$trunc,$gy,$subdef,$page) = @_;

	if (!defined $page) { $page = 1; }
	if (!defined $ptd) { $ptd = 10; }
	if (!defined $trunc || $trunc == 0) { $trunc = 400; }
	if (!defined $sort) { $sort = "default"; }
	if (!defined $disp) { $disp = "default"; }

	my $offset = ($ptd * ($page - 1));

	my $linick = skettiGrabLogin();
	my $theme = skettiGrabTheme();
	$query = $db->prepare(qq|SELECT EXCLUDE FROM USERS WHERE NICK="$linick"|);
	$query->execute;
	my $excludes = $query->fetchrow_array;
	$query = $db->prepare(qq|SELECT POLLIMAGE FROM THEMES WHERE TITLE="$theme";|);
	$query->execute;
	my $pimage=$query->fetchrow_array;
	my $exc_text ="";
	if (defined $excludes && $excludes ne ""){
		my @excl = split(/##/,$excludes);
		my $exc;
		foreach $exc(@excl){
			$exc =~ s/#//g;
			if ($exc eq $subdef) { next; }
			$exc_text .= "AND FORUM != \"$exc\" ";
		}
	}
	if ($sort eq "Post_Number_Desc") { $sort = "descending"; }elsif ($sort eq "Post_Number_Asc") { $sort = "ascending"; }
	if ($sort eq "ascending") { $sort = "MID ASC"; }elsif ($sort eq "descending"){ $sort = "MID DESC"; }elsif ($sort eq "Score_Asc") { $sort = "SCORE ASC"; }elsif ($sort eq "Score_Desc") { $sort = "SCORE DESC"; }else{ $sort = "LASTR DESC"; }
	
	my $start = skettiCount("BASE",undef);
	
	my $gy_text;
	if ($gy eq "" || $gy == 1) { $gy_text = "= 1"; } else { $gy_text = "= 0"; }
	
	if ($disp eq "long") { $limtxt = ""; } else { $limtxt = "LIMIT $offset,$ptd;"; }
	
	my $subselect = "";
	if (defined $subdef){
		$subselect = qq|AND FORUM = "$subdef"|; 
		if ($subdef =~ m/^\%/) { $gy_text = ">= 1"; }
	}
	
	#wow all that work and we finally got this hacked-ass sql select
	$query = $db->prepare(qq|SELECT MID,TYPE FROM BASE WHERE VISIBLE $gy_text $exc_text $subselect ORDER BY $sort $limtxt|);
	$query->execute;
	my $posts = $query->fetchall_arrayref();
	
	my $basetxt;

	if ($disp eq "long"){
		
		for my $post (@{$posts}){
			
			$query = $db->prepare("SELECT SUBJECT,MID,TOPIC,NICK,TIME FROM " . uc($post->[1]) . "S WHERE MID = " . $post->[0] . ";");
			$query->execute;
			my $post_info = $query->fetchrow_hashref;

			$query = $db->prepare(qq|SELECT IMG FROM SUBJECTS WHERE NAME = "| . $$post_info{'SUBJECT'} . qq|"|);
			$query->execute;
			my $subj_image = $query->fetchrow_array;
			
			my $replies = skettiCount("REPLIES",qq|MID = $$post_info{'MID'}|);

			$basetxt .= qq|<p align="left">|;
			$basetxt .= qq|<img src="$subj_image" width="30" height="35" alt="$$post_info{'SUBJECT'}"/> &nbsp; <a
				href="viewrp.cgi?id=$$post_info{'MID'}"><strong>$$post_info{'TOPIC'}</strong> <em>($$post_info{'SUBJECT'})</em></a> -
				<strong>$post->[1]</strong> by $$post_info{'NICK'} @ $$post_info{'TIME'} <u>|;
		
			$basetxt .= qq|($replies repl|;
			$basetxt .= $replies == 1 ? qq|y| : qq|ies|;
			$basetxt .= qq|)</u>\n<br/>|;
		}
	
	return $basetxt . "</p>";
	
	}else{
	
		for my $post (@{$posts}){
			
			if ($post->[1] eq "post"){
			
				$basetxt .= skettiBuildPost ($post->[0],$gy,$trunc,$subdef);
				
			}elsif ($post->[1] eq "poll"){
			
				$basetxt .= skettiBuildPoll ($post->[0],$gy,$pimage,$subdef);
				
			}
			
		}
		
	}
	
	return $basetxt;
	
}

sub skettiUpdateVisitors
{
	my $db = skettiLoadDb();
	my $localtime = localtime;
	$localtime =~ s/  / /;
	my ($day,$month,$time,$blah,$year) = split(/ /,$localtime);
	my $query = $db->prepare("SELECT VISITORS FROM VISITORS WHERE MONTH='$month' AND YEAR=$year;");
	$query->execute;
	if ($query->rows == 0) {
		skettiQuery ("INSERT INTO VISITORS (MONTH,YEAR,VISITORS) VALUES ('$month',$year,1);");
	}else{
		skettiQuery ("UPDATE VISITORS SET VISITORS = VISITORS + 1 WHERE MONTH='$month' AND YEAR=$year;");
	}
}
sub skettiGrabVisitors
{
	my $stat = shift;
	my $db = skettiLoadDb();
	my $localtime = localtime;
	$localtime =~ s/  / /;
	my ($day,$month,$time,$blah,$year) = split(/ /,$localtime);
	my $query = $db->prepare("SELECT VISITORS FROM VISITORS WHERE MONTH='$month';");
	$query->execute;
	my $monthtotal = $query->fetchrow_array;
	if ($stat eq "month") { return $monthtotal; }
	
	$query = $db->prepare("SELECT VISITORS FROM VISITORS WHERE YEAR=$year;");
	$query->execute;
	my ($ytemp,$yeartotal);
	while ($ytemp = $query->fetchrow_array){
		$yeartotal += $ytemp;
	}
	if ($stat eq "year") { return $yeartotal; }
	
	$query = $db->prepare("SELECT VISITORS FROM VISITORS;");
	$query->execute;
	my ($vis_a,$visitors);
	while ($vis_a = $query->fetchrow_array) {	$visitors += $vis_a;	}
	
	return $visitors;
}
sub skettiBuildClans
{
my $nick = shift;
my $db = skettiLoadDb();
my $clantxt = "";

my $query = $db->prepare(qq|SELECT CLANS FROM USERS WHERE NICK="$nick";|);
$query->execute;
my @clans = split(/##/,$query->fetchrow_array);
my $clan;
my $i = 1;
foreach $clan (@clans)
{
	$clan =~ s/#//g;
	if ($clan ne "" && defined $clan) {
	my $query = $db->prepare("SELECT LEADER,NAME FROM CLANS WHERE CID=$clan;");
	$query->execute;
	my ($leader,$name) = $query->fetchrow_array;
	my $clan_posts = skettiCount("BASE", qq|FORUM = "$name" AND VISIBLE != 0|);
	my $tr_class = (($i % 2) == 0) ? "even_row" : "odd_row";
	my $post_text = $clan_posts == 1 ? "post" : "posts";
	my $link_name = substr($name,1,length($name));
	$link_name =~ s/ /%20/g;
	if ($leader eq $nick)
	{
		$clantxt .= qq|<tr class="$tr_class"><td><strong><a href="/clans/$link_name/" title="$nick is the Leader of Clan $name">$name</a></strong><br/>(<a href="/clans/$link_name/forum/" class="alt_links_clan">$clan_posts $post_text</a>)</td></tr>|;
	}else{
		$clantxt .= qq|<tr class="$tr_class"><td><a href="/clans/$link_name/" title="Clan $name">$name</a><br/>(<a href="/clans/$link_name/forum/" class="alt_links_clan">$clan_posts $post_text</a>)</td></tr>|;
	}
	$i++;
}
}
if ($clantxt eq "") { $clantxt = "<tr class=\"odd_row\"><td><em>None!</em></td></tr>"; }
return $clantxt;
}
sub skettiBuildBookmarks
{
	my $nick = shift;
	my ($bkm,$bkmrks);
	my $bmtxt = "";
	my $db = skettiLoadDb();
	$query = $db->prepare(qq|SELECT BKMRKS FROM USERS WHERE NICK="$nick"|);
	$query->execute;
	$bkmrks = $query->fetchrow_array;
	my $i = 1;
	if ($query->rows != 0 && defined $bkmrks){
		my @bkmrk = split(/##/,$bkmrks);
		foreach $bkm(@bkmrk){
			my $tr_class = (($i % 2) == 0) ? "even_row" : "odd_row";
			$bkm =~ s/#//g;
			my $type = skettiGrabType($bkm);
			$type =~ tr/[a-z]/[A-Z]/;
			$type .= "S";
			$query = $db->prepare("SELECT TOPIC FROM $type WHERE MID = $bkm;");
			$query->execute;
			my $topic = $query->fetchrow_array;
			my $replies = skettiCount("REPLIES",qq|MID = $bkm|);
			my $reply_text = $replies == 1 ? "reply" : "replies";
			$bmtxt .= qq|<tr class="$tr_class"><td><a href="viewrp.cgi?id=$bkm" title="View Post #$bkm - $topic">$topic</a><br/>($replies $reply_text)</td></tr>|;
			$i++;
		}
	}
	
	if ($bmtxt eq ""){ $bmtxt = "<tr class=\"odd_row\"><td><em>None!</em></td></tr>"; }
	
	return $bmtxt;
}

1;
