#!/usr/bin/perl -w

use HTML::Entities;
use Encode;

use Getopt::Long qw(:config permute);
my $input = "";
sub add {
	$input = $_[0];
}
my $convert = 1;
my $tag_lang = "";
my $info = "";
GetOptions('convertmode!' => \$convert, 'sound-tag|s=s' => \$tag_lang, 'info=s' =>\$info, '<>' => \&add);

if ($input){
	open FILE, "<", "$input";
}
else{
	open FILE, "-";
}
foreach (<FILE>){
	chomp;
	push @dict_data, $_;
}

if ($convert){
	$line = 0;
	foreach (@dict_data){
		use utf8;
		$_ = decode ('utf8', $_);
		$_ = decode_entities($_);
		no utf8;
		$_ = encode ('utf8', $_);
		if ((($_ =~ /(^[^k]|^k[^e]|^ke[^y]|^key[^:])|^key:[^ ]/)) || (!$_)){
			s/ / /g;#replace space " " by " " character
			$dict_data[$line] = $_;
			if ($line > 0){
				if ($_ =~ /^data: <k>.*<\/k>$/){
					$dict_data[$line] = $dict_data[$line-1];
					$dict_data[$line -1] = "";
				}
				else{
					$dict_data[$line] = $dict_data[$line-1].$dict_data[$line]."\\n";
					$dict_data[$line-1] = "";
				}
			}
		}
		if ($_ =~ /^key: /){
			s/$/  \\n/g;
			s/^key: //g;
			if ($tag_lang){
				$_ = $_."\\s"."$tag_lang:"." $_";#add tag \s...\s here
				s/  \\n$/\\s\\n/g;
				s/\\n//;
			}
			$dict_data[$line] = $_;
		}
		$line++;
	}
}
else{
	foreach (@dict_data){
		if ($tag_lang){
			@temp = split /  /;
			s/$temp[0]  //;
			$_ = $temp[0]."  \\s"."$tag_lang: $temp[0]\\s".$_;
		}
		use utf8;
		$_ = decode ('utf8', $_);
		$_ = decode_entities($_);
		no utf8;
		$_ = encode ('utf8', $_);
	}
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

foreach (@dict_data){
	if ($_){
		print $_,"\n";
	}
}
