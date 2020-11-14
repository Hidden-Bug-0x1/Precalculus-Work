# Extrema of a graph

def get_extrema(func, step=1, max_x = 1000, inJupyter = True):
    """
        Takes a function and finds the extrema of the function
        Returns:
            Highest value achieved,
            Lowest value achieved,
            Maximums,
            and Minimums of any given function
            in the format:
                (x, y, max or min) or (highest or lowest, y, junk value)
        
        Could make the function faster using threads and splitting the workload
    """
    if step < 0:
        step = 1
        
    py_old = func(0)
    ny_old = func(0)
    py = func(step)
    ny = func(-step)
    px_trend_old = (py - py_old) / step # Can be 1 for increasing, -1 for decreasing
    px_trend_old = px_trend_old / abs(px_trend_old) if abs(px_trend_old) > 0 else 0
    nx_trend_old = (ny_old - ny) / step # Can be 1 for increasing, -1 for decreasing
    nx_trend_old = nx_trend_old / abs(nx_trend_old) if abs(nx_trend_old) > 0 else 0
    py_old = py
    ny_old = ny
    
    rets = [] # Mins and maxes of the graph in (x, y) pairs
    
    lowest = min(ny, ny_old, py, py_old)
    highest = max(ny, ny_old, py, py_old)
    its = int((max_x + 1)/step)
    
    # Start at 0 and work my way out
    for x in range(2, its):
        if not inJupyter:
            # progress bar
            print('\r['+ '#'*int( x / its * 10 ) + ' '*int( (1 - x / its) * 10 ) + ']', end='\r')
        
        # Keep track of positive x trends
        py = func(x*step)
        
        px_trend = (py - py_old) / step 
        px_trend = px_trend / abs(px_trend) if abs(px_trend) > 0 else 0 # get it to 1 or -1
        if px_trend != px_trend_old and px_trend_old != 0: # aka a change occured
            pair = ((x - 1)*step, func((x - 1)*step), 'min' if px_trend == 1 else 'max') # because the point was hit last iteration
            rets.append(pair)
        
        
        px_trend_old = px_trend
        py_old = py
        
        # Keep track of negative x trends
        ny = func(-(x*step))
        
        nx_trend = (ny_old - ny) / step
        nx_trend = nx_trend / abs(nx_trend) if abs(nx_trend) > 0 else 0 # get it to 1 or -1
        if nx_trend != nx_trend_old and nx_trend_old != 0: # again, a change occured
            pair = ( -(x - 1)*step, func(-((x - 1)*step)), 'min' if nx_trend == -1 else 'max')
            rets.append(pair)
        
        nx_trend_old = nx_trend
        ny_old = ny        
        
        lowest = min(lowest, ny, py)
        highest = max(highest, ny, py)
        
    rets.append( ("lowest", lowest, None) )
    rets.append( ("highest", highest, None) )
    return set(rets) 

def extrema_program():
    print("Don't forget to set func inside extrema_program!")
    func = lambda x: pow(x, 3) + 2 * pow(x, 2) - 4 * x - 6
    extrema = get_extrema(func, step=0.001, max_x=10000)

    round_to = 100

    for x, y, m in extrema:
        if x == "highest":
            print("The highest value could be infinity")
            print(f"Highest: {y}")
            print()
        elif x == "lowest":
            print("The lowest value could be -infinity")
            print(f'Lowest: {y}')
            print()

    print("Extrema:")    
    for x, y, m in extrema:
        print(f'\t{m}: ({round(x, round_to)}, {round(y, round_to)})') if x not in ["highest", "lowest"] else None
import math
def factors(num):
    # Returns all of the factors (+/-) of a number in O(num/2) time
    if num < 0:
        num *= -1
    facts = []
    last = None
    for i in range(1, math.ceil((num+1)/2)+1):
        if last != None and i == last:
            break
        if num % i == 0:
            last = int(num/i)
            facts.append(i)
            facts.append(int(num/i))
            facts.append(-i)
            facts.append(int(-num/i))
    return facts

def commonFactor(*coeffs):
    # Gets the common factors of any amount of coefficients
    facts = []
    for x in coeffs:
        facts.extend(factors(x))
    facts = set(facts)
    commons = []
    for fact in facts:
        isGood = True
        for coeff in coeffs:
            isGood = isGood and coeff % fact == 0
            if not isGood:
                break
        if isGood:
            commons.append(fact)
    return commons

def ApplyRealZeroFactorTheorem(*coeffs):
    # set up the variables
    first = coeffs[0]
    second = coeffs[-1]
    # p is the set of factors of the constant term
    setp = factors(second)
    # q is the set of factors of the leading coefficient
    setq = factors(first)
   
    # Find the set of p/q
    to_test = []
    for p in setp:
        for q in setq:
            to_test.append(float(p/q))
    to_test = set(to_test)
    
    # Test all of possible zeros
    zeros = []
    coeffs = coeffs[1:]
    for num in to_test:
        test = first
        for coeff in coeffs:
            test = coeff + test * num
        if test == 0: # the sum of the function is 0, exactly what we're looking for
            zeros.append(num)
    
    # Clean up any possible errors of simplifying too much and forgetting a factor
    cf = commonFactor(*[first, second])
    c = set([abs(x) for x in cf if x > 0]) # Set of all positive factors
    if c.__contains__(1): # We don't care about a factor of 1 or -1, it will be in the final answer
        c.remove(1)
    # This is a magic bit of code, don't touch
    ret = None
    for f in cf:
        if c.__contains__(abs(f)):
            ret = f
    # end of magic code, no idea how it works! 
            
    return (zeros, ret)
    
def numPastDecimal(dec):
    # Counts the number of places past a decimal
    count = 0
    counting = False
    for char in dec:
        if counting:
            count += 1
        if char == '.': # only start counting when you hit the decimal place
            counting = True
    return count

def toFraction(X):
    # Converts a decimal to a tuple of the numerator and denominator of a fraction
    # could return fractions.Fraction if this code section is refactored
   
    digits = numPastDecimal(str(X))
    if digits > 10: # you shouldn't need more than 10^10, it starts to overflow and mess up
        digits = 10
        
    # Perform the math
    p = pow(10, digits)
    right_side = p * X - X
    p = p - 1
    
    # Convert the right side of the equation to an integer
    if (right_side - int(right_side)) > 0:
        right_side = math.ceil(right_side)
    else:
        right_side = int(right_side)
        
    # Get the gcd
    div = math.gcd(p, right_side)
    # Solve for each piece
    numerator = int(right_side / div)
    denominator = int(p / div)
    
    return (numerator, denominator)

def real_zeros_program():
    print("This application only accepts items separated with spaces\n")
    zeros = ApplyRealZeroFactorTheorem(*[int(x) for x in input("Enter your coefficients:\n").split()])
    func = ""
    if not zeros[1] == None:
        func += str(zeros[1])
    for z in zeros[0]:
        if z < 0:
            func += f"(x + {int(abs(z))})"
        elif z >= 1:
            func += f"(x - {int(z)})"
        elif z < 1 and z > 0:
            fract = toFraction(z)
            func += f"({fract[1]}x - {fract[0]})"
        elif z < 0 and z > -1:
            fract = toFraction(abs(z))
            func += f"({fract[1]}x + {fract[0]})"

    if len(zeros[0]) > 0:
        print(f'f(x) = {func}')
    else:
        print("No real zeros exist for these coefficients")
real_zeros_program()
