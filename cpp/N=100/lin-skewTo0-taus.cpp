#include <iostream>
#include "bits/stdc++.h"

using namespace std;

const int duration = 1000000000;
signed char x[duration];
int tauA = 0, tauB = 0;
const int d = 20;
const signed char N = 100;
default_random_engine generator;
uniform_real_distribution<double> distribution(0.0, 1.0);

double fA_Preprocessed[N+1];
double fB_Preprocessed[N+1];

/**
 *
 * @return current index of x
 */
long long initialize() {
    int m = max(tauA, tauB);
    for(int i = 0; i < m; ++i) {
        x[i] = 0;
    }
    x[m] = 1;
    return (long long) m;
}

double mean(long long length) {
    double sum = 0;
    for(int i = 10000; i < length; ++i) {
        sum += (double) x[i];
    }
    return sum / length;
}

signed char increase(long long current) {
    signed char y = x[current];
    y += 1;
    if(y > N / 2) {
        y = N / 2;
    }
    return y;
}

signed char decrease(long long current) {
    signed char y = x[current];
    y -= 1;
    if(y < -N / 2) {
        y = -N / 2;
    }
    return y;
}

double fA_preprocess(const signed char &x) {
    return x <= d ? N/2 : double(-N/2*x+(N/2)*(N/2))/double(N/2-d);
}

double fB_preprocess(const signed char &x) {
    return x >= -d ? N/2 : double(N/2*x+(N/2)*(N/2))/double(N/2-d);
}

double fA(const signed char &x) {
    return fA_Preprocessed[x + N/2];
}

double fB(const signed char &x) {
    return fB_Preprocessed[x + N/2];
}

void preprocess() {
    for(int x = -N/2; x <= N/2; ++x) {
        fA_Preprocessed[x + N/2] = fA_preprocess(x);
        fB_Preprocessed[x + N/2] = fB_preprocess(x);
    }
}

double calculateProbability(double r) {
    return 0.5 + 0.99 * r / N;
}

long long run() {
    long long current = initialize();
    generator.seed(std::chrono::system_clock::now().time_since_epoch().count());


    while(current < duration-1) {
        double previousA = fA(x[current - tauA]);
        double previousB = fB(x[current - tauB]);

        double prob = calculateProbability(previousA - previousB);
        double r = distribution(generator);
        signed char nextElement;

        if(r < prob) {
            nextElement = increase(current);  // +1
        } else {
            nextElement = decrease(current);  // -1
        }

        ++current;
        x[current] = nextElement;
    }

    return current;
}

const size_t TAU_VALUE_NUMBER = 51u;
const int tauValues[TAU_VALUE_NUMBER] = {
    200, 202, 204, 206, 208, 210, 212, 214, 216, 218, 220, 222, 224, 226, 228, 230, 232, 234, 236, 238, 240, 242, 244, 246, 248, 250, 252, 254, 256, 258, 260, 262, 264, 266, 268, 270, 272, 274, 276, 278, 280, 282, 284, 286, 288, 290, 292, 294, 296, 298, 300
};

int main() {
    long long length;
    double avg;
    preprocess();

    fstream io;
    io.open("./csv/N=100/lin-skewTo0-taus-d20.csv", ios_base::out | ios_base::app);
    if(!io.is_open()) {
        cout << "Error opening file!";
        return 1;
    }
    io << "d,τ,µ" << endl;

    for(int i = 0; i < TAU_VALUE_NUMBER; ++i) {
        tauA = tauValues[i];
        length = run();
        avg = mean(length);
        io << (int) d << "," << tauA << "," << avg << endl;
    }
    io.close();

    return 0;
}