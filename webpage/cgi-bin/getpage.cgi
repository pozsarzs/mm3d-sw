#!/usr/bin/perl
# +----------------------------------------------------------------------------+
# | MM3D v0.4 * Growing house controlling and remote monitoring system         |
# | Copyright (C) 2018-2019 Pozsár Zsolt <pozsar.zsolt@.szerafingomba.hu>      |
# | getpage.cgi                                                                |
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

$dark="<img src=\"/pics/dark.png\">";
$green="<img src=\"/pics/green.png\">";
$red="<img src=\"/pics/red.png\">";
$yellow="<img src=\"/pics/yellow.png\">";

# create diagram pictures
system("/usr/local/bin/mm3d-creatediagrams");

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
    case "lng" { $lang = $columns[1]; }
    case "dir_htm" { $dir_htm = $columns[1]; }
    case "dir_lck" { $dir_lck = $columns[1]; }
    case "dir_log" { $dir_log = $columns[1]; }
    case "dir_msg" { $dir_msg = $columns[1]; }
    case "dir_shr" { $dir_shr = $columns[1]; }
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
    case "usr_dt3" { $usr_dt3 = $columns[1]; }
    case "web_lines" { $web_lines = $columns[1]; }
  }
}
close CONF;

# load messages
$msg01 = "MM3D - controlling and monitoring system";
$msg04 = "Site";
$msg05 = "House";
$msg06 = "Names";
$msg07 = "Input";
$msg08 = "Output";
$msg09 = "Error light";
$msg12 = "Date";
$msg13 = "Time";
$msg14 = "T";
$msg15 = "RH";
$msg16 = "In";
$msg17 = "Out";
$msg18 = "Err";
$msg19 = "Refresh";
$msg20 = "Latest status";
$msg21 = "Log";
$msg22 = "";
$msg23 = "If you want to see full log, please login to unit via SSH, and use <i>mm3d-viewlog</i> command.";

$msgfile = "$dir_msg/$lang/mm3d.msg";
open MSG, "< $msgfile";
while(<MSG>)
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
    case "msg01" { $msg01 = $columns[1]; }
    case "msg04" { $msg04 = $columns[1]; }
    case "msg05" { $msg05 = $columns[1]; }
    case "msg06" { $msg06 = $columns[1]; }
    case "msg07" { $msg07 = $columns[1]; }
    case "msg08" { $msg08 = $columns[1]; }
    case "msg09" { $msg09 = $columns[1]; }
    case "msg12" { $msg12 = $columns[1]; }
    case "msg13" { $msg13 = $columns[1]; }
    case "msg14" { $msg14 = $columns[1]; }
    case "msg15" { $msg15 = $columns[1]; }
    case "msg16" { $msg16 = $columns[1]; }
    case "msg17" { $msg17 = $columns[1]; }
    case "msg18" { $msg18 = $columns[1]; }
    case "msg19" { $msg19 = $columns[1]; }
    case "msg20" { $msg20 = $columns[1]; }
    case "msg21" { $msg21 = $columns[1]; }
    case "msg22" { $msg22 = $columns[1]; }
    case "msg23" { $msg23 = $columns[1]; }
  }
}
close MSG;

# create output
$datafile = "$dir_log/mm3d.log";
$footerfile = "$dir_shr/footer_$lang.html";
$headerfile = "$dir_shr/header_$lang.html";
$lockfile = "$dir_lck/mm3d.lock";
open DATA, "< $datafile" or die "ERROR: Cannot open log file!";
close DATA;

print "Content-type:text/html\r\n\r\n";
open HEADER, $headerfile;
while (<HEADER>)
{
  chomp;
  print "$_";
}
close HEADER;

# check lockfile
while (-e $lockfile)
{
  sleep 1;
}

