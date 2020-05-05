{ +--------------------------------------------------------------------------+ }
{ | MM3D v0.5 * Growing house controlling and remote monitoring system       | }
{ | Copyright (C) 2018-2020 Pozsár Zsolt <pozsar.zsolt@.szerafingomba.hu>    | }
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
  gotoxy(4,3); writeln('Lights switch-on time #1:');
  gotoxy(4,4); writeln('Lights switch-off time #1:');
  gotoxy(4,5); writeln('Lights switch-on time #2:');
  gotoxy(4,6); writeln('Lights switch-off time #2:');
  gotoxy(45,3); if hlightson1<10 then write(' '); write(hlightson1,'.00');
  gotoxy(45,4); if hlightsoff1<10 then write(' '); write(hlightsoff1,'.00');
  gotoxy(45,5); if hlightson2<10 then write(' '); write(hlightson2,'.00');
  gotoxy(45,6); if hlightsoff2<10 then write(' '); write(hlightsoff2,'.00');
end;
