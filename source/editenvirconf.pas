{ +--------------------------------------------------------------------------+ }
{ | MM3D v0.4 * Growing house controlling and remote monitoring system       | }
{ | Copyright (C) 2018-2019 Pozsár Zsolt <pozsar.zsolt@.szerafingomba.hu>    | }
{ | editenvirconf.pas                                                        | }
{ | Full-screen program for edit envir.ini file                              | }
{ +--------------------------------------------------------------------------+ }

//   This program is free software: you can redistribute it and/or modify it
// under the terms of the European Union Public License 1.1 version.
//
//   This program is distributed in the hope that it will be useful, but WITHOUT
// ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
// FOR A PARTICULAR PURPOSE.

program editenvirconf;
{$MODE OBJFPC}{$H+}
uses
  INIFiles, SysUtils,
  character, crt,
  untcommon;
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
const
  VERSION: string='v0.4';
const
  blocks: array[1..8] of byte=(3,3,3,3,3,3,3,3);
  minposx: array[1..8,1..4] of byte=((46,17,35,0),
                                     (0,0,0,0),
                                     (0,0,0,0),
                                     (0,0,0,0),
                                     (0,0,0,0),
                                     (0,0,0,0),
                                     (0,0,0,0),
                                     (0,0,0,0));
  minposy: array[1..8,1..4] of byte=((3,10,10,0),
                                     (0,0,0,0),
                                     (0,0,0,0),
                                     (0,0,0,0),
                                     (0,0,0,0),
                                     (0,0,0,0),
                                     (0,0,0,0),
                                     (0,0,0,0));
  maxposy: array[1..8,1..4] of byte=((6,21,21,0),
                                     (0,0,0,0),
                                     (0,0,0,0),
                                     (0,0,0,0),
                                     (0,0,0,0),
                                     (0,0,0,0),
                                     (0,0,0,0),
                                     (0,0,0,0));

{$I page1screen.inc}
{$I page2screen.inc}
{$I page3screen.inc}
{$I page4screen.inc}
{$I page5screen.inc}
{$I page6screen.inc}
{$I page7screen.inc}
{$I page8screen.inc}
{$I loadinifile.inc}
{$I saveinifile.inc}

procedure screen(page: byte);
begin
  background;
  header('EditEnvirConf '+VERSION+' * Page '+inttostr(page)+'/8: Growing hyphae - humidity');
  case page of
    1: page1screen;
    2: page2screen;
    3: page3screen;
    4: page4screen;
    5: page5screen;
    6: page6screen;
    7: page7screen;
    8: page8screen;
  end;
  footer('<Tab>/<Up>/<Down> move  <Enter> edit  <Home>/<PgUp>/<PgDn>/<End> paging');
  textbackground(black); gotoxy(1,25); clreol;
end;

procedure getvalue(page,block,posy: byte);
var
  c: char;
  s: string;
  b: byte;
begin
  textbackground(black);
  footer('<Enter> accept  <Esc> cancel');
  gotoxy(1,25); write('>');
  s:='';
  repeat
    c:=readkey;
    if isnumber(c) then
    begin
      if block=1 then
      begin
        if length(s)<2 then s:=s+c;
      end else
        if (c='0') or (c='1') then s:=c;
    end;
    if c=#8 then delete(s,length(s),1);
    gotoxy(1,25); clreol; write('>'+s);
  until (c=#13) or (c=#27);
  if (c=#13) and (length(s)>0) then
  begin
    // page #1
    if page=1 then
    begin
      // page #1 - block #1
      if block=1 then
      begin
        gotoxy(minposx[page,block]-length(s)+1,posy); textbackground(blue);
        case posy of
          3: begin hhummin:=strtoint(s); write(hhummin); end;
          4: begin hhumon:=strtoint(s); write(hhumon); end;
          5: begin hhumoff:=strtoint(s); write(hhumoff); end;
          6: begin hhummax:=strtoint(s); write(hhummax); end;
        end;
      end;
      // page #1 - block #2
      if block=2 then
      begin
        gotoxy(minposx[page,block],posy); textbackground(blue);
        hhumdis[posy-10]:=strtoint(s);
        write(hhumdis[posy-10]);
      end;
      // page #1 - block #3
      if block=3 then
      begin
        gotoxy(minposx[page,block],posy); textbackground(blue);
        hhumdis[posy+2]:=strtoint(s);
        write(hhumdis[posy+2]);
      end;
    end;
  end;
  footer('<Tab>/<Up>/<Down> move  <Enter> edit  <Home>/<PgUp>/<PgDn>/<End> paging');
  gotoxy(1,25); clreol;
end;

function setvalues: boolean;
var
  page, block, posy: byte;
  k : char;
  s: string;
label back;
begin
  page:=1;
  block:=1;
  screen(page);
 back:
  textbackground(black);
  gotoxy(1,25); clreol;
  footer('<Tab>/<Up>/<Down> move  <Enter> edit  <Home>/<PgUp>/<PgDn>/<End> paging');
  posy:=minposy[page,block];
  gotoxy(minposx[page,block],posy);
  repeat
    k:=readkey;
    if k=#0 then k:=readkey;
    case k of
      // first page
      #71: begin
             page:=1;
             screen(page);
           end;
      // previous page
      #73: begin
             page:=page-1;
             if page<1 then page:=1;
             screen(page);
           end;
      // next page
      #81: begin
             page:=page+1;
             if page>8 then page:=8;
             screen(page);
           end;
      // last page
      #79: begin
             page:=8;
             screen(page);
           end;
      // next block on page
       #9: begin
             block:=block+1;
             if block>blocks[page] then block:=1;
             posy:=minposy[page,block];
             gotoxy(minposx[page,block],posy);
           end;
      // previous item in block
       #72: begin
             posy:=posy-1;
             if posy<minposy[page,block] then posy:=maxposy[page,block];
             gotoxy(minposx[page,block],posy);
            end;
      // next item in block
       #80: begin
             posy:=posy+1;
             if posy>maxposy[page,block] then posy:=minposy[page,block];
             gotoxy(minposx[page,block],posy);
            end;
      // select and edit item
       #13: begin
              getvalue(page,block,posy);
              gotoxy(minposx[page,block],posy);
            end;
        end;
  // exit
  until k=#27;
  footer('<Esc> cancel');
  gotoxy(1,25); write('Save to '+paramstr(1)+'? (y/n) ');
  repeat
    k:=lowercase(readkey);
    if k=#27 then goto back;
  until (k='y') or (k='n');
  if k='y' then setvalues:=true else setvalues:=false;
end;

begin
  textcolor(lightgray); textbackground(black);
  if paramcount=0 then
    quit(1,false,'Usage:'+#10+'    '+paramstr(0)+' /path/envir.ini');
  if not loadinifile(paramstr(1)) then
    quit(2,false,'ERROR: Cannot read '+paramstr(1)+' file!');
  if not setvalues then
    quit(0,true,'File '+paramstr(1)+' is not saved.');
  if not saveinifile(paramstr(1)) then
    quit(3,true,'ERROR: Cannot write '+paramstr(1)+' file!');
  quit(0,true,'');
end.
