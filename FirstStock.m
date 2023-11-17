clearvars, clc;

% This is all ChatGPT so far


% Geometric Brownian Motion Parameters
mu = 0.1;   % Drift
sigma = 0.2;   % Volatility

% Time parameters
T = 1;       % Time to simulate
dt = 0.01;   % Time step
t = 0:dt:T;  % Time vector

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
figure;
plot(t, S');
title('Geometric Brownian Motion Simulations');
xlabel('Time');
ylabel('Stock Price');
grid on;

