import streamlit as st
import random

def search_value(array, value):
    indexes = [i for i, num in enumerate(array) if num == value]
    count = len(indexes)
    return indexes, count

def count_odd_even(array):
    odd_count = sum(1 for num in array if num % 2 != 0)
    even_count = len(array) - odd_count
    return odd_count, even_count

def main():
    st.title("Array Operations")
    
    st.write("______\n")
    st.write("\n p1: [9] => T3,I3,M1: array operations on 1x[N] of random int\n")
    st.write("______")
    
    size = st.number_input("Enter N size number of elements for 1x[N] array:", min_value=1, step=1)
    
    number = st.number_input("Guess a number in -100..100 to be randomed in 1x[N]:", min_value=-100, max_value=100, step=1)
    
    array = [random.randint(-100, 100) for _ in range(int(size))]
    
    odd_count, even_count = count_odd_even(array)
    
    SUM = sum(array)
    PRODUCT = 1
    min_value = min(array)
    min_indexes = [i for i, num in enumerate(array) if num == min_value]
    max_value = max(array)
    max_indexes = [i for i, num in enumerate(array) if num == max_value]
    guess_indexes, GUESS_COUNT = search_value(array, number)
    
    for num in array:
        PRODUCT *= num
    st.write("\nArray:", array)
    st.write("Sum: {:,}".format(SUM))
    st.write("Product: {:,}".format(PRODUCT))
    st.write("\nMinimum Value:", min_value)
    st.write("Minimum Indexes:", min_indexes)
    st.write("Maximum Value:", max_value)
    st.write("Maximum Indexes:", max_indexes)
    st.write("\nNumber", number, "Presence:")
    st.write("Indexes:", guess_indexes)
    st.write("Count:", GUESS_COUNT)
    mean = SUM / len(array)
    geometric_mean = PRODUCT ** (1 / len(array))
    st.write("\nMean: {:.2f}".format(mean))
    st.write("Geometric Mean: {:.2f}".format(geometric_mean))
    sorted_array = sorted(array)
    st.write("\nSorted Array (Ascending):", sorted_array)
    st.write("Sorted Array (Descending):", sorted_array[::-1])
    search_value_input = st.text_input("Enter a value to search in the array (type 666 to exit):")
    if search_value_input != '666':
        search_value_input = int(search_value_input)
        if st.button("Search"):
            indexes, count = search_value(array, search_value_input)
            st.write("Indexes:", indexes)
            st.write("Count:", count)

if __name__ == "__main__":
    main()
