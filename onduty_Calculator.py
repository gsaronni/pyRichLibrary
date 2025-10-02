import random

def allocate_tokens(num_days):
    total_tokens = (25 * num_days) / 7
    print("Total tokens: ", total_tokens)
    tokens_per_day = int(total_tokens / num_days)
    remaining_tokens = int(total_tokens % num_days)
    
    tokens_allocation = [tokens_per_day] * num_days
    for i in range(remaining_tokens):
        tokens_allocation[i] += 1
    
    random.shuffle(tokens_allocation)
    
    return tokens_allocation

def main():
    num_days_worked = int(input("Enter the number of days worked: "))
    if num_days_worked <= 0:
        print("Invalid number of days.")
        return
    
    tokens_allocation = allocate_tokens(num_days_worked)

if __name__ == "__main__":
    main()
