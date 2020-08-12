#include <iostream>
#include "bits/stdc++.h"

using namespace std;

const int duration = 1000000000;
signed short int x[duration];
int tauA = 0, tauB = 0;
int d = 50;
const signed short int N = 500;
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

signed short int increase(long long current) {
    signed short int y = x[current];
    y += 1;
    if(y > N / 2) {
        y = N / 2;
    }
    return y;
}

signed short int decrease(long long current) {
    signed short int y = x[current];
    y -= 1;
    if(y < -N / 2) {
        y = -N / 2;
    }
    return y;
}

double fA_preprocess(const signed short int &x) {
    return x <= d ? N/2 : double(-N/2*x+(N/2)*(N/2))/double(N/2-d);
}

double fB_preprocess(const signed short int &x) {
    return x >= -d ? N/2 : double(N/2*x+(N/2)*(N/2))/double(N/2-d);
}

double fA(const signed short int &x) {
    return fA_Preprocessed[x + N/2];
}

double fB(const signed short int &x) {
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
        signed short int nextElement;

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

size_t TAU_VALUE_NUMBER = 100u;
int tauValues[500u];

int main()
{
  long long length;
  double avg;
  preprocess();

  fstream io;
  ifstream parametersStream;
  //get parameters
  parametersStream.open("./in/taus.in", ios_base::in);
  if(!parametersStream.is_open())
  {
    cout << "Error opening file!";
    return 2;
  }
  int ioMode;
  parametersStream >> ioMode;
  std::ios_base::openmode mode;
  if(ioMode == 0)
    mode = ios_base::ios_base::app;
  else
    mode = ios_base::ios_base::trunc;
  parametersStream >> d;
  parametersStream >> TAU_VALUE_NUMBER;
  for (size_t i = 0; i < TAU_VALUE_NUMBER; i++)
  {
    parametersStream >> tauValues[i];
  }
  parametersStream.close();

  //open csv data file

    stringstream fileStream;
    auto prefix = "lin-skewTo0";
    fileStream << "./csv/N=" << N << "/" << prefix << "-taus-d" << d << ".csv";
    io.open(fileStream.str(), ios_base::out | mode);
    if(!io.is_open()) {
        cout << "Error opening file!";
        return 1;
    }
    if (mode == ios_base::trunc)
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