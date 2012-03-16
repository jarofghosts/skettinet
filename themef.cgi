#!/usr/bin/perl -w

package SkettiSCRIPT;
use CGI;
use sketdb;
use sketact;
use sketusr;
use sketboard;
use sketziggy;
use sketlog;

#skettiStartBoard();

my $upld = new CGI;
print $upld->header();
#skettiStartBoardNoHead("New Theme");
my $db = skettiLoadDb();

my $mode = $upld->param('mode');
my $bg = "";
my $query;

my $nickn = skettiGrabLogin();
if ($nickn != -1) { 
	skettiUpdateLa($nickn);
	$query = $db->prepare("SELECT FONTC FROM USERS WHERE NICK = '$nickn';");
	$query->execute;
	$bg = $query->fetchrow_array;
}

if ($mode eq "get" || $mode eq "")
{
	print <<END;

<form method="POST" enctype="multipart/form-data" action="themef.cgi">
<input type="hidden" name="mode" value="save">
<table border=0 cellspacing=0 cellpadding=10>
END
if ($nickn == -1)
{
	print <<END;
	<tr><td><strong><u>Nickname:</u></strong></td><td><input type="text" name="nick" class="text"/></td></tr>
	<tr><td><strong><u>Password:</u></strong></td><td><input type="password" name="pass" class="text"/></td></tr>
END
}else{
	my $npass = skettiGrabPass($nickn);
	print <<END;
	<tr><td bgcolor="$bg"><strong><u>Nickname:</u></strong></td><td>$nickn</td></tr>
	<input type="hidden" name="nick" value="$nickn">
	<input type="hidden" name="pass" value="$npass">
END
}

print <<END;
<tr><td bgcolor="$bg"><strong><u>Title:</u></strong></td><td><input type="text" name="title" class="text"/></td></tr>
<tr><td bgcolor="$bg"><strong><u>Index File:</u></strong></td><td><input type="file" name="index" class="text"/></td></tr>
<tr><td bgcolor="$bg"><strong><u>Top File:</u></strong></td><td><input type="file" name="top" class="text"/></td></tr>
<tr><td bgcolor="$bg"><strong><u>Bottom File:</u></strong></td><td><input type="file" name="bottom" class="text"/></td></tr>
<tr><td bgcolor="$bg"><strong><u>Post File:</u></strong></td><td><input type="file" name="post" class="text"/></td></tr>
<tr><td bgcolor="$bg"><strong><u>Reply File:</u></strong></td><td><input type="file" name="reply" class="text"/></td></tr>
<tr><td bgcolor="$bg"><strong><u>Poll File:</u></strong></td><td><input type="file" name="poll" class="text"/></td></tr>
<tr><td bgcolor="$bg"><strong><u>Poll Image File:</u></strong></td><td><input type="file" name="pollimg" class="text"/></td></tr></table>
<center><input type="submit" value="save"></form>

END

	skettiEndBoard();
}elsif ($mode eq "save")
{
	my $upload_dir = "pub/tmp";

	my $nick = $upld->param('nick');
	my $pass = $upld->param('pass');
	my $title = $upld->param('title');
	my $indx = $upld->param('index');
	my $topf = $upld->param('top');
	my $botf = $upld->param('bottom');
	my $postf = $upld->param('post');
	my $repf = $upld->param('reply');
	my $pollf = $upld->param('poll');
	my $pimgf = $upld->param('pollimg');

	$indx =~ s/.*[\/\\](.*)/$1/gi;
	$topf =~ s/.*[\/\\](.*)/$1/gi;
	$botf =~ s/.*[\/\\](.*)/$1/gi;
	$postf =~ s/.*[\/\\](.*)/$1/gi;
	$repf =~ s/.*[\/\\](.*)/$1/gi;
	$pollf =~ s/.*[\/\\](.*)/$1/gi;
	$pimgf =~ s/.*[\/\\](.*)/$1/gi;

	my $indexf = $upld->upload("index");
	my $topfile = $upld->upload("top");
	my $botfile = $upld->upload("bottom");
	my $pfile = $upld->upload("post");
	my $repfile = $upld->upload("reply");
	my $pollfile = $upld->upload("poll");
	my $pifile = $upld->upload("pollimg");

	$title =~ s/'/\\'/gi;
	if ($nick eq "" || $pass eq "" || $title eq "")
	{
		print <<END;

Umm.. you are missing some stuff for your theme there.. you should probably <a href="themef.cgi?mode=get">go back</a> and fill it in.

END
	skettiEndBoard();
}
	$query = $db->prepare("SELECT AUTHOR FROM THEMES WHERE TITLE = '$title';");
	$query->execute;
		if ($query->rows != 0){
			print <<END;

Whoa, whoa, whoa!<br/>
Simmer down now, someone has already created a theme with that title, sorry.<br/>
Why don't you try a <a href="themef.cgi?mode=get">different one</a>?

END
	skettiEndBoard();
}
	$query = $db->prepare("SELECT PASS,BAN FROM USERS WHERE NICK = '$nick';");
	$query->execute;
	my $test = $query->rows;
	if ($test == 0)
	{
		print <<END;

SRRY!<br/><br/>You must <a href="register.cgi?mode=get">register</a> first.

END
	skettiEndBoard();
}
	my @info = $query->fetchrow_array;
	my ($upass,$ban) = @info;
	if ($ban == 1) {
		print "You have been BANISHED!  Do not attempt to return here.\n";
		skettiEndBoard();
	}
	if ($upass ne $pass)
	{
		print <<END;
WRONG PASSWORD  <a href="themef.cgi?mode=get">try again</a>

END
	skettiEndBoard();
}
	my ($indl,$postl,$repl,$polll,$chanl,$topl,$botl);
	open(INDEX,">/sketti/pub/tmp/index.sr");
	while ( <$indexf> )
	{
		print INDEX;
	}
	close(INDEX);
	
	open(TOP,">/sketti/pub/tmp/top.tf");
	while ( <$topfile> )
	{
		print TOP;
	}
	close(TOP);
	open(BOT,">/sketti/pub/tmp/bot.bf");
	while ( <$botfile> )
	{
		print BOT;
	}
	close(BOT);
	open(POLL,">/sketti/pub/tmp/poll.pof");
	while ( <$pollfile> )
	{
		print POLL;
	}
	close(POLL);
	open(POST,">/sketti/pub/tmp/post.pf");
	while ( <$pfile> )
	{
		print POST;
	}
	close(POST);
	open (PIMAG, ">/sketti/pub/$pimgf");
	while ( <$pifile> )
	{
		print PIMAG;
	}
	close (PIMAG);
	open(REP,">/sketti/pub/tmp/rep.rf");
	while ( <$repfile> )
	{
		print REP;
	}
	close(REP);
	
	open(INDEX,"/sketti/pub/tmp/index.sr");
	while ( <INDEX> )
	{
		$indl .= $_;
	}
	close(INDEX);
	
	open(TOP,"/sketti/pub/tmp/top.tf");
	while ( <TOP> )
	{
		$topl .= $_;
	}
	close(TOP);
	open(BOT,"/sketti/pub/tmp/bot.bf");
	while ( <BOT> )
	{
		$botl .= $_;
	}
	close(BOT);
	open(POLL,"/sketti/pub/tmp/poll.pof");
	while ( <POLL> )
	{
		$polll .= $_;
	}
	close(POLL);
	open(POST,"/sketti/pub/tmp/post.pf");
	while ( <POST> )
	{
		$postl .= $_;
	}
	close(POST);

	open(REP,"/sketti/pub/tmp/rep.rf");
	while ( <REP> )
	{
		$repl .= $_;
	}
	close(REP);
	$query = $db->prepare("SELECT TID FROM THEMES;");
	$query->execute;
	my $tid = $query->rows;
	my $time = localtime;
	my $ip = $ENV{'REMOTE_ADDR'};
	$time =~ s/  / /gi;
	skettiUpdateLvl($nick,5);
	skettiSendZiggyMsg ($nick, "Since you created &quot;$title&quot;, you've gained 5 EXP!");
	$indl =~ s/'/\\'/gi;
	$topl =~ s/'/\\'/gi;
	$botl =~ s/'/\\'/gi;
	$postl =~ s/'/\\'/gi;
	$repl =~ s/'/\\'/gi;
	$polll =~ s/'/\\'/gi;
	$chanl =~ s/'/\\'/gi;
	$pimgf =~ s/'/\\'/gi;
	skettiQuery ("INSERT INTO THEMES (TID,AUTHOR,TITLE,LUP,MAIN,TOP,BOTTOM,POST,REPLY,POLL,POLLIMAGE) VALUES ($tid, '$nick', '$title', '$time', '$indl', '$topl', '$botl', '$postl', '$repl', '$polll', 'pub/$pimgf');");
	print "Thank you, $nick.  Click <a href=\"sbase.cgi\">here</a> to return to the base.";
	skettiLog ("$nick creates '$title' theme");
	skettiEndBoard();
}
