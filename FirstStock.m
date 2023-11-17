clearvars, clc;

% This is all ChatGPT so far


% Geometric Brownian Motion Parameters
mu = 0.1;   % Drift
sigma = 0.2;   % Volatility

% Time parameters

% only 22 days of simulation, and for each day, only 12 hours of trading
% stock gets updated each minute

T = 22;       % Time to simulate
dt = 1/(12*60);   % Time step
t = 0:dt:T;  % Time vector

length(t)

% Number of simulations
numSimulations = 5;

% Initial values
S0 = 100;    % Initial stock price

% Simulate Geometric Brownian Motion
S = zeros(numSimulations, length(t));
S(:, 1) = S0;

for i = 1:numSimulations
    for j = 2:length(t)
        dW = sqrt(dt) * randn;
        S(i, j) = S(i, j-1) * exp((mu - 0.5 * sigma^2) * dt + sigma * dW);
    end
end

% Plot the simulations
% figure;
% plot(t, S');
% title('Geometric Brownian Motion Simulations');
% xlabel('Time [days]');
% ylabel('Stock Price');
% grid on;



% compare trading strategies to each other

% for every strategy: average over different stock simulations
function reward = JustHold(stockEvolution, taxFactor)

    reward = 0;

    for i = 1:numSimulations 
        tempReward = stockEvolution(end) - stockEvolution(1);
        reward = reward + tempReward;
    end

    % average
    reward = reward / numSimulations;

    if reward > 0
        reward = reward * taxFactor; 
    end
    
end




function reward = SellEveningBuyMorning(stockEvolution, taxFactor)

    reward = 0; 

    for i = 1:numSimulations
        tempReward = 0;
    
        for dayIndex = 1:22
    
            tempReward = tempreward + stockEvolution(dayIndex * (12*60)) - stockEvolution(dayIndex);  
            
        end

        reward = reward + tempReward;
    end

    reward = reward / numSimulations;

    if reward > 0
        reward = reward * taxFactor;
    end
    
end


