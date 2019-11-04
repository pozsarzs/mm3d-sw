{ +--------------------------------------------------------------------------+ }
{ | MM3D v0.4 * Growing house controlling and remote monitoring system       | }
{ | Copyright (C) 2018-2019 Pozsár Zsolt <pozsar.zsolt@.szerafingomba.hu>    | }
{ | page6screen.inc                                                          | }
{ | Show screen content of page #6                                           | }
{ +--------------------------------------------------------------------------+ }

//   This program is free software: you can redistribute it and/or modify it
// under the terms of the European Union Public License 1.1 version.
//
//   This program is distributed in the hope that it will be useful, but WITHOUT
// ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
// FOR A PARTICULAR PURPOSE.

procedure page6screen;
begin
  header('EditEnvirConf '+VERSION+' * Page 6/8: Growing mushroom - heating');
  textcolor(white);
  gotoxy(4,3); writeln('Minimal temperature:');
  gotoxy(4,4); writeln('Heating switch-on temperature:');
  gotoxy(4,5); writeln('Heating switch-off temperature:');
  gotoxy(4,6); writeln('Maximal temperature:');
  if mtempmin>9 then gotoxy(45,3) else gotoxy(46,3); writeln(mtempmin,' °C');
  if mtempon>9 then gotoxy(45,4) else gotoxy(46,4); writeln(mtempon,' °C');
  if mtempoff>9 then gotoxy(45,5) else gotoxy(46,5); writeln(mtempoff,' °C');
  if mtempmax>9 then gotoxy(45,6) else gotoxy(46,6); writeln(mtempmax,' °C');
  gotoxy(4,9); writeln('Disable heater (0/1):');
  gotoxy(4,10); writeln(' 0.00...0.59 ',mheaterdis[0]);
  gotoxy(4,11); writeln(' 1.00...1.59 ',mheaterdis[1]);
  gotoxy(4,12); writeln(' 2.00...2.59 ',mheaterdis[2]);
  gotoxy(4,13); writeln(' 3.00...3.59 ',mheaterdis[3]);
  gotoxy(4,14); writeln(' 4.00...4.59 ',mheaterdis[4]);
  gotoxy(4,15); writeln(' 5.00...5.59 ',mheaterdis[5]);
  gotoxy(4,16); writeln(' 6.00...6.59 ',mheaterdis[6]);
  gotoxy(4,17); writeln(' 7.00...7.59 ',mheaterdis[7]);
  gotoxy(4,18); writeln(' 8.00...8.59 ',mheaterdis[8]);
  gotoxy(4,19); writeln(' 9.00...9.59 ',mheaterdis[9]);
  gotoxy(4,20); writeln('10.00..10.59 ',mheaterdis[10]);
  gotoxy(4,21); writeln('11.00..11.59 ',mheaterdis[11]);
  gotoxy(22,10); writeln('12.00..12.59 ',mheaterdis[12]);
  gotoxy(22,11); writeln('13.00..13.59 ',mheaterdis[13]);
  gotoxy(22,12); writeln('14.00..14.59 ',mheaterdis[14]);
  gotoxy(22,13); writeln('15.00..15.59 ',mheaterdis[15]);
  gotoxy(22,14); writeln('16.00..16.59 ',mheaterdis[16]);
  gotoxy(22,15); writeln('17.00..17.59 ',mheaterdis[17]);
  gotoxy(22,16); writeln('18.00..18.59 ',mheaterdis[18]);
  gotoxy(22,17); writeln('19.00..19.59 ',mheaterdis[19]);
  gotoxy(22,18); writeln('20.00..20.59 ',mheaterdis[20]);
  gotoxy(22,19); writeln('21.00..21.59 ',mheaterdis[21]);
  gotoxy(22,20); writeln('22.00..22.59 ',mheaterdis[22]);
  gotoxy(22,21); writeln('23.00..23.59 ',mheaterdis[23]);
end;
