{ +--------------------------------------------------------------------------+ }
{ | MM3D v0.4 * Growing house controlling and remote monitoring system       | }
{ | Copyright (C) 2018-2019 Pozsár Zsolt <pozsar.zsolt@.szerafingomba.hu>    | }
{ | page4screen.inc                                                          | }
{ | Show screen content of page #4                                           | }
{ +--------------------------------------------------------------------------+ }

//   This program is free software: you can redistribute it and/or modify it
// under the terms of the European Union Public License 1.1 version.
//
//   This program is distributed in the hope that it will be useful, but WITHOUT
// ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
// FOR A PARTICULAR PURPOSE.

procedure page4screen;
begin
  header('EditEnvirConf '+VERSION+' * Page 4/8: Growing hyphae - ventilating');
  textcolor(white);
  gotoxy(4,3); writeln('Ventilators switch-on minute:');
  gotoxy(4,4); writeln('Ventilators switch-off minute:');
  gotoxy(45,3); if hventon<10 then write('0'); write(hventon);
  gotoxy(45,4); if hventoff<10 then write('0'); write(hventoff);
  gotoxy(4,9); writeln('Disable ventilators (0/1):');
  gotoxy(4,10); writeln('00.00-00.59  ',hventdis[0]);
  gotoxy(4,11); writeln('01.00-01.59  ',hventdis[1]);
  gotoxy(4,12); writeln('02.00-02.59  ',hventdis[2]);
  gotoxy(4,13); writeln('03.00-03.59  ',hventdis[3]);
  gotoxy(4,14); writeln('04.00-04.59  ',hventdis[4]);
  gotoxy(4,15); writeln('05.00-05.59  ',hventdis[5]);
  gotoxy(4,16); writeln('06.00-06.59  ',hventdis[6]);
  gotoxy(4,17); writeln('07.00-07.59  ',hventdis[7]);
  gotoxy(4,18); writeln('08.00-08.59  ',hventdis[8]);
  gotoxy(4,19); writeln('09.00-09.59  ',hventdis[9]);
  gotoxy(4,20); writeln('10.00-10.59  ',hventdis[10]);
  gotoxy(4,21); writeln('11.00-11.59  ',hventdis[11]);
  gotoxy(22,10); writeln('12.00-12.59  ',hventdis[12]);
  gotoxy(22,11); writeln('13.00-13.59  ',hventdis[13]);
  gotoxy(22,12); writeln('14.00-14.59  ',hventdis[14]);
  gotoxy(22,13); writeln('15.00-15.59  ',hventdis[15]);
  gotoxy(22,14); writeln('16.00-16.59  ',hventdis[16]);
  gotoxy(22,15); writeln('17.00-17.59  ',hventdis[17]);
  gotoxy(22,16); writeln('18.00-18.59  ',hventdis[18]);
  gotoxy(22,17); writeln('19.00-19.59  ',hventdis[19]);
  gotoxy(22,18); writeln('20.00-20.59  ',hventdis[20]);
  gotoxy(22,19); writeln('21.00-21.59  ',hventdis[21]);
  gotoxy(22,20); writeln('22.00-22.59  ',hventdis[22]);
  gotoxy(22,21); writeln('23.00-23.59  ',hventdis[23]);
  gotoxy(40,9); writeln('Disable if ext. temp. is low (0/1):');
  gotoxy(40,10); writeln('00.00-00.59  ',hventdislowtemp[0]);
  gotoxy(40,11); writeln('01.00-01.59  ',hventdislowtemp[1]);
  gotoxy(40,12); writeln('02.00-02.59  ',hventdislowtemp[2]);
  gotoxy(40,13); writeln('03.00-03.59  ',hventdislowtemp[3]);
  gotoxy(40,14); writeln('04.00-04.59  ',hventdislowtemp[4]);
  gotoxy(40,15); writeln('05.00-05.59  ',hventdislowtemp[5]);
  gotoxy(40,16); writeln('06.00-06.59  ',hventdislowtemp[6]);
  gotoxy(40,17); writeln('07.00-07.59  ',hventdislowtemp[7]);
  gotoxy(40,18); writeln('08.00-08.59  ',hventdislowtemp[8]);
  gotoxy(40,19); writeln('09.00-09.59  ',hventdislowtemp[9]);
  gotoxy(40,20); writeln('10.00-10.59  ',hventdislowtemp[10]);
  gotoxy(40,21); writeln('11.00-11.59  ',hventdislowtemp[11]);
  gotoxy(58,10); writeln('12.00-12.59  ',hventdislowtemp[12]);
  gotoxy(58,11); writeln('13.00-13.59  ',hventdislowtemp[13]);
  gotoxy(58,12); writeln('14.00-14.59  ',hventdislowtemp[14]);
  gotoxy(58,13); writeln('15.00-15.59  ',hventdislowtemp[15]);
  gotoxy(58,14); writeln('16.00-16.59  ',hventdislowtemp[16]);
  gotoxy(58,15); writeln('17.00-17.59  ',hventdislowtemp[17]);
  gotoxy(58,16); writeln('18.00-18.59  ',hventdislowtemp[18]);
  gotoxy(58,17); writeln('19.00-19.59  ',hventdislowtemp[19]);
  gotoxy(58,18); writeln('20.00-20.59  ',hventdislowtemp[20]);
  gotoxy(58,19); writeln('21.00-21.59  ',hventdislowtemp[21]);
  gotoxy(58,20); writeln('22.00-22.59  ',hventdislowtemp[22]);
  gotoxy(58,21); writeln('23.00-23.59  ',hventdislowtemp[23]);
end;
