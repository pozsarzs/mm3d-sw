{ +--------------------------------------------------------------------------+ }
{ | MM3D v0.4 * Growing house controlling and remote monitoring system       | }
{ | Copyright (C) 2018-2019 Pozsár Zsolt <pozsar.zsolt@.szerafingomba.hu>    | }
{ | page3screen.inc                                                          | }
{ | Show screen content of page #3                                           | }
{ +--------------------------------------------------------------------------+ }

//   This program is free software: you can redistribute it and/or modify it
// under the terms of the European Union Public License 1.1 version.
//
//   This program is distributed in the hope that it will be useful, but WITHOUT
// ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
// FOR A PARTICULAR PURPOSE.

procedure page3screen;
begin
  header('EditEnvirConf '+VERSION+' * Page 3/8: Growing hyphae - lighting');
  textcolor(white);
  gotoxy(4,3); writeln('1st time when lights switch on:');
  gotoxy(4,4); writeln('1st time when lights switch off:');
  gotoxy(4,5); writeln('2nd time when lights switch on:');
  gotoxy(4,6); writeln('2nd time when lights switch off:');
  gotoxy(45,3); if hlightson1<10 then write('0'); write(hlightson1,'.00');
  gotoxy(45,4); if hlightsoff1<10 then write('0'); write(hlightsoff1,'.00');
  gotoxy(45,5); if hlightson2<10 then write('0'); write(hlightson2,'.00');
  gotoxy(45,6); if hlightsoff2<10 then write('0'); write(hlightsoff2,'.00');
end;
