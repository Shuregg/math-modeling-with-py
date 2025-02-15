clc; clear; close all;
T = 1
%w = [0, 1/T, 10/T, 10e3];
%w = [0, 1/T, 10/T, inf];
w = logspace(0, 2);

xi = [0.1, 0.5, 0.8]
%xi = 0.8

for i = 1:1:3

  u = (1 - T.^2 * w .^ 2) ./ ( (1 - T^2 * w.^2) + (2 .* xi(1, i) .* w.^2))
  v = -(2 .* xi(1, i) .* w) ./ ((1 - T.^2 .* w.^2).^2 +(2 .* xi(1, i) .* w).^2)
  k = 1;

%A = k ./ sqrt((1 - T^2 * w.^2) + (2 * xi * T * w).^2)

  A = sqrt(u.^2 + v.^2)

  L = -20 * log10(A)
%A = 20 * log10(k) - 20 * log10(sqrt((1 - T^2 * w.^2) + (2 * xi * T * w).^2));
  A_t = A';

  figure(1)
  hold on
  grid on
  plot(w, L)
  plot(w, L, 'o')
  legend
  %clear('L')
 end

 hold off
