{ +--------------------------------------------------------------------------+ }
{ | MM3D v0.4 * Growing house controlling and remote monitoring system       | }
{ | Copyright (C) 2018-2019 Pozsár Zsolt <pozsar.zsolt@.szerafingomba.hu>    | }
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

procedure footer(title: string);
procedure header(title: string);
procedure quit(halt_code: byte; clear: boolean; message: string);

implementation

// write footer
procedure footer(title: string);
var
  b: byte;
begin
  textbackground(lightgray); textcolor(black);
  gotoxy(1,24); clreol;
  write(' '+title);
  textcolor(lightgray);textbackground(black);
end;

// write header
procedure header(title: string);
var
  b: byte;
begin
  textbackground(lightgray); textcolor(black);
  gotoxy(1,1); clreol;
  write(' '+title);
  textcolor(lightgray);textbackground(black);
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