# write body
print "    <table border=\"0\" cellspacing=\"0\" cellpadding=\"6\" width=\"100%\">";
print "      <tbody>";
print "        <tr>";
print "          <td colspan=\"2\" class=\"header\" align=\"center\">";
print "            <b class=\"title0\">$usr_dt1 - $usr_dt3</b>";
print "          </td>";
print "        </tr>";
print "      </tbody>";
print "    </table>";
print "    <br>";
print "    <b class=\"title1\">$msg06</b><br>";
print "    <br>";
print "    <table border=\"0\" cellpadding=\"3\" cellspacing=\"0\">";
print "      <tbody>";
print "        <tr>";
print "          <td><b>$msg07 #1:</b></td><td>$nam_in1</td> <td>&nbsp;&nbsp;&nbsp;</td>";
print "          <td><b>$msg08 #1:</b></td><td>$nam_out1</td><td>&nbsp;&nbsp;&nbsp;</td>";
print "          <td><b>$msg09 #1:</b></td><td>$nam_err1</td>";
print "        </tr>";
print "        <tr>";
print "          <td><b>$msg07 #2:</b></td><td>$nam_in2</td> <td>&nbsp;&nbsp;&nbsp;</td>";
print "          <td><b>$msg08 #2:</b></td><td>$nam_out2</td><td>&nbsp;&nbsp;&nbsp;</td>";
print "          <td><b>$msg09 #2:</b></td><td>$nam_err2</td>";
print "        </tr>";
print "        <tr>";
print "          <td><b>$msg07 #3:</b></td><td>$nam_in3</td> <td>&nbsp;&nbsp;&nbsp;</td>";
print "          <td><b>$msg08 #3:</b></td><td>$nam_out3</td><td>&nbsp;&nbsp;&nbsp;</td>";
print "          <td><b>$msg09 #3:</b></td><td>$nam_err3</td>";
print "        </tr>";
print "        <tr>";
print "          <td><b>$msg07 #4:</b></td><td>$nam_in4</td> <td>&nbsp;&nbsp;&nbsp;</td>";
print "          <td><b>$msg08 #4:</b></td><td>$nam_out4</td><td>&nbsp;&nbsp;&nbsp;</td>";
print "          <td><b>$msg09 #4:</b></td><td>$nam_err4</td>";
print "        </tr>";
print "      </tbody>";
print "    </table>";
print "    <br>";
print "    <b class=\"title1\">$msg20</b><br>";
print "    <br>";
print "    <table border=\"1\" cellpadding=\"3\" cellspacing=\"0\" width=\"100%\">";
print "      <tbody>";
print "        <tr>";
print "          <th>$msg12</th><th>$msg13</th><th>$msg14</th><th>$msg15</th>";
print "          <th>$msg16 #1</th><th>$msg16 #2</th><th>$msg16 #3</th><th>$msg16 #4</th>";
print "          <th>$msg17 #1</th><th>$msg17 #2</th><th>$msg17 #3</th><th>$msg17 #4</th>";
print "          <th>$msg18 #1</th><th>$msg18 #2</th><th>$msg18 #3</th><th>$msg18 #4</th>";
print "        </tr>";

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
  print "        <tr align=\"center\">";
  print "          <td>$columns[0]</td>";
  print "          <td>$columns[1]</td>";
  print "          <td>$columns[2] &deg;C</td>";
  print "          <td>$columns[3] %</td>";
  if ($columns[4] eq 1) { $columns[4] = $green } else { $columns[4] = $dark };
  if ($columns[5] eq 1) { $columns[5] = $green } else { $columns[5] = $dark };
  if ($columns[6] eq 1) { $columns[6] = $green } else { $columns[6] = $dark };
  if ($columns[7] eq 1) { $columns[7] = $green } else { $columns[7] = $dark };
  if ($columns[8] eq 1) { $columns[8] = $yellow } else { $columns[8] = $dark };
  if ($columns[9] eq 1) { $columns[9] = $yellow } else { $columns[9] = $dark };
  if ($columns[10] eq 1) { $columns[10] = $yellow } else { $columns[10] = $dark };
  if ($columns[11] eq 1) { $columns[11] = $yellow } else { $columns[11] = $dark };
  if ($columns[12] eq 1) { $columns[12] = $red } else { $columns[12] = $dark };
  if ($columns[13] eq 1) { $columns[13] = $red } else { $columns[13] = $dark };
  if ($columns[14] eq 1) { $columns[14] = $red } else { $columns[14] = $dark };
  if ($columns[15] eq 1) { $columns[15] = $red } else { $columns[15] = $dark };
  print "          <td>$columns[4]</td>";
  print "          <td>$columns[5]</td>";
  print "          <td>$columns[6]</td>";
  print "          <td>$columns[7]</td>";
  print "          <td>$columns[8]</td>";
  print "          <td>$columns[9]</td>";
  print "          <td>$columns[10]</td>";
  print "          <td>$columns[11]</td>";
  print "          <td>$columns[12]</td>";
  print "          <td>$columns[13]</td>";
  print "          <td>$columns[14]</td>";
  print "          <td>$columns[15]</td>";
  print "        </tr>";
  last;
}
close DATA;
print "      </tbody>";
print "    </table>";
print "    <br>";
print "    <form action=\"getpage.cgi\" method=\"get\">";
print "      <center>";
print "        <input value=\"$msg19\" type=\"submit\" width=\"100\" style=\"width:100px\">";
print "      </center>";
print "    </form>";
print "    <hr>";
print "    <br>";
print "    <b class=\"title1\">$msg21</b><br>";
print "    <br>";
print "    <br>";
print "    <table border=\"1\" cellpadding=\"3\" cellspacing=\"0\" width=\"100%\">";
print "      <tbody>";
print "        <tr>";
print "          <td><img src=\"/pics/temperature.png\" width=\"100%\"></td>";
print "          <td><img src=\"/pics/humidity.png\" width=\"100%\"></td>";
print "        </tr>";
print "      </tbody>";
print "    </table>";
print "    <br>";
print "    <table border=\"1\" cellpadding=\"3\" cellspacing=\"0\" width=\"100%\">";
print "      <tbody>";
print "        <tr>";
print "          <th>$msg12</th><th>$msg13</th><th>$msg14</th><th>$msg15</th>";
print "          <th>$msg16 #1</th><th>$msg16 #2</th><th>$msg16 #3</th><th>$msg16 #4</th>";
print "          <th>$msg17 #1</th><th>$msg17 #2</th><th>$msg17 #3</th><th>$msg17 #4</th>";
print "          <th>$msg18 #1</th><th>$msg18 #2</th><th>$msg18 #3</th><th>$msg18 #4</th>";
print "        </tr>";

