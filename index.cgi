#!/usr/bin/perl -w

#SkettiSCRIPT v1.5
#All code by Jesse Keane

package SkettiSCRIPT;
use strict;
use sketdb;
use sketusr;
use sketact;
use sketsauce;
use sketbase;
use sketpriv;
use sketlinks;
use sketusrs;
use CGI qw(debug);
use POSIX;

my $cgi = new CGI;
my $forum = defined $cgi->param('forum') ? $cgi->param('forum') : $cgi->cookie('forum');
my $grave_yard = $cgi->param('gy');
my $page = $cgi->param('pg');

if (!defined $page) { $page = 1; }
if (!defined $grave_yard) { $grave_yard = 0; }

my $db = skettiLoadDb();
my $query;

$forum =~ s/^%25/%/g;

if (!defined $cgi->cookie('forum') || (defined $cgi->param('forum') && $cgi->param('forum') ne $cgi->cookie('forum')))
{

	if ((defined $forum && $forum ne "*") && skettiCount("SUBJECTS",qq|NAME = "$forum"|) == 0){
		
		skettiStartBoard("Error!");
		print "No such forum: $forum. Please, <a href=\"/\">go back</a>";
		skettiEndBoard();
			
	}
	
	my $forum_cookie = $cgi->cookie(-name=>'forum', -value=> $cgi->param('forum'), -expires=>'+1y');
	print $cgi->header(-cookie=>$forum_cookie);

}else{

	print $cgi->header();

}

if ($forum eq "*"){ $forum = undef; }

skettiUpdateVisitors();
	
my $forum_image = defined $forum ? skettiQuery (qq|SELECT IMG FROM SUBJECTS WHERE NAME = "$forum"|) : "default_icon.png";

my ($nick,$li,$uid,$status,$fontc,$rname,$sb,$ppp,$dt,$trunc,$title,$exp,$lvl,$ln,$ban,$pmd,$privs,$theme);

$nick = skettiGrabLogin();

skettiUpdateLITable(skettiGetTA());

if ($nick == -1) {
	$li = 0;
	$ln = 5;
	$theme = skettiGrabTheme();
	$sb = "default";
	$ppp = 10;
} else {
	$li = 1;
	skettiUpdateLa($nick);
	$query = $db->prepare(qq|SELECT UID,STATUS,FONTC,RNAME,SB,MPP,DT,TRUNC,EXP,TITLE,LVL,BAN,LN,PMD,THEME FROM USERS WHERE NICK = "$nick";|);
	$query->execute;
	($uid,$status,$fontc,$rname,$sb,$ppp,$dt,$trunc,$exp,$title,$lvl,$ban,$ln,$pmd,$theme) = $query->fetchrow_array;
	$sb =~ s/ /_/gi;
}
my $motd;
open (MOTD, "sketti.motd");
while (<MOTD>){	$motd .= "\n$_";}
close(MOTD);
$motd =~ s/\r\n/<br\/>/g;
$motd = saucify $motd;

my $lnick = $nick;
$lnick =~ s/ /%20/gi;

