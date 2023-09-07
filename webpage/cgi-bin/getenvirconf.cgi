#!/usr/bin/perl
# +----------------------------------------------------------------------------+
# | MM3D v0.9 * Growing house controlling and remote monitoring system         |
# | Copyright (C) 2018-2023 Pozsár Zsolt <pozsarzs@gmail.com>                  |
# | getenvirconf.cgi                                                           |
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
use 5.010;
use Config::Tiny;
use Data::Dumper qw(Dumper);

# load configuration
#my $conffile = "/etc/mm3d/mm3d.ini";
my $conffile = "/usr/local/etc/mm3d/mm3d.ini";
my $row;
my $usr_dt1;
my $usr_dt3;
my $dir_msg;
my $dir_shr;
my $lang;
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
    case "usr_dt1" { $usr_dt1 = $columns[1]; }
    case "usr_dt3" { $usr_dt3 = $columns[1]; }
    case "lng" { $lang = $columns[1]; }
    case "dir_msg" { $dir_msg = $columns[1]; }
    case "dir_shr" { $dir_shr = $columns[1]; }
  }
}
close CONF;

# load messages
my $msg01 = "MM3D - controlling and monitoring system";
my $msg29 = "To set environment characteristic, please login into unit via SSH, and use <i>mm3d-editenvirconf</i> command!";
my $msg30 = "Environment characteristic";
my $msg31 = "Growing hyphae";
my $msg32 = "Growing mushroom";
my $msg33 = "heater";
my $msg34 = "humidifier";
my $msg35 = "ventilator";
my $msg36 = "lamp";
my $msg37 = "on";
my $msg38 = "off";
my $msg39 = "minimum";
my $msg40 = "maximum";
my $msg41 = "disable power on";
my $msg42 = "timed";
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
    case "msg29" { $msg29 = $columns[1]; }
    case "msg30" { $msg30 = $columns[1]; }
    case "msg31" { $msg31 = $columns[1]; }
    case "msg32" { $msg32 = $columns[1]; }
    case "msg33" { $msg33 = $columns[1]; }
    case "msg34" { $msg34 = $columns[1]; }
    case "msg35" { $msg35 = $columns[1]; }
    case "msg36" { $msg36 = $columns[1]; }
    case "msg37" { $msg37 = $columns[1]; }
    case "msg38" { $msg38 = $columns[1]; }
    case "msg39" { $msg39 = $columns[1]; }
    case "msg40" { $msg40 = $columns[1]; }
    case "msg41" { $msg41 = $columns[1]; }
    case "msg42" { $msg42 = $columns[1]; }
  }
}
close MSG;

