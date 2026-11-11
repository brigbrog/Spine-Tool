# Brian Brogan
# Bloss Lab
# The Jackson Laboratory
# 9 November 2026 
# parse script for neuron studio output file
# converts tabular text file to csv

use strict;
use warnings;


unless (@ARGV == 2) {
	die "Usage: perl swc_parse_csv.pl <input file dir> <output file dir>"
}

my $in_fname = $ARGV[0]; 
my $out_fname = $ARGV[1];

sub parseNS2CSV {
	
	# get the file paths
	my ($in_fname, $out_fname) = @_;

	# open the files
	open(my $in_fh, '<', $in_fname)
		or die "Cannot load provided file: $in_fname"; 
	
	open(my $out_fh, '>', $out_fname)
		or die "Cannot load provided file: $out_fname"; 
	
	# parse the data 	
	while (my $line = <$in_fh>) {
		
		# remove newline char
		chomp($line);
		
		# split row into words array
		my @words = split(' ', $line);
		my $csv   = join(',', @words);	
		
		# write the data to the new file
		print $out_fh "$csv\n";

	}
	
	## close files
	close($in_fh);
	close($out_fh);
}


parseNS2CSV($in_fname, $out_fname);

print("finished processing $in_fname to $out_fname\n");
