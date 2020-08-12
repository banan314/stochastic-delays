#include <iostream>
#include "bits/stdc++.h"
#include <string>
#include <sys/stat.h>
#include <thread>

using namespace std;

const int duration = 1000000;
int tauA = 1, tauB = 0;
signed char N = 100;
const signed char MAXN = 50;
default_random_engine generator;
uniform_real_distribution<double> distribution(0.0, 1.0);

double fA_Preprocessed[MAXN + 1];
double fB_Preprocessed[MAXN + 1];

size_t TAU_VALUE_NUMBER = 51u;
const int tauValues[51u] = {
    0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50};

struct Result
{
  int tauA, mu;
  int N, tauB;
};

#include "../include/initialize.h"
#include "../include/mean.h"
#include "../include/decrease.h"
#include "../include/increase.h"

double fA_preprocess(const signed char &x)
{
  return x <= 0 ? N / 2 : N / 2 - x;
}

double fB_preprocess(const signed char &x)
{
  return x <= 0 ? x + N / 2 : N / 2;
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
  return 0.5 + r / N;
}

long long run(int tauA, int tauB, signed char x[], unsigned int histogram[])
{
  long long current = initialize(tauA, tauB, x, histogram);
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
      nextElement = increase(current, x); // +1
    }
    else
    {
      nextElement = decrease(current, x); // -1
    }

    ++current;
    x[current] = nextElement;
    histogram[nextElement + N / 2] += 1;
  }

  return current;
}

Result results[6];

void threadRun(int tauA, int tauB, size_t thread_no)
{
  signed char x[duration];
  unsigned int histogram[MAXN + 1];

  fstream histogramFile;
  string ss;

  long long length;
  double avg;

  length = run(tauA, tauB, x, histogram);
  avg = mean(length, x);
  results[thread_no].tauA = tauA;
  results[thread_no].mu = avg;

  struct stat buffer;
  ss = string("");
  ss += "./csv/tent/N=" + int(N) + "/histogram/tent-histogram" + "-tau=" + tauA + ".csv";
  cout << "run" << endl;

  //if file exists, continue
  if (stat(ss.str().c_str(), &buffer) == 0)
    return;
  histogramFile.open(ss.str(), ios_base::out | ios_base::trunc);
  if (!histogramFile.is_open())
  {
    cout << "Error opening histogram file!";
  }
  ss.str("");
  ss << "tau=" << tauA;
  histogramFile << ss.str() << endl;
  for (auto j = 0; j <= N; j++)
  {
    histogramFile << histogram[j] << endl;
  }
  histogramFile.close();
}

int main(int argc, char *argv[])
{
  stringstream ss;

  for (auto i = 1; i < argc; i++)
  {
    if (string(argv[i]) == "-n")
    {
      if (i + 1 < argc)
      {
        try
        {
          N = atoi(argv[++i]);
          cout << int(N) << endl;
        }
        catch (const std::exception &)
        {
          cout << "N not an int" << endl;
        }
      }
    }
    else if (string(argv[i]) == "--tau")
    {
      if (i + 1 < argc)
      {
        try
        {
          TAU_VALUE_NUMBER = atoi(argv[++i]);
          cout << TAU_VALUE_NUMBER << endl;
        }
        catch (const std::exception &)
        {
          cout << "TAU_VALUE_NUMBER not an int" << endl;
        }
      }
    }
  }

  fstream io;

  ss << "./csv/tent/N=" << int(N) << "/tent.csv";
  io.open(ss.str(), ios_base::out | ios_base::trunc);
  if (!io.is_open())
  {
    cout << "Error opening file!" << endl
         << strerror(errno);
    return 1;
  }
  io << "τ,µ" << endl;

  preprocess();

  for (tauA = 0; tauA < TAU_VALUE_NUMBER; tauA += 6)
  {
    thread threads[6];

    for (auto j = 0; j < 6; j++)
      if (TAU_VALUE_NUMBER > tauA + j)
        threads[j] = thread(threadRun, tauA + j, tauB, j);

    for (auto j = 0; j < 6; j++)
      if (TAU_VALUE_NUMBER > tauA + j)
        threads[j].join();

    for (auto j = 0; j < 6; j++)
      if (TAU_VALUE_NUMBER > tauA + j)
        io << results[j].tauA << "," << results[j].mu << endl;
  }

  io.close();

  return 0;
}
