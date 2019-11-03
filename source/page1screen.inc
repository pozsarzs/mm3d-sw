{ +--------------------------------------------------------------------------+ }
{ | MM3D v0.4 * Growing house controlling and remote monitoring system       | }
{ | Copyright (C) 2018-2019 Pozsár Zsolt <pozsar.zsolt@.szerafingomba.hu>    | }
{ | page1screen.inc                                                          | }
{ | Show screen content of page #1                                           | }
{ +--------------------------------------------------------------------------+ }

//   This program is free software: you can redistribute it and/or modify it
// under the terms of the European Union Public License 1.1 version.
//
//   This program is distributed in the hope that it will be useful, but WITHOUT
// ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
// FOR A PARTICULAR PURPOSE.

procedure page1screen;
begin
  gotoxy(4,3);writeln('Minimal RH:');
  gotoxy(4,4);writeln('RH when humidifier switch on:');
  gotoxy(4,5);writeln('RH when humidifier switch off:');
  gotoxy(4,6);writeln('Maximal RH:');
  gotoxy(46,3);writeln(hhummin,' %');
  gotoxy(46,4);writeln(hhumon,' %');
  gotoxy(46,5);writeln(hhumoff,' %');
  gotoxy(46,6);writeln(hhummax,' %');
  gotoxy(2,8);writeln('Disable humidifier:');
  gotoxy(4,10);writeln('00.00-00.59  ',hhumdis[0]);
  gotoxy(4,11);writeln('01.00-01.59  ',hhumdis[1]);
  gotoxy(4,12);writeln('02.00-02.59  ',hhumdis[2]);
  gotoxy(4,13);writeln('03.00-03.59  ',hhumdis[3]);
  gotoxy(4,14);writeln('04.00-04.59  ',hhumdis[4]);
  gotoxy(4,15);writeln('05.00-05.59  ',hhumdis[5]);
  gotoxy(4,16);writeln('06.00-06.59  ',hhumdis[6]);
  gotoxy(4,17);writeln('07.00-07.59  ',hhumdis[7]);
  gotoxy(4,18);writeln('08.00-08.59  ',hhumdis[8]);
  gotoxy(4,19);writeln('09.00-09.59  ',hhumdis[9]);
  gotoxy(4,20);writeln('10.00-10.59  ',hhumdis[10]);
  gotoxy(4,21);writeln('11.00-11.59  ',hhumdis[11]);
  gotoxy(22,10);writeln('12.00-12.59  ',hhumdis[12]);
  gotoxy(22,11);writeln('13.00-13.59  ',hhumdis[13]);
  gotoxy(22,12);writeln('14.00-14.59  ',hhumdis[14]);
  gotoxy(22,13);writeln('15.00-15.59  ',hhumdis[15]);
  gotoxy(22,14);writeln('16.00-16.59  ',hhumdis[16]);
  gotoxy(22,15);writeln('17.00-17.59  ',hhumdis[17]);
  gotoxy(22,16);writeln('18.00-18.59  ',hhumdis[18]);
  gotoxy(22,17);writeln('19.00-19.59  ',hhumdis[19]);
  gotoxy(22,18);writeln('20.00-20.59  ',hhumdis[20]);
  gotoxy(22,19);writeln('21.00-21.59  ',hhumdis[21]);
  gotoxy(22,20);writeln('22.00-22.59  ',hhumdis[22]);
  gotoxy(22,21);writeln('23.00-23.59  ',hhumdis[23]);
end;