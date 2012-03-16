#!/usr/bin/perl -w

#### SkettiSCRIPT v1.5                    ####
#### Auth: Jesse Keane                     ####

package SkettiSCRIPT;
use strict;
use sketdb;
use sketusr;
use sketsauce;
use skettime;

my ($query);
my $linick = skettiGrabLogin();
my $theme = skettiGrabTheme();
my $db = skettiLoadDb();

sub skettiRound {
    my $number = shift;
    return int($number + .5);
}

sub skettiSmilies {
	my $text = shift;
	#best way i could think of to try and prevent smilies from overriding each other (get the biggest ones first!)->
	my $query = $db->prepare("SELECT * FROM SMILIES ORDER BY LENGTH(KEYWORD) DESC;");
	$query->execute;
	my ($keyword,$simage);
	while (($keyword,$simage) = $query->fetchrow_array) {
		$keyword =~ s/\)/\\)/g;
		$keyword =~ s/\(/\\(/g;
		$keyword =~ s/\?/\\?/g;
		$keyword =~ s/\^/\\^/g;
		$text =~ s/(?!<.*?)($keyword)(?![^<>]*?>)/<img src=\"$simage\" alt=\"$keyword\"\/>/g;
}
	return $text;
}
sub skettiBuildChat
{
	my $chatbox =<<END;
	
<div id="chatter" class="sketti_chat">
<br/><br/><br/><center><img src="/mattdenum/construction_denum.gif" alt="Loading!"/><br/><em><span style="font-size:18pt">Loading...</span></em></center>
</div>
<form name="cform" action="chatter.cgi" method="post" id="chatform" onSubmit=" var pars = Form.serialize('chatform'); new Ajax.Updater( 'chatter',  'chatter.cgi', { parameters: pars }); clearbox(); return false;">
<input type="hidden" name="mode" value="put"/>
<input type="text" name="cmessage" class="text" value=""/> <input name="post" type="submit" value="say" class="submit"/></form>
END

	return $chatbox;
}
sub skettiBuildPoll
{
	my ($pid,$gy,$pimage,$subdef) = @_;

	$query = $db->prepare("SELECT * FROM POLLS WHERE MID = $pid;");
	$query->execute;
	my ($mid,$pnick,$subject,$topic,$time,$visible,$txt,$opt1,$opt2,$opt3,$opt4,$opt5,$opt1n,$opt2n,$opt3n,$opt4n,$opt5n,$ip,$total,$voters,$views) = $query->fetchrow_array;
	
	if ($gy == 1) { $query = $db->prepare("SELECT MID FROM REPLIES WHERE MID = $mid;"); }else {$query = $db->prepare("SELECT MID FROM REPLIES WHERE OID = $mid;"); }
	$query->execute;
	my $replies = $query->rows;

	$txt =~ s/\r\n/<br\/>/g;
	$txt =~ s/<br\/*>/<br\/>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;/gi;
	$txt = saucify $txt;
	$topic = saucify $topic;
	$opt1 = saucify $opt1;
	$opt2 = saucify $opt2;
	$opt3 = saucify $opt3;
	$opt4 = saucify $opt4;
	$opt5 = saucify $opt5;

	$query = $db->prepare(qq|SELECT UID,NICK,STATUS,URL,FONTC,EMAIL,RNAME,UIN,AVATAR,LVL,TITLE,EXP FROM USERS WHERE NICK = "$pnick";|);
	$query->execute;
	my ($uid,$unick,$stat,$url,$fontc,$email,$rname,$uin,$ava,$lvl,$title,$exp) = $query->fetchrow_array;
	my $postn = skettiCount("POSTS", qq|NICK = "$unick" AND VISIBLE != 0|);
	my $ptext;
	
	if ($lvl < 2 && $stat ne "SkettiOP") {
		$txt =~ s/</&lt;/gi;
		$txt =~ s/^(&lt;)(.*)+br\/*>/<br>/gi;
		$txt =~ s/^(&lt;)(.*)+p>/<p>/gi;
		$txt =~ s/^(&lt;)(.*)+b>/<b>/gi;
		$txt =~ s/^(&lt;)(.*)+\/b>/<\/b>/gi;
		$txt =~ s/^(&lt;)(.*)+font /<font /gi;
		$txt =~ s/^(&lt;)(.*)+a h/<a h/gi;
		$txt =~ s/^(&lt;)(.*)+\/a/<\/a/gi;
		$topic =~ s/</&lt;/g;
		$topic =~ s/>/&gt;/g;
	}
	if (!($voters =~ /\&$linick\&/) || $linick == -1) {
		$ptext = qq|<form action="vote.cgi" method="POST"><p align="center"><input type="hidden" name="id" value="$mid"><table width="95%" cellspacing="0" cellpadding="4">|;
		$ptext .= qq|<tr><td><input type="radio" name="choice" value="1">$opt1</td></tr>\n|;
		if ($opt2 ne "") { $ptext .= qq|<tr><td><input type="radio" name="choice" value="2">$opt2</td></tr>\n|; }
		if ($opt3 ne "") { $ptext .= qq|<tr><td><input type="radio" name="choice" value="3">$opt3</td></tr>\n|; }
		if ($opt4 ne "") { $ptext .= qq|<tr><td><input type="radio" name="choice" value="4">$opt4</td></tr>\n|; }
		if ($opt5 ne "") { $ptext .= qq|<tr><td><input type="radio" name="choice" value="5">$opt5</td></tr>\n|; }
		$ptext .= qq|</table><br/><input type="submit" value="vote" class="submit"/></form></p>|;
	
	}else{
	
		my $po1 = skettiRound ( ($opt1n/$total) * 100 );
		my $po2 = skettiRound ( ($opt2n/$total) * 100 );
		my $po3 = skettiRound ( ($opt3n/$total) * 100 );
		my $po4 = skettiRound ( ($opt4n/$total) * 100 );
		my $po5 = skettiRound ( ($opt5n/$total) * 100 );
		my $to1 = ($po1 * 2);
		my $to2 = ($po2 * 2);
		my $to3 = ($po3 * 2);
		my $to4 = ($po4 * 2);
		my $to5 = ($po5 * 2);
	$query = $db->prepare(qq|SELECT POLLIMAGE FROM THEMES WHERE TITLE = "$theme"|);
	$query->execute;
	my $pimage = $query->fetchrow_array;
		$ptext = qq|<p align="center"><table width="95%" cellspacing="0" cellpadding="4">|;
		$ptext .= qq|<tr><td><strong>$opt1</td><td><img src="$pimage" width="$to1" height="20"/> &nbsp; $opt1n ($po1%)</td></tr>|;
		if ($opt2 ne "") { $ptext .= qq|<tr><td><strong>$opt2</td><td><img src="$pimage" width="$to2" height="20"/> &nbsp; $opt2n ($po2%)</td></tr>|; }
		if ($opt3 ne "") { $ptext .= qq|<tr><td><strong>$opt3</td><td><img src="$pimage" width="$to3" height="20"/> &nbsp; $opt3n ($po3%)</td></tr>|; }
		if ($opt4 ne "") { $ptext .= qq|<tr><td><strong>$opt4</td><td><img src="$pimage" width="$to4" height="20"/> &nbsp; $opt4n ($po4%)</td></tr>|; }
		if ($opt5 ne "") { $ptext .= qq|<tr><td><strong>$opt5</td><td><img src="$pimage" width="$to5" height="20"/> &nbsp; $opt5n ($po5%)</td></tr>|; }
		$ptext .= qq|</table><br/><strong>Total:</strong> $total</p>|;
		
	}
	
	$query = $db->prepare(qq|SELECT POLL FROM THEMES WHERE TITLE = "$theme"|);
	$query->execute;
	my $pf = $query->fetchrow_array;
	my $lnick = $pnick;
	$lnick =~ s/ /%20/gi;
	my $lsubject = $subject;
	$lsubject =~ s/%/%25/g;
	$lsubject =~  s/ /%20/g;
	$query = $db->prepare(qq|SELECT IMG FROM SUBJECTS WHERE NAME="$subject"|);
	$query->execute;
	my $subjecti = $query->fetchrow_array;
	my $li;
	if ($linick != -1) { $li = 1; }else{$li=0;}
		$pf =~ s/!uid/$uid/gi;
		$pf =~ s/!(time[0-6])/skettiTimeForm($time,$1)/egsi;
		$pf =~ s/!nick/$pnick/gi;
		$pf =~ s/!lnick/$lnick/gi;
		$pf =~ s/!views/$views/gi;
		$pf =~ s/!mid/$mid/gi;
		$pf =~ s/!lvl/$lvl/gi;
		$pf =~ s/!title/$title/gi;
		$pf =~ s/!exp/$exp/gi;
		$pf =~ s/!pid/$mid/gi;
		$pf =~ s/!tsubject/$subject/gi;
		$pf =~ s/!lsubject/$lsubject/gi;
		$pf =~ s/!url/$url/gi;
		$pf =~ s/!subject/$subjecti/gi;
		$pf =~ s/!fontc/$fontc/gi;
		if ($ava eq "") { $ava = "ava_ernest.gif"; }
		$pf =~ s/!avatar/$ava/gi;
		$pf =~ s/!topic/$topic/gi;
		if ($li == 1) { $pf =~ s/\<lio\>([^\"]*)\<\/lio\>/$1/gi; }else{ $pf =~ s/\<lio\>([^\"]*)\<\/lio\>//gi; }
		$pf =~ s/!postn/$postn/gi;
		$pf =~ s/!msg/$txt/gi;
		$pf =~ s/!email/$email/gi;
		$pf =~ s/!name/$rname/gi;
		$pf =~ s/!uin/$uin/gi;
		$pf =~ s/!icq/$uin/gi;
		$pf =~ s/!status/$stat/gi;
		$pf =~ s/!rname/$rname/gi;
		$pf =~ s/!message/$txt/gi;
		$pf =~ s/!poll/$ptext/gi;
		$pf =~ s/!replies/$replies/gi;
		return $pf;
}
sub skettiBuildPost
{
	my ($pid,$gy,$trunc,$subdef,$key) = @_;
	$query = $db->prepare(qq|SELECT * FROM POSTS WHERE MID = $pid|);
	$query->execute;
	my $post_info = $query->fetchrow_hashref;
	$$post_info{'RAT'} = saucify $$post_info{'RAT'};
	$$post_info{'QUOTEE'} = saucify $$post_info{'QUOTEE'};
	
	my $replies = $gy == 1 ? skettiCount("REPLIES",qq|MID = $pid|) : skettiCount("REPLIES",qq|OID = $pid|);
	
	$$post_info{'MSG'} = "&nbsp;" x 5 . $$post_info{'MSG'};
	if (!defined $$post_info{'SMILIE'}) { $$post_info{'SMILIE'} = 0; }
	if ($$post_info{'SMILIE'} != 0) { $$post_info{'MSG'} = skettiSmilies($$post_info{'MSG'}); }
	$$post_info{'MSG'} =~ s/\r\n/<br\/>/g;
	$$post_info{'MSG'} =~ s/<br(\/)*>/<br\/>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;/gi;
	$$post_info{'MSG'} = saucify $$post_info{'MSG'};
	my ($new_post, $new_replies) = "";
	
	if (skettiGrabLogin() != -1 && ($$post_info{'LASTR'} > skettiGrabLLI(skettiGrabLogin())))
	{
		if ($replies > 0) { $new_replies = "<strong><sup>!!</sup></strong>"; }
		else { $new_post = "<strong><sup>!!</sup></strong>"; }
	}

# time0 = Short_day Short_month Date Long_time Year
# time1 = Long_day, Long_Month Year (Short_time)
# time2 = Long_time (Numeral_month/Numeral_day/Year)
# time3 = Long_day, Short_month Date @Short_time
# time4 = Long_day, Short_month Date @Long_time
# time5 = Short_month/Date/Year @Long_time
# time6 = Short_month/Date/Year @Short_time

	$query = $db->prepare(qq|SELECT UID,STATUS,URL,FONTC,EMAIL,RNAME,UIN,AVATAR,LVL,TITLE,EXP FROM USERS WHERE NICK = "$$post_info{'NICK'}"|);
	$query->execute;
	my $user_info = $query->fetchrow_hashref;
	
	my $postn = skettiCount("POSTS",qq|NICK = "$$post_info{'NICK'}" AND VISIBLE != 0|);

			if ($$user_info{'LVL'} < 2 && $$user_info{'STATUS'} ne "SkettiOP" && !(skettiIsOp($$post_info{'NICK'},$$post_info{'SUBJECT'}))) {
			$$post_info{'MSG'} =~ s/</&lt;/g;
			$$post_info{'MSG'} =~ s/&lt;br(\/)*>/<br\/>/gi;
			$$post_info{'MSG'} =~ s/&lt;+p>/<p>/gi;
			$$post_info{'MSG'} =~ s/&lt;b>/<b>/gi;
			$$post_info{'MSG'} =~ s/&lt;\/b>/<\/b>/gi;
			$$post_info{'MSG'} =~ s/&lt;font /<font /gi;
			$$post_info{'MSG'} =~ s/&lt;\/font>/<\/font>/gi;
			$$post_info{'MSG'} =~ s/&lt;a h/<a h/gi;
			$$post_info{'MSG'} =~ s/^&lt;\/a/<\/a/gi;
			
			$$post_info{'TOPIC'} =~ s/</&lt;/g;
			$$post_info{'QUOTE'} =~ s/</&lt;/g;
			$$post_info{'QUOTEE'} =~ s/</&lt;/g;
		}
		if (defined $key) {
			$$post_info{'MSG'} =~ s/(?!<.*?)($key)(?![^<>]*?>)/<span style=\"background-color:#FFE600;color:#000000;font-weight:bold;\">$1<\/span>/gi;
			$$post_info{'TOPIC'} =~ s/(?!<.*?)($key)(?![^<>]*?>)/<span style=\"background-color:#FFE600;color:#000000;font-weight:bold;\">$1<\/span>/gi;
			$$post_info{'QUOTE'} =~ s/(?!<.*?)($key)(?![^<>]*?>)/<span style=\"background-color:#FFE600;color:#000000;font-weight:bold;\">$1<\/span>/gi;
			$$post_info{'QUOTEE'} =~ s/(?!<.*?)($key)(?![^<>]*?>)/<span style=\"background-color:#FFE600;color:#000000;font-weight:bold;\">$1<\/span>/gi;
			}
if (length($$post_info{'MSG'}) > $trunc) { $$post_info{'MSG'} = substr($$post_info{'MSG'},0,$trunc) . "</a>..\<a href=\"viewrp.cgi?id=$pid\"\>Read More<\/a>\n"; }
	my $link_nick = $$post_info{'NICK'};
	my $logged_in;
	if ($linick == -1) { $logged_in = 0; }else{ $logged_in = 1; }
	$link_nick =~ s/ /%20/gi;
	$query = $db->prepare(qq|SELECT IMG FROM SUBJECTS WHERE NAME="$$post_info{'SUBJECT'}"|);
	$query->execute;
	my $subject_image = $query->fetchrow_array;
	$query = $db->prepare(qq|SELECT POST FROM THEMES WHERE TITLE="$theme"|);
	$query->execute;
	if (!defined $$post_info{'RAT'}) { $$post_info{'RAT'} = ""; }
	if ($$user_info{'AVATAR'} eq "" || !defined $$user_info{'AVATAR'}) { $$user_info{'AVATAR'} = "ava_ernest.gif"; }
	if ($$post_info{'QUOTEE'} eq "") { $$post_info{'QUOTEE'} = "Anonymous"; }
	my $link_subject = $$post_info{'SUBJECT'};
	$link_subject =~ s/%/%25/g;
	$link_subject =~  s/ /%20/g;
	my $mf = $query->fetchrow_array;
		$mf =~ s/!uid/$$user_info{'UID'}/gi;
		$mf =~ s/!(time[0-6])/skettiTimeForm($$post_info{'TIME'},$1)/egsi;
		$mf =~ s/!nick/$$post_info{'NICK'}/gi;
		$mf =~ s/!lnick/$link_nick/gi;
		$mf =~ s/!rating/$$post_info{'RAT'}/gi;
		$mf =~ s/!views/$$post_info{'VIEWS'}/gi;
		$mf =~ s/!score/$$post_info{'SCORE'}/gi;
		$mf =~ s/!mid/$pid/gi;
		$mf =~ s/!lvl/$$user_info{'LVL'}/gi;
		$mf =~ s/!title/$$user_info{'TITLE'}/gi;
		$mf =~ s/!exp/$$user_info{'EXP'}/gi;
		$mf =~ s/!pid/$pid/gi;
		$mf =~ s/!tsubject/$$post_info{'SUBJECT'}/gi;
		$mf =~ s/!url/$$user_info{'URL'}/gi;
		$mf =~ s/!subject/$subject_image/gi;
		$mf =~ s/!lsubject/$link_subject/gi;
		$mf =~ s/!fontc/$$user_info{'FONTC'}/gi;
		$mf =~ s/!avatar/$$user_info{'AVATAR'}/gi;
		$mf =~ s/!topic/$$post_info{'TOPIC'}$new_post/gi;
		$mf =~ s/!postn/$postn/gi;
		$mf =~ s/!msg/$$post_info{'MSG'}/gi;
		$mf =~ s/!email/$$user_info{'EMAIL'}/gi;
		$mf =~ s/!name/$$user_info{'RNAME'}/gi;
		$mf =~ s/!uin/$$user_info{'UIN'}/gi;
		if ($logged_in == 1) { $mf =~ s/\<lio\>(.*?)\<\/lio\>/$1/gis; }else{ $mf =~ s/\<lio\>(.*?)\<\/lio\>//gis; }
		$mf =~ s/!icq/$$user_info{'UIN'}/gi;
		$mf =~ s/!status/$$user_info{'STATUS'}/gi;
		$mf =~ s/!rname/$$user_info{'RNAME'}/gi;
		$mf =~ s/!message/$$post_info{'MSG'}/gi;
		if ($$post_info{'QUOTE'} eq "") {
			$mf =~ s/!quote//gi;
			$mf =~ s/!pquotee//gi;
		}else{
		$mf =~ s/!quote/<em>&quot;$$post_info{'QUOTE'}&quot;<\/em>/gi;
		$mf =~ s/!pquotee/--$$post_info{'QUOTEE'}/gi;
		}
		$mf =~ s/!replies/$replies$new_replies/gi;
		return $mf;
}
sub skettiBuildReply
{
	my ($pid,$rid,$key,$logged_in) = @_;
	my $pid_column = $pid != -2 ? "MID" : "OID";
	
	my $db = skettiLoadDb();
	my $query = $db->prepare(qq|SELECT * FROM REPLIES WHERE $pid_column = $pid AND RID = $rid|);
	$query->execute;
	my $reply_info = $query->fetchrow_hashref;
	
	if (!defined $$reply_info{'RATE_SCORE'}){
	
		$$reply_info{'RATE_SCORE'} = 0;
		$$reply_info{'RATE'} = "Not Rated";
	}
	if (!defined $$reply_info{'QUOTEE'} || $$reply_info{'QUOTEE'} eq ""){
	
		$$reply_info{'QUOTEE'} = "Anonymous";
		
	}
	
	my $link_nick = $$reply_info{'NICK'};
	$link_nick =~ s/ /%20/gi;
	
	$$reply_info{'MSG'} =~ s/\r\n/<br\/>/gi;
	$$reply_info{'MSG'} = "&nbsp;" x 5 . $$reply_info{'MSG'};
	$$reply_info{'MSG'} =~ s/<br\/*>/<br\/>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;/gi;
	
	if ($$reply_info{'SMILIES'} != 0) { $$reply_info{'MSG'} = skettiSmilies($$reply_info{'MSG'}); }
	
	$$reply_info{'MSG'} = saucify $$reply_info{'MSG'};
	$$reply_info{'QUOTE'} = saucify $$reply_info{'QUOTE'};
	$$reply_info{'QUOTEE'} = saucify $$reply_info{'QUOTEE'};

	$query = $db->prepare(qq|SELECT UID,STATUS,URL,FONTC,RNAME,AVATAR,EXP,TITLE,LVL FROM USERS WHERE NICK = "$$reply_info{'NICK'}"|);
	$query->execute;
	my $user_info = $query->fetchrow_hashref;
	
	$$user_info{'AVATAR'} = (!defined $$user_info{'AVATAR'} || $$user_info{'AVATAR'} eq "") ? "ava_ernest.gif" : $$user_info{'AVATAR'};
	
	my $postn = skettiCount("POSTS",qq|NICK = "$$reply_info{'NICK'}" AND VISIBLE != 0|);
	
	my $query = $db->prepare("SELECT REPLY FROM THEMES WHERE TITLE='$theme';");
	$query->execute;
	my $rtq = $query->fetchrow_array;
	
		if ($$user_info{'LVL'} < 2 && $$user_info{'STATUS'} ne "SkettiOP"){
			$$reply_info{'MSG'} =~ s/</&lt;/gi;
			$$reply_info{'MSG'} =~ s/&lt;b/<b/gi;
			$$reply_info{'MSG'} =~ s/&lt;\/b/<\/b/gi;
			$$reply_info{'MSG'} =~ s/&lt;a h/<a h/gi;
			$$reply_info{'MSG'} =~ s/&lt;\/a/<\/a/gi;
			$$reply_info{'MSG'} =~ s/&lt;img/<img/gi;
			$$reply_info{'QUOTE'} =~ s/</&lt;/gi;
			$$reply_info{'QUOTEE'} =~ s/</&lt;/gi;
			$$reply_info{'MSG'} =~ s/&lt;pull_quote/<pull_quote/gi;
			$$reply_info{'MSG'} =~ s/&lt;\/pull_quot/<\/pull_quot/gi;
		}
		
		if (defined $key) {
		
			$$reply_info{'MSG'} =~ s/(?!<.*?)($key)(?![^<>]*?>)/<span style=\"background-color:#FFE600;color:#000000;font-weight:bold;\">$1<\/span>/gi;
			$$reply_info{'QUOTE'} =~ s/(?!<.*?)($key)(?![^<>]*?>)/<span style=\"background-color:#FFE600;color:#000000;font-weight:bold;\">$1<\/span>/gi;
			$$reply_info{'QUOTEE'} =~ s/(?!<.*?)($key)(?![^<>]*?>)/<span style=\"background-color:#FFE600;color:#000000;font-weight:bold;\">$1<\/span>/gi;
			
		}
		
	my ($rtitle,$rep_fontc,$rep_fontc_end) = "";
	
	if (defined $$reply_info{'QUOTE_REP'}){
	
		$query = $db->prepare(qq|SELECT FONTC,AVATAR,UID FROM USERS WHERE NICK = "$$reply_info{'QUOTE_REP'}"|);
		$query->execute;
		my ($font_color,$avatar,$uid) = $query->fetchrow_array;
		$rep_fontc = "<span style=\"color:$font_color !important\">";
		$avatar = defined $avatar && $avatar ne "" ? $avatar : "ava_ernest.gif";
		$rep_fontc_end = "<\/span>";
		
		$rtitle = qq|<legend><span class="sketti_quote"><a href="users.cgi?id=$uid"><img src="$avatar" width="30" height="35" border="0" alt="$$reply_info{'QUOTE_REP'}" style="vertical-align:middle"/></a><span style="display:inline;vertical-align:middle">&nbsp;&nbsp;<strong>$$reply_info{'QUOTE_REP'} said:</strong></span></span></legend>\n|; }
		
		if ($logged_in == 1){
		
			$rtq =~ s/\<lio\>(.*?)\<\/lio\>/$1/gis;
			
		}else{
		
			$rtq =~ s/\<lio\>(.*?)\<\/lio\>//gis;
			
		}
		
		$$reply_info{'MSG'} =~ s/<pull_quote>/<fieldset class=\"rep_quote\">$rtitle$rep_fontc\n<br\/>/gi;
		$$reply_info{'MSG'} =~ s/<\/pull_quote>/$rep_fontc_end<\/fieldset>/gi;
		
		$rtq =~ s/!uid/$$user_info{'UID'}/gi;
		$rtq =~ s/!(time[0-6])/skettiTimeForm($$reply_info{'TIME'},$1)/egi;
		$rtq =~ s/!topic//gi;
		$rtq =~ s/!nick/$$reply_info{'NICK'}/gi;
		$rtq =~ s/!lnick/$link_nick/gi;
		$rtq =~ s/!rname/$$user_info{'RNAME'}/gi;
		$rtq =~ s/!mid/$pid/gi;
		$rtq =~ s/!pid/$rid/gi;
		$rtq =~ s/!url/$$user_info{'URL'}/gi;
		$rtq =~ s/!name/$$user_info{'RNAME'}/gi;
		$rtq =~ s/!exp/$$user_info{'EXP'}/gi;
		$rtq =~ s/!title/$$user_info{'TITLE'}/gi;
		$rtq =~ s/!lvl/$$user_info{'LVL'}/gi;
		$rtq =~ s/!avatar/$$user_info{'AVATAR'}/gi;
		$rtq =~ s/!postn/$postn/gi;
		$rtq =~ s/!fontc/$$user_info{'FONTC'}/gi;
		$rtq =~ s/!rating/$$reply_info{'RATE'}/gi;
		$rtq =~ s/!rate_score/$$reply_info{'RATE_SCORE'}/gi;
		$rtq =~ s/!msg/$$reply_info{'MSG'}/gi;
		$rtq =~ s/!status/$$user_info{'STATUS'}/gi;
		$rtq =~ s/!message/$$reply_info{'MSG'}/gi;
		
		if ($$reply_info{'QUOTE'} eq "" || !defined $$reply_info{'QUOTE'}) {
		
			$rtq =~ s/!quote//gi;
			$rtq =~ s/!pquotee//gi;
			
		}else{
		
			$rtq =~ s/!quote/<em>&quot;$$reply_info{'QUOTE'}&quot;<\/em>/gi;
			$rtq =~ s/!pquotee/--$$reply_info{'QUOTEE'}/gi;
			
		}
		
		return $rtq;
}
1;
