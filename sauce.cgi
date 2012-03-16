#!/usr/bin/perl -w

package SkettiSCRIPT;
use strict;
use sketdb;
use sketsauce;
use sketact;
use sketboard;
use sketusr;
use CGI qw(param);

skettiStartBoard("SkettiSauce");

my $db = skettiLoadDb();
my $lonick = skettiGrabLogin();
my $viewr;

if ($lonick != -1) {
	skettiUpdateLa($lonick);
	my $q = $db->prepare("SELECT VIEWR FROM USERS WHERE NICK = '$lonick';");
	$q->execute;
	$viewr = $q->fetchrow_array;
}else{ $viewr = param('viewr'); }

my ($method,$query,$db,@ninfo);
my $defi = param('def');
$defi =~ s/&#040;/\(/g;
$defi =~ s/&#041;/\)/g;
my $def_id = param('def_id');
my $last = param('lastm');
my $sdef = param('query');

if ($defi eq "add def") { addDef(); }
if ($defi eq "add xtra") { addXtra(); }
if ($defi eq "insert def") { insertDef(); }
if ($defi eq "delete def") { deleteDef(); }
if ($defi eq "save xtra") { saveXtra(); }
if ($defi eq "saverate") { saverate(); }
if ($defi eq "edit def") { editDef(); }
if ($defi eq "rate def") { rateDef(); }
if ($defi eq "update def") { updateDef(); }
if ($defi eq "search") { searchDef(); }
if ($defi eq "remove") { removeDef(); }
if ($defi eq "") { $method = "num"; }else{ $method = "str"; }
if ($method eq "num")
{
	my $db = skettiLoadDb();
	$query = $db->prepare("SELECT * FROM SAUCE WHERE ID = $def_id;");
	$query->execute;
if ($query->rows == 0){
	$defi = $def_id;
	searchDef(); }
@ninfo = $query->fetchrow_array;
}
if ($method eq "str")
{
	my $db = skettiLoadDb();
	$defi =~ s/'/\\'/gi;
$query = $db->prepare("SELECT * FROM SAUCE WHERE KW = '$defi';");
$query->execute;
if ($query->rows == 0){
	$sdef = $defi;
	searchDef(); }
@ninfo = $query->fetchrow_array;
}
my ($id,$key,$def,$auth,$time,$type,$rat) = @ninfo;
my $db = skettiLoadDb();
$query = $db->prepare("SELECT * FROM SAUCER WHERE ID = $id;");
$query->execute;
my $x = $query->rows;
$def =~ s/\r\n/<br>/gi;
$def = saucify $def;

print <<END;
<div class="skettiSauce">
				<p align="center"><img src="/images/sketsauce.jpg" alt="SkettiSauce"/></p>
				<p align="right"><span class="sauceKey">&quot;$key&quot;</span></p>
				<p align="center"><br/>
				<div class="sauceLeft"><div class="sauceHeader"><span style="color:#9a9a9a"><u>Author:</u></span> $auth <img src="/kab0b0/images/spacer.png" alt="0"/> <span style="color:#9a9a9a"><u>Type:</u></span> $type <img src="/kab0b0/images/spacer.png" alt="0"/> <span style="color:#9a9a9a"><u>Rating:</u></span> $rat <img src="/kab0b0/images/spacer.png" alt="0"/> <span style="color:#9a9a9a"><u>ID:</u></span> $id</div>
				$def
				</div>
				<div style="clear:both"></div>
				<div class="sauceBottom"><a href="sauce.cgi?def=edit+def&id=$id" title="Edit $key Definition" class="sauce_link"> edit </a>       <a href="sauce.cgi?def=delete+def&id=$id" title="Delete $key Definition" class="sauce_link"> delete </a>       <a href="sauce.cgi?def=rate+def&id=$id" title="Rate $key Definition" class="sauce_link"> rate </a>       <a href="sauce.cgi?def_id=$id&viewr=1" class="sauce_link"> xtra: $x </a>        <a href="sbase.cgi" class="sauce_link"> back to forum </a>        <a href="sauce.cgi?def=add+def" class="sauce_link"> create saucedef </a>
				
<form action="sauce.cgi" method="GET"><input type="hidden" name="def" value="search"/><input type="text" name="query" class="text"/>  <input type="submit" value="saucesearch" class="submit"/></form></div>

END

