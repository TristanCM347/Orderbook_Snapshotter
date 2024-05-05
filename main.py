import sys

import message
# import time
from market import Symbol

def main():
    N = int(sys.argv[1])
    file_path = "output2.log"
    file = open(file_path, "w")

    financial_market = dict() # symbol : Symbol
    
    # start_time = time.time()

    for header, order in message.gen_from(sys.stdin.buffer):
        # print(f"{header.seq_num}/{header.msg_type}/{vars(order)}")
        # add symbol to market
        if order.symbol not in financial_market:
            financial_market[order.symbol] = Symbol(N)

        output = None
        # change associated price depth
        if header.msg_type == 'A':
            output = financial_market[order.symbol].add(order.side, order.price, order.volume, order.order_id)
        elif header.msg_type == 'U':
            output = financial_market[order.symbol].update(order.side, order.price, order.volume, order.order_id)
        elif header.msg_type == "D":
            output = financial_market[order.symbol].delete(order.side, order.order_id)
        elif header.msg_type == "E":
            output = financial_market[order.symbol].execute(order.side, order.volume, order.order_id)
        else:
            continue

        # print if change happens to top N price level for associated price depth
        if output:
            # print output to file
            print(f"{header.seq_num}, {order.symbol}, {output[0]}, {output[1]}", file=file)

    # end_time = time.time()
    # print(f"The function took {end_time - start_time} seconds to complete.")
    file.close()
    # end of function

if __name__ == "__main__":
    main()

# STRATEGY
### Array ###
# Add : O(n) + log(n) # add and search to maintain order
# Update (no del) : O(1)
# Delete : O(n)
# Display : O(k) # first k in array
# If need to Display # Keep track of last price from last dipaly O(1)

### 2Heaps ###
# Add : O(log n)
# Update (no del) : O(1)
# Delete : O(n) + O(logn)
# Display : O(k)
# If need to Display # Keep track of last price from last dipaly O(1)

### Balanced BST ###
# Add : O(log n)
# Update (no del) : O(1)
# Delete : O(logn)
# Display : O(k)
    

# should i use dictioanry for price : index of last snapshot list
##############################
# with extra dictionary times

# 0.4421868324279785
# 0.45505380630493164
# 0.4494130611419678
# 0.45299315452575684
# 0.4428088665008545
    
# 0.43416404724121094
# 0.449735164642334
# 0.4359166622161865
# 0.4260218143463135
# 0.4603152275085449
    
##############################
# without extra dictionary times

# 0.43174290657043457
# 0.4380040168762207
# 0.4225430488586426
# 0.471466064453125
# 0.45966506004333496
    
# 0.41711997985839844
# 0.42703914642333984
# 0.43161916732788086
# 0.4447791576385498
# 0.44901609420776367