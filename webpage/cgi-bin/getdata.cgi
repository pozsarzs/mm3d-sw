#!/usr/bin/perl
# +----------------------------------------------------------------------------+
# | MM3D v0.11 * Growing house controlling and remote monitoring system        |
# | Copyright (C) 2018-2019 Pozsár Zsolt <pozsar.zsolt@.szerafingomba.hu>      |
# | getdata.cgi                                                                |
# | CGI program                                                                |
# +----------------------------------------------------------------------------+
#
#   This program is free software: you can redistribute it and/or modify it
# under the terms of the European Union Public License 1.1 version.
#
#   This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.

use lib 'cgi-bin';
use Switch;

$contname = 'MM3D';
$contversion = 'v0.11';

# get data
local ($buffer, @pairs, $pair, $name, $value, %FORM);
$ENV{'REQUEST_METHOD'} =~ tr/a-z/A-Z/;
if ($ENV{'REQUEST_METHOD'} eq "GET")
{
  $buffer = $ENV{'QUERY_STRING'};
}

# split input data
@pairs = split(/&/, $buffer);
foreach $pair (@pairs)
{
  ($name, $value) = split(/=/, $pair);
  $value =~ tr/+/ /;
  $value =~ s/%(..)/pack("C", hex($1))/eg;
  $FORM{$name} = $value;
}

# load configuration
$conffile = "/usr/local/etc/mm3d/mm3d.ini";
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
$datafile = "$dir_log/mm3d.log";
$lockfile = "$dir_lck/mm3d.lock";
open DATA, "< $datafile" or die "ERROR: Cannot open log file!";
close DATA;

print "Content-type:text/html\r\n\r\n";

$serialnumber = $FORM{uid};
if ( $serialnumber eq $usr_uid )
{
  # check lockfile
  while (-e $lockfile)
  {
    sleep 1;
  }
  if ( $FORM{value} eq '0' )
  {
    print "$contname\n";
    print "$contversion\n";
    exit 0;
  }
  if ( $FORM{value} eq '1' )
  {
    print "$usr_nam\n";
    print "$usr_dt1\n";
    print "$usr_dt2\n";
    print "$usr_dt3\n";
    exit 0;
  }
  if ( $FORM{value} eq '2' )
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
      last;
    }
    close DATA;
  }
}
exit 0;
