program gate_of_data;
uses
    sysutils;
type
    bfp=file of byte;
var
    opt:Integer;
    fp1:^bfp;
    fp2:^text;
    is_opened_1:boolean;
    is_opened_2:boolean;
    buf:^byte;
    bufsize:Integer;

procedure open_gate();
var
    gateopt:Integer;
begin
    writeln('Which gate?');
    writeln('1.gate of byte');
    writeln('2.gate of text');
    flush(output);
    readln(gateopt);
    case gateopt of
        1:begin
            if is_opened_1 then begin
                writeln('The gate of byte is watching you.');
                exit;
            end;
            new(fp1);
            assign(fp1^,'/dev/urandom');
            reset(fp1^);
            is_opened_1:=True
        end;
        2:begin
            if is_opened_2 then begin
                writeln('The gate of text cannot be opened twice.');
                exit;
            end;
            new(fp2);
            assign(fp2^,'/dev/urandom');
            reset(fp2^);
            is_opened_2:=True
        end;
    else
        writeln('Invalid gate choice.');
        exit;
    end;
    writeln('Gate oppened.')
end;

procedure close_gate();
var
    gateopt:Integer;
begin
    writeln('Which gate?');
    writeln('1.gate of byte');
    writeln('2.gate of text');
    flush(output);
    readln(gateopt);
    case gateopt of
        1:begin
            if not is_opened_1 then begin
                writeln('The gate of byte is closed.');
                exit;
            end;
            close(fp1^);
            is_opened_1:=false;
            dispose(fp1);
        end;
        2:begin
            if not is_opened_2 then begin
                writeln('The gate of text cannot be closed twice.');
                exit;
            end;
            close(fp2^);
            is_opened_2:=false;
            dispose(fp2);
        end;
    else
        writeln('Invalid gate choice.');
        exit;
    end;
    writeln('Gate oppened.')
end;

procedure create_ocean();
begin
    writeln('Please input the size of the data ocean.');
    flush(output);
    readln(bufsize);
    if bufsize>$400 then begin
        writeln('No such big ocean.');
        exit;
    end;
    if buf<>nil then freemem(buf);
    getmem(buf,bufsize);
    writeln('New ocean flowing.');
end;

procedure pull_data();
var
    len:Integer;
    i:Integer;
    gateopt:Integer;
begin
    if buf=nil then begin
        writeln('The ocean is dry.');
        exit;
    end;
    writeln('How much data?');
    flush(output);
    readln(len);
    if len > bufsize then begin
        writeln('Data flows over the ocean.');
        exit;
    end;

    writeln('Which gate?');
    writeln('1.gate of byte');
    writeln('2.gate of text');
    flush(output);
    readln(gateopt);
    case gateopt of
        1:begin
            if not is_opened_1 then begin
                writeln('The gate of byte is closed.');
                exit;
            end;
            blockread(fp1^,buf^,len);
        end;
        2:begin
            writeln('Oops, maybe the sea');
            if not is_opened_2 then begin
                writeln('The gate of text is closed.');
                exit;
            end;
            for i:=0 to len-1 do read(fp2^,buf[i]);
        end;
    else
        writeln('Invalid gate choice.');
        exit;
    end;
    writeln('you have pulled ',len,' bytes from the gate:');
    for i:=0 to len-1 do begin
        write(format('%2.2x',[buf[i]]));
        if (i+1) mod 16=8 then write(':') else write(' ');
        if (i+1) mod 16=0 then writeln();
    end;
    writeln()


end;

procedure banner();
begin
    writeln('**GATES OF DATA**');
    writeln('1.OPEN A NEW GATE');
    writeln('2.CLOSE THE OLD GATE');
    writeln('3.CREATE OCEAN OF DATA');
    writeln('4.PULL DATA FROM GATE TO OCEAN');
    writeln('choice >');
end;

begin
    buf:=nil;
    bufsize:=0;
    fp1:=nil;
    is_opened_1:=false;
    fp2:=nil;
    is_opened_2:=false;
    while True do begin
        banner();
        flush(output);
        readln(opt);
        case opt of
            1: open_gate();
            2: close_gate();
            3: create_ocean();
            4: pull_data();
        else
            writeln('Invalid choice.');
        end;
    end;
end.