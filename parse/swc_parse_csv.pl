use strict;
use warnings;


# parse script for neuron studio output file

# converts tabular text file to csv


unless (@ARGV == 2) {
	die "Usage: perl swc_parse_csv.pl <input file dir> <output file dir>"
}

# my $in_fname = '../data/test/spine_test.txt'; 
# my $out_fname = '../data/test/spine_test.csv';


my $in_fname = $ARGV[0]; 
my $out_fname = $ARGV[1];

# open file
open(my $in_fh, '<', $in_fname) 
	or die "Cannot open file: $!";

# save file
open(my $out_fh, '>', $out_fname)
	or die "Cannot find write file: $1";


# process lines
my $i = 0;
while (my $line = <$in_fh>) {
	
	# remove newline char
	chomp($line);
	
	# split row into words array
	my @words = split(' ', $line);
	my $csv   = join(',', @words);	

	print $out_fh "$csv\n";

}


# close files
close($in_fh);
close($out_fh);


print("finished processing $in_fname\n to $out_fname");

