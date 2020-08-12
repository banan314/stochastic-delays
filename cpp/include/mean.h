double mean(long long length)
{
    double sum = 0;
    for (int i = 10000; i < length; ++i)
    {
        sum += (double)x[i];
    }
    return sum / (length - 10000);
}