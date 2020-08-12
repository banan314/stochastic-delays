# N=300
g++ N=300/lin-step.cpp -o build/N=300/lin-step
g++ N=300/lin-smooth.cpp -o build/N=300/lin-smooth
g++ N=300/lin-skew45.cpp -o build/N=300/lin-skew45
g++ N=300/lin-skewTo0.cpp -o build/N=300/lin-skewTo0

g++ N=300/lin-step-taus.cpp -o build/N=300/lin-step-taus
g++ N=300/lin-smooth-taus.cpp -o build/N=300/lin-smooth-taus
g++ N=300/lin-skewTo0-taus.cpp -o build/N=300/lin-skewTo0-taus
g++ N=300/lin-skew45-taus.cpp -o build/N=300/lin-skew45-taus

