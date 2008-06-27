#!/usr/bin/perl -w

use HTML::Entities;
use Encode;

use Pod::Usage;
pod2usage("No file input specified.") if ((@ARGV == 0)&&(-t STDIN));

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
--html					convert HTML tags to lightlang tags
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
$html = "";
GetOptions('convertmode!' => \$convert, 'sound-tag|s=s' => \$tag_lang, 'info=s' =>\$info, 'html' => \$html, 'help|h' => \$help, '<>' => \&add);

#print help messages
pod2usage(-message => $message, -output => \*STDOUT) if ($help);

if ($input){
	if (! open FILE, "<", "$input"){
		die "File doesn't exist";
	}
}
else{
	if (! open FILE, "-"){
		die "No file input specified.";
	}
}
foreach (<FILE>){
	chomp;
	if ($html){
		s/<(br|p)>/\\n/ig;
		s/<(b>|b [^>]*>)/\\[/ig;
		s/<abr>/\\</ig;
		s/<\/abr>/\\>/ig;
		s/<\/b>/\\]/ig;
		s/<i>/\\(/ig;
		s/<\/i>/\\)/ig;
		s/<k>/\\</ig;
		s/<\/k>/\\>/ig;
		s/<img[^<]*>/\\[[i•]\\]/ig;
	}
	push @dict_data, $_;
	my $tags = ();
	while ($_ =~ /(<[^>]*>)/){
		push @{$tags}, $1;
		s/<[^>]*>//;
	}
	push @TAGS, $tags;
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

if ($html){
	$line = 0;
	foreach (@dict_data){
		my @font_tags = ();
		foreach $match(@{$TAGS[$line]}){
			if ($match =~ /<font/i){
				push @font_tags, $match;
				if ($match =~ /color/i){
					s/<font color[^>]*>/\\</i;
				} else{
					s/<font[^>]*>//i;
				}
			} elsif ($match =~ /\/font/i){
				if (($swap = pop @font_tags) && ($swap =~ /color/i)){
					s/<\/font[^>]*>/\\>/i;
				} else{
					s/<\/font[^>]*>//i;
				}
			} elsif ($match =~ /<\/([a-zA-Z]+)>/i){
				s/<(|\/)\Q${1}\E[^<]*>//ig;
			}
		}
		$line++;
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
			if ($_ =~ /^data: /){
				s/^data: //;
			}
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
