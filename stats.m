P = [];
k = 6; # a rendszer alapja
n = 1;

for x=[-10:10]
    m = abs(int16(x/k))+1;
    y = 0.0;
    if (m == 6) or (m == 1)
        y = 0;
    else
        y = double(1)/double(k**m);
    endif
    P=[P;x, y]
endfor

plot(P(:, 1), P(:, 2))

while 1
endwhile
