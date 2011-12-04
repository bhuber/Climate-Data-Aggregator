#!/usr/bin/perl -w

use strict;
use Getopt::Std;
use GD;
use Data::Dumper;



my %opts;
getopts('x:s:r:c:f:', \%opts);

my $file = $opts{'f'} || 'data';
my $num_rows = $opts{'r'} || 99999;
my $num_cols = $opts{'c'} || 99999;
my $steps = $opts{'s'} || 5;

my $row_count = 0;
my $col_count = 0;

my $min;
my $max;


my @data;

open(DATA, "<$file");
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
    if(undef($min)){ $min = $e; }
    if(undef($max)){ $max = $e; }
    #print "$row_count,$col_count: $e\t";
    $col_count++;
    die "too many cols: $col_count $num_cols" if($col_count > $num_cols);
    $data[$row_count][$col_count] = $e;
  }
  #print "\n";
}

print "rows: $row_count cols: $col_count\n";

my $im = new GD::Image($col_count,$row_count);
my @colors;

my $white = $im->colorAllocate(255,255,255);
push(@colors, $white);
for (my $i = 1; $i <= $steps; $i++){
  my $color = int(255-255/$i);
  push(@colors, $im->colorAllocate($color, $color, $color));
}
my $black = $im->colorAllocate(0,0,0);

open (PNG, ">out.png");
binmode PNG;

sub color_index { #choose a color shade based on max, min, 
}

for (my $r = 0; $r < $row_count; $r++) {
   for (my $c = 0; $c < $col_count; $c++) {
     $im->setPixel($r, $c, $colors[int(rand(5))]);
   }
}

print PNG $im->png;

close(DATA);
close(PNG);
