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