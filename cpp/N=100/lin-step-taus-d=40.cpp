#include <iostream>
#include "bits/stdc++.h"

using namespace std;

const int duration = 1000000000;
signed char x[duration];
int tauA = 50, tauB = 0;
const int d = 40;
const signed char N = 100;
default_random_engine generator;
uniform_real_distribution<double> distribution(0.0, 1.0);

const size_t TAU_VALUE_NUMBER = 51u;
const int tauValues[TAU_VALUE_NUMBER] = {
    0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50
};

double fA_Preprocessed[N + 1];
double fB_Preprocessed[N + 1];

unsigned int histogram[N+1];

/**
 *
 * @return current index of x
 */
long long initialize()
{
    int m = max(tauA, tauB);
    for (int i = 0; i < m; ++i)
    {
        x[i] = 0;
    }
    x[m] = 1;

    for(auto i = 0; i <= N; ++i) {
        histogram[i] = 0;
    }

    return (long long)m;
}

double mean(long long length)
{
    double sum = 0;
    for (int i = 10000; i < length; ++i)
    {
        sum += (double)x[i];
    }
    return sum / (length - 10000);
}

signed char increase(long long current)
{
    signed char y = x[current];
    y += 1;
    if (y > N / 2)
    {
        y = N / 2;
    }
    return y;
}

signed char decrease(long long current)
{
    signed char y = x[current];
    y -= 1;
    if (y < -N / 2)
    {
        y = -N / 2;
    }
    return y;
}

double fA_preprocess(const signed short int &x)
{
    return x <= d ? N / 2 : 0;
}

double fB_preprocess(signed short int x)
{
    return x >= -d ? N / 2 : 0;
}

double fA(const signed short int &x)
{
    return fA_Preprocessed[x + N / 2];
}

double fB(const signed short int &x)
{
    return fB_Preprocessed[x + N / 2];
}

void preprocess()
{
    for (int x = -N / 2; x <= N / 2; ++x)
    {
        fA_Preprocessed[x + N / 2] = fA_preprocess(x);
        fB_Preprocessed[x + N / 2] = fB_preprocess(x);
    }
}

double calculateProbability(const double &r)
{
    return 0.5 + 0.99 * r / N;
}

long long run(const int &dNumber)
{
    long long current = initialize();
    generator.seed(std::chrono::system_clock::now().time_since_epoch().count());

    while (current < duration - 1)
    {
        double previousA = fA(x[current - tauA]);
        double previousB = fB(x[current - tauB]);

        double prob = calculateProbability(previousA - previousB);
        double r = distribution(generator);
        signed char nextElement;

        if (r < prob)
        {
            nextElement = increase(current); // +1
        }
        else
        {
            nextElement = decrease(current); // -1
        }

        ++current;
        x[current] = nextElement;
        histogram[nextElement + N/2] += 1;
    }

    return current;
}

int main()
{
    long long length;
    double avg;

    fstream io, histogramFile;
    stringstream ss;

    ss << "./csv/N=100/lin-step-ds-tau-" << tauA << ".csv";
    io.open(ss.str(), ios_base::out | ios_base::trunc);
    if (!io.is_open())
    {
        cout << "Error opening file!";
        return 1;
    }
    io << "d,τ,µ" << endl;

    preprocess();

    //    tauA = 50;
    for (int i = 0; i < TAU_VALUE_NUMBER; ++i)
    {
        tauA = tauValues[i];
        length = run(i);
        avg = mean(length);
        io << (int)d << "," << tauA << "," << avg << endl;

        ss.str("");
        ss << "./csv/N=100/histogram/lin-step-histogram-d=" << d << "-tau=" << tauA << ".csv";
        histogramFile.open(ss.str(), ios_base::out | ios_base::trunc);
        if(!histogramFile.is_open()) {
            cout << "Error opening histogram file!";
        }
        ss.str("");
        ss << "d=" << d << "-tau=" << tauA;
        histogramFile << ss.str() << endl;
        for(auto j = 0; j <= N; j++) {
            histogramFile << histogram[j] << endl;
        }
        histogramFile.close();
    }
    io.close();

    return 0;
}