$line = 0;
open DATA, "< $datafile" or die "Cannot open log file!";
while (<DATA>)
{
  chop;
  my(@columns) = split(",");
  my($colnum) = $#columns;
  $row = "";
  foreach $colnum (@columns)
  {
    $row = $row . $colnum;
  }
  my(@datarow) = split("\"\"",$row);
  my($datarownum) = $#datarow;
  print "        <tr align=\"center\">";
  print "          <td>$columns[0]</td>";
  print "          <td>$columns[1]</td>";
  print "          <td>$columns[2] &deg;C</td>";
  print "          <td>$columns[3] %</td>";
  if ($columns[4] eq 1) { $columns[4] = $green } else { $columns[4] = $dark };
  if ($columns[5] eq 1) { $columns[5] = $green } else { $columns[5] = $dark };
  if ($columns[6] eq 1) { $columns[6] = $green } else { $columns[6] = $dark };
  if ($columns[7] eq 1) { $columns[7] = $green } else { $columns[7] = $dark };
  if ($columns[8] eq 1) { $columns[8] = $yellow } else { $columns[8] = $dark };
  if ($columns[9] eq 1) { $columns[9] = $yellow } else { $columns[9] = $dark };
  if ($columns[10] eq 1) { $columns[10] = $yellow } else { $columns[10] = $dark };
  if ($columns[11] eq 1) { $columns[11] = $yellow } else { $columns[11] = $dark };
  if ($columns[12] eq 1) { $columns[12] = $red } else { $columns[12] = $dark };
  if ($columns[13] eq 1) { $columns[13] = $red } else { $columns[13] = $dark };
  if ($columns[14] eq 1) { $columns[14] = $red } else { $columns[14] = $dark };
  if ($columns[15] eq 1) { $columns[15] = $red } else { $columns[15] = $dark };
  print "          <td>$columns[4]</td>";
  print "          <td>$columns[5]</td>";
  print "          <td>$columns[6]</td>";
  print "          <td>$columns[7]</td>";
  print "          <td>$columns[8]</td>";
  print "          <td>$columns[9]</td>";
  print "          <td>$columns[10]</td>";
  print "          <td>$columns[11]</td>";
  print "          <td>$columns[12]</td>";
  print "          <td>$columns[13]</td>";
  print "          <td>$columns[14]</td>";
  print "          <td>$columns[15]</td>";
  print "        </tr>";
  $line = $line + 1;
  if ($line eq $web_lines) { last };
}
close DATA;
print "      </tbody>";
print "    </table>";
print "    <br>";
print "    $msg23";
print "    <br>";

# write footer
open FOOTER, $footerfile;
while (<FOOTER>)
{
  chomp;
  print "$_";
}
close FOOTER;
exit 0;
