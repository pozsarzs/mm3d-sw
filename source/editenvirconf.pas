{ +--------------------------------------------------------------------------+ }
{ | MM3D v0.4 * Growing house controlling and remote monitoring system       | }
{ | Copyright (C) 2018-2019 Pozsár Zsolt <pozsar.zsolt@.szerafingomba.hu>    | }
{ | editenvirconf.pas                                                        | }
{ | Full-screen program for edit envir.ini file.                             | }
{ +--------------------------------------------------------------------------+ }

//   This program is free software: you can redistribute it and/or modify it
// under the terms of the European Union Public License 1.1 version.
//
//   This program is distributed in the hope that it will be useful, but WITHOUT
// ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
// FOR A PARTICULAR PURPOSE.

program editenvirconf;
uses
  INIFiles;
var
  hheaterdis, mheaterdis: array[0..23] of byte;
  hhumdis, mhumdis: array[0..23] of byte;
  hventdis, mventdis: array[0..23] of byte;
  hventdislowtemp, mventdislowtemp: array[0..23] of byte;
  hhummax, mhummax: byte;
  hhummin, mhummin: byte;
  hhumoff, mhumoff: byte;
  hhumon, mhumon: byte;
  hlightsoff1, mlightsoff1: byte;
  hlightsoff2, mlightsoff2: byte;
  hlightson1, mlightson1: byte;
  hlightson2, mlightson2: byte;
  htempmax, mtempmax: byte;
  htempmin, mtempmin: byte;
  htempoff, mtempoff: byte;
  htempon, mtempon: byte;
  hventlowtemp, mventlowtemp: byte;
  hventoff, mventoff: byte;
  hventon, mventon: byte;

{  $I loadinifile.inc}
{$I saveinifile.inc}

function setvalues: boolean;
begin
end;

begin
  if paramcount=0 then
  begin
    writeln('Usage:');
    writeln('    ',paramstr(0),' /path/envir.ini');
    halt(1);
  end;
  if not loadinifile(paramstr(1)) then
  begin
    writeln('ERROR: Cannot read ',paramstr(1),' file!');
    halt(2);
  end;
  if not setvalues then halt(0);
  if not saveinifile(paramstr(1)) then
  begin
    writeln('ERROR: Cannot write ',paramstr(1),' file!');
    halt(3);
  end;
  halt(0);
end.
