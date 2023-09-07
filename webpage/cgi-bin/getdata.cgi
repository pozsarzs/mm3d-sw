#!/usr/bin/perl
# +----------------------------------------------------------------------------+
# | MM3D v0.9 * Growing house controlling and remote monitoring system         |
# | Copyright (C) 2018-2023 Pozsár Zsolt <pozsarzs@gmail.com>                  |
# | getdata.cgi                                                                |
# | CGI program                                                                |
# +----------------------------------------------------------------------------+

#   This program is free software: you can redistribute it and/or modify it
# under the terms of the European Union Public License 1.1 version.
#
#   This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.

use lib 'cgi-bin';
use Switch;
use strict;
use warnings;

my $contname = 'MM3D';
my $contversion = 'v0.9';

# get data
my $buffer;
my @pairs;
my $pair;
my $name;
my $value;
my %FORM;
$ENV{'REQUEST_METHOD'} =~ tr/a-z/A-Z/;
if ($ENV{'REQUEST_METHOD'} eq "GET")
{
  $buffer = $ENV{'QUERY_STRING'};
}
@pairs = split(/&/, $buffer);
foreach $pair (@pairs)
{
  ($name, $value) = split(/=/, $pair);
  $value =~ tr/+/ /;
  $value =~ s/%(..)/pack("C", hex($1))/eg;
  $FORM{$name} = $value;
}

# load configuration
#my $conffile = "/etc/mm3d/mm3d.ini";
my $conffile = "/usr/local/etc/mm3d/mm3d.ini";
my $row;
my $dir_lck;
my $dir_log;
my $dir_var;
my $nam_err1;
my $nam_err2;
my $nam_err3;
my $nam_err4;
my $nam_in1;
my $nam_in2;
my $nam_in3;
my $nam_in4;
my $nam_out1;
my $nam_out2;
my $nam_out3;
my $nam_out4;
my $usr_nam;
my $usr_dt1;
my $usr_dt2;
my $usr_dt3;
my $usr_uid;
open CONF, "< $conffile" or die "ERROR: Cannot open configuration file!";
while (<CONF>)
{
  chop;
  my(@columns) = split("=");
  my($colnum) = $#columns;
  $row = "";
  foreach $colnum (@columns)
  {
    $row = $row . $colnum;
  }
  my(@datarow) = split("\"\"",$row);
  my($datarownum) = $#datarow;
  switch ($columns[0])
  {
    case "dir_lck" { $dir_lck = $columns[1]; }
    case "dir_log" { $dir_log = $columns[1]; }
    case "dir_var" { $dir_var = $columns[1]; }
    case "nam_err1" { $nam_err1 = $columns[1]; }
    case "nam_err2" { $nam_err2 = $columns[1]; }
    case "nam_err3" { $nam_err3 = $columns[1]; }
    case "nam_err4" { $nam_err4 = $columns[1]; }
    case "nam_in1" { $nam_in1 = $columns[1]; }
    case "nam_in2" { $nam_in2 = $columns[1]; }
    case "nam_in3" { $nam_in3 = $columns[1]; }
    case "nam_in4" { $nam_in4 = $columns[1]; }
    case "nam_out1" { $nam_out1 = $columns[1]; }
    case "nam_out2" { $nam_out2 = $columns[1]; }
    case "nam_out3" { $nam_out3 = $columns[1]; }
    case "nam_out4" { $nam_out4 = $columns[1]; }
    case "usr_dt1" { $usr_dt1 = $columns[1]; }
    case "usr_dt2" { $usr_dt2 = $columns[1]; }
    case "usr_dt3" { $usr_dt3 = $columns[1]; }
    case "usr_nam" { $usr_nam = $columns[1]; }
    case "usr_uid" { $usr_uid = $columns[1]; }
  }
}
close CONF;

