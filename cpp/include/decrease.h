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