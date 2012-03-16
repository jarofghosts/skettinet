#!/usr/bin/perl

package SkettiSCRIPT;
use sketdb;

exit if fork();
while (1)
{
	sleep(2);
system("ls /sketti/enid/*.jpg > .picindex");
open(PICS,".picindex");
my $picstemp;
while (<PICS>) { $picstemp .= $_ . ","; }
close(PICS);
my @pics = split(/,/,$picstemp);
my $rande = $pics[rand @pics];
$rande =~ s/\/sketti\///g;
my $db= skettiLoadDb();
my $query = $db->prepare("UPDATE USERS SET AVATAR = \"$rande\" WHERE NICK=\"KaB0b0\";");
$query->execute;
}
