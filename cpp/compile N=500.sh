
# N=500
g++ N=500/lin-step.cpp -o build/N=500/lin-step
g++ N=500/lin-smooth.cpp -o build/N=500/lin-smooth
g++ N=500/lin-skew45.cpp -o build/N=500/lin-skew45
g++ N=500/lin-skewTo0.cpp -o build/N=500/lin-skewTo0

g++ N=500/lin-skewTo0-taus.cpp -o build/N=500/lin-skewTo0-taus
g++ N=500/lin-skew45-taus.cpp -o build/N=500/lin-skew45-taus
g++ N=500/lin-step-taus.cpp -o build/N=500/lin-step-taus
g++ N=500/lin-smooth-taus.cpp -o build/N=500/lin-smooth-taus
