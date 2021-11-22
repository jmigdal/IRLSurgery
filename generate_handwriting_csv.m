clc, clear, close all

s = load("C:\Users\James Migdal\Downloads\mixoutALL_shifted.mat");

episodes = zeros(2 * length(s.mixout), 206); %alternating rows of deltax and deltay data w/ length 1 greater than longest episode

l = []
for i = 1:length(s.mixout)
    ep = s.mixout{i}(1:2,:);
    pad = zeros(2, 206 - length(ep(1,:)));
    ep = [ep, pad];
    episodes(2*i - 1, :)    = ep(1,:);
    episodes(2*i, :)        = ep(2,:);
end

writematrix(episodes,'episodes.csv') 