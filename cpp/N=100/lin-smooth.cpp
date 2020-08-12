#include <iostream>
#include "bits/stdc++.h"

using namespace std;

const int duration = 1000000000;
signed char x[duration];
const int tauA = 50, tauB = 0;
int d = 20;
const signed char N = 100;
default_random_engine generator;
uniform_real_distribution<double> distribution(0.0, 1.0);

const size_t D_VALUE_NUMBER = 38;
const int dValues[D_VALUE_NUMBER] = {
    0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40, 42, 44, 46, 47, 48, 49, 50, 52,
    54, 56, 58, 60, 62, 64, 66, 68, 70};

double fA_Preprocessed[N + 1][D_VALUE_NUMBER];
double fB_Preprocessed[N + 1][D_VALUE_NUMBER];

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
    return (long long)m;
}

double mean(const long long &length)
{
    double sum = 0;
    for (int i = 10000; i < length; ++i)
    {
        sum += (double)x[i];
    }
    return sum / (length - 10000);
}

signed char increase(const long long &current)
{
    signed char y = x[current];
    y += 1;
    if (y > N / 2)
    {
        y = N / 2;
    }
    return y;
}

signed char decrease(const long long &current)
{
    signed char y = x[current];
    y -= 1;
    if (y < -N / 2)
    {
        y = -N / 2;
    }
    return y;
}

double fA_preprocess(const signed char &x, const int &d, const double &omega)
{
    return double(N / 4) * (tanh(-omega * (x - d)) + 1);
}

double fB_preprocess(const signed char &x, const int &d, const double &omega)
{
    return double(N / 4) * (tanh(omega * (x + d)) + 1);
}

double fA(const signed char &x, const int &dNumber)
{
    return fA_Preprocessed[x + N / 2][dNumber];
}

double fB(const signed char &x, const int &dNumber)
{
    return fB_Preprocessed[x + N / 2][dNumber];
}

void preprocess()
{
    for (int x = -N / 2; x <= N / 2; ++x)
    {
        for (int y = 0; y < D_VALUE_NUMBER; y++)
        {
            fA_Preprocessed[x + N / 2][y] = fA_preprocess(x, dValues[y], 1.0);
            fB_Preprocessed[x + N / 2][y] = fB_preprocess(x, dValues[y], 1.0);
        }
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
        double previousA = fA(x[current - tauA], dNumber);
        double previousB = fB(x[current - tauB], dNumber);

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
    }

    return current;
}

int main()
{
    long long length;
    double avg;

    fstream io;
    io.open("./csv/N=100/lin-smooth-ds-tau50.csv", ios_base::out | ios_base::trunc);
    if (!io.is_open())
    {
        cout << "Error opening file!";
        return 1;
    }
    io << "d,τ,µ" << endl;

    preprocess();

    //    tauA = 50;
    for (int i = 0; i < D_VALUE_NUMBER; ++i)
    {
        d = dValues[i];
        length = run(i);
        avg = mean(length);
        io << (int)d << "," << tauA << "," << avg << endl;
    }
    io.close();

    return 0;
}