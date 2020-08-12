#include <iostream>
#include "bits/stdc++.h"
#include <sys/stat.h>

using namespace std;

const int duration = 1000000000;
signed char x[duration];
const int tauA = 2, tauB = 0;
unsigned int d = 1;
const signed char N = 20;
default_random_engine generator;
uniform_real_distribution<double> distribution(0.0, 1.0);

size_t D_VALUE_NUMBER = 1;
int dValues[500u] = {1};

double fA_Preprocessed[N + 1][500u];
double fB_Preprocessed[N + 1][500u];

unsigned int histogram[N + 1];

#include "../include/initialize.h"
#include "../include/mean.h"
#include "../include/decrease.h"
#include "../include/increase.h"

double fA_preprocess(const signed char &x, const int &d)
{
  if (x <= 0)
    return d;
  if(x < d) 
    return d-x;
  return 0;
}

double fB_preprocess(const signed char &x, const int &d)
{
  if (x <= -d)
    return 0;
  if (x < 0)
    return d+x;
  return d;
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
      fA_Preprocessed[x + N / 2][y] = fA_preprocess(x, dValues[y]);
      fB_Preprocessed[x + N / 2][y] = fB_preprocess(x, dValues[y]);
    }
  }
}

double calculateProbability(const double &r)
{
  return 0.5 + r / (2*d);
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
    histogram[nextElement + N / 2] += 1;
  }

  return current;
}

int main()
{
  long long length;
  double avg;

  fstream io, histogramFile;
  stringstream ss;
  ss << "./csv/deterministic/tent/without-d" << d << "-tau-" << tauA << ".csv";
  io.open(ss.str(), ios_base::out | ios_base::trunc);
  if (!io.is_open())
  {
    cout << "Error opening file!";
    return 1;
  }
  io << "d,τ,µ" << endl;

  preprocess();

  for (int i = 0; i < D_VALUE_NUMBER; ++i)
  {
    d = dValues[i];
    length = run(i);
    avg = mean(length);
    io << (int)d << "," << tauA << "," << avg << endl;

    struct stat buffer;
    ss.str("");
    ss << "./csv/deterministic/tent/histogram/without-d=" << d << "-tau=" << tauA << ".csv";
    
    //if file exists, continue
    if (stat(ss.str().c_str(), &buffer) == 0)
      continue;
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