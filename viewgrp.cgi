#!/usr/bin/perl -w

package SkettiSCRIPT;
use strict;
use sketsauce;
use sketusr;
use sketboard;
use sketact;
use sketdb;
use sketlog;
use CGI qw(param);

skettiStartBoard("Clans");

my $id = param('id');
my $name = param('name');
my $mode = param('mode');

my $db = skettiLoadDb();
my $query;

my $lnick = skettiGrabLogin();
if ($lnick != -1) { skettiUpdateLa($lnick); } elsif ($lnick == -1 && ($mode eq "edit" || $mode eq "create"))
{
	print "You must be <a href=\"login.cgi\">logged in</a> to perform that action<br/><a href=\"sbase.cgi\">back to the forum</a>";
	skettiEndBoard(); }
if ($mode eq "create") { createGrp(); }
if ($id ne "" && $name eq "") { $query = $db->prepare("SELECT * FROM CLANS WHERE CID = $id;"); }
elsif ($name ne "" && $id eq "") { $query = $db->prepare("SELECT * FROM CLANS WHERE NAME = \"$name\";"); }
else { listGrp(); }

$query->execute;
my ($cid, $name, $leader, $members, $descrip, $active, $pass, $bg, $flag) = $query->fetchrow_array;

if ($mode eq "" || $mode eq "basic")
{
	if ($active == 0)
	{
		print "That clan is inactive or doesn't exist-- sorry.<br/>Please, <a href=\"/\">return</a> to the base.";
		skettiEndBoard(); }
	my $leaderl = $leader;
	$leaderl =~ s/ /%20/g;
	my $posts = skettiCount("BASE",qq|FORUM = "$name"|);
	my $posts_text = $posts == 1 ? "post" : "posts";
	my $url_name = substr($name,1,length($name));
	print <<END;

	<center><font size="+3">$name</font></center><br>
	<table border="0" cellspacing="0" cellpadding="10">
	<tr><td bgcolor="$bg"><center><img src="$flag" alt="$name" height="140" width="120"></td></tr>
	<tr><td bgcolor="$bg"><strong><u>Clan ID:</u></strong></td><td>$cid</td></tr>
	<tr><td bgcolor="$bg"><strong><u>Forum:</u></strong></td><td><a href="/clans/$url_name/forum/" title="Official Forum of Clan $name">Official $name Forum</a> ($posts $posts_text)</td></tr>
	<tr><td bgcolor="$bg"><strong><u>Leader:</u></strong></td><td><a href="users.cgi?nick=$leaderl">$leader</a></td></tr>
	<tr><td bgcolor="$bg"><strong><u>Members</u></strong></td><td><ol>

END
	my $mem;
	$query = $db->prepare("SELECT NICK FROM USERS WHERE (CLANS REGEXP \"#$cid#\");");
	$query->execute;
	while ($mem = $query->fetchrow_array)
	{
		my $meml = $mem;
		$meml =~ s/ /%20/g;
		print "<li><a href=\"users.cgi?nick=$meml\">$mem</a><br/>\n";
	}
	$descrip =~ s/\r\n/<br\/>/g;
	print <<END;

	</td></tr>
	<tr><td bgcolor="$bg"><strong><u>Send a Message:</u></strong></td><td><form method="POST" action="sendmsg.cgi"><input type="hidden" name="to" value="$name"><input type="text" class="text" name="msg"/> &nbsp; <input type="submit" value="send" class="submit"/></form></td></tr>
	<tr><td bgcolor="$bg"><strong><u>Description</u></strong></td><td style="padding:20px">$descrip</td></tr>
	</table><br><center><a href="viewgrp.cgi?id=$cid&mode=edit">edit this info</a><br/><br/>
	<form method="POST" action="viewgrp.cgi"><input type="hidden" name="id" value="$cid">
	<input type="hidden" name="mode" value="join"><strong>Password:</strong> <input type="password" name="pass" class="text"/> <input type="submit" value="join clan" class="submit"/></form>

END
	skettiEndBoard();
}elsif ($mode eq "edit")
{
	if ($leader ne $lnick)
	{
		print "You must be the clan leader in order to edit clan info.<br/><a href=\".\">back to the forum</a>";
		skettiEndBoard(); }
	print <<END;
	<form method="POST" action="viewgrp.cgi">
	<input type="hidden" name="id" value="$cid">
	<input type="hidden" name="mode" value="save">
	<table border="0" cellspacing="0" cellpadding="5">
	<tr><td bgcolor="$bg"><strong><u>Flag:</u></strong></td><td><input type="text" class="text" name="flag" value="$flag"/></td></tr>
	<tr><td bgcolor="$bg"><strong><u>Password:</u></strong></td><td><input type="password" name="pass1" value="$pass" class="text"/></td></tr>
	<tr><td bgcolor="$bg"><strong><u>Password (verify):</u></strong></td><td><input type="password" name="pass2" value="$pass" class="text"/></td></tr>
	<tr><td bgcolor="$bg"><strong><u>Color:</u></strong></td><td><input type="text" class="text" name="color" value="$bg"/></td></tr>
	<tr><td bgcolor="$bg"><strong><u>Members:</u></strong></td><td><em>Delete:</em>
END
	my $mem;
	$query = $db->prepare("SELECT NICK FROM USERS WHERE (CLANS REGEXP \"#$cid#\");");
	$query->execute;
	while ($mem = $query->fetchrow_array) { if ($mem ne $leader) { print "<input type=\"checkbox\" name=\"members\" value=\"$mem\">$mem<br/>\n"; } }
	print <<END;
	<tr><td bgcolor="$bg"><strong><u>Description</u></strong></td><td><textarea rows="25" cols="80" name="descrip" class="textarea"/>$descrip</textarea></td></tr>
	</table><center><input type="submit" value="save" class="submit"/></form>
END
	skettiEndBoad(); }
	elsif ($mode eq "save") {
	my $fl = param('flag');
	my @mem = param('members');
	my $des = param('descrip');
	my $pass1 = param('pass1');
	my $pass2 = param('pass2');
	my $color = param('color');
	if ($pass1 ne $pass2)
	{
		print "Those two passwords don't match.. <a href=\"viewgrp.cgi?id=$cid&mode=edit\">try again</a>";
		skettiEndBoard(); }
		$des =~ s/'/\\'/g;
		$des =~ s/\r\n/<br\/>/g;
	$query=$db->prepare ("UPDATE CLANS SET COLOR='$color',FLAG='$fl',DESCRIPT='$des',PASS='$pass1' WHERE CID = $cid;");
	$query->execute;
	my $me;
	foreach $me(@mem)
	{
		my $query = $db->prepare("SELECT CLANS FROM USERS WHERE NICK=\"$me\";");
		$query->execute;
		my $clnz = $query->fetchrow_array;
		$clnz =~ s/#$cid#//g;
		if ($clnz == $cid) { $clnz = ""; }
		skettiQuery ("UPDATE USERS SET CLANS = \"$clnz\" WHERE NICK = \"$me\";");
		skettiQuery ("UPDATE CLANS SET MEMBERS = MEMBERS - 1 WHERE CID = $cid;");
	}
	print "Clan $name updated.<br\/><a href=\".\">Return to the forum</a> or <a href=\"viewgrp.cgi?id=$cid\">View the updated clan info</a>?";
	skettiEndBoard();
} elsif ($mode eq "join")
{
	my $password = param('pass');
	if ($pass ne $password)
	{
		print "Sorry, that is the incorrect password.<br/><a href=\".\">Return to the forum</a>.";
		skettiEndBoard(); }
	my $query = $db->prepare("SELECT NICK FROM USERS WHERE (CLANS REGEXP \"#$cid#\") AND NICK=\"$lnick\";");
	$query->execute;
	if ($query->rows != 0)
	{
		print "You are already in that clan!<a href=\".\">AWAY with you!</a>";
		skettiEndBoard(); }
	$query = $db->prepare("SELECT CLANS FROM USERS WHERE NICK=\"$lnick\";");
	$query->execute;
	if ($query->fetchrow_array eq "") { $query = $db->prepare ("UPDATE USERS SET CLANS = \"#$cid#\" WHERE NICK=\"$lnick\";"); } else {
		$query = $db->prepare ("UPDATE USERS SET CLANS = CONCAT(\"#$cid#\",CLANS) WHERE NICK=\"$lnick\";"); }
	$query->execute;
	skettiQuery ("UPDATE CLANS SET MEMBERS = MEMBERS + 1;");
	print "Congrats! You are now a member of $name!<br/><a href=\".\">Back to the forum</a>.";
	skettiEndBoard();
}
 elsif ($mode eq "make")
{
	my $pass1 = param('pass1');
	my $pass2 = param('pass2');
	my $name = param('name');
	my $flag = param('flag');
	my $color = param('color');
	my $descrip = param('descrip');
	if ($pass1 ne $pass2)
	{
		print "Those two passwords don't match.<br/><a href=\"viewgrp.cgi?mode=create\">Try again</a>";
		skettiEndBoard(); }
	if ($name eq "" || $flag eq "" || $color eq "" || $descrip eq "")
	{
		print "You're missing some stuff there...<a href=\"viewgrp.cgi?mode=create\">FILL IT IN!</a>";
		skettiEndBoard(); }
	my $query = $db->prepare("SELECT CID FROM CLANS;");
	$query->execute;
	my $cid = $query->rows;
	$descrip =~ s/"/\\"/g;
	$query=$db->prepare ("INSERT INTO CLANS (CID,NAME,FLAG,DESCRIPT,PASS,ACTIVE,LEADER,MEMBERS,COLOR) VALUES ($cid,\"\%$name\",\"$flag\",\"$descrip\",\"$pass1\",1,\"$lnick\",1,\"$color\");");
	$query->execute;
	skettiQuery (qq|INSERT INTO SUBJECTS (NAME,IMG) VALUES ("\%$name","$flag")|);
	$query = $db->prepare("SELECT CLANS FROM USERS WHERE NICK=\"$lnick\";");
	$query->execute;
	if ($query->fetchrow_array eq "") { skettiQuery ("UPDATE USERS SET CLANS = \"#$cid#\" WHERE NICK=\"$lnick\";"); }
	else {
		skettiQuery ("UPDATE USERS SET CLANS = CONCAT(\"#$cid#\",CLANS) WHERE NICK=\"$lnick\";"); }
	print qq|Clan $name created!<br/>Your clan page is <a href="/clans/$name/">here</a>. Your forums are located <a href="/clans/$name/forum/">here</a>.|;
	skettiEndBoard(); }
