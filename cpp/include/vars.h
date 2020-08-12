default_random_engine generator;
uniform_real_distribution<double> distribution(0.0, 1.0);

unsigned int histogram[MAXN + 1];

const int duration = 1000000000;
signed char x[duration];