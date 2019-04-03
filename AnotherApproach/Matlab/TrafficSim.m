%% Processing the obtained data %%
%%
clc;

load('patience');
load('velocity');
load('Accidents');

a= zeros;
b= zeros(length(velocity),2);
P= zeros;
columns = size(velocity);
t = zeros;
i=1;
for c=1:columns(1,2)
    for r=2:length(velocity)-1
        if (Accidents(r,c) == 1)
            %a(i,1) = patience(r,c);
            b(i,1)=r;
            b(i,2)=c;
            i=i+1;
            break
             
        end
    
    end
end

for e = 1:length(velocity)
    if b(e,1)==0
       break
    else
       t(e,1)= velocity(b(e,1)-1,b(e,2)); 
       P(e,1)= patience(b(e,1),b(e,2));
      
    end
       
end

figure(1)
histogram(P, 'BinWidth', 0.1,'BinLimits',[0,1]);
xlabel('Patience Level'); 
ylabel('No of accidents');
title('The influence of the number of accidents on Patience level');


figure(2)
histogram(t, 'BinWidth', 0.1,'BinLimits',[0,4]);
xlabel('Velocity [Pixels/itr]'); 
ylabel('No of accidents');
title('The influence of the number of accidents on Velocity[Pixels/itr]');


figure(3)
X=[P t];
hist3(X);
title('The influence of the number of accidents on Patience level and Velocity')
xlabel('Patience Level'); 
ylabel('Velocity before crash');
set(get(gca,'child'),'FaceColor','interp','CDataMode','auto');
%colormap (hot)
view(3)


figure(4)
boxplot(P);
xlabel('Vehicles that me with Accidents'); 
ylabel('Patience level');
title('Boxplot showing the patience level of the crashed cars');


figure(5)
plot(patience)
xlabel('elapsed time')
ylabel('Patience level')
title('Change of Patience level over time')



%% Time calculation %%
% Scatter plots for average times taken by the vehicles
%% 

timeR = zeros;
it=0;
numAccidents=0;
MeanTime = 0;
load('time');

for tc = 1:length(time)
    
    if time(1,tc)==0
       numAccidents=numAccidents+1;
    else
       it=it+1;
       timeR(1,it)= time(1,tc);
    end
       
end

figure(6)
scatter([1:1:length(timeR)],timeR,'Filled')
lsline;
xlabel('Number of Vehicles(that did not crash)'); 
ylabel('Time taken to reach destination');
title('Time taken by vehicles to reach their assigned destination');

MeanTime = mean(timeR);
numAccidents;
