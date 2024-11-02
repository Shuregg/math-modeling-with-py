clc; close all;
TSW = 7;
cic1 = ones(2 ^ TSW, 1);
cic2 = conv(cic1, cic1);
cic4 = conv(cic2, cic2);
cic4 = cic4 / sum(cic4);

a = 28621495321396;
b = 29171251135283;

order = 32;
scale = 2 ^ order;

p = [a * ones(1000, 1); b * ones(1000, 1)];
size(p)
size(cic4)

am = floor(a / scale);
bm = floor(b / scale);

pm = [am * ones(1000, 1); bm * ones(1000, 1)];
size(pm);

pf = conv(cic4, p);
size(pf)

pfm = conv(cic4, pm) * scale;
%figure(1, WindowStyle="docked")
figure('windowstyle','docked')
    clf
    hold on
        plot(p)
        plot(pf)
        plot(pfm)
    hold off
    grid