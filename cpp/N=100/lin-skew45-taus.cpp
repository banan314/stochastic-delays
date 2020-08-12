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

double fA_Preprocessed[N + 1];
double fB_Preprocessed[N + 1];

unsigned int histogram[N + 1];

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

  for (auto i = 0; i <= N; ++i)
  {
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
  return sum / length;
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

double fA_preprocess(const signed char &x)
{
  double k = double(N - 2 * d) / 2;
  return x <= d ? k : -x + k + d;
}

double fB_preprocess(signed char x)
{
  double k = double(N - 2 * d) / 2;
  return x >= -d ? k : x + k + d;
}

double fA(const signed char &x)
{
  return fA_Preprocessed[x + N / 2];
}

double fB(const signed char &x)
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

double calculateProbability(double r)
{
  return 0.5 + 0.99 * r / N;
}

long long run()
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
    histogram[nextElement + N / 2] += 1;
  }

  return current;
}

const size_t TAU_VALUE_NUMBER = 35u;
const int tauValues[TAU_VALUE_NUMBER] = {
    0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40, 42, 44, 46, 48, 50, 52, 54, 56, 58, 60, 62, 64, 66, 68
};

int main()
{
  long long length;
  double avg;
  preprocess();

  fstream io, histogramFile;
  io.open("./csv/N=100/lin-skew45-taus-d20-to70.csv", ios_base::out | ios_base::app);
  if (!io.is_open())
  {
    cout << "Error opening file!";
    return 1;
  }
  io << "d,τ,µ" << endl;

  for (int i = 0; i < TAU_VALUE_NUMBER; ++i)
  {
    tauA = tauValues[i];
    length = run();
    avg = mean(length);
    io << (int)d << "," << tauA << "," << avg << endl;

    stringstream ss;
    ss.str("");
    ss << "./csv/N=100/histogram/lin-skew45-histogram-d=" << d << "-tau=" << tauA << ".csv";
    histogramFile.open(ss.str(), ios_base::out | ios_base::trunc);
    if (!histogramFile.is_open())
    {
      cout << "Error opening histogram file!";
    }
    ss.str("");
    ss << "d=" << d << "-tau=" << tauA;
    histogramFile << ss.str() << endl;
    for (auto j = 0; j <= N; j++)
    {
      histogramFile << histogram[j] << endl;
    }
    histogramFile.close();
  }
  io.close();

  return 0;
}