sub createGrp()
{
	my $query = $db->prepare("SELECT FONTC FROM USERS WHERE NICK=\"$lnick\";");
	$query->execute;
	my $bg = $query->fetchrow_array;
	print <<END;
	<form method="POST" action="viewgrp.cgi">
	<input type="hidden" name="mode" value="make">
	<table border="0" cellpadding="5" cellspacing="0">
	<tr><td bgcolor="$bg"><strong><u>Clan Name:</u></strong></td><td>%<input type="text" class="text" name="name"/></td></tr>
	<tr><td bgcolor="$bg"><strong><u>Flag:</u></strong></td><td><input type="text" class="text" name="flag"/></td></tr>
	<tr><td bgcolor="$bg"><strong><u>Password:</u></strong></td><td><input type="password" name="pass1" class="text"/></td></tr>
	<tr><td bgcolor="$bg"><strong><u>Password (verify)</u></strong></td><td><input type="password" name="pass2" class="text"/></td></tr>
	<tr><td bgcolor="$bg"><strong><u>Official Color:</u></strong></td><td><input type="text" class="text" name="color"/></td></tr>
	<tr><td bgcolor="$bg"><strong><u>Description</u></strong></td><td><textarea rows="25" cols="80" name="descrip" class="textarea"/></textarea></td></tr>
	</table><center><input type="submit" value="create" class="submit"/></form>
END
	skettiEndBoard();
}
sub listGrp()
{
	my $query = $db->prepare("SELECT CID,NAME FROM CLANS WHERE ACTIVE != 0;");
	$query->execute;
	if ($query->rows == 0)
	{
		print "No clans active at this time.<br/>Would you like to <a href=\"viewgrp.cgi?mode=create\">make one</a> or <a href=\".\">return to the forum</a>?";
		skettiEndBoard(); }
	my ($cid,$name);
	print <<END;

	<form method="POST" action="viewgrp.cgi">
	<input type="hidden" name="mode" value="basic"><center><select name="id">

END
	while (($cid,$name) = $query->fetchrow_array) {	print "<option value=\"$cid\">$name</option>"; }
	print "</select><br/><br/><input type=\"submit\" value=\"view info\" class=\"submit\"/></form>";
	skettiEndBoard(); }
