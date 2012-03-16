#!/usr/bin/perl -w

package SkettiSCRIPT;
use strict;
use sketdb;
use CGI qw(param);
use sketact;
use sketusr;
use sketboard;
use URI::Escape;

skettiStartBoard("Edit Pub");

my $mode = param('mode');
my $nick = skettiGrabLogin();
skettiUpdateLa(skettiGetTA());


if (!defined $mode || $mode eq "edit"){
	
	system(qq|dir -1 "/sketti/pub/$nick/" > .$nick\files|);
	open(FILES,".$nick\files");
	
	my $i = 0;
	my @files;
	
	while (<FILES>){
		$files[$i] = $_;
		$i++;
	}
	
	close(FILES);
	system("rm -f .$nick\files");
	print qq|<form method="POST" action="editpub.cgi">\n
	<input type="hidden" name="mode" value="delete">\n|;
	print "<h1>/~$nick</h1><br/><br/>";
	
	for my $file (@files){
		
		chomp($file);
		
		$file =~ s/\\//g;
		print qq|<input type="checkbox" name="files" value="$file"/> $file |;
		
		my $file_link = uri_escape($file);
		my $nick_link = uri_escape($nick);
		
		print qq|(<a href="/~$nick_link/$file_link" title="View $file" class="alt_links">view</a>) |;
		
		if ($file =~ m/(.*?)\.html$/ || $file =~ m/(.*?)\.htm$/ || $file =~ m/(.*?)\.js$/ ||  $file =~ m/(.*?)\.css$/ || $file =~ m/(.*?)\.txt$/ || $file =~ m/(.*?)\.cgi$/){
			
			print qq|(<a href="editpub.cgi?mode=file&file=$file_link" title="Edit $file" class="alt_links">edit</a>)|;
			
		}
		
		print qq|<br/>|;
		
	}
	
		print qq|<br/><input type="submit" value="delete" class="submit"/>|;
	
}elsif ($mode eq "file"){
	
	my $file_name = param('file');
	my $file_handle;
	open(FILE,"/sketti/pub/$nick/$file_name");
	
	while (<FILE>){
		
		$file_handle .= $_;
		
	}
	close(FILE);
	print <<END;
	<h1>$file_name</h1><br/>
	<form method="POST" action="editpub.cgi">
	<input type="hidden" name="mode" value="save">
	<input type="hidden" name="file" value="$file_name">
	<textarea rows="25" cols="100" class="textarea" name="filehandle">$file_handle</textarea><br/>
	<input type="submit" value="save" class="submit"/>
	
END

}elsif ($mode eq "save"){
	
	my $file_name = param('file');
	my $file_handle = param('filehandle');
	system("rm -f \"/sketti/pub/$nick/$file_name\"");
	open(FILE,">/sketti/pub/$nick/$file_name");
	
	print FILE $file_handle;
	
	close(FILE);
	my $link_nick = uri_escape($nick);
	my $link_file = uri_escape($file_name);
	print qq|Success! Back to <a href="editpub.cgi">your pub</a> or <a href="~$link_nick/$link_file">view the file</a>.|;
}elsif ($mode eq "delete"){
	
	my @files = param('files');
	
	for my $file (@files){
		
		system("rm -f \"/sketti/pub/$nick/$file\"");
		print "<em>$file deleted</em><br/>";
		
	}
	
	print qq|<a href="editpub.cgi">back to your pub</a>|;
	
}
skettiEndBoard();