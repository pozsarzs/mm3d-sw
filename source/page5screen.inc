{ +--------------------------------------------------------------------------+ }
{ | MM3D v0.4 * Growing house controlling and remote monitoring system       | }
{ | Copyright (C) 2018-2019 Pozsár Zsolt <pozsar.zsolt@.szerafingomba.hu>    | }
{ | page5screen.inc                                                          | }
{ | Show screen content of page #5                                           | }
{ +--------------------------------------------------------------------------+ }

//   This program is free software: you can redistribute it and/or modify it
// under the terms of the European Union Public License 1.1 version.
//
//   This program is distributed in the hope that it will be useful, but WITHOUT
// ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
// FOR A PARTICULAR PURPOSE.

procedure page5screen;
begin
  header('EditEnvirConf '+VERSION+' * Page 5/8: Growing mushroom - humidifying');
  textcolor(white);
  gotoxy(4,3); writeln('Minimal relative humidity (0-99):');
  gotoxy(4,4); writeln('RH when humidifier switch on (0-99):');
  gotoxy(4,5); writeln('RH when humidifier switch off (0-99):');
  gotoxy(4,6); writeln('Maximal relative humidity (0-99):');
  if mhummin>9 then gotoxy(45,3) else gotoxy(46,3); writeln(mhummin,' %');
  if mhumon>9 then gotoxy(45,4) else gotoxy(46,4); writeln(mhumon,' %');
  if mhumoff>9 then gotoxy(45,5) else gotoxy(46,5); writeln(mhumoff,' %');
  if mhummax>9 then gotoxy(45,6) else gotoxy(46,6); writeln(mhummax,' %');
  gotoxy(4,9); writeln('Disable humidifier (0/1):');
  gotoxy(4,10); writeln('00.00-00.59  ',mhumdis[0]);
  gotoxy(4,11); writeln('01.00-01.59  ',mhumdis[1]);
  gotoxy(4,12); writeln('02.00-02.59  ',mhumdis[2]);
  gotoxy(4,13); writeln('03.00-03.59  ',mhumdis[3]);
  gotoxy(4,14); writeln('04.00-04.59  ',mhumdis[4]);
  gotoxy(4,15); writeln('05.00-05.59  ',mhumdis[5]);
  gotoxy(4,16); writeln('06.00-06.59  ',mhumdis[6]);
  gotoxy(4,17); writeln('07.00-07.59  ',mhumdis[7]);
  gotoxy(4,18); writeln('08.00-08.59  ',mhumdis[8]);
  gotoxy(4,19); writeln('09.00-09.59  ',mhumdis[9]);
  gotoxy(4,20); writeln('10.00-10.59  ',mhumdis[10]);
  gotoxy(4,21); writeln('11.00-11.59  ',mhumdis[11]);
  gotoxy(22,10); writeln('12.00-12.59  ',mhumdis[12]);
  gotoxy(22,11); writeln('13.00-13.59  ',mhumdis[13]);
  gotoxy(22,12); writeln('14.00-14.59  ',mhumdis[14]);
  gotoxy(22,13); writeln('15.00-15.59  ',mhumdis[15]);
  gotoxy(22,14); writeln('16.00-16.59  ',mhumdis[16]);
  gotoxy(22,15); writeln('17.00-17.59  ',mhumdis[17]);
  gotoxy(22,16); writeln('18.00-18.59  ',mhumdis[18]);
  gotoxy(22,17); writeln('19.00-19.59  ',mhumdis[19]);
  gotoxy(22,18); writeln('20.00-20.59  ',mhumdis[20]);
  gotoxy(22,19); writeln('21.00-21.59  ',mhumdis[21]);
  gotoxy(22,20); writeln('22.00-22.59  ',mhumdis[22]);
  gotoxy(22,21); writeln('23.00-23.59  ',mhumdis[23]);
end;