if ($viewr == 1) {showXtra($id);}else { print "</div>"; }
skettiEndBoard();
sub addDef ()
{
	print <<END;
<div class="skettiSauce">
<img src="/images/sketsauce.jpg" alt="SkettiSauce"/><p>
<form method="POST" action="sauce.cgi">
<input type="hidden" name="def" value="insert def">

END
my $nickn = skettiGrabLogin();
print qq|<table border="0">|;
if ($nickn == -1)
{
	print <<END;
<tr><td><strong>Nickname:</strong></td><td><input type="text" name="nick" class="text"/></td></tr>
<tr><td><strong>Password:</strong></td><td><input type="password" name="pass" class="text"/></td></tr>
END
}else{
	skettiUpdateLa($nickn);
	my $passn = skettiGrabPass($nickn);
	print <<END;
<tr><td><strong>Nickname:</strong></td><td>$nickn</td></tr>
<input type="hidden" name="nick" value="$nickn">
<input type="hidden" name="pass" value="$passn">

END
}
print <<END;
<tr><td><strong>Saucedef Key:</strong></td><td><input type="text" name="skey" class="text"/></td></tr>
<tr><td><strong>Saucedef Category:</strong></td><td><select name="cat">
<option>Person(s)</option><option>Place(s)</option><option>Thing(s)</option><option>Idea(s)</option><option>Term(s)</option></select></td></tr>
<tr><td><strong>Definition:</strong></td>
<td><textarea name="defin" rows="30" cols="70" class="textarea"></textarea></td></tr>
<tr><td colspan="2"><input type="submit" value="add def" class="submit"/></td></tr></table>
</form>
</div>
END
skettiEndBoard();
}
sub insertDef()
{
	my $nick = param('nick');
	my $pass = param('pass');
	my $skey = param('skey');
	my $cat = param('cat');
	my $defin = param('defin');
	$skey =~ s/'/\\'/gi;
	$defin =~ s/'/\\'/gi;
	my $db = skettiLoadDb();
	$query = $db->prepare("SELECT PASS,STATUS,LVL FROM USERS WHERE NICK = '$nick';");
	$query->execute;
	if ($query->rows == 0){
		print "Hmm... sorry, you don't exist... how would you like to <a href=\"register.cgi?mode=get\">materialize</a>?";
		skettiEndBoard(); }
my @usr = $query->fetchrow_array;
my ($upass,$ustat,$lvl) = @usr;
if ($pass ne $upass)
{
	print "I'm afraid that is an incorrect password.. maybe you typed it wrong or maybe you're a dirty imposter!<br/>The <a href=\"sbase.cgi\">world</a> may never know..";
	skettiEndBoard(); }
$query = $db->prepare("SELECT ID FROM SAUCE WHERE KW = '$skey';");
$query->execute;
if ($query->rows != 0 || $skey eq "add def" || $skey eq "insert def" || $skey eq "delete def" || $skey eq "drop def" || $skey eq "rate def" || $skey eq "insert rating" || $skey eq "add response" || $skey eq "insert response" || $skey eq "edit def" || $skey eq "update def")
{
	$skey =~ s/ /%20/gi;
	print <<END;

It appears someone has already <a href="sauce.cgi?def=$skey&lastm=0">defined</a> that term.  Try thinking of a new one.

END
skettiEndBoard();
}
$query = $db->prepare("SELECT ID FROM SAUCE ORDER BY ID DESC;");
$query->execute;
my $nid = $query->fetchrow_array;
$nid++;
my $time = localtime;
$query = $db->prepare ("INSERT INTO SAUCE VALUES ($nid,'$skey','$defin','$nick','$time','$cat',0);");
$query->execute;
my $defkey = $skey;
$defkey =~ s/ /%20/gi;
print <<END;

Your <a href="sauce.cgi?def=$defkey&lastm=0">definition</a> for $skey has been added.<br/>
You can return to the <a href="sbase.cgi">base</a> as well.

END
skettiEndBoard();
}
sub editDef()
{
	my $db = skettiLoadDb();
	my $id = param('id');
	$query = $db->prepare("SELECT * FROM SAUCE WHERE ID = $id;");
	$query->execute;
if ($query->rows == 0)
{
	print <<END;
That saucedef does not exist.. sorry.  You could <a href="sauce.cgi?def=add%20def">click here</a> and create some though..

END
skettiEndBoard();
}
my ($nid,$key,$def,$auth,$time,$type,$rat) = $query->fetchrow_array;
print <<END;
<div class="skettiSauce">
<img src="/images/sketsauce.jpg" alt="SkettiSauce"/><br/>
<h1>&quot;$key&quot;</h1>
<form method="POST" action="sauce.cgi">
<table border="0">
END
if ($lonick != -1)
{
	my $lopass = skettiGrabPass($lonick);
	print <<END;
<tr><td><strong>Nickname:</strong></td><td>$lonick</td></tr>
<input type="hidden" name="nick" value="$lonick">
<input type="hidden" name="pass" value="$lopass">
END
}else{
	print <<END;
<tr><td><strong>Nickname:</strong></td><td><input type="text" name="nick" class="text"/></td></tr>
<tr><td><strong>Password:</strong></td><td><input type="password" name="pass" class="text"/></td></tr>
END
}
print <<END;
<tr><td><strong>Definition:</strong></td>
<td><textarea name="defin" cols="70" rows="25" class="textarea">$def</textarea></td></tr>
<tr><td colspan="2"><input type="submit" value="change def" class="submit"/></td></tr>
<input type="hidden" name="def" value="update def">
<input type="hidden" name="id" value="$nid"></table>
</form>
</div>
END

skettiEndBoard();
}
sub updateDef ()
{
	my $nick = param('nick');
	my $pass = param('pass');
	my $nid = param('id');
	my $ndef = param('defin');
	my $db = skettiLoadDb();
	$query = $db->prepare("SELECT PASS,STATUS,LVL FROM USERS WHERE NICK='$nick';");
	$query->execute;
	my ($rpass,$stat,$lvl) = $query->fetchrow_array;
	$query = $db->prepare("SELECT NICK FROM SAUCE WHERE ID = $nid;");
	$query->execute;
	my $nauth = $query->fetchrow_array;
	if ($stat ne "SkettiOP" && $stat ne "SkettiMEMBER" && $stat ne "SkettiPHILE")
	{
		print <<END;

Hmm.. looks like you are not of a high enough ranking to be making any changes to anyone's saucedefs, you can still <a href="sbase.cgi">post</a>, though.

END
	skettiEndBoard();
}
	if ($nauth ne $nick && $lvl < 4 && $stat ne "SkettiOP" || $pass ne $rpass)
	{
		print <<END;

Sorry.. unless you are a SkettiOP, you cannot make changes to others' saucedefs, so don't try.  You can <a href="sauce.cgi?def=add%20def">make your own</a>, however.

END
	skettiEndBoard();
}
	$ndef =~ s/'/\\'/gi;
	$query = $db->prepare ("UPDATE SAUCE SET DEF='$ndef' WHERE ID = $nid;");
	$query->execute;
	print "The <a href=\"sauce.cgi?def_id=$nid&lastm=0\">definition</a> has been updated, $nick.";
	skettiEndBoard();
}
sub searchDef()
{
	my $db = skettiLoadDb();
	if ($sdef ne "" && defined $sdef) { $query = $db->prepare("SELECT * FROM SAUCE WHERE (UPPER(KW) LIKE UPPER(\"%$sdef%\") OR UPPER(DEF) LIKE UPPER(\"%$sdef%\")) ORDER BY TYPE;"); }else{ $query = $db->prepare("SELECT * FROM SAUCE ORDER BY TYPE;"); }
	$query->execute;
	print qq|<div class="skettiSauce"><img src="/images/sketsauce.jpg" alt="SkettiSauce"><br/><br/><h2>SauceSearch</h2><br/></center><p align=\"left\"><em>Results for $sdef</em><br/><ol/>\n|;
	my @sauce;
	my $ctr = 0;
	while (@sauce = $query->fetchrow_array)
	{
		my ($nid, $kw, $def, $author, $time, $type, $rat) = @sauce;
		print "<li><a href=\"sauce.cgi?def_id=$nid&lastm=0\">\"$kw\"<\/a> [$type] by $author (def_id: $nid | rat: $rat)<br/>";
	}
	$ctr = $query->rows;
	print "</ol><br><em>xtras:</em><br/><ol>\n";
	if ($sdef ne "") { $query = $db->prepare("SELECT * FROM SAUCER WHERE UPPER(DEF) LIKE UPPER(\"$sdef\") ORDER BY TYPE;"); } else { $query = $db->prepare("SELECT * FROM SAUCER;"); }
	$query->execute;
	while (@sauce = $query->fetchrow_array)
	{
		my ($nid,$def,$author,$time,$type) = @sauce;
		print "<li><a href=\"sauce.cgi?def_id=$nid&lastm=0&viewr=1#xtras\">$nid=>xtra<\/a> [$type] by $author<br/>";
	}
	$ctr += $query->rows;
	print <<END;
</ol><br/><strong>Returned $ctr Results</strong></p><p><hr noshade></p>
<p>
<div class="sauceBottom"><a href="sauce.cgi?def=$key&viewr=1&lastm=0" class="sauce_link"> xtra: 0 </a>        <a href="sbase.cgi" class="sauce_link"> back to forum </a>        <a href="sauce.cgi?def=add+def" class="sauce_link"> create saucedef </a>

<form action="sauce.cgi" method="GET"><input type="hidden" name="def" value="search"/><input type="text" name="query" class="text"/>  <input type="submit" value="saucesearch" class="submit"/></form></div></div>
END

skettiEndBoard();
}
sub rateDef ()
{
	my $id = param('id');
	my $db = skettiLoadDb();
	my $query = $db->prepare("SELECT * FROM SAUCE WHERE ID = $id;");
	$query->execute;
	if ($query->rows == 0)
	{
		print "That def does not exist, try just following links instead of making them up.";
		skettiEndBoard();
	}
	my ($nid, $key, $def, $auth, $time, $type, $rat) = $query->fetchrow_array;
	$def =~ s/\r\n/<br\/>/gi;
	print <<END;
<div class="skettiSauce">
<img src="/images/sketsauce.jpg" alt="SkettiSauce"><br/>
&quot;$key&quot by $auth:<br/><br/>
<blockquote>$def</blockquote><br/><br/><hr noshade><br/>
<form method="POST" action="sauce.cgi">
<table border="0">
END
my $nickn = skettiGrabLogin();
if ($nickn == -1) {
	print <<END;

<tr><td><strong>Nickname:</strong></td><td><input type="text" name="nick" class="text"/></td></tr>
<tr><td><strong>Password:</strong></td><td><input type="password" name="pass" class="text"/></td></tr>
END
}else{
	$query = $db->prepare("SELECT STATUS,LVL FROM USERS WHERE NICK = '$nickn';");
	$query->execute;
	my ($status, $lvl) = $query->fetchrow_array;
	if ($status ne "SkettiOP" && $lvl < 6) { print "You must be at least an OP or a <em>Messiah</em>.";
	skettiEndBoard(); }
	$query = $db->prepare("SELECT PASS FROM USERS WHERE NICK = '$nickn';");
	$query->execute;
	my $passn = $query->fetchrow_array;
	print <<END;
<input type="hidden" value="$nickn" name="nick">
<input type="hidden" value="$passn" name="pass">
END
}
print <<END;
<input type="hidden" value="saverate" name="def">
<input type="hidden" name="id" value="$id">
<tr><td colspan="2"><select name="rating">
<option>-10</option><option>-9</option><option>-8</option><option>-7</option><option>-6</option><option>-5</option><option>-4</option><option>-3</option><option>-2</option><option>-1</option><option>1</option><option>2</option><option>3</option><option>4</option><option>5</option><option>6</option><option>7</option><option>8</option><option>9</option><option>10</option>
</select></td></tr>
<tr><td colspan="2"><input type="submit" value="rate def" class="submit"/></td></tr></table></form></div>
END

skettiEndBoard();
}
sub saverate ()
{
	my $nick = param('nick');
	my $pass = param('pass');
	my $rating = param('rating');
	my $id = param('id');
	my $db = skettiLoadDb();
	my $query=$db->prepare("SELECT STATUS,LVL FROM USERS
	WHERE NICK = '$nick' AND PASS = '$pass';");
	$query->execute;
	if ($query->rows == 0){
		print "Hmmm... no, don't do that, <a href=\"sbase.cgi\">leave<\/a>.";
		skettiEndBoard();
		exit;
	}
	my ($status, $lvl) = $query->fetchrow_array;
	if ($status ne "SkettiOP" && $lvl < 6) { print "You must be at least an OP or a <em>Messiah</em>.";
	skettiEndBoard(); }

	$query = $db->prepare("SELECT RATING,NICK FROM SAUCE WHERE ID = $id;");
	$query->execute;
	my ($rat,$nicholas) = $query->fetchrow_array;
	if ($nick eq $nicholas)
	{
		print "Don't rate your own definition!  Geez!  Get <a href=\"sbase.cgi\">outta here</a>\n";
		skettiEndBoard();
		exit;
	}
	$query = $db->prepare("SELECT STATUS,EXP,LVL,TITLE,SEX FROM USERS WHERE NICK = '$nicholas';");
	$query->execute;
	if ($rating < 0) { my $ratso = abs($rating); skettiSendZiggyMsg $nicholas, "<a href=\"sauce.cgi?def_id=$id\">Your definition</a> just lost you $ratso EXP."; }else{
		skettiSendZiggyMsg $nicholas, "<a href=\"sauce.cgi?def_id=$id\">Your definition</a> just gained you $rating EXP.  Congratulations.  Rejoice."; }
	skettiUpdateLvl ($nicholas,$rating);
	$query = $db->prepare ("UPDATE SAUCE SET RATING = RATING + $rating WHERE ID = $id;");
	$query->execute;
	print "The <a href=\"sauce.cgi?def_id=$id\">definition<\/a> has been updated.";
	skettiEndBoard();
}
sub deleteDef()
{
	my $id = param('id');
	my $db = skettiLoadDb();
	$query = $db->prepare("SELECT KW,NICK FROM SAUCE WHERE ID = $id;");
	$query->execute;
	my ($kw, $knick) = $query->fetchrow_array;
	print "Sure to delete $kw by $knick?<br/><br/><form method=\"POST\" action=\"sauce.cgi\">";
	print "<input type=\"hidden\" name=\"id\" value=$id><input type=\"hidden\" name=\"def\" value=\"remove\"><input type=\"submit\" value=\"doit\" class=\"submit\"/></form>";
	skettiEndBoard();
}
sub removeDef ()
{
	my $id = param('id');
	my $db = skettiLoadDb();
	skettiQuery ("DELETE FROM SAUCE WHERE ID = $id;");
	print "Def #$id has been deleted.  <a href=\"sbase.cgi\">Thank you</a>.";
	skettiEndBoard();
}
sub showXtra
{
	my $sid = shift;
	my @sinfo;
	my $db = skettiLoadDb();
	my $query = $db->prepare("SELECT * FROM SAUCER WHERE ID = $sid;");
	$query->execute;
	print "<a name=\"xtras\"></a><p><hr noshade></p><p><center><h1>xtras</h1></center></p>";
	while (@sinfo = $query->fetchrow_array)
	{
		my ($sid,$def,$nick,$time,$type) = @sinfo;
		my $query2 = $db->prepare("SELECT FONTC FROM USERS WHERE NICK = '$nick';");
		$query2->execute;
		my $font = $query2->fetchrow_array;
		$def =~ s/\r\n/<br\/>/gi;
		$def = saucify $def;
		print <<END;
<p><hr noshade></p>
<p align="center"><strong>$nick \@ $time <em>($type)</em></strong></p>
<p align="left"><font size=-1 color="$font">$def</font></p>
END
	}
	print "<p><hr noshade></p><p align=\"center\"><a href=\"sauce.cgi?def=add+xtra&id=$id\">add xtra</a></p></div>";
}
sub addXtra
{
	my $sid = param('id');
	my $nick = skettiGrabLogin();
	if ($nick == -1 || $nick == -2)
	{
		print "You have to be <a href=\"login.cgi\">logged in</a>.";
		skettiEndBoard();
	}
	print <<END;
<form method="POST" action="sauce.cgi">
<table border="0">
<input type="hidden" name="def" value="save xtra">
<input type="hidden" name="id" value="$sid">
<input type="hidden" name="nick" value="$nick">
<tr><td><strong>Nickname:</strong></td><td>$nick</td></tr>
<tr><td><strong>Type:</strong></td><td><select name="type">
<option>Person(s)</option><option>Place(s)</option>
<option>Thing(s)</option><option>Idea(s)</option>
<option>Term(s)</option></select></td></tr>
<tr><td><strong>xtra:</strong></td><td>
<textarea rows="15" cols="55" name="xtra" class="textarea"></textarea></td></tr>
<tr><td colspan="2"><input type="submit" value="save xtra" class="submit"/></td></tr>
</table>
</form>
END
	skettiEndBoard();
}
sub saveXtra
{
	my $db = skettiLoadDb();
	my $sid = param('id');
	my $nick = param('nick');
	my $type = param('type');
	my $xtra = param('xtra');
	$xtra =~ s/'/\\'/gi;
	my $time = localtime;
	$time =~ s/  / /gi;
	$query=$db->prepare ("INSERT INTO SAUCER (ID,DEF,NICK,TIME,TYPE) VALUES ($sid,'$xtra','$nick','$time','$type');");
	print "Thanks, $nick, the <a href=\"sauce.cgi?def_id=$sid&viewr=1\">xtra</a> has been added.";
	$query->execute;
	skettiEndBoard();
}
