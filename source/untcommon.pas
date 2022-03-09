{ +--------------------------------------------------------------------------+ }
{ | MM3D v0.8 * Growing house controlling and remote monitoring system       | }
{ | Copyright (C) 2018-2022 Pozsár Zsolt <pozsar.zsolt@szerafingomba.hu>     | }
{ | untcommon.pas                                                            | }
{ | Common functions and procedures                                          | }
{ +--------------------------------------------------------------------------+ }

//   This program is free software: you can redistribute it and/or modify it
// under the terms of the European Union Public License 1.1 version.
//
//   This program is distributed in the hope that it will be useful, but WITHOUT
// ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
// FOR A PARTICULAR PURPOSE.

unit untcommon;
interface
uses
  crt;

function terminalsize: boolean;
procedure background;
procedure footer(ypos: byte; title: string);
procedure header(title: string);
procedure quit(halt_code: byte; clear: boolean; message: string);

implementation

// check terminal size
function terminalsize: boolean;
begin
  if (screenwidth>=80) and (screenheight>=25)
    then terminalsize:=true
    else terminalsize:=false;
end;

procedure background;
begin
  textbackground(blue);
  clrscr;
end;

// write footer
procedure footer(ypos: byte; title: string);
var
  b: byte;
begin
  textbackground(lightgray); textcolor(black);
  gotoxy(1,ypos); clreol;
  gotoxy(2,ypos);
  for b:=1 to length(title) do
  begin
    case title[b] of
      '<': textcolor(red);
      '>': textcolor(black);
    else write(title[b]);
    end;
  end;
  textcolor(white); textbackground(black);
end;

// write header
procedure header(title: string);
begin
  textbackground(lightgray); textcolor(black);
  gotoxy(1,1); clreol;
  write(' '+title);
  textcolor(white); textbackground(blue);
end;

// exit
procedure quit(halt_code: byte; clear: boolean; message: string);
begin
  textcolor(lightgray); textbackground(black);
  if clear then clrscr;
  writeln(message);
  halt(halt_code);
end;

end.
