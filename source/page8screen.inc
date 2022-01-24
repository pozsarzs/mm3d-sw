{ +--------------------------------------------------------------------------+ }
{ | MM3D v0.7 * Growing house controlling and remote monitoring system       | }
{ | Copyright (C) 2018-2022 Pozsár Zsolt <pozsar.zsolt@szerafingomba.hu>     | }
{ | page8screen.inc                                                          | }
{ | Show screen content of page #8                                           | }
{ +--------------------------------------------------------------------------+ }

//   This program is free software: you can redistribute it and/or modify it
// under the terms of the European Union Public License 1.1 version.
//
//   This program is distributed in the hope that it will be useful, but WITHOUT
// ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
// FOR A PARTICULAR PURPOSE.

procedure page8screen;
begin
  header('EditEnvirConf '+VERSION+' * Page 8/8: Growing mushroom - ventilating');
  textcolor(white);
  gotoxy(4,3); writeln('Ventilators switch-on minute:');
  gotoxy(4,4); writeln('Ventilators switch-off minute:');
  gotoxy(45,3); if mventon<10 then write('0'); write(mventon);
  gotoxy(45,4); if mventoff<10 then write('0'); write(mventoff);
  gotoxy(4,7); writeln('Disable ventilators (0/1):');
  gotoxy(4,8); writeln(' 0.00...0.59 ',mventdis[0]);
  gotoxy(4,9); writeln(' 1.00...1.59 ',mventdis[1]);
  gotoxy(4,10); writeln(' 2.00...2.59 ',mventdis[2]);
  gotoxy(4,11); writeln(' 3.00...3.59 ',mventdis[3]);
  gotoxy(4,12); writeln(' 4.00...4.59 ',mventdis[4]);
  gotoxy(4,13); writeln(' 5.00...5.59 ',mventdis[5]);
  gotoxy(4,14); writeln(' 6.00...6.59 ',mventdis[6]);
  gotoxy(4,15); writeln(' 7.00...7.59 ',mventdis[7]);
  gotoxy(4,16); writeln(' 8.00...8.59 ',mventdis[8]);
  gotoxy(4,17); writeln(' 9.00...9.59 ',mventdis[9]);
  gotoxy(4,18); writeln('10.00..10.59 ',mventdis[10]);
  gotoxy(4,19); writeln('11.00..11.59 ',mventdis[11]);
  gotoxy(22,8); writeln('12.00..12.59 ',mventdis[12]);
  gotoxy(22,9); writeln('13.00..13.59 ',mventdis[13]);
  gotoxy(22,10); writeln('14.00..14.59 ',mventdis[14]);
  gotoxy(22,11); writeln('15.00..15.59 ',mventdis[15]);
  gotoxy(22,12); writeln('16.00..16.59 ',mventdis[16]);
  gotoxy(22,13); writeln('17.00..17.59 ',mventdis[17]);
  gotoxy(22,14); writeln('18.00..18.59 ',mventdis[18]);
  gotoxy(22,15); writeln('19.00..19.59 ',mventdis[19]);
  gotoxy(22,16); writeln('20.00..20.59 ',mventdis[20]);
  gotoxy(22,17); writeln('21.00..21.59 ',mventdis[21]);
  gotoxy(22,18); writeln('22.00..22.59 ',mventdis[22]);
  gotoxy(22,19); writeln('23.00..23.59 ',mventdis[23]);
  gotoxy(40,7); writeln('Disable if ext. temp. is low (0/1):');
  gotoxy(40,8); writeln(' 0.00...0.59 ',mventdislowtemp[0]);
  gotoxy(40,9); writeln(' 1.00...1.59 ',mventdislowtemp[1]);
  gotoxy(40,10); writeln(' 2.00...2.59 ',mventdislowtemp[2]);
  gotoxy(40,11); writeln(' 3.00...3.59 ',mventdislowtemp[3]);
  gotoxy(40,12); writeln(' 4.00...4.59 ',mventdislowtemp[4]);
  gotoxy(40,13); writeln(' 5.00...5.59 ',mventdislowtemp[5]);
  gotoxy(40,14); writeln(' 6.00...6.59 ',mventdislowtemp[6]);
  gotoxy(40,15); writeln(' 7.00...7.59 ',mventdislowtemp[7]);
  gotoxy(40,16); writeln(' 8.00...8.59 ',mventdislowtemp[8]);
  gotoxy(40,17); writeln(' 9.00...9.59 ',mventdislowtemp[9]);
  gotoxy(40,18); writeln('10.00..10.59 ',mventdislowtemp[10]);
  gotoxy(40,19); writeln('11.00..11.59 ',mventdislowtemp[11]);
  gotoxy(58,8); writeln('12.00..12.59 ',mventdislowtemp[12]);
  gotoxy(58,9); writeln('13.00..13.59 ',mventdislowtemp[13]);
  gotoxy(58,10); writeln('14.00..14.59 ',mventdislowtemp[14]);
  gotoxy(58,11); writeln('15.00..15.59 ',mventdislowtemp[15]);
  gotoxy(58,12); writeln('16.00..16.59 ',mventdislowtemp[16]);
  gotoxy(58,13); writeln('17.00..17.59 ',mventdislowtemp[17]);
  gotoxy(58,14); writeln('18.00..18.59 ',mventdislowtemp[18]);
  gotoxy(58,15); writeln('19.00..19.59 ',mventdislowtemp[19]);
  gotoxy(58,16); writeln('20.00..20.59 ',mventdislowtemp[20]);
  gotoxy(58,17); writeln('21.00..21.59 ',mventdislowtemp[21]);
  gotoxy(58,18); writeln('22.00..22.59 ',mventdislowtemp[22]);
  gotoxy(58,19); writeln('23.00..23.59 ',mventdislowtemp[23]);
  gotoxy(4,21); writeln('Low external temperature:');
  gotoxy(46,21);
  if mventlowtemp>9 then gotoxy(wherex-1,21);
  if mventlowtemp<0 then gotoxy(wherex-1,21);
  if mventlowtemp<-9 then gotoxy(wherex-1,21);
  writeln(mventlowtemp,' °C');
end;
