{ +--------------------------------------------------------------------------+ }
{ | MM3D v0.9 * Growing house controlling and remote monitoring system       | }
{ | Copyright (C) 2018-2023 Pozsár Zsolt <pozsar.zsolt@szerafingomba.hu>     | }
{ | incsaveinifile.pas                                                       | }
{ | Save configuration to ini file                                           | }
{ +--------------------------------------------------------------------------+ }

//   This program is free software: you can redistribute it and/or modify it
// under the terms of the European Union Public License 1.1 version.
//
//   This program is distributed in the hope that it will be useful, but WITHOUT
// ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
// FOR A PARTICULAR PURPOSE.

// save environment characteristics file
function saveinifile(filename: string): boolean;
var
  iif: text;
  b:   byte;

  // write header to file
  procedure fileheader;
  var
    b:  byte;
    l:  string;

    // completes the line to be 80 chars long
    function fullline(strin: string): string;
    begin
      fullline:='; | '+strin;
      repeat
        fullline:=fullline+' ';
      until length(fullline)>=79;
      fullline:=fullline+'|';
    end;

    begin
    l:='; +';
    for b:=1 to 76 do l:=l+'-';
    l:=l+'+';
    writeln(iif,l);
    writeln(iif,fullline('MM3D v'+VERSION+' * Growing house controlling and remote monitoring system'));
    writeln(iif,fullline(COPYRIGHT));
    writeln(iif,fullline('envir.ini'));
    writeln(iif,fullline('Growing environment characteristic'));
    writeln(iif,l);
    writeln(iif,'');
  end;

begin
  saveinifile:=true;
  try
    assign(iif,filename);
    rewrite(iif);
    fileheader;
    writeln(iif,'['+C+']');
    writeln(iif,'; common parameters');
    writeln(iif,'gasconcentrate_max=',gasconmax);
    writeln(iif,'');
    writeln(iif,'['+H+']');
    writeln(iif,'; humidifier');
    writeln(iif,'humidity_min=',hhummin);
    writeln(iif,'humidifier_on=',hhumon);
    writeln(iif,'humidifier_off=',hhumoff);
    writeln(iif,'humidity_max=',hhummax);
    for b:=0 to 9 do
      writeln(iif,'humidifier_disable_0'+inttostr(b)+'=',hhumdis[b]);
    for b:=10 to 23 do
      writeln(iif,'humidifier_disable_'+inttostr(b)+'=',hhumdis[b]);
    writeln(iif,'');
    writeln(iif,'; heaters');
    writeln(iif,'temperature_min=',htempmin);
    writeln(iif,'heater_on=',htempon);
    writeln(iif,'heater_off=',htempoff);
    writeln(iif,'temperature_max=',htempmax);
    for b:=0 to 9 do
      writeln(iif,'heater_disable_0'+inttostr(b)+'=',hheaterdis[b]);
    for b:=10 to 23 do
      writeln(iif,'heater_disable_'+inttostr(b)+'=',hheaterdis[b]);
    writeln(iif,'');
    writeln(iif,'; lights');
    writeln(iif,'light_on1=',hlightson1);
    writeln(iif,'light_off1=',hlightsoff1);
    writeln(iif,'light_on2=',hlightson2);
    writeln(iif,'light_off2=',hlightsoff2);
    writeln(iif,'');
    writeln(iif,'; ventillators');
    writeln(iif,'vent_on=',hventon);
    writeln(iif,'vent_off=',hventoff);
    for b:=0 to 9 do
      writeln(iif,'vent_disable_0'+inttostr(b)+'=',hventdis[b]);
    for b:=10 to 23 do
      writeln(iif,'vent_disable_'+inttostr(b)+'=',hventdis[b]);
    for b:=0 to 9 do
      writeln(iif,'vent_disablelowtemp_0'+inttostr(b)+'=',hventdislowtemp[b]);
    for b:=10 to 23 do
      writeln(iif,'vent_disablelowtemp_'+inttostr(b)+'=',hventdislowtemp[b]);
    writeln(iif,'vent_lowtemp=',hventlowtemp);
    for b:=0 to 9 do
      writeln(iif,'vent_disablehightemp_0'+inttostr(b)+'=',hventdishightemp[b]);
    for b:=10 to 23 do
      writeln(iif,'vent_disablehightemp_'+inttostr(b)+'=',hventdishightemp[b]);
    writeln(iif,'vent_hightemp=',hventhightemp);
    writeln(iif,'');
    writeln(iif,'['+M+']');
    writeln(iif,'; humidifier');
    writeln(iif,'humidity_min=',mhummin);
    writeln(iif,'humidifier_on=',mhumon);
    writeln(iif,'humidifier_off=',mhumoff);
    writeln(iif,'humidity_max=',mhummax);
    for b:=0 to 9 do
      writeln(iif,'humidifier_disable_0'+inttostr(b)+'=',mhumdis[b]);
    for b:=10 to 23 do
      writeln(iif,'humidifier_disable_'+inttostr(b)+'=',mhumdis[b]);
    writeln(iif,'');
    writeln(iif,'; heaters');
    writeln(iif,'temperature_min=',mtempmin);
    writeln(iif,'heater_on=',mtempon);
    writeln(iif,'heater_off=',mtempoff);
    writeln(iif,'temperature_max=',mtempmax);
    for b:=0 to 9 do
      writeln(iif,'heater_disable_0'+inttostr(b)+'=',mheaterdis[b]);
    for b:=10 to 23 do
      writeln(iif,'heater_disable_'+inttostr(b)+'=',mheaterdis[b]);
    writeln(iif,'');
    writeln(iif,'; lights');
    writeln(iif,'light_on1=',mlightson1);
    writeln(iif,'light_off1=',mlightsoff1);
    writeln(iif,'light_on2=',mlightson2);
    writeln(iif,'light_off2=',mlightsoff2);
    writeln(iif,'');
    writeln(iif,'; ventillators');
    writeln(iif,'vent_on=',mventon);
    writeln(iif,'vent_off=',mventoff);
    for b:=0 to 9 do
      writeln(iif,'vent_disable_0'+inttostr(b)+'=',mventdis[b]);
    for b:=10 to 23 do
      writeln(iif,'vent_disable_'+inttostr(b)+'=',mventdis[b]);
    for b:=0 to 9 do
      writeln(iif,'vent_disablelowtemp_0'+inttostr(b)+'=',mventdislowtemp[b]);
    for b:=10 to 23 do
      writeln(iif,'vent_disablelowtemp_'+inttostr(b)+'=',mventdislowtemp[b]);
    writeln(iif,'vent_lowtemp=',mventlowtemp);
    for b:=0 to 9 do
      writeln(iif,'vent_disablehightemp_0'+inttostr(b)+'=',mventdishightemp[b]);
    for b:=10 to 23 do
      writeln(iif,'vent_disablehightemp_'+inttostr(b)+'=',mventdishightemp[b]);
    writeln(iif,'vent_hightemp=',mventhightemp);
    writeln(iif,'');
    close(iif);
  except
    saveinifile:=false;
  end;
end;
