{ +--------------------------------------------------------------------------+ }
{ | MM3D v0.8 * Growing house controlling and remote monitoring system       | }
{ | Copyright (C) 2018-2022 Pozsár Zsolt <pozsar.zsolt@szerafingomba.hu>     | }
{ | incloadinifile.pas                                                       | }
{ | Load configuration from ini file                                         | }
{ +--------------------------------------------------------------------------+ }

//   This program is free software: you can redistribute it and/or modify it
// under the terms of the European Union Public License 1.1 version.
//
//   This program is distributed in the hope that it will be useful, but WITHOUT
// ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
// FOR A PARTICULAR PURPOSE.

// load environment characteristics file
function loadinifile(filename: string): boolean;
var
  iif: TINIFile;
  b:   byte;

begin
  iif:=TIniFile.Create(filename);
  loadinifile:=true;
  try
    gasconmax:=strtoint(iif.ReadString(C,'gasconcentrate_max','0'));
    hhummax:=strtoint(iif.ReadString(H,'humidity_max','0'));
    hhummin:=strtoint(iif.ReadString(H,'humidity_min','0'));
    hhumoff:=strtoint(iif.ReadString(H,'humidifier_off','0'));
    hhumon:=strtoint(iif.ReadString(H,'humidifier_on','0'));
    for b:=0 to 9 do
      hhumdis[b]:=strtoint(iif.ReadString(H,'humidifier_disable_0'+inttostr(b),'0'));
    for b:=10 to 23 do
      hhumdis[b]:=strtoint(iif.ReadString(H,'humidifier_disable_'+inttostr(b),'0'));
    htempmin:=strtoint(iif.ReadString(H,'temperature_min','0'));
    htempon:=strtoint(iif.ReadString(H,'heater_on','0'));
    htempoff:=strtoint(iif.ReadString(H,'heater_off','0'));
    htempmax:=strtoint(iif.ReadString(H,'temperature_max','0'));
    for b:=0 to 9 do
      hheaterdis[b]:=strtoint(iif.ReadString(H,'heater_disable_0'+inttostr(b),'0'));
    for b:=10 to 23 do
      hheaterdis[b]:=strtoint(iif.ReadString(H,'heater_disable_'+inttostr(b),'0'));
    hlightson1:=strtoint(iif.ReadString(H,'light_on1','0'));
    hlightsoff1:=strtoint(iif.ReadString(H,'light_off1','0'));
    hlightson2:=strtoint(iif.ReadString(H,'light_on2','0'));
    hlightsoff2:=strtoint(iif.ReadString(H,'light_off2','0'));
    hventon:=strtoint(iif.ReadString(H,'vent_on','0'));
    hventoff:=strtoint(iif.ReadString(H,'vent_off','0'));
    for b:=0 to 9 do
      hventdis[b]:=strtoint(iif.ReadString(H,'vent_disable_0'+inttostr(b),'0'));
    for b:=10 to 23 do
      hventdis[b]:=strtoint(iif.ReadString(H,'vent_disable_'+inttostr(b),'0'));
    for b:=0 to 9 do
      hventdislowtemp[b]:=strtoint(iif.ReadString(H,'vent_disablelowtemp_0'+inttostr(b),'0'));
    for b:=10 to 23 do
      hventdislowtemp[b]:=strtoint(iif.ReadString(H,'vent_disablelowtemp_'+inttostr(b),'0'));
    hventlowtemp:=strtoint(iif.ReadString(H,'vent_lowtemp','0'));
    for b:=0 to 9 do
      hventdishightemp[b]:=strtoint(iif.ReadString(H,'vent_disablehightemp_0'+inttostr(b),'0'));
    for b:=10 to 23 do
      hventdishightemp[b]:=strtoint(iif.ReadString(H,'vent_disablehightemp_'+inttostr(b),'0'));
    hventhightemp:=strtoint(iif.ReadString(H,'vent_hightemp','0'));
    mhummax:=strtoint(iif.ReadString(M,'humidity_max','0'));
    mhummin:=strtoint(iif.ReadString(M,'humidity_min','0'));
    mhumoff:=strtoint(iif.ReadString(M,'humidifier_off','0'));
    mhumon:=strtoint(iif.ReadString(M,'humidifier_on','0'));
    for b:=0 to 9 do
      mhumdis[b]:=strtoint(iif.ReadString(M,'humidifier_disable_0'+inttostr(b),'0'));
    for b:=10 to 23 do
      mhumdis[b]:=strtoint(iif.ReadString(M,'humidifier_disable_'+inttostr(b),'0'));
    mtempmin:=strtoint(iif.ReadString(M,'temperature_min','0'));
    mtempon:=strtoint(iif.ReadString(M,'heater_on','0'));
    mtempoff:=strtoint(iif.ReadString(M,'heater_off','0'));
    mtempmax:=strtoint(iif.ReadString(M,'temperature_max','0'));
    for b:=0 to 9 do
      mheaterdis[b]:=strtoint(iif.ReadString(M,'heater_disable_0'+inttostr(b),'0'));
    for b:=10 to 23 do
      mheaterdis[b]:=strtoint(iif.ReadString(M,'heater_disable_'+inttostr(b),'0'));
    mlightson1:=strtoint(iif.ReadString(M,'light_on1','0'));
    mlightsoff1:=strtoint(iif.ReadString(M,'light_off1','0'));
    mlightson2:=strtoint(iif.ReadString(M,'light_on2','0'));
    mlightsoff2:=strtoint(iif.ReadString(M,'light_off2','0'));
    mventon:=strtoint(iif.ReadString(M,'vent_on','0'));
    mventoff:=strtoint(iif.ReadString(M,'vent_off','0'));
    for b:=0 to 9 do
      mventdis[b]:=strtoint(iif.ReadString(M,'vent_disable_0'+inttostr(b),'0'));
    for b:=10 to 23 do
      mventdis[b]:=strtoint(iif.ReadString(M,'vent_disable_'+inttostr(b),'0'));
    for b:=0 to 9 do
      mventdislowtemp[b]:=strtoint(iif.ReadString(M,'vent_disablelowtemp_0'+inttostr(b),'0'));
    for b:=10 to 23 do
      mventdislowtemp[b]:=strtoint(iif.ReadString(M,'vent_disablelowtemp_'+inttostr(b),'0'));
    mventlowtemp:=strtoint(iif.ReadString(M,'vent_lowtemp','0'));
    for b:=0 to 9 do
      mventdishightemp[b]:=strtoint(iif.ReadString(M,'vent_disablehightemp_0'+inttostr(b),'0'));
    for b:=10 to 23 do
      mventdishightemp[b]:=strtoint(iif.ReadString(M,'vent_disablehightemp_'+inttostr(b),'0'));
    mventhightemp:=strtoint(iif.ReadString(M,'vent_hightemp','0'));
  except
    loadinifile:=false;
  end;
  iif.Free;
end;