my $post_number;
	
	if (defined $forum){

		$post_number = skettiCount("BASE",qq|FORUM = "$forum"|);
		
	}elsif (!defined $forum && $grave_yard == 0){
	
		$post_number = skettiCount("POSTS",qq|VISIBLE != 0|);;
		
	} elsif (!defined $forum && $grave_yard == 1){
	
		$post_number = skettiCount("POSTS",qq|VISIBLE = 0|);
		
	}
	
	my $pages = ($post_number / $ppp);
	$pages = ceil($pages);
	
	my $pages_text = qq(<select name="pg">);
	my $i = 1;
	while ($i <= $pages){
	
			$pages_text .= $i == $page ? qq(<option selected value="$i">$i</option>) : qq(<option value="$i">$i</option>);
		
		$i++;
		
	}
	$pages_text .= qq(</select>);
	
	$query = $db->prepare("SELECT NAME FROM SUBJECTS ORDER BY NAME DESC");
	$query->execute;
	
	my $forum_text = qq|<select name="forum" onChange="form.submit()"><option value="*">Sketti.net</option>|;
	my $sub_names;
	
	while ($sub_names = $query->fetchrow_array)
	{
	
		my $sub_display = length($sub_names) > 10 ? substr($sub_names,0,10) . ".." : $sub_names;
		
			$forum_text .= defined $forum && $sub_names eq $forum ? qq|<option selected value="$sub_names">$sub_display</option>| : qq|<option value="$sub_names">$sub_display</option>|;
		
	}
	
	$forum_text .= qq|</select>|;
	
	$query = $db->prepare("SELECT MAIN FROM THEMES WHERE TITLE='$theme';");
	$query->execute;
	my $sr = $query->fetchrow_array;
	
	if (!defined $forum)
	{
	
		$sr =~ s/<sub_forum>(.*?)<\/sub_forum>//gis;
		
	} else {
	
		$sr =~ s/<sub_forum>(.*?)<\/sub_forum>/$1/gis;
		
	}
	
	if ($li == 1)
	{
		if ($status ne "SkettiOP" && $lvl < 8) {
		
			$sr =~ s/\<mods\>(.*?)\<\/mods\>//gi;
			
		} elsif ($status eq "SkettiOP" || $lvl >= 8){
		
			$sr =~ s/\<mods\>(.*?)\<\/mods\>/$1/gis;
			
		}
		
		$sr =~ s/\<lio\>(.*?)\<\/lio\>/$1/gis;
		$sr =~ s/\^fontc/$fontc/gi;
		$sr =~ s/\^uid/$uid/gi;
		$sr =~ s/\^rname/$rname/gi;
		$sr =~ s/\^nick/$nick/gi;
		$sr =~ s/\^lnick/$lnick/gi;
		$sr =~ s/\^status/$status/gi;
		$sr =~ s/\^exp/$exp/gi;
		$sr =~ s/\^lvl/$lvl/gi;
		$sr =~ s/\^title/$title/gi;
		$sr =~ s/\^bookmarks/skettiBuildBookmarks($nick)/egi;
		$sr =~ s/\^clans/skettiBuildClans($nick)/egi;
		$sr =~ s/!priv/skettiBuildPrivs($nick,$pmd)/egi;
		$sr =~ s/!chatbox/skettiBuildChat()/egi;
		$sr =~ s/\^login/Logged in as: $nick/gi;
		$sr =~ s/\<nli\>(.*?)\<\/nli\>//gis;
	
	}else{
	
		$sr =~ s/\<lio\>(.*?)\<\/lio\>//gis;
		$sr =~ s/\<nli\>(.*?)\<\/nli\>/$1/gis;
		$sr =~ s/\<mods\>(.*?)\<\/mods\>//gis;
		$sr =~ s/!priv//gi;
		$sr =~ s/\^clans//gi;
		$sr =~ s/\^bookmarks//gi;
		$sr =~ s/\^fontc//gi;
		$sr =~ s/\^uid//gi;
		$sr =~ s/\^rname//gi;
		$sr =~ s/\^nick//gi;
		$sr =~ s/\^lnick//gi;
		$sr =~ s/\^status//gi;
		$sr =~ s/\^exp//gi;
		$sr =~ s/\^lvl//gi;
		$sr =~ s/\^title//gi;
		$sr =~ s/\^login/<form method=\"POST\" action=\"login.cgi\"><table border=\"0\"><tr><td><strong>Nickname:<\/strong><\/td><td><input type=\"text\" name=\"nick\" class=\"text\"\/><\/td><\/tr><tr><td><strong>Password:<\/strong><\/td><td><input type=\"password\" name=\"pass\" class=\"text\"\/><\/td><\/tr><tr><td colspan=\"2\"><center><input type=\"submit\" value=\"login\" class=\"submit\"\/><\/center><\/td><\/tr><\/table><\/form>/gi;

	}

	$sr =~ s/!gobutton/<input type=\"submit\" value=\"go\" class=\"submit\"\/>/gi;
	$sr =~ s/!form/<form method=\"GET\" action=\"\/sbase.cgi\">/gi;
	$sr =~ s/!board/skettiBuildBase($dt,$ppp,$sb,$trunc,!$grave_yard,$forum,$page)/egi;
	$sr =~ s/!counter/skettiGrabVisitors('all')/egi;
	$sr =~ s/!mcounter/skettiGrabVisitors('month')/egi;
	$sr =~ s/!ycounter/skettiGrabVisitors('year')/egi;
	$sr =~ s/!users/skettiBuildUsers()/egi;
	$sr =~ s/!links/skettiBuildLinks($ln)/egi;
	$sr =~ s/!postnum/skettiCount("POSTS",qq|VISIBLE != 0|)/egi;
	$sr =~ s/!linknum/skettiCount("LINKS",undef)/egi;
	$sr =~ s/!replynum/skettiCount("REPLIES",qq|MID > -2|)/egi;
	$sr =~ s/!pollnum/skettiCount("POLLS",qq|VISIBLE != 0|)/gi;
	$sr =~ s/!totalnum/skettiCount("POLLS",qq|VISIBLE != 0|) + skettiCount("REPLIES",qq|MID > -2|) + skettiCount("LINKS",undef) + skettiCount("POSTS",qq|VISIBLE != 0|) + skettiCount("SAUCE",undef) + skettiCount("SAUCER",undef)/egi;
	$sr =~ s/!delposts/skettiCount("POSTS",qq|VISIBLE = 0|)/egi;
	$sr =~ s/!forums/$forum_text/gi;
	$sr =~ s/!delrps/skettiCount("REPLIES",qq|MID = -2|)/egi;
	$sr =~ s/\@forum/$forum/gi;
	$sr =~ s/\@page/$page/gi;
	$sr =~ s/\@icon/$forum_image/gi;
	$sr =~ s/!delpolls/skettiCount("POLLS",qq|VISIBLE = 0|)/egi;
	$sr =~ s/!saucenum/skettiCount("SAUCE",undef)/egi;
	$sr =~ s/!xtranum/skettiCount("SAUCER",undef)/egi;
	$sr =~ s/!totaldel/skettiCount("POLLS",qq|VISIBLE = 0|) + skettiCount("POSTS",qq|VISIBLE = 0|) + skettiCount("REPLIES",qq|MID = -2|)/egi;
	$sr =~ s/!usernum/skettiCount("USERS",undef)/egi;
	$sr =~ s/!motd/$motd/gi;
	$sr =~ s/!pages/$pages_text/gi;
	$sr =~ s/!stime/localtime/egi;
	
	print $sr;
	
exit;
