#!/usr/bin/perl -w

package SkettiSCRIPT;
use strict;
use sketdb;
use sketsauce;
use sketboard;
use sketusr;
use sketact;
use CGI qw(debug);

my $cgi = new CGI;

my $mode = $cgi->param('mode');
my $msg = $cgi->param('cmessage');

skettiUpdateLa(skettiGrabLogin());


print $cgi->header();
sub skettiSmilies {

	my $db = skettiLoadDb();
	my $text = shift;
	#best way i could think of to try and prevent smilies from overriding each other (get the biggest ones first!)->
	my $query = $db->prepare("SELECT * FROM SMILIES ORDER BY LENGTH(KEYWORD) DESC;");
	$query->execute;
	
	while (my ($keyword,$simage) = $query->fetchrow_array) {
	
		$keyword =~ s/\)/\\)/g;
		$keyword =~ s/\(/\\(/g;
		$keyword =~ s/\?/\\?/g;
		$keyword =~ s/\^/\\^/g;
		$text =~ s/(?!<.*?)($keyword)(?![^<>]*?>)/<img src=\"$simage\" alt=\"$keyword\"\/>/g;
		
	}
	
	return $text;
	
}
sub printMsg
{

	my $db = skettiLoadDb();
	my $chatbox_limit = skettiQuery(qq|SELECT CHATBOX FROM USERS WHERE NICK = "| . skettiGrabLogin() . qq|"|);
	my $query = $db->prepare(qq|SELECT UID,MESSAGE FROM CHATTER ORDER BY MID ASC LIMIT | . (skettiCount("CHATTER",undef) - $chatbox_limit ) . qq|,$chatbox_limit|);
	$query->execute;
	my $messages = $query->fetchall_arrayref();
	for my $message (@{$messages})
	{
	
		my $uid = $message->[0];
		my $message_text = $message->[1];
		
		$query = $db->prepare("SELECT NICK,FONTC FROM USERS WHERE UID = $uid");
		$query->execute;
		my ($nick,$font_color) = $query->fetchrow_array();
		
		my $message_buffer = $message_text =~ m/^\/me / ? qq|<span style="color:$font_color"><em>*$nick | : qq|&lt;<a href="users.cgi?id=$uid" title="View $nick\'s Profile">$nick</a>&gt; <span style="color:$font_color">|;
		
		$message_text = $message_text =~ m/^\/me / ? substr($message_text,4,length($message_text)) : $message_text;
		$message_text =~ s/</&lt;/g;
		$message_text = skettiSmilies($message_text);
		$message_text = saucify($message_text);
		
		$message_buffer .= $message_text . "</span></em><br/>";
		
		print $message_buffer;
		
	}
	exit;
}

if (!defined $mode || $mode eq "get")
{

	printMsg();
	
}elsif ($mode eq "put")
{
	my $db = skettiLoadDb();
	my $uid = skettiQuery(qq|SELECT UID FROM USERS WHERE NICK = "| . skettiGrabLogin() . qq|"|);
	my $message = $msg;
	$message =~ s/\"/&quot;/g;
	my $ip = $ENV{'REMOTE_ADDR'};
	if (defined $message) { my $query = $db->prepare(qq|INSERT INTO CHATTER (UID,TIME,MESSAGE,IP) VALUES ($uid,NOW(),"$message","$ip")|);
	$query->execute; }
	printMsg();
}

exit;
