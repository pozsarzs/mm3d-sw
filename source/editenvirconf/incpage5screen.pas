{ +--------------------------------------------------------------------------+ }
{ | MM3D v0.9 * Growing house controlling and remote monitoring system       | }
{ | Copyright (C) 2018-2023 Pozsár Zsolt <pozsar.zsolt@szerafingomba.hu>     | }
{ | incpage5screen.pas                                                       | }
{ | Show screen content of page #5                                           | }
{ +--------------------------------------------------------------------------+ }

//   This program is free software: you can redistribute it and/or modify it
// under the terms of the European Union Public License 1.1 version.
//
//   This program is distributed in the hope that it will be useful, but WITHOUT
// ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
// FOR A PARTICULAR PURPOSE.

// write options to screen
procedure page5screen;
var
  b: byte;
begin
  header(PRGNAME+' '+VERSION+' * Page 5/11: Growing hyphae - ventilating 2');
  textcolor(white);
  gotoxy(4,3); writeln('Disable if ext. temp. is high (0/1):');
  for b:=0 to 9 do
  begin
    gotoxy(4,b+4);
    writeln(' '+inttostr(b)+'.00...'+inttostr(b)+'.59 ',hventdishightemp[b]);
  end;
  for b:=10 to 11 do
  begin
    gotoxy(4,b+4);
    writeln(inttostr(b)+'.00..'+inttostr(b)+'.59 ',hventdishightemp[b]);
  end;
  for b:=12 to 23 do
  begin
    gotoxy(22,b-8);
    writeln(inttostr(b)+'.00..'+inttostr(b)+'.59 ',hventdishightemp[b]);
  end;
  gotoxy(4,17); writeln('High external temperature:');
  gotoxy(46,17);
  if hventhightemp>9 then gotoxy(wherex-1,17);
  if hventhightemp<0 then gotoxy(wherex-1,17);
  if hventhightemp<-9 then gotoxy(wherex-1,17);
  writeln(hventhightemp,' °C');
end;
