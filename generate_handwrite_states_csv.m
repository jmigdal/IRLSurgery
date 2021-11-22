clc, clear, close all

episodes = csvread('C:\Users\James Migdal\Documents\MATLAB\episodes.csv');
state_episodes = zeros(length(episodes), 206); %alternating rows of L and theta data w/ length 1 greater than longest episode

%!!! When looking a compass normally w/ north at the top, 0 rad is east,
%pi/2 is north, 3pi/2 is south
lastTheta = 0;
for j = 1:(length(episodes)/2)
    cumL = zeros(1,206);
    cumTheta = zeros(1,206);
    
    x = episodes(2*j-1,:);
    y = episodes(2*j,:);
    first = 1; %flag to mark the first non-zero data
    lastTheta = 0;
    for i = 1:206
        if i == 1
            cumL(i) = sqrt(x(i)^2 + y(i)^2);
        else
            cumL(i) = cumL(i-1) + sqrt(x(i)^2 + y(i)^2);
        end

        if x(i) == 0
            if y(i) == 0
                theta = lastTheta;
            elseif y(i) > 0
                theta = pi/2;
            else
                theta = 3*pi/2;
            end
        elseif x(i) > 0
            if y(i) > 0
                theta = atan(y(i)/x(i));
            else
                theta = atan(y(i)/x(i)) + 2*pi;
            end
        else
            theta = atan(y(i)/x(i)) + pi;
        end
        
        if first && theta == 0
            cumTheta(i) = 0;
        elseif first && theta ~= 0
            first = 0;
            cumTheta(i) = 0;
        elseif theta - lastTheta > pi
            cumTheta(i) = cumTheta(i-1) + ((theta - 2*pi) - lastTheta);
        elseif theta - lastTheta < -pi
            cumTheta(i) = cumTheta(i-1) + ((theta + 2*pi) - lastTheta);
        else
            cumTheta(i) = cumTheta(i-1) + (theta - lastTheta);
        end
        lastTheta = theta;
        
    end
    state_episodes(2*j-1,:) = cumL;
    state_episodes(2*j,:) = cumTheta;
end

writematrix(state_episodes,'episodes_states.csv');