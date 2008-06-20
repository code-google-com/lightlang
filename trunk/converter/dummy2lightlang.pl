#!/usr/bin/perl -w

use HTML::Entities;
use Encode;

use Pod::Usage;
pod2usage("No files input.") if ((@ARGV == 0));

use Getopt::Long;
$input = "";
sub add {
	$input = $_[0];
}

$message  = "
dummy2lightlang [OPTIONS] input

OPTIONS:
--noconvertmode				do not convert \"dummy\" to lightlang [default=yes]
-s, --sound-tag				add sound tags
--info					dictionary informations from file
-h, --help				print this help

USAGE examples:
makedict -o dummy -i dictd russian-english.index|dummy2lightlang -s ru > result

makedict -o dummy -i stardict english-german.ifo|dummy2lightlang -s en --info english-german.ifo > result

dummy2lightlang -s en --info english-german.ifo english-german.dummy > result

dummy2lightlang --noconvertmode -s ru russian-english_lightlang_format > result";

$convert = 1;
$tag_lang = "";
$info = "";
$help = "";
GetOptions('convertmode!' => \$convert, 'sound-tag|s=s' => \$tag_lang, 'info=s' =>\$info, 'help|h' => \$help, '<>' => \&add);

#print help messages
pod2usage(-message => $message, -output => \*STDOUT) if ($help);

if ($input){
	if (! open FILE, "<", "$input"){
		die "File doesn't exist";
	}
}
else{
	if (! open FILE, "-"){
		exit (-1);
	}
}
foreach (<FILE>){
	chomp;
	push @dict_data, $_;
}

if ($info){
	open DICT_INFO, "<", "$info";
	foreach (<DICT_INFO>){
		chomp;
		push @dict_info, $_;
	}
	foreach (@dict_info){
		if ($_ =~ /(wordcount|synwordcount|bookname|author|email|description)/){
			s/^/#/g;
			s/=/: /g;
			print "$_\n";
		}
	}
}

if ($convert){
	$line = 0;
	foreach (@dict_data){
		$_ = decode ('utf8', $_);
		$_ = decode_entities($_);
		$_ = encode ('utf8', $_);
		if ($_ =~ /^key: /){
			s/$/  /g;
			s/^key: //g;
			if ($tag_lang){
				$_ = $_."\\s"."$tag_lang:"." $_";#add tag \s...\s here
				s/  $/\\s/g;
			}
			if ($line){
				$_ = "\n".$_;
			}
			print $_.'\n';
		} else{
			s/ / /g;#replace space " " by " " character
			unless (($_ =~ /^data: <k>.*<\/k>$/) || ($_ =~ /^<k>[^<]*<\/k>$/)){
				print $_.'\n';
			}
		}
		$line = 1;
	}
}
else{
	foreach (@dict_data){
		if ($tag_lang){
			if ($_ =~ /^[^#]/){
				@temp = split /  /;
				s/$temp[0]  //;
				$_ = $temp[0]."  \\s"."$tag_lang: $temp[0]\\s".$_;
			}
		}
		$_ = decode ('utf8', $_);
		$_ = decode_entities($_);
		$_ = encode ('utf8', $_);
		print $_."\n";
	}
}
