import math
import collections

def calculate_entropy(data):
    """
    Calculate Shannon entropy of data (measure of randomness)
    Higher entropy = more random = potentially encrypted
    """
    if len(data) == 0:
        return 0.0
    
    # Count frequency of each byte value
    frequency = collections.Counter(data)
    data_length = len(data)
    
    entropy = 0.0
    for count in frequency.values():
        # Probability of this byte occurring
        probability = count / data_length
        # Entropy contribution
        if probability > 0:
            entropy -= probability * math.log2(probability)
    
    return entropy

def file_entropy(filepath):
    """
    Calculate entropy of a file
    """
    try:
        with open(filepath, 'rb') as f:
            data = f.read()
        return calculate_entropy(data)
    except Exception as e:
        print(f"❌ Error reading {filepath}: {e}")
        return 0.0

# Test the function
if __name__ == "__main__":
    # Test with low entropy (text)
    test_text = b"aaaaabbbbcccdd"
    print(f"Low entropy text: {calculate_entropy(test_text):.2f}")
    
    # Test with high entropy (random)
    import os
    test_random = os.urandom(100)
    print(f"High entropy random: {calculate_entropy(test_random):.2f}")