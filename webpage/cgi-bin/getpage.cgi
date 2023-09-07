#!/usr/bin/perl
# +----------------------------------------------------------------------------+
# | MM3D v0.9 * Growing house controlling and remote monitoring system         |
# | Copyright (C) 2018-2023 Pozsár Zsolt <pozsarzs@gmail.com>                  |
# | getpage.cgi                                                                |
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

my $dark="<img src=\"/pics/dark.png\">";
my $green="<img src=\"/pics/green.png\">";
my $red="<img src=\"/pics/red.png\">";
my $yellow="<img src=\"/pics/yellow.png\">";

# create diagram pictures
#system("/usr/bin/mm3d-creatediagrams");
system("/usr/local/bin/mm3d-creatediagrams");

# load configuration
#my $conffile = "/etc/mm3d/mm3d.ini";
my $conffile = "/usr/local/etc/mm3d/mm3d.ini";
my $row;
my $cam1_enable;
my $cam2_enable;
my $cam_show;
my $dir_htm;
my $dir_lck;
my $dir_log;
my $dir_msg;
my $dir_shr;
my $dir_var;
my $lang;
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
my $usr_dt1;
my $usr_dt3;
my $web_lines;
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
    case "cam1_enable" { $cam1_enable = $columns[1]; }
    case "cam2_enable" { $cam2_enable = $columns[1]; }
    case "cam_show" { $cam_show = $columns[1]; }
    case "dir_htm" { $dir_htm = $columns[1]; }
    case "dir_lck" { $dir_lck = $columns[1]; }
    case "dir_log" { $dir_log = $columns[1]; }
    case "dir_msg" { $dir_msg = $columns[1]; }
    case "dir_shr" { $dir_shr = $columns[1]; }
    case "dir_var" { $dir_var = $columns[1]; }
    case "lng" { $lang = $columns[1]; }
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
my $msg01 = "MM3D - controlling and monitoring system";
my $msg04 = "Site";
my $msg05 = "House";
my $msg06 = "Names";
my $msg07 = "Input";
my $msg08 = "Output";
my $msg09 = "Error light";
my $msg12 = "Date";
my $msg13 = "Time";
my $msg14 = "T";
my $msg15 = "RH";
my $msg16 = "In";
my $msg17 = "Out";
my $msg18 = "Err";
my $msg19 = "Refresh";
my $msg20 = "Latest status";
my $msg21 = "Log";
my $msg22 = "Cameras";
my $msg23 = "If you want to see full log, please login into unit via SSH, and use <i>mm3d-viewlog</i> command.";
my $msg24 = "Override outputs";
my $msg25 = "neutral";
my $msg26 = "switched on";
my $msg27 = "switched off";
my $msg28 = "To set override, please login into unit via SSH, and use <i>mm3d-override</i> command!";
my $msg29 = "To set environment characteristic, please login into unit via SSH, and use <i>mm3d-editenvirconf</i> command!";
my $msgfile = "$dir_msg/$lang/mm3d.msg";
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
    case "msg24" { $msg24 = $columns[1]; }
    case "msg25" { $msg25 = $columns[1]; }
    case "msg26" { $msg26 = $columns[1]; }
    case "msg27" { $msg27 = $columns[1]; }
    case "msg28" { $msg28 = $columns[1]; }
    case "msg29" { $msg29 = $columns[1]; }
  }
}
close MSG;
$msg26 = "<font color=green>$msg26</font>";
$msg27 = "<font color=red>$msg27</font>";

# create output
my $datafile = "$dir_log/mm3d.log";
my $footerfile = "$dir_shr/footer_$lang.html";
my $headerfile = "$dir_shr/header_$lang.html";
my $lockfile = "$dir_lck/mm3d.lock";
my $out1file = "$dir_var/out1";
my $out2file = "$dir_var/out2";
my $out3file = "$dir_var/out3";
my $out4file = "$dir_var/out4";
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
while (-e $lockfile)
{
  sleep 1;
}
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
# names
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
print "    <hr>";
print "    <br>";
# latest status
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
print "    <br>";
print "    $msg29";
print "    <hr>";
print "    <br>";
# override
my $out1;
my $out2;
my $out3;
my $out4;
print "    <b class=\"title1\">$msg24</b><br>";
print "    <br>";
print "    <br>";
print "    <table border=\"0\" cellpadding=\"3\" cellspacing=\"0\">";
print "      <tbody>";
print "        <tr>";
print "          <td><b>$msg08 #1:</b></td>";
open DATA, "< $out1file" or $out1 = $msg25;
my $o1 = <DATA>;
close DATA;
if ($o1 eq "neutral") { $out1 = $msg25 };
if ($o1 eq "on") { $out1 = $msg26 };
if ($o1 eq "off") { $out1 = $msg27 };
print "          <td>$out1</td>";
print "        </tr>";
print "        <tr>";
print "          <td><b>$msg08 #2:</b></td>";
open DATA, "< $out2file" or $out2 = $msg25;
my $o2 = <DATA>;
close DATA;
if ($o2 eq "neutral") { $out2 = $msg25 };
if ($o2 eq "on") { $out2 = $msg26 };
if ($o2 eq "off") { $out2 = $msg27 };
print "          <td>$out2</td>";
print "        </tr>";
print "        <tr>";
print "          <td><b>$msg08 #3:</b></td>";
open DATA, "< $out3file" or $out3 = $msg25;
my $o3 = <DATA>;
close DATA;
if ($o3 eq "neutral") { $out3 = $msg25 };
if ($o3 eq "on") { $out3 = $msg26 };
if ($o3 eq "off") { $out3 = $msg27 };
print "          <td>$out3</td>";
print "        </tr>";
print "        <tr>";
print "          <td><b>$msg08 #4:</b></td>";
open DATA, "< $out4file" or $out4 = $msg25;
my $o4 = <DATA>;
close DATA;
if ($o4 eq "neutral") { $out4 = $msg25 };
if ($o4 eq "on") { $out4 = $msg26 };
if ($o4 eq "off") { $out4 = $msg27 };
print "          <td>$out4</td>";
print "        </tr>";
print "      </tbody>";
print "    </table>";
print "    <br>";
print "    $msg28";
print "    <hr>";
print "    <br>";
# section cameras
if ($cam_show eq 1)
{
  #system("/usr/bin/mm3d-getsnapshots");
  system("/usr/local/bin/mm3d-getsnapshots");
  print "    <b class=\"title1\">$msg22</b><br>";
  print "    <br>";
  print "    <br>";
  print "    <table border=\"1\" cellpadding=\"20\" cellspacing=\"0\" width=\"100%\">";
  print "      <tbody>";
  print "        <tr>";
  print "          <td width=\"50%\"><img src=\"/pics/camera1.jpg\" width=\"100%\"></td>";
  print "          <td width=\"50%\"><img src=\"/pics/camera2.jpg\" width=\"100%\"></td>";
  print "        </tr>";
  print "      </tbody>";
  print "    </table>";
  print "    <br>";
  print "    <hr>";
  print "    <br>";
}
# section log
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
my $line = 0;
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
