{ +--------------------------------------------------------------------------+ }
{ | MM3D v0.9 * Growing house controlling and remote monitoring system       | }
{ | Copyright (C) 2018-2023 Pozsár Zsolt <pozsarzs@gmail.com>                | }
{ | incpage2screen.pas                                                       | }
{ | Show screen content of page #2                                           | }
{ +--------------------------------------------------------------------------+ }

//   This program is free software: you can redistribute it and/or modify it
// under the terms of the European Union Public License 1.1 version.
//
//   This program is distributed in the hope that it will be useful, but WITHOUT
// ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
// FOR A PARTICULAR PURPOSE.

// write options to screen
procedure page2screen;
var
  b: byte;
begin
  header(PRGNAME+' '+VERSION+' * Page 2/11: Growing hyphae - heating');
  textcolor(white);
  gotoxy(4,3); writeln('Minimal temperature:');
  gotoxy(4,4); writeln('Heating switch-on temperature:');
  gotoxy(4,5); writeln('Heating switch-off temperature:');
  gotoxy(4,6); writeln('Maximal temperature:');
  if htempmin>9 then gotoxy(45,3) else gotoxy(46,3); writeln(htempmin,' °C');
  if htempon>9 then gotoxy(45,4) else gotoxy(46,4); writeln(htempon,' °C');
  if htempoff>9 then gotoxy(45,5) else gotoxy(46,5); writeln(htempoff,' °C');
  if htempmax>9 then gotoxy(45,6) else gotoxy(46,6); writeln(htempmax,' °C');
  gotoxy(4,9); writeln('Disable heater (0/1):');
  for b:=0 to 9 do
  begin
    gotoxy(4,b+10);
    writeln(' '+inttostr(b)+'.00...'+inttostr(b)+'.59 ',hheaterdis[b]);
  end;
  for b:=10 to 11 do
  begin
    gotoxy(4,b+10);
    writeln(inttostr(b)+'.00..'+inttostr(b)+'.59 ',hheaterdis[b]);
  end;
  for b:=12 to 23 do
  begin
    gotoxy(22,b-2);
    writeln(inttostr(b)+'.00..'+inttostr(b)+'.59 ',hheaterdis[b]);
  end;
end;
