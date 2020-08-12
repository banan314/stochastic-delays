#include <iostream>
#include "bits/stdc++.h"
#include <sys/stat.h>

using namespace std;

const int duration = 1000000000;
signed char x[duration];
unsigned int tauA = 2, tauB = 0;
const int d = 10;
const signed char N = 100;
default_random_engine generator;
uniform_real_distribution<double> distribution(0.0, 1.0);

size_t TAU_VALUE_NUMBER = 11;
int tauValues[500u] = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10};

double fA_Preprocessed[N + 1];
double fB_Preprocessed[N + 1];

unsigned int histogram[N + 1];

#include "../include/initialize.h"
#include "../include/mean.h"
#include "../include/decrease.h"
#include "../include/increase.h"

double fA_preprocess(const signed char &x)
{
  if (x <= 0)
    return d;
  if(x < d) 
    return d-x;
  return 0;
}

double fB_preprocess(const signed char &x)
{
  if (x <= -d)
    return 0;
  if (x < 0)
    return d+x;
  return d;
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

double calculateProbability(const double &r)
{
  return 0.5 + r / (2*d);
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

int main()
{
  long long length;
  double avg;

  fstream io, histogramFile;
  stringstream ss;
  ss << "./csv/deterministic/tent/without-taus-d" << d << ".csv";
  io.open(ss.str(), ios_base::out | ios_base::trunc);
  if (!io.is_open())
  {
    cout << "Error opening file!";
    return 1;
  }
  io << "d,τ,µ" << endl;

  preprocess();

  for (int i = 0; i < TAU_VALUE_NUMBER; ++i)
  {
    tauA = tauValues[i];
    length = run();
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