# create output
my $datafile = "$dir_log/mm3d.log";
my $lockfile = "$dir_lck/mm3d.lock";
open DATA, "< $datafile" or die "ERROR: Cannot open log file!";
close DATA;
print "Content-type:text/plain\r\n\r\n";
my $serialnumber = $FORM{uid};
if ( $serialnumber eq $usr_uid )
{
  # check lockfile
  while (-e $lockfile)
  {
    sleep 1;
  }
  if ( $FORM{value} eq '0' )
  {
    if ( $FORM{type} eq 'xml' )
    {
      print "<?xml version=\"1.0\" encoding=\"utf-8\"?>\n";
      print "<xml>\n";
      print "  <about>\n";
      print "    <name>$contname</name>\n";
      print "    <version>$contversion</version>\n";
      print "  </about>\n";
      print "</xml>\n";
    } else
    {
      print "$contname\n";
      print "$contversion\n";
    }
    exit 0;
  }
  if ( $FORM{value} eq '1' )
  {
    if ( $FORM{type} eq 'xml' )
    {
      print "<?xml version=\"1.0\" encoding=\"utf-8\"?>\n";
      print "<xml>\n";
      print "  <user>\n";
      print "    <name>$usr_nam</name>\n";
      print "    <data1>$usr_dt1</data1>\n";
      print "    <data2>$usr_dt2</data2>\n";
      print "    <data3>$usr_dt3</data3>\n";
      print "  </user>\n";
      print "</xml>\n";
    } else
    {
      print "$usr_nam\n";
      print "$usr_dt1\n";
      print "$usr_dt2\n";
      print "$usr_dt3\n";
    }
    exit 0;
  }
  if ( $FORM{value} eq '2' )
  {
    if ( $FORM{type} eq 'xml' )
    {
      print "<?xml version=\"1.0\" encoding=\"utf-8\"?>\n";
      print "<xml>\n";
      print "  <titles>\n";
      print "    <input1>$nam_in1</input1>\n";
      print "    <input2>$nam_in2</input2>\n";
      print "    <input3>$nam_in3</input3>\n";
      print "    <input4>$nam_in4</input4>\n";
      print "    <errorlight1>$nam_err1</errorlight1>\n";
      print "    <errorlight2>$nam_err2</errorlight2>\n";
      print "    <errorlight3>$nam_err3</errorlight3>\n";
      print "    <errorlight4>$nam_err4</errorlight4>\n";
      print "    <output1>$nam_out1</output1>\n";
      print "    <output2>$nam_out2</output2>\n";
      print "    <output3>$nam_out3</output3>\n";
      print "    <output4>$nam_out4</output4>\n";
      print "  </titles>\n";
      print "</xml>\n";
    } else
    {
      print "$nam_in1\n";
      print "$nam_in2\n";
      print "$nam_in3\n";
      print "$nam_in4\n";
      print "$nam_err1\n";
      print "$nam_err2\n";
      print "$nam_err3\n";
      print "$nam_err4\n";
      print "$nam_out1\n";
      print "$nam_out2\n";
      print "$nam_out3\n";
      print "$nam_out4\n";
    }
    exit 0;
  }
  if ( $FORM{value} eq '3' )
  {
    open DATA, "< $datafile" or die "Cannot open log file!";
    while (<DATA>)
    {
      chop;
      my(@columns)= split(",");
      my($colnum)=$#columns;
      $row = "";
      foreach $colnum (@columns)
      {
        $row = $row . $colnum;
      }
      my(@datarow) = split("\"\"",$row);
      my($datarownum) = $#datarow;
      if ( $FORM{type} eq 'xml' )
      {
        print "<?xml version=\"1.0\" encoding=\"utf-8\"?>\n";
        print "<xml>\n";
        print "  <environment>\n";
        print "    <date>$columns[0]</date>\n";
        print "    <time>$columns[1]</time>\n";
        print "    <temperature>$columns[2]</temperature>\n";
        print "    <humidity>$columns[3]</humidity>\n";
        print "    <input1>$columns[4]</input1>\n";
        print "    <input2>$columns[5]</input2>\n";
        print "    <input3>$columns[6]</input3>\n";
        print "    <input4>$columns[7]</input4>\n";
        print "    <errorlight1>$columns[12]</errorlight1>\n";
        print "    <errorlight2>$columns[13]</errorlight2>\n";
        print "    <errorlight3>$columns[14]</errorlight3>\n";
        print "    <errorlight4>$columns[15]</errorlight4>\n";
        print "    <output1>$columns[8]</output1>\n";
        print "    <output2>$columns[9]</output2>\n";
        print "    <output3>$columns[10]</output3>\n";
        print "    <output4>$columns[11]</output4>\n";
        print "  </environment>\n";
        print "</xml>\n";
      } else
      {
        print "$columns[0]\n";
        print "$columns[1]\n";
        print "$columns[2]\n";
        print "$columns[3]\n";
        print "$columns[4]\n";
        print "$columns[5]\n";
        print "$columns[6]\n";
        print "$columns[7]\n";
        print "$columns[8]\n";
        print "$columns[9]\n";
        print "$columns[10]\n";
        print "$columns[11]\n";
        print "$columns[12]\n";
        print "$columns[13]\n";
        print "$columns[14]\n";
        print "$columns[15]\n";
      }
      last;
    }
    close DATA;
    exit 0;
  }
  if ( $FORM{value} eq '4' )
  {
    my $out1;
    my $out2;
    my $out3;
    my $out4;
    my $out1file = "$dir_var/out1";
    my $out2file = "$dir_var/out2";
    my $out3file = "$dir_var/out3";
    my $out4file = "$dir_var/out4";
    open DATA, "< $out1file" or $out1 = "neutral";
    my $o1 = <DATA>;
    close DATA;
    switch ($o1)
    {
      case "neutral" { $out1 = "neutral"; }
      case "on" { $out1 = "on"; }
      case "off" { $out1 = "off"; }
    }
    open DATA, "< $out2file" or $out2 = "neutral";
    my $o2 = <DATA>;
    close DATA;
    switch ($o2)
    {
      case "neutral" { $out2 = "neutral"; }
      case "on" { $out2 = "on"; }
      case "off" { $out2 = "off"; }
    }
    open DATA, "< $out3file" or $out3 = "neutral";
    my $o3 = <DATA>;
    close DATA;
    switch ($o3)
    {
      case "neutral" { $out3 = "neutral"; }
      case "on" { $out3 = "on"; }
      case "off" { $out3 = "off"; }
    }
    open DATA, "< $out4file" or $out4 = "neutral";
    my $o4 = <DATA>;
    close DATA;
    switch ($o4)
    {
      case "neutral" { $out4 = "neutral"; }
      case "on" { $out4 = "on"; }
      case "off" { $out4 = "off"; }
    }
    if ( $FORM{type} eq 'xml' )
    {
      print "<?xml version=\"1.0\" encoding=\"utf-8\"?>\n";
      print "<xml>\n";
      print "  <override>\n";
      print "    <channel1>$out1</channel1>\n";
      print "    <channel2>$out2</channel2>\n";
      print "    <channel3>$out3</channel3>\n";
      print "    <channel4>$out4</channel4>\n";
      print "  </override>\n";
      print "</xml>\n";
    } else
    {
      print "$out1\n";
      print "$out2\n";
      print "$out3\n";
      print "$out4\n";
    }
    exit 0;
  }
}
exit 0;
