{ +--------------------------------------------------------------------------+ }
{ | MM3D v0.8 * Growing house controlling and remote monitoring system       | }
{ | Copyright (C) 2018-2022 Pozsár Zsolt <pozsar.zsolt@szerafingomba.hu>     | }
{ | incpage9screen.pas                                                       | }
{ | Show screen content of page #9                                           | }
{ +--------------------------------------------------------------------------+ }

//   This program is free software: you can redistribute it and/or modify it
// under the terms of the European Union Public License 1.1 version.
//
//   This program is distributed in the hope that it will be useful, but WITHOUT
// ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
// FOR A PARTICULAR PURPOSE.

// write options to screen
procedure page9screen;
var
  b: byte;
begin
  header(PRGNAME+' '+VERSION+' * Page 9/11: Growing mushroom - ventilating 1');
  textcolor(white);
  gotoxy(4,3); writeln('Ventilators switch-on minute:');
  gotoxy(4,4); writeln('Ventilators switch-off minute:');
  gotoxy(45,3); if mventon<10 then write('0'); write(mventon);
  gotoxy(45,4); if mventoff<10 then write('0'); write(mventoff);
  gotoxy(4,7); writeln('Disable ventilators (0/1):');
  for b:=0 to 9 do
  begin
    gotoxy(4,b+8);
    writeln(' '+inttostr(b)+'.00...'+inttostr(b)+'.59 ',mventdis[b]);
  end;
  for b:=10 to 11 do
  begin
    gotoxy(4,b+8);
    writeln(inttostr(b)+'.00..'+inttostr(b)+'.59 ',mventdis[b]);
  end;
  for b:=12 to 23 do
  begin
    gotoxy(22,b-4);
    writeln(inttostr(b)+'.00..'+inttostr(b)+'.59 ',mventdis[b]);
  end;
  gotoxy(40,7); writeln('Disable if ext. temp. is low (0/1):');
  for b:=0 to 9 do
  begin
    gotoxy(40,b+8);
    writeln(' '+inttostr(b)+'.00...'+inttostr(b)+'.59 ',mventdislowtemp[b]);
  end;
  for b:=10 to 11 do
  begin
    gotoxy(40,b+8);
    writeln(inttostr(b)+'.00..'+inttostr(b)+'.59 ',mventdislowtemp[b]);
  end;
  for b:=12 to 23 do
  begin
    gotoxy(58,b-4);
    writeln(inttostr(b)+'.00..'+inttostr(b)+'.59 ',mventdislowtemp[b]);
  end;
  gotoxy(4,21); writeln('Low external temperature:');
  gotoxy(46,21);
  if mventlowtemp>9 then gotoxy(wherex-1,21);
  if mventlowtemp<0 then gotoxy(wherex-1,21);
  if mventlowtemp<-9 then gotoxy(wherex-1,21);
  writeln(mventlowtemp,' °C');
end;
