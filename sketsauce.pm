#!/usr/bin/perl -w

package SkettiSCRIPT;
use strict;
use sketdb;
use sketusr;

sub saucedef
{
	my $mode = shift;
	my $text = shift;
	my $db = skettiLoadDb();
	my $nick = skettiGrabLogin();
	if ($nick != -1)
	{
		my $query = $db->prepare(qq|SELECT SAUCEDEF FROM USERS WHERE NICK="$nick"|);
		$query->execute;
		$mode = $query->fetchrow_array;
	}
		
	my $text2 = "";
	if ($text =~ /\|/) { ($text,$text2) = split(/\|/,$text); }
	my $txtlink = $text;
	my $txtin="";
	my $preurl = "sauce.cgi";
	if ($mode eq "short") { $preurl = "qsauce.cgi"; }
	my $rdef = $text;
	my $disp;
	if ($text2 ne "") { $disp = $text2; } else { $disp = $text; }
		if ($rdef =~ /\@/)
		{
			($txtin,$preurl) = split(/\@/,$rdef);
			if ($preurl ne "" && $mode ne "short") { $preurl .= "/sauce.cgi"; }
			elsif ($preurl ne "" && $mode eq "short") { $preurl .= "/qsauce.cgi"; }
			$txtlink = $txtin;
		}
		$txtlink =~ s/ /+/gi;
	if ($mode ne "short")
	{
		return qq|<a href="$preurl?def=$txtlink" title="Saucedef: $disp" class="sauce_def">$disp<\/a>|;
	}else{
		return qq|<a href=""  title="Saucedef: $disp" class="sauce_def" onClick="javascript:window.open('$preurl?def=$txtlink','saucedef: $disp','width=340,scrollbars=yes,location=no,height=340,screenX=200,screenY=200');return false;\">$disp<\/a>|;
	}
}

sub saucify
{
	my $txt = shift;
	my $mode = shift;
	if (!defined $mode) { $mode = "short"; }
	$txt =~ s/\[(.*?)\]/saucedef($mode,$1)/egs;
	return $txt;
	#fuck
}
1;