# create output
my $footerfile = "$dir_shr/footer_$lang.html";
my $headerfile = "$dir_shr/header_$lang.html";
#my $envirconffile = "/etc/mm3d/envir.ini";
my $envirconffile = "/usr/local/etc/mm3d/envir.ini";
my $config = Config::Tiny->read( $envirconffile, 'utf8' );
my $section;
my $v;
print "Content-type:text/html\r\n\r\n";
open HEADER, $headerfile;
while (<HEADER>)
{
  chomp;
  print "$_";
}
close HEADER;
# growing hyphae
$section = "hyphae";
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
print "    <b class=\"title1\">$msg30</b><br>";
print "    <br>";
print "    <br>";
print "    <b class=\"title2\">$msg31</b><br>";
print "    <br>";
print "    <table cellspacing=\"0\" border=\"1\">";
print "      <colgroup width=\"115\"></colgroup>";
print "      <colgroup span=\"10\" width=\"55\"></colgroup>";
print "      <tr>";
print "        <td align=\"center\"><b><br></b></td>";
print "        <td colspan=2 align=\"center\"><b>$msg33</b></td>";
print "        <td colspan=2 align=\"center\"><b>$msg34</b></td>";
print "        <td colspan=6 align=\"center\"><b>$msg35</b></td>";
print "        <td colspan=2 align=\"center\"><b>$msg36</b></td>";
print "      </tr>";
print "      <tr>";
print "        <td align=\"left\" valign=top><b>$msg37</b></td>";
print "        <td align=\"center\">$config->{$section}{heater_on}<br></td>";
print "        <td align=\"center\">°C</td>";
print "        <td align=\"center\">$config->{$section}{humidifier_on}<br></td>";
print "        <td align=\"center\">%</td>";
print "        <td align=\"center\">$config->{$section}{vent_on}<br></td>";
print "        <td align=\"center\">m<br></td>";
print "        <td class=\"empty\" colspan=2 rowspan=4 align=\"center\"><br></td>";
print "        <td class=\"empty\" colspan=2 rowspan=4 align=\"center\"><br></td>";
print "        <td align=\"center\">$config->{$section}{light_on1}<br></td>";
print "        <td align=\"center\">h<br></td>";
print "      </tr>";
print "      <tr>";
print "        <td align=\"left\"><b>$msg38</b></td>";
print "        <td align=\"center\">$config->{$section}{heater_off}<br></td>";
print "        <td align=\"center\">°C</td>";
print "        <td align=\"center\">$config->{$section}{humidifier_off}<br></td>";
print "        <td align=\"center\">%</td>";
print "        <td align=\"center\">$config->{$section}{vent_off}<br></td>";
print "        <td align=\"center\">m<br></td>";
print "        <td align=\"center\">$config->{$section}{light_off1}<br></td>";
print "        <td align=\"center\">h<br></td>";
print "      </tr>";
print "      <tr>";
print "        <td align=\"left\"><b>$msg37</b></td>";
print "        <td class=\"empty\" colspan=2 rowspan=2 align=\"center\"><br></td>";
print "        <td class=\"empty\" colspan=2 rowspan=2 align=\"center\"><br></td>";
print "        <td class=\"empty\" colspan=2 rowspan=2 align=\"center\"><br></td>";
print "        <td align=\"center\">$config->{$section}{light_on2}<br></td>";
print "        <td align=\"center\">h<br></td>";
print "      </tr>";
print "      <tr>";
print "        <td align=\"left\"><b>$msg38</b></td>";
print "        <td align=\"center\">$config->{$section}{light_off2}<br></td>";
print "        <td align=\"center\">h<br></td>";
print "      </tr>";
print "      <tr>";
print "        <td align=\"left\"><b>$msg39</b></td>";
print "        <td align=\"center\">$config->{$section}{temperature_min}<br></td>";
print "        <td align=\"center\">°C</td>";
print "        <td align=\"center\">$config->{$section}{humidity_min}<br></td>";
print "        <td align=\"center\">%</td>";
print "        <td class=\"empty\" colspan=2 rowspan=2 align=\"center\"><br></td>";
print "        <td class=\"empty\" colspan=2 rowspan=2 align=\"center\"><br></td>";
print "        <td class=\"empty\" colspan=2 rowspan=2 align=\"center\"><br></td>";
print "        <td class=\"empty\" colspan=2 rowspan=2 align=\"center\"><br></td>";
print "      </tr>";
print "      <tr>";
print "        <td align=\"left\"><b>$msg40</b></td>";
print "        <td align=\"center\">$config->{mushroom}{temperature_max}<br></td>";
print "        <td align=\"center\">°C</td>";
print "        <td align=\"center\">$config->{mushroom}{humidity_max}<br></td>";
print "        <td align=\"center\">%</td>";
print "      </tr>";
print "      <tr>";
print "        <td rowspan=26 align=\"center\"><b>$msg41</b></td>";
print "        <td colspan=2 align=\"center\"><i>$msg42</i></td>";
print "        <td colspan=2 align=\"center\"><i>$msg42</i></td>";
print "        <td colspan=2 align=\"center\"><i>$msg42</i></td>";
print "        <td colspan=2 align=\"center\"><i>< $config->{$section}{vent_lowtemp} °C</i></td>";
print "        <td colspan=2 align=\"center\"><i>> $config->{$section}{vent_hightemp} °C</i></td>";
print "        <td class=\"empty\" colspan=2 rowspan=25 align=\"center\"><br></td>";
print "      </tr>";
my @i = (0..23);
for (@i)
{
  print "      <tr>";
  print "        <td align=\"center\">$_</td>";
  $v = "heater_disable_" . sprintf ("%02d",$_);
  print "        <td align=\"center\">$config->{$section}{$v}<br></td>";
  print "        <td align=\"center\">$_</td>";
  $v = "humidifier_disable_" . sprintf ("%02d",$_);
  print "        <td align=\"center\">$config->{$section}{$v}<br></td>";
  print "        <td align=\"center\">$_</td>";
  $v = "vent_disable_" . sprintf ("%02d",$_);
  print "        <td align=\"center\">$config->{$section}{$v}<br></td>";
  print "        <td align=\"center\">$_</td>";
  $v = "vent_disablelowtemp_" . sprintf ("%02d",$_);
  print "        <td align=\"center\">$config->{$section}{$v}<br></td>";
  print "        <td align=\"center\">$_</td>";
  $v = "vent_disablehightemp_" . sprintf ("%02d",$_);
  print "        <td align=\"center\">$config->{$section}{$v}<br></td>";
  print "      </tr>";
}
print "    </table>";
print "    <br>";
print "    <br>";
# growing mushroom
$section = "mushroom";
print "    <b class=\"title2\">$msg32</b><br>";
print "    <br>";
print "    <table cellspacing=\"0\" border=\"1\">";
print "      <colgroup width=\"115\"></colgroup>";
print "      <colgroup span=\"10\" width=\"55\"></colgroup>";
print "      <tr>";
print "        <td align=\"center\"><b><br></b></td>";
print "        <td colspan=2 align=\"center\"><b>$msg33</b></td>";
print "        <td colspan=2 align=\"center\"><b>$msg34</b></td>";
print "        <td colspan=6 align=\"center\"><b>$msg35</b></td>";
print "        <td colspan=2 align=\"center\"><b>$msg36</b></td>";
print "      </tr>";
print "      <tr>";
print "        <td align=\"left\" valign=top><b>$msg37</b></td>";
print "        <td align=\"center\">$config->{$section}{heater_on}<br></td>";
print "        <td align=\"center\">°C</td>";
print "        <td align=\"center\">$config->{$section}{humidifier_on}<br></td>";
print "        <td align=\"center\">%</td>";
print "        <td align=\"center\">$config->{$section}{vent_on}<br></td>";
print "        <td align=\"center\">m<br></td>";
print "        <td class=\"empty\" colspan=2 rowspan=4 align=\"center\"><br></td>";
print "        <td class=\"empty\" colspan=2 rowspan=4 align=\"center\"><br></td>";
print "        <td align=\"center\">$config->{$section}{light_on1}<br></td>";
print "        <td align=\"center\">h<br></td>";
print "      </tr>";
print "      <tr>";
print "        <td align=\"left\"><b>$msg38</b></td>";
print "        <td align=\"center\">$config->{$section}{heater_off}<br></td>";
print "        <td align=\"center\">°C</td>";
print "        <td align=\"center\">$config->{$section}{humidifier_off}<br></td>";
print "        <td align=\"center\">%</td>";
print "        <td align=\"center\">$config->{$section}{vent_off}<br></td>";
print "        <td align=\"center\">m<br></td>";
print "        <td align=\"center\">$config->{$section}{light_off1}<br></td>";
print "        <td align=\"center\">h<br></td>";
print "      </tr>";
print "      <tr>";
print "        <td align=\"left\"><b>$msg37</b></td>";
print "        <td class=\"empty\" colspan=2 rowspan=2 align=\"center\"><br></td>";
print "        <td class=\"empty\" colspan=2 rowspan=2 align=\"center\"><br></td>";
print "        <td class=\"empty\" colspan=2 rowspan=2 align=\"center\"><br></td>";
print "        <td align=\"center\">$config->{$section}{light_on2}<br></td>";
print "        <td align=\"center\">h<br></td>";
print "      </tr>";
print "      <tr>";
print "        <td align=\"left\"><b>$msg38</b></td>";
print "        <td align=\"center\">$config->{$section}{light_off2}<br></td>";
print "        <td align=\"center\">h<br></td>";
print "      </tr>";
print "      <tr>";
print "        <td align=\"left\"><b>$msg39</b></td>";
print "        <td align=\"center\">$config->{$section}{temperature_min}<br></td>";
print "        <td align=\"center\">°C</td>";
print "        <td align=\"center\">$config->{$section}{humidity_min}<br></td>";
print "        <td align=\"center\">%</td>";
print "        <td class=\"empty\" colspan=2 rowspan=2 align=\"center\"><br></td>";
print "        <td class=\"empty\" colspan=2 rowspan=2 align=\"center\"><br></td>";
print "        <td class=\"empty\" colspan=2 rowspan=2 align=\"center\"><br></td>";
print "        <td class=\"empty\" colspan=2 rowspan=2 align=\"center\"><br></td>";
print "      </tr>";
print "      <tr>";
print "        <td align=\"left\"><b>$msg40</b></td>";
print "        <td align=\"center\">$config->{mushroom}{temperature_max}<br></td>";
print "        <td align=\"center\">°C</td>";
print "        <td align=\"center\">$config->{mushroom}{humidity_max}<br></td>";
print "        <td align=\"center\">%</td>";
print "      </tr>";
print "      <tr>";
print "        <td rowspan=26 align=\"center\"><b>$msg41</b></td>";
print "        <td colspan=2 align=\"center\"><i>$msg42</i></td>";
print "        <td colspan=2 align=\"center\"><i>$msg42</i></td>";
print "        <td colspan=2 align=\"center\"><i>$msg42</i></td>";
print "        <td colspan=2 align=\"center\"><i>< $config->{$section}{vent_lowtemp} °C</i></td>";
print "        <td colspan=2 align=\"center\"><i>> $config->{$section}{vent_hightemp} °C</i></td>";
print "        <td class=\"empty\" colspan=2 rowspan=25 align=\"center\"><br></td>";
print "      </tr>";
my @i = (0..23);
for (@i)
{
  print "      <tr>";
  print "        <td align=\"center\">$_</td>";
  $v = "heater_disable_" . sprintf ("%02d",$_);
  print "        <td align=\"center\">$config->{$section}{$v}<br></td>";
  print "        <td align=\"center\">$_</td>";
  $v = "humidifier_disable_" . sprintf ("%02d",$_);
  print "        <td align=\"center\">$config->{$section}{$v}<br></td>";
  print "        <td align=\"center\">$_</td>";
  $v = "vent_disable_" . sprintf ("%02d",$_);
  print "        <td align=\"center\">$config->{$section}{$v}<br></td>";
  print "        <td align=\"center\">$_</td>";
  $v = "vent_disablelowtemp_" . sprintf ("%02d",$_);
  print "        <td align=\"center\">$config->{$section}{$v}<br></td>";
  print "        <td align=\"center\">$_</td>";
  $v = "vent_disablehightemp_" . sprintf ("%02d",$_);
  print "        <td align=\"center\">$config->{$section}{$v}<br></td>";
  print "      </tr>";
}
print "    </table>";
print "    <br>";
print "    $msg29";
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
