#!/usr/bin/perl -w

use strict;
use CGI qw(param);

print "Content-type: text/html\n\n";

my $nick = param('nick');
my $bugm = param('bugm');
my $mode = param('mode');

if ($mode eq "send") {
print "Fine, I'll send an email to KaB0b0....";

open (MAIL, "|/usr/lib/sendmail kab0b0\@catlover.com") || print "Welp, looks like he WON'T be getting that message.";
print MAIL "Subject: Tall One\n";
print MAIL "Sender: tallernest\@sketti.net\n";
print MAIL "\nA bug has been reported by $nick\n\n
$bugm\n\n-Tall Ernest\n ";
print MAIL " ";
close(MAIL);

exit;
}
print <<END;

<html>
<head>
<title>Tall Ernest Secretarial Services</title>
</head>

<form method="POST" action="bugrep.cgi">
<strong>Find a bug?  Well, tell Tall Ernest and he'll send it to KaB0b0..</strong><br><br>Hey! Tall Ernest!  <br> My name is <input type="text" name="nick"> and I have a problem with KaB0b0's crappy code. <br><br> Ya see it all happened one day when <br><textarea name="bugm" rows = 20 cols = 30></textarea><br>
<input type="hidden" name="mode" value="send">
<center><input type="submit" value="SO DO SOMETHING ABOUT IT!"></form></html>

END
exit;
