approximatedProbs = [0.9899999990779907, 0.9899999990779907, 0.9899999990779907, 0.9899999990779907, 0.9899999990779907, 0.9899999990779907, 0.9899999990779907, 0.9899999990779907, 0.9899999990779907, 0.9899999990779907, 0.9899999990779907, 0.9899999990779907, 0.9899999990779907, 0.9899999990779907, 0.9899999990779907, 0.9899999990779907, 0.9899999990779907, 0.9899999990779907, 0.9899999990779907, 0.9899999990779907, 0.9899999990779907, 0.9899999990779907, 0.9899999990779907, 0.9899999990779907, 0.9899999990779907, 0.9899999990779907, 0.9899999853875489, 0.9899997868761421, 0.9899979341030122, 0.989985427884385, 0.4999999995343387, 0.4999999995343387, 0.4999999995343387, 0.4999999995343387, 0.4999999995343387, 0.4999999995343387, 0.4999999995343387, 0.4999999995343387, 0.4999999995343387, 0.4999999995343387, 0.4999999995343387, 0.4999999995343387, 0.4999999995343387, 0.4999999995343387, 0.4999999995343387, 0.4999999995343387, 0.4999999995343387, 0.4999999858438969, 0.4999997873324901, 0.4999979345593602, 0.4999854283407331,
                     0.4999203960038722, 0.4999203960038722, 0.4996494279336185, 0.4996494279336185, 0.4987203945498914, 0.4987203945498914, 0.4960494235716761, 0.4960494235716761, 0.48952038340270526, 0.48952038340270526, 0.4758093990478665, 0.4758093990478665, 0.45088033658452337, 0.45088033658452337, 0.4114093210175634, 0.4114093210175634, 0.35675714561715727, 0.35675714561715727, 0.290393789773807, 0.290393789773807, 0.21960621020756663, 0.21960621020756663, 0.15324285436421634, 0.15324285436421634, 0.0985906789638102, 0.0985906789638102, 0.05911966339685023, 0.05911966339685023, 0.034190600933507086, 0.034190600933507086, 0.02047961657866836, 0.02047961657866836, 0.013950576409697534, 0.013950576409697534, 0.011279605431482199, 0.011279605431482199, 0.010350572047755125, 0.010350572047755125, 0.010079603977501395, 0.010079603977501395, 0.010014571640640499, 0.010014571640640499, 0.010002065422013404, 0.010002065422013404, 0.010000212648883462, 0.010000212648883462, 0.010000014137476684, 0.010000014137476684, 0.010000000447034838, 0.010000000447034838]


N=100

def multiply(pos, tau, destination):
        def canDecrement(pos, tau, destination):
            if pos >= destination:
                return pos-1 >= -N/2
            return destination-(pos-1) <= tau-1 and pos-1 >= -N/2

        def canIncrement(pos, tau, destination):
            if pos <= destination:
                return pos+1 <= N/2
            return pos+1-destination <= tau-1 and pos+1 <= N/2

        if tau == 0:
            return 0.0

        accumulator = 0.0
        if canDecrement(pos, tau, destination):
            accumulator += (1-approximatedProbs[pos]) * \
                multiply(pos-1, tau-1, destination)
        if canIncrement(pos, tau, destination):
            accumulator += approximatedProbs[pos] * \
                multiply(pos+1, tau-1, destination)

        return accumulator


print(multiply(20, 2, 20))