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
xdxf2lightlang [OPTION] [xdxf] [lightlang]

OPTIONS:
-s					add sound tag
--html					convert HTML tags to lightlang tags
-h, --help				print this help
";
$tag_lang = "";
$help = "";
$html = "";

GetOptions('s' => \$tag_lang, 'html' => \$html, 'help|h' => \$help, '<>' => \&add);

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

for ($i = 1; $i <= 3; $i++){
	$_ = <FILE>;
	if (/encoding=\"(\S+)\"/){
		push @info, lc($1);
	} elsif (/lang_from=\"(\w+)\"/){
		push @info, substr(lc($1), 0, -1);
	}
}
###
$ar_open = 0;
$ar_close = 0;
###
$key_phrase = "";
$keyword = ();
foreach (<FILE>){
	my $count = 0;

	chomp;
	#remove HTML tags
	s/<(br|p)>/\\n/ig;
	s/<(b>|b [^>]*>)/\\[/ig;
	s/<\/b>/\\]/ig;
	s/<i>/\\(/ig;
	s/<\/i>/\\)/ig;
	s#<(|/)opt>##g;
	s#<(|/)pos>##g;
	s#</xdxf>##g;
	if (/<ar [^>]*>/){
		$ar_open = 1;
		$ar_close = 0;
	}
	if (/<\/ar>/){
		$ar_open = 0;
		$ar_close = 1;
		$_ = $key_phrase . $_;
		while (/<k>([^<]*)<\/k>/){
			s/<k>([^<]*)<\/k>//;
			$count++;
			$keyword[$count-1] = $1;
		}
		$key_phrase = "";
	}
	if ($ar_open == 1){
		if (/<def>/){
			$key_phrase = $key_phrase . $_ ;
		} else{
			$key_phrase = $key_phrase . $_ . "\\n";
		}
		$_ = "";
	}
	if (($ar_open == 0) && ($ar_close == 0)){
		$_ = "#" . $_;
	}


	if ($_ ne ""){
		s#<(|/)full_name>##g;
		s#<(|/)description>##g;
		s#<ar [^>]*>##g;
		s#</ar>##g;
		s#<def>#\\{#g;
		s#</def>#\\}#g;
		s#<(abr|ex)>#\\<#g;
		s#</(abr|ex)>#\\>#g;
		s#<tr>#\\(\\<#g;
		s#</tr>#\\>\\)#g;
		s#<iref>#\\_\\(#;
		s#</iref>#\\)\\_#;
		$_ = decode("$info[0]", $_);
		$_ = decode_entities($_);
		$_ = encode ('utf8', $_);
		s# # #g;
		if ($count > 0){
			for ($i = 0; $i < $count; $i++){
				$keyword[$i] = $keyword[$i] . "  " . $_;
				push @dict_data, $keyword[$i];
			}
		} else{
			push @dict_data, $_;
		}
	}
	my $tags = ();
	while ($_ =~ /(<[^>]*>)/){
		push @{$tags}, $1;
		s/<[^>]*>//;
	}
	push @TAGS, $tags;
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

#print result to STDOUT
foreach (@dict_data){
	if ($tag_lang){
		if (/^(\S+)  /){
			$swap = $1;
			s#  #  \\s$info[1]: $swap\\s#;
		}
	}
	if ($html){
		s/<img[^<]*>/\\[[i•]\\]/ig;
	}
	print $_."\n";
}

