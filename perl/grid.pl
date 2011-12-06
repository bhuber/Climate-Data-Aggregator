#!/usr/bin/perl -w

use strict;
use Getopt::Std;
use GD;
use Data::Dumper;

sub usage {
  print<<EOUSAGE
grid.pl  this program reads in an ascii grid and processes it, spitting out an image (and maybe eventually a NetCDF file)
 -?  help
 -s  number of steps for coloring the graph 1-255
 -r  number of rows expected (used for validating only)
 -c  number of cols expected (used for validating only)
 -f  file to read in

Requires GD for image creation ( sudo apt-get install libgd-gd2-perl )
EOUSAGE
}

my %opts;
getopts('?x:s:r:c:f:', \%opts);
usage() && exit if $opts{'?'};
my $file = $opts{'f'} || 'data';
my $num_rows = $opts{'r'} || 99999;
my $num_cols = $opts{'c'} || 99999;
my $steps = $opts{'s'} || 5;
die "can't go above 255 steps" if ($steps > 255);

my $row_count = 0;
my $col_count = 0;
my $min = "no";
my $max = "no";

my @data;

open(DATA, "<$file") or die "couldn't open $file $!";
while(<DATA>) {
  my $line = $_;
  $line =~ s/^\s+//g;
  $line =~ s/\s+$//g;
  $row_count++;
  $col_count = 0;
  die "too many rows: $row_count $num_rows" if($row_count > $num_rows);
  my @elems = split(/\s+/, $line);
  foreach my $e (@elems) {
    next unless ($e);
    if($e eq "-999.000"){ $e = 0; } #FLAG #TODO this needs to be set to null and transparent
    if($min eq "no"){ $min = $e; }
    if($max eq "no"){ $max = $e; }
    if($e < $min && $e ne "-999.000") { $min = $e; }
    if($e > $max) { $max = $e; }
    $col_count++;
    die "too many cols: $col_count $num_cols" if($col_count > $num_cols);
    $data[$row_count][$col_count] = $e;
  }
}

print "rows: $row_count cols: $col_count\n";
print "min: $min max: $max\n";

my $im = new GD::Image($col_count,$row_count);

my $color = 255;
my $white = $im->colorAllocate($color,$color,$color);
my $black = $im->colorAllocate(0,0,0);

my @colors;
push(@colors, $white);
for (my $i = 1; $i <= $steps; $i++){
  $color -= int(255/$steps);
  push(@colors, $im->colorAllocate($color, $color, $color));
}
print "colors: " . join(',',@colors) . "\n";

for (my $c = 0; $c < $col_count; $c++) {
   for (my $r = 0; $r < $row_count; $r++) {
     $im->setPixel($c, $row_count - $r, $colors[color_index($min,$max,$data[$r][$c])]);
   }
}

open (PNG, ">out.png");
binmode PNG;
print PNG $im->png;

close(DATA);
close(PNG);

sub color_index { #choose a color shade based on max, min, 
  #does this fall into the top $steps'th
  my $low = shift;
  my $high = shift;
  my $datapoint = shift;
  return 0 unless $datapoint;
  if ($datapoint eq "-999.000") { return 0; }
  my $range = $max-$min;
  my $step = $range/$steps;
  for (my $i = $steps; $i > 0; $i--) {
    if ($datapoint > ($i * $step) ) {
      return $i;
    }
  }
  return 0;
}
