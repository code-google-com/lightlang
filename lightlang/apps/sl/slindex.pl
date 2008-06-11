#!/usr/bin/perl -w

@path = ("/usr/bin", "/usr/local/bin", "/bin");
$swap = 0;
foreach (@path){
	if (-e "$_/sl" and -X "$_/sl"){
		$swap = 1;
	}
}
unless ($swap){
	die ("sl program's not found!\n");
}

#@special_char = ( "\\\\", "\\!", "\\\$", "\\^", "\\&", "\\*", "\\\(", "\\\)", "\\=", "\\|", "\\[", "\\]", "\\{", "\\}", "\\;", "\\'", "\\\"" );
#sub get_path{
#	$_ = $_[0];
#	foreach my $swap (@special_char){
#		s/${swap}/${swap}/g;
#	}
#	s/\?/\\\?/g;
#	$_;
#}

if (@ARGV == 0){
	$arg_null = 1;
}
use Encode;
use Getopt::Long;
use Pod::Usage;
$message = "
slindex [-h|--help] [-r|--re-index] [-d <WORKING_DIRECTORY>] [-a|--all] [-p|--pattern <PATTERN>] [-i <INPUT>] [-o <OUTPUT>]

USAGE:
-h, --help		print this help
-a, --all		process all files in the working directory
-d			working directory
-i			single input file
-o			output file or directory, if output file's not defined, then the output is the same as the input
-p			files's name that's matched the <PATTERN>
-r, --reindex		remove the old index part of dictionaries before processing.
			***NOTE*** if this option is not enabled, only NON-indexed file will be processed.
";
$wdir = "";
$allfiles = "";
$input = "";
$output = "";
$help = "";
$reindex = "";
$pattern = "";

GetOptions('all|a' => \$allfiles, 'd=s' => \$wdir, 'pattern|p=s' => \$pattern, 're-index|r' => \$reindex, 'i=s' => \$input, 'o=s' => \$output, 'help|h' => \$help);

pod2usage(-message => $message, -output => \*STDOUT) if ( ($help) || ($arg_null) || ($wdir && !($allfiles || $pattern) && !$input) || ((!$allfiles)&&(!$pattern)&&(!$input)) );
pod2usage("**********Options --all|-a and -p can't be set at the same time with -i option") if (($allfiles || $pattern) && $input);

if ($allfiles || $pattern){
	unless ($wdir){
		$wdir = ".";
	}
	opendir WD, "$wdir" or die "**********Can not access $wdir directory: $!";
	while ($file = readdir WD){
		if ($pattern){
			next unless $file =~ /${pattern}/;
		}
		my $swap = "$wdir/$file";
		next unless -f $swap and -r $swap;
		$in_path = $wdir;
		#push @in_list, $swap;
		push @name_list, $file;
		#------------------------------------------------------------
		if ($output && -d $output){
			push @out_list, "$output/$file";
		} elsif(!$output){
			push @out_list, $swap;
		} else{
			die "**********Output directory is not specified!\n";
		}
	}
	close WD;
}

if ($input){
	$_ = $input;
	s/^.*\///g;
	push @name_list, "$_";

	if ($wdir){
		$in_path = $wdir;
#		$input = "$wdir/$input";
	} elsif($input =~ /\//){
		$in_path = substr( $input, 0, length($input) - length($_) );
	} else{
		$in_path = ".";
	}
#	push @in_list, $input;
	if ($output && !(-d $output)){
		if ($output =~ /\//){
			$_ = $output;
			s/^.*\///g;
			$swap = substr( $output, 0, length($output) - length($_) );
			if (-d "$swap/" ){
				push @out_list, $output;
				$output = $swap;
			} else{
				die "**********Output directory is not specified!\n";
			}
		} else{
			push @out_list, "$in_path/$output";
			$output = $in_path;
		}
	} elsif ($output && -d $output){
		push @out_list, "$output/$_";
	} elsif (!$output){
		push @out_list, $input;
	}
}

#foreach (@name_list){
#	print "$in_path/------ $_\n";
#}
#foreach (@out_list){
#	print "---$_\n";
#}

$count = 0;
$signal = 0;
foreach $file (@name_list){
	if ($reindex){
		if ($output){
			$temp1 = "$output/.$file";
			open SWAP, ">", $temp1;
		} else{
			$temp1 = "$in_path/.$file";
			open SWAP, ">", $temp1;
		}
	}
	open FILE, "<", "$in_path/$file" or die "**********Can not open file $file: $!";
	while (<FILE>){
		$_ = decode ('utf8', $_);
		if ($_ =~ /^\[index\]/){
			if ($reindex){
				$signal = 1;
			}else {
				$file = "";
			}
			last;
		}
	}
	if ($reindex){
		if ($signal){
			foreach (<FILE>){
				$_ = decode ('utf8', $_);
				unless ($_ =~ /(^\[index\]|^\[\/index\]|^. [0-9]*$)/){
					$_ = encode ('utf8', $_);
					print SWAP $_;
				}
			}
		}
		close SWAP;
	}
	close FILE;
	if ($file){
		unless ($signal){
			$temp1 = "$in_path/$file";
		}
		if ($output){
			$temp2 = $output;
		} else{
			$temp2 = $in_path;
		}
		system("sl --print-index \"$temp1\" > \"$temp2/.sl_index1\"");
		system("cat \"$temp1\" >> \"$temp2/.sl_index1\"");
		system("sl --print-index \"$temp2/.sl_index1\" > \"$temp2/.sl_index2\"");
		system("cat \"$temp1\" >> \"$temp2/.sl_index2\"");
		system("mv -f \"$temp2/\.sl_index2\" \"$out_list[$count]\"");
		system("rm -f \"$temp2/.sl_index1\"");
		system("rm -f \"$temp2/.$file\"");
	}
	$count++;
}
