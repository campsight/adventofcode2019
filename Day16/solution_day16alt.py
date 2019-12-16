import itertools as itt
#input_signal = "12345678"
#input_signal = "80871224585914546619083218645595"
#input_signal = "19617804207202209144916044189917"
#input_signal = "69317163492948606335995924319873"
input_signal = "59777373021222668798567802133413782890274127408951008331683345339720122013163879481781852674593848286028433137581106040070180511336025315315369547131580038526194150218831127263644386363628622199185841104247623145887820143701071873153011065972442452025467973447978624444986367369085768018787980626750934504101482547056919570684842729787289242525006400060674651940042434098846610282467529145541099887483212980780487291529289272553959088376601234595002785156490486989001949079476624795253075315137318482050376680864528864825100553140541159684922903401852101186028076448661695003394491692419964366860565639600430440581147085634507417621986668549233797848"
#input_signal = "03036732577212944063491565474664"
input_array = [int(x) for x in input_signal]

base_pattern = [0, 1, 0, -1]

print(input_array)
#print(base_pattern * 2)
#print([(x for x in base_pattern for i in range(2)])
#list(itt.chain.from_iterable(itt.repeat(x, 2) for x in base_pattern))


def generate_pattern(n, lim):
    pos = -1
    sign = 1
    while pos < lim:
        yield sign, pos + n, pos + 2 * n
        pos += 2 * n
        sign *= -1


def get_faster(input_fast):
    cumulative_sum = [0]
    current = 0
    for gfel in input_fast:
        current = (current + gfel)  # % 10
        cumulative_sum.append(current)

    def get_cumulative_sum(i):
        if i >= len(cumulative_sum):
            return cumulative_sum[-1]
        return cumulative_sum[i]

    s_len = len(input_fast)
    result = [99] * s_len

    for i in range(1, 1 + s_len):
        #print("calculating number", i)
        product_sum = 0
        for sign, index1, index2 in generate_pattern(i, s_len):
            product_sum += sign * (get_cumulative_sum(index1) - get_cumulative_sum(index2))
        if abs(product_sum) > 9:
            product_sum = int(str(product_sum)[-1])
        # print("final sum", abs(product_sum))
        result[i-1] = abs(product_sum)
    return result


#part 1
p = input_array
for r in range(100):
    p = get_faster(p)
    #print(p)
print(p)
print("Solution part 1:", p[:7])

#part 2
p = input_array*10000
#offset = str(p[0:7]) #''.join(p[0:7])
offset = int(''.join([str(x) for x in p[0:7]]))
print(offset)
for i in range(100):
    p = get_faster(p)
    if (p%5) == 0: print("just calculated step ", i)
print("Solution part 2:", p[(offset-1):offset+9])
