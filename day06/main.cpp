#include <iostream>
#include <fstream>
#include <unordered_map>

void insert(std::unordered_map<char, int>& counts, char c) {
    if (!counts.count(c)) {
        counts[c] = 0;
    }
    counts[c]++;
}

void remove(std::unordered_map<char, int>& counts, char c) {
    if (!counts.count(c)) {
        return;
    }
    counts[c]--;
    if (counts[c] == 0) {
        counts.erase(c);
    }
}

int solve(const std::string& input, int n) {
    std::unordered_map<char, int> counts;
    for (int i = 0; i < n; i++) {
        insert(counts, input[i]);
    }
    if (counts.size() == n) {
        return n;
    }

    for (int i = n; i < input.size(); i++) {
        insert(counts, input[i]);
        remove(counts, input[i - n]);
        if (counts.size() == n) {
            return i + 1;
        }
    }
    return -1;
}

const std::string INPUT_FILE = "./input.txt";

int main() {
    std::ifstream in(INPUT_FILE);
    std::string input;
    in >> input;
    std::cout << "Part 1: " << solve(input, 4) << "\n";
    std::cout << "Part 2: " << solve(input, 14) << "\n";